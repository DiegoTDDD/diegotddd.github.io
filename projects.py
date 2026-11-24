"""Content of the site: one entry per project, taken from each repository's README.

Every number here is a measured result stated in that README; the check in CI fails if a
project has no result or no link to its code.
"""

GH = "https://github.com/DiegoTDDD/"

AI, DATA = "ai", "data"
GROUPS = {
    AI: "AI engineering",
    DATA: "Data engineering and machine learning",
}

PROJECTS = [
    {
        "slug": "fraud-investigation-agents",
        "group": AI,
        "name": "Fraud investigation agents",
        "line": "A team of agents that investigates card-fraud alerts and has its reports checked against the evidence.",
        "headline": ("77%", "fraud patterns named correctly, up from 47% for a single model call"),
        "problem": "Agents that investigate fraud alerts are easy to demo and hard to trust: they can name a "
        "pattern the data does not show, skip a check, or clear a fraudulent purchase in confident prose.",
        "solution": "A LangGraph team. A Planner chooses which checks to run, a Researcher runs them through "
        "two MCP servers (card activity and the fraud model), a Reporter writes a verdict that cites the "
        "evidence, and a rule-based Critic rejects reports the evidence does not support and sends the work "
        "back. It runs on a local 3B model on a free CPU runner.",
        "how": [
            "Code fetches every number; the language models only decide what to check and what it means.",
            "The Critic is rules over the evidence, so its decisions are reproducible and explainable.",
            "Measured on 30 alerts with known answers against the fraud model alone, plain rules and a single LLM call.",
        ],
        "results": [
            ("77%", "fraud pattern right, against 47% for a single LLM call"),
            ("6 of 7", "legitimate purchases cleared, against 2 of 7 in the first evaluation run"),
            ("83%", "verdict right (fraud or legitimate) on all 30 alerts"),
        ],
        "limits": "The data is synthetic. The Critic checks the verdict, fraud type and cited evidence, not "
        "the free-text summary, which can still misstate the evidence.",
        "stack": ["LangGraph", "MCP", "Ollama", "XGBoost", "pytest"],
        "video": "fraud-investigation-agents",
        "video_caption": "Two investigations recorded in the evaluation: the Critic rejects the first report "
        "with the rule it breaks and the second round reaches the right verdict.",
    },
    {
        "slug": "sec-mcp-agent",
        "group": AI,
        "name": "SEC MCP agent",
        "line": "MCP servers over SEC filings and a fraud model, and an agent whose citations are checked against the source.",
        "headline": ("17 of 22", "evaluation questions passed, up from 7 over six measured runs"),
        "problem": "Answers about filings are only useful if every claim can be traced to the source, and small "
        "models invent sources that look real. Tools are also usually wired into one agent, so nothing else "
        "can use them.",
        "solution": "Two MCP servers, one over 10-K filings with BM25 search and one over the fraud model, and "
        "a tool-calling agent that answers from them. Every citation is checked against the passage it "
        "claims to quote before the answer is returned. The same servers plug into Claude Desktop.",
        "how": [
            "A citation passes only if its quote is found in the retrieved passage.",
            "Six evaluation runs on a CPU runner, each failure traced and fixed in the agent or the tools.",
            "The fraud tool reuses the XGBoost model from the real-time fraud project at a pinned commit.",
        ],
        "results": [
            ("17 of 22", "evaluation questions passed (7 in the first run)"),
            ("62", "tests, including the servers through the MCP client"),
            ("6", "measured evaluation runs, each failure traced to the agent or the tools and fixed"),
        ],
        "limits": "A 3B model still misses some multi-step questions; the evaluation set is small.",
        "stack": ["MCP Python SDK", "Pydantic", "Ollama", "XGBoost"],
        "video": "sec-mcp-agent",
        "video_caption": "Two answers recorded in the final evaluation run: the tool calls, the answer and its verified citations.",
    },
    {
        "slug": "llm-guardrails-redteam",
        "group": AI,
        "name": "LLM guardrails and red team",
        "line": "Guardrails around both agents and a red-team suite that attacks them on every pull request.",
        "headline": ("23 of 23", "attacks blocked, each proven to work without the guardrails"),
        "problem": "Agents read documents and call tools, so anyone who can write into a document, a merchant "
        "name or a question can try to steer them. A model's own refusals are not a defence, and traces "
        "quietly collect the personal data users type.",
        "solution": "Six layers wrapped around the agents without changing their code: input checks, quarantine "
        "of instructions found in data, personal-data redaction, a tool policy, output checks and redacted "
        "traces. The suite drives the real agents with a model that obeys any instruction it can see, so "
        "blocking never depends on a model refusing.",
        "how": [
            "Each attack must succeed without the guardrails and fail with them.",
            "Some attacks are worded to evade detection, so the later layers are tested on their own.",
            "A false-positive suite on real recorded data fails the build if anything legitimate is touched.",
        ],
        "results": [
            ("23 of 23", "attacks blocked across injection, exfiltration, tool misuse, critic bypass and logs"),
            ("0 of 283", "real texts flagged; 0 of 22 questions and 0 of 3 investigations changed"),
            ("66", "tests; the suite found a bug in the guardrails themselves"),
        ],
        "limits": "Injection detection is pattern-based; new phrasings will get past it, which is why the "
        "later layers are tested separately.",
        "stack": ["MCP", "LangGraph", "OpenTelemetry", "pytest"],
    },
    {
        "slug": "llm-evals-observability",
        "group": AI,
        "name": "LLM evals and observability",
        "line": "A regression gate on every pull request and weekly live evaluations traced into Langfuse.",
        "headline": ("162", "real model tool calls replayed on every pull request"),
        "problem": "Agents built on small local models fail in ways unit tests do not see: the model sends "
        "arguments the tools reject, a reply never ends, a fix in one place breaks another.",
        "solution": "Versioned datasets recorded from real runs, an offline gate that replays them on every "
        "pull request, weekly live runs of both agents traced with OpenTelemetry into a self-hosted Langfuse, "
        "and a public dashboard.",
        "how": [
            "Datasets are immutable and versioned with a sha256 manifest.",
            "Baselines carry tolerances measured from run-to-run variance.",
            "Langfuse runs inside CI with Docker Compose, so tracing is tested end to end.",
        ],
        "results": [
            ("162", "recorded tool calls in the offline gate"),
            ("1", "regression blocked on a real pull request"),
            ("0.705", "live pass rate of the filings agent (± 0.15 across runs)"),
        ],
        "limits": "Live results vary between runs of the same code; the gate uses tolerances instead of exact values.",
        "stack": ["OpenTelemetry", "Langfuse", "GitHub Actions", "GitHub Pages"],
        "extra_links": [("Dashboard", "https://diegotddd.github.io/llm-evals-observability/")],
    },
    {
        "slug": "finetune-and-serve",
        "group": AI,
        "name": "Fine-tune and serve",
        "line": "A 0.5B model fine-tuned on a free CPU runner to tag financial facts in 10-K sentences, served with llama.cpp.",
        "headline": ("0.82", "F1 on auditor-tagged facts, against 0.65 for a 3B model prompted with examples"),
        "problem": "Structured extraction is usually done by prompting a large model, and every request pays "
        "for a long prompt on an API or on hardware big enough for the model. Whether a small model trained "
        "for the one job does better and costs less is a question of measurement.",
        "solution": "LoRA fine-tuning of Qwen2.5-0.5B on sentences from 10-K notes tagged by auditors with XBRL "
        "concepts (FiNER-139), export to GGUF with 8-bit and 4-bit quantization, and serving with llama.cpp. "
        "It is compared with prompting the same model and a 3B model on quality, latency, throughput and cost.",
        "how": [
            "Train, quantize, evaluate and benchmark in one GitHub Actions workflow on a 4-core CPU.",
            "Loss and output logits only at the answer tokens, so a 152k-token vocabulary fits in memory.",
            "Every model served by the same llama-server with the same JSON schema enforced by the grammar.",
            "Cost from a VM the runner's size against API list prices with the measured prompt sizes.",
        ],
        "results": [
            ("0.82", "fact F1 at 4 bits (398 MB), against 0.65 for Qwen2.5-3B with six examples and 0.19 before fine-tuning"),
            ("3.7×", "the requests per second of the 3B model on the same CPU (1.60 against 0.43)"),
            ("$35", "per million requests self-hosted at full load; Claude Haiku 5.5 at list price would cost $45 to $91"),
        ],
        "limits": "One training run, stopped by its time budget at 79% of an epoch; the APIs' accuracy on the "
        "task was not measured, only their price.",
        "stack": ["PyTorch", "PEFT", "llama.cpp", "GitHub Actions"],
        "extra_links": [("Model release", "https://github.com/DiegoTDDD/finetune-and-serve/releases/tag/model-44606410559")],
    },
    {
        "slug": "llm-from-scratch",
        "group": AI,
        "name": "LLM from scratch",
        "line": "A GPT-style model written from scratch and trained on 10-K filings on a free CPU runner.",
        "headline": ("32.0", "validation perplexity, against 837 for a unigram baseline"),
        "problem": "Most LLM projects call an API or fine-tune someone else's model. When something breaks, "
        "such as a tokenizer mismatch, a cache bug or a sampling setting, you need to understand the parts.",
        "solution": "Every part of a decoder-only transformer built and tested on its own: byte-level BPE, "
        "causal self-attention, the training loop, sampling and KV-cache decoding, trained on Business, "
        "Risk Factors and MD&A sections of 10-K filings.",
        "how": [
            "Each component has its own tests, including a naive BPE as a reference for the fast one.",
            "Training runs on the free GitHub Actions runner, so anyone can reproduce it.",
            "KV-cache decoding is checked to produce the same tokens as full recomputation.",
        ],
        "results": [
            ("32.0", "validation perplexity (837 for a unigram baseline)"),
            ("5.8×", "faster generation with the KV cache at 224 new tokens"),
            ("13M", "characters of 10-K text in the training set"),
        ],
        "limits": "A small model trained on one CPU: it learns the style of filings, not facts.",
        "stack": ["PyTorch", "GitHub Actions"],
        "image": "llm-from-scratch",
        "image_alt": "Training and validation loss curves",
    },
    {
        "slug": "sec-filings-rag",
        "group": AI,
        "name": "SEC filings RAG",
        "line": "Question answering over 10-K and 10-Q filings, with the sources each answer used.",
        "headline": ("0.80", "hit@5 for hybrid retrieval with re-ranking, against 0.43 for dense search"),
        "problem": "Analysts need answers from long filings they can verify, not a summary with no trace "
        "back to the text.",
        "solution": "Retrieval-augmented generation over the filings of Apple, NVIDIA and JPMorgan: hybrid "
        "dense and keyword retrieval, re-ranking, a local model through Ollama, and an evaluation that runs "
        "on GitHub Actions with RAGAS.",
        "how": [
            "66 questions, each generated from one known chunk, so retrieval is measured exactly.",
            "Five retrieval strategies compared; the measurements chose the hybrid pipeline.",
            "A public demo serves answers recorded from the real pipeline.",
        ],
        "results": [
            ("0.80", "hit@5 with hybrid search and re-ranking (dense alone 0.43)"),
            ("0.97", "recall@20 of the hybrid retriever"),
            ("66", "evaluation questions, run monthly on CI"),
        ],
        "limits": "The public demo replays recorded answers, because a free host cannot run Qdrant and Ollama.",
        "stack": ["Qdrant", "Ollama", "sentence-transformers", "FastAPI", "RAGAS"],
        "demo": "https://sec-filings-rag-demo.streamlit.app",
        "image": "sec-filings-rag",
        "image_alt": "The dashboard answering a question about Apple with its sources",
    },
    {
        "slug": "freight-intelligence",
        "group": DATA,
        "name": "LogiNexus freight intelligence",
        "line": "Freight analytics for the US and Brazil: a 97.6-million-row pipeline, forecasting, optimization and routing.",
        "headline": ("97.6M", "rows through the medallion pipeline"),
        "problem": "Freight planning needs volumes by corridor and mode, forecasts that hold up on years they "
        "were not trained on, and allocations that respect capacity, from sources with different units and gaps.",
        "solution": "A medallion pipeline over the US Freight Analysis Framework and Brazilian rail, road, "
        "water, air and pipeline sources, evaluated forecasting baselines, a transport optimizer, truck-aware "
        "routing and a documented read-only API.",
        "how": [
            "Bronze, Silver and Gold layers with staged file replacement and source hashes.",
            "Forecasts evaluated with expanding windows and reserved test years.",
            "Routing with separate car and truck engines that respect dimensions and weight.",
        ],
        "results": [
            ("97.6M", "rows processed from source CSV to Gold"),
            ("5", "Brazilian transport modes with observed histories"),
            ("510", "observed cabotage port pairs, all 98 reviewed origins"),
        ],
        "limits": "The free demo host sleeps after 15 minutes; the first visit can take about a minute.",
        "stack": ["Python", "Polars", "DuckDB", "FastAPI", "Docker"],
        "demo": "https://loginexus-dashboard-preview.onrender.com/",
        "image": "freight-intelligence",
        "image_alt": "Freight analytics overview in the dashboard",
    },
    {
        "slug": "realtime-fraud-detection-ml",
        "group": DATA,
        "name": "Real-time fraud detection",
        "line": "An XGBoost model scoring a live Kafka stream, with precision and recall for each fraud pattern.",
        "headline": ("0.9925", "PR-AUC on the latest 20% of transactions, split by time"),
        "problem": "A monitor that only counts transactions tells a fraud team what already happened. Each "
        "transaction needs a score the moment it arrives, and the team must know which kinds of fraud it misses.",
        "solution": "An XGBoost classifier trained offline scores every transaction inside Spark Structured "
        "Streaming. A dashboard shows live precision and recall for each fraud pattern, and a model card "
        "documents the weak spots.",
        "how": [
            "The threshold maximizes mean recall across patterns while keeping precision at 95% or more.",
            "Training and streaming compute features with the same code, checked by a test.",
            "The model is reused by the SEC MCP agent and the fraud investigation agents.",
        ],
        "results": [
            ("0.9925", "PR-AUC"),
            ("95.8% / 96.6%", "precision and recall at the chosen threshold"),
            ("64.7%", "recall on impossible travel, the documented weak spot"),
        ],
        "limits": "Trained on synthetic transactions; impossible travel is partly indistinguishable from real travel.",
        "stack": ["XGBoost", "Spark Structured Streaming", "Kafka", "Streamlit"],
        "demo": "https://realtime-fraud-detection-ml.streamlit.app",
        "image": "realtime-fraud-detection-ml",
        "image_alt": "Live scoring dashboard",
    },
    {
        "slug": "realtime-fraud-streaming",
        "group": DATA,
        "name": "Real-time fraud streaming",
        "line": "A streaming pipeline that counts every fraud pattern per minute, with a data contract on the way in.",
        "headline": ("~10/s", "card transactions through Redpanda and Spark"),
        "problem": "Card fraud happens in seconds, and its signal is in patterns over time. A nightly batch "
        "report sees it a day late.",
        "solution": "Transactions flow from Redpanda through Spark Structured Streaming into Parquet layers "
        "and a live dashboard, with event-time windows and watermarks. Every event is checked against one "
        "contract by the producer and again by Spark; failures are quarantined with the reasons.",
        "how": [
            "One row per minute in Gold: counts, amounts and fraud by pattern.",
            "A minute is written about two minutes after it ends, to wait for late events.",
            "CI runs the full pipeline on Linux with Redpanda and on Windows with Kafka.",
        ],
        "results": [
            ("~10/s", "transactions, keyed by card over 3 partitions"),
            ("~2 min", "from the end of a minute to its row in Gold"),
            ("24", "tests, including Spark on a local session"),
        ],
        "limits": "The public dashboard serves a recorded sample of the stream.",
        "stack": ["Redpanda", "Spark Structured Streaming", "Parquet", "Streamlit"],
        "demo": "https://realtime-fraud-streaming.streamlit.app",
        "image": "realtime-fraud-streaming",
        "image_alt": "Streaming dashboard overview",
    },
    {
        "slug": "supply-chain-risk-intelligence",
        "group": DATA,
        "name": "Supply chain risk intelligence",
        "line": "Delivery delay from cause to decision: causal inference, survival analysis, forecasting, risk and optimization.",
        "headline": ("94.8%", "of the riskiest tenth of orders are actually late"),
        "problem": "“We are often late” is not something operations can act on. They need the cause, the "
        "timing, the volume coming, the orders at risk and what to change.",
        "solution": "Five connected analyses of 180,519 real orders: propensity score matching, survival "
        "models, demand forecasting, a calibrated risk model explained with SHAP, and a linear program that "
        "turns the risk scores into a cheaper shipping allocation.",
        "how": [
            "Causal effect estimated on 35,216 matched pairs with balanced covariates.",
            "Forecasts compared with a naive baseline on a 30-day holdout.",
            "The optimization is stress-tested with 10,000 Monte Carlo runs.",
        ],
        "results": [
            ("1.99 days", "later delivery for Second Class than Standard Class, against the promise"),
            ("33%", "lower forecast error than the naive baseline (MAPE 5.9% vs 8.9%)"),
            ("94.8%", "of the top 10% riskiest orders are late (AUC 0.73)"),
        ],
        "limits": "The optimization saves 1.01% of expected cost: real, but small, and reported as such.",
        "stack": ["statsmodels", "lifelines", "Prophet", "XGBoost", "SHAP", "PuLP"],
        "demo": "https://diego-supply-chain-risk.streamlit.app",
        "image": "supply-chain-risk-intelligence",
        "image_alt": "Forecast comparison against the naive baseline",
    },
    {
        "slug": "nyc-tip-mlops",
        "group": DATA,
        "name": "NYC tip MLOps",
        "line": "Versioned training, a model registry with automatic promotion, an API and drift monitoring.",
        "headline": ("29", "tests over features, promotion rule, registry and every API endpoint"),
        "problem": "A model is only useful in production if every step around it can be trusted: repeatable "
        "training, a rule for which version is live, features computed the same way in serving, and a "
        "signal when the data changes.",
        "solution": "An MLOps system around a classifier that predicts at pickup whether a NYC taxi ride will "
        "tip more than 20%: MLflow tracking and registry, a FastAPI service, Evidently drift reports, a "
        "Streamlit operations dashboard, and CI that runs the whole loop including Docker.",
        "how": [
            "No label leakage: only what is known at pickup is used, which caps the score honestly.",
            "A new version becomes the champion only if its validation AUC beats the current one.",
            "A test checks that the API computes features exactly as training does.",
        ],
        "results": [
            ("0.624", "validation AUC without label leakage"),
            ("4% → 13%", "drift in the share of unknown payment type, caught from 2024 to 2025"),
            ("29", "tests, plus a weekly retrain in CI"),
        ],
        "limits": "Tipping is hard to predict from trip data; the project's value is the engineering around the model.",
        "stack": ["MLflow", "FastAPI", "Evidently", "Docker", "Streamlit"],
        "demo": "https://nyc-tip-mlops.streamlit.app",
        "image": "nyc-tip-mlops",
        "image_alt": "Operations dashboard with the live model",
    },
    {
        "slug": "nyc-taxi-lakehouse",
        "group": DATA,
        "name": "NYC taxi lakehouse",
        "line": "A Delta Lake medallion lakehouse over 22.3 million trips, measuring the effect of congestion pricing.",
        "headline": ("−15.1%", "average Manhattan trip duration after the congestion fee"),
        "problem": "Whether New York's 2025 congestion fee changed taxi use means combining months of trip "
        "files whose schema changes mid-way, removing about a fifth of the records as invalid, and trusting "
        "the aggregates that come out.",
        "solution": "Bronze, Silver and Gold layers in Delta Lake, transformed with DuckDB and orchestrated by "
        "Dagster, with ten data-quality checks that stop bad data before it reaches the numbers.",
        "how": [
            "Schema evolution handles the fee column that only exists from 2025.",
            "Quality checks block the pipeline instead of passing bad rows downstream.",
            "Assets and their lineage are visible in Dagster.",
        ],
        "results": [
            ("22.3M", "trips in the lakehouse"),
            ("−10.7%", "Manhattan pickups after the fee"),
            ("−15.1%", "average trip duration"),
        ],
        "limits": "Before and after periods fall in different seasons, so part of the change may be seasonal.",
        "stack": ["Delta Lake", "DuckDB", "Dagster", "Streamlit"],
        "demo": "https://nyc-taxi-lakehouse.streamlit.app",
        "image": "nyc-taxi-lakehouse",
        "image_alt": "Congestion pricing impact on the dashboard",
    },
    {
        "slug": "olist-analytics",
        "group": DATA,
        "name": "Olist e-commerce analytics",
        "line": "A tested dbt star schema over 100,000 orders that measures how much late deliveries hurt reviews.",
        "headline": ("4.29 → 2.99", "average review when an order is 1 to 5 days late"),
        "problem": "A marketplace knows late deliveries hurt reviews, but not how much, how quickly, or "
        "whether to reduce the size of delays or prevent them altogether.",
        "solution": "A star schema built with dbt on DuckDB over about 100,000 real Olist orders, with tests "
        "for every business rule, and a dashboard that answers the question.",
        "how": [
            "14 dbt models and 35 tests run on every change, from the raw files.",
            "Five singular tests encode the business rules.",
            "The dashboard has screenshots in the repository in case the free app is asleep.",
        ],
        "results": [
            ("4.29", "average review for orders on time"),
            ("2.99", "for orders 1 to 5 days late: the drop happens on the first day"),
            ("35", "dbt tests on 14 models"),
        ],
        "limits": "Correlation from observational data; late orders may differ in other ways.",
        "stack": ["dbt", "DuckDB", "Streamlit"],
        "demo": "https://diegotddd-olist-analytics.streamlit.app",
        "image": "olist-analytics",
        "image_alt": "Dashboard overview",
    },
    {
        "slug": "economic-data-platform",
        "group": DATA,
        "name": "Economic data platform",
        "line": "ELT for Brazilian macro indicators and market data that never shows an empty or half-written table.",
        "headline": ("5", "quality checks every batch must pass before it may replace the Gold layer"),
        "problem": "Public economic data sources fail in ordinary ways: rate limits, timeouts, empty answers, "
        "a changed format. A dashboard fed straight from them goes blank or shows wrong numbers unnoticed.",
        "solution": "An ELT platform that pulls Banco Central do Brasil indicators and Yahoo Finance data with "
        "retries, checks every batch before it may replace the PostgreSQL Gold layer, writes it atomically "
        "and serves it on a dashboard.",
        "how": [
            "Range, null, duplicate, future-date and row-count checks on every batch.",
            "A failing batch is rejected and Gold keeps its previous data.",
            "A test proves on a real PostgreSQL that a failed insert rolls back the delete.",
        ],
        "results": [
            ("5", "quality checks on every batch before it reaches Gold"),
            ("3", "attempts per step, with backoff on rate limits and timeouts"),
            ("1", "transaction per refresh: Gold is never empty"),
        ],
        "limits": "The public dashboard reads a Gold snapshot that CI refreshes monthly.",
        "stack": ["PostgreSQL", "Docker", "GitHub Actions", "Streamlit"],
        "demo": "https://diegotddd-economic-data-platform.streamlit.app",
        "repo": "Economic-data-platform",
        "image": "economic-data-platform",
        "image_alt": "Macroeconomic indicators on the dashboard",
    },
]
