"""Content of the site: one entry per project, taken from each repository's README.

Every number here is a measured result stated in that README; the check in CI fails if a
project has no result or no link to its code.
"""

GH = "https://github.com/DiegoTDDD/"

AI, DATA, TEAM = "ai", "data", "team"
GROUPS = {
    AI: "AI engineering",
    DATA: "Data engineering and machine learning",
    TEAM: "Team projects in real use",
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
        "solution": "A LangGraph team. A planner chooses which checks to run, a researcher runs them through "
        "two MCP servers (card activity and the fraud model), a reporter writes a verdict that cites the "
        "evidence, and a rule-based critic rejects reports the evidence does not support and sends the work "
        "back. It runs on a local 3B model on a free CPU runner.",
        "how": [
            "Code fetches every number; the language models only decide what to check and what it means.",
            "The critic is rules over the evidence, so its decisions are reproducible and explainable.",
            "Measured on 30 alerts with known answers against the fraud model alone, plain rules and a single LLM call.",
        ],
        "results": [
            ("77%", "fraud pattern right, against 47% for a single LLM call"),
            ("6 of 7", "legitimate purchases cleared, against 2 of 7 in the first evaluation run"),
            ("83%", "verdict right (fraud or legitimate) on all 30 alerts"),
        ],
        "limits": "The data is synthetic. The critic checks the verdict, fraud type and cited evidence, not "
        "the free-text summary, which can still misstate the evidence.",
        "stack": ["LangGraph", "MCP", "Ollama", "XGBoost", "pytest"],
        "video": "fraud-investigation-agents",
        "video_caption": "A real investigation recorded in the evaluation: the critic rejects the first report "
        "with the rule it breaks, the second round gets it right, and the result across all 30 alerts.",
    },
    {
        "slug": "sec-mcp-agent",
        "group": AI,
        "name": "SEC MCP agent",
        "line": "MCP servers over SEC filings and a fraud model, and an agent whose citations are checked against the source.",
        "headline": ("18 of 22", "evaluation questions passed in the seventh measured run, up from 7 in the first"),
        "problem": "Answers about filings are only useful if every claim can be traced to the source, and small "
        "models invent sources that look real. Tools are also usually wired into one agent, so nothing else "
        "can use them.",
        "solution": "Two MCP servers, one over 10-K filings with BM25 search and one over the fraud model, and "
        "a tool-calling agent that answers from them. Every citation is checked against the passage it "
        "claims to quote before the answer is returned. The same servers plug into Claude Desktop.",
        "how": [
            "A citation passes only if its quote is found in the retrieved passage.",
            "Seven evaluation runs on a CPU runner, each failure traced and fixed in the agent or the tools; the evaluation reruns every week.",
            "The fraud tool reuses the XGBoost model from the real-time fraud project at a pinned commit.",
        ],
        "results": [
            ("18 of 22", "evaluation questions passed in the seventh run (7 in the first)"),
            ("64", "tests, including the servers through the MCP client"),
            ("7", "measured evaluation runs, each failure traced to the agent or the tools and fixed"),
        ],
        "limits": "A 3B model still misses some multi-step questions; the evaluation set is small.",
        "stack": ["MCP Python SDK", "Pydantic", "Ollama", "XGBoost"],
        "video": "sec-mcp-agent",
        "video_caption": "Two answers recorded in the sixth evaluation run: the tool calls, the answer and its verified citations.",
    },
    {
        "slug": "olist-ai-analyst",
        "group": AI,
        "name": "Olist AI analyst",
        "line": "A local-model analyst that turns a business question into a decision memo, with code checking the SQL and every number.",
        "headline": ("68%", "of 25 business questions answered with the same result as hand-written reference SQL"),
        "problem": "A model writing SQL fails in ways that look right: a query that runs but filters the wrong "
        "rows, or a memo that quotes a number the query never produced. An analyst's answer is only worth "
        "something if the decision maker can trust it.",
        "solution": "An analyst over the real Olist marketplace data (99,441 orders) that follows the five steps "
        "of the Data-Driven Decisions books: name the decision, trust the data, show the work, read the trend "
        "and make it last. The model writes the SQL and the memo; code checks the SQL, runs it read-only, reads "
        "the trend and requires every number in the memo to exist in the result.",
        "how": [
            "DuckDB's own parser allows one SELECT over three analysis tables, on a read-only connection with file and network access off.",
            "Errors go back to the model, up to three tries; a memo with a number not in the result gets one rewrite, then is marked unverified.",
            "The trend is read by code from a fitted line over full months, never described by the model.",
            "An evaluation with reference SQL runs weekly with Ollama on a free CPU runner and commits its results.",
        ],
        "results": [
            ("68%", "execution accuracy on 25 questions with qwen2.5-coder 7B, in the third of three measured runs"),
            ("92%", "of memos with every number found in the query result; the others are marked unverified"),
            ("100%", "valid SQL after retries with the error message (88% on the first try)"),
        ],
        "limits": "The number check proves a number exists in the result, not that the sentence attaches it to "
        "the right row; the questions are few and were written by the same person as the pipeline.",
        "stack": ["DuckDB", "Ollama", "Qwen2.5-Coder", "GitHub Actions"],
        "extra_links": [("Evaluation results", "https://github.com/DiegoTDDD/olist-ai-analyst/blob/main/eval/results.md")],
    },
    {
        "slug": "llm-guardrails-redteam",
        "group": AI,
        "name": "LLM guardrails and red team",
        "line": "Guardrails around both agents and a red-team suite that attacks them on every pull request.",
        "headline": ("26 of 27", "attacks blocked, each proven to work without the guardrails; one reported as a gap"),
        "problem": "Agents read documents and call tools, so anyone who can write into a document, a merchant "
        "name or a question can try to steer them. A model's own refusals are not a defence, and traces "
        "quietly collect the personal data users type.",
        "solution": "Six layers wrapped around the agents without changing their code: input checks, quarantine "
        "of instructions found in data, personal-data redaction, a tool policy, output checks and redacted "
        "traces. The suite drives the real agents with a model that obeys any instruction it can see, so "
        "blocking never depends on a model refusing.",
        "how": [
            "Each attack must succeed without the guardrails and fail with them.",
            "Some attacks are worded to evade detection, so the later layers are tested on their own; reworded "
            "injections go to a local trained classifier whose threshold the false-positive suite sets.",
            "A false-positive suite on real recorded data fails the build if anything legitimate is touched.",
        ],
        "results": [
            ("26 of 27", "attacks blocked across injection, exfiltration, tool misuse, critic bypass and logs"),
            ("0 of 283", "real texts flagged; 0 of 22 questions and 0 of 3 investigations changed"),
            ("79", "tests; the suite found a bug in the guardrails themselves"),
        ],
        "limits": "Patterns and a classifier still miss some phrasings: one reworded document instruction gets "
        "through and is kept in the suite as a known gap, which is why the later layers are tested separately.",
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
            "KV-cache decoding is checked to produce the same tokens as full recomputation, also past the "
            "context with a sliding window; fused attention is measured against the written-out one.",
        ],
        "results": [
            ("32.0", "validation perplexity (837 for a unigram baseline)"),
            ("5.0×", "faster generation with the KV cache at 224 new tokens, checked token for token"),
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
        "line": "An XGBoost model scoring a live Kafka stream, with per-card state that survives restarts, exactly-once predictions and a model monitor.",
        "headline": ("0", "missing or duplicate predictions after the scoring job is killed mid-stream and restarted, checked in CI"),
        "problem": "A monitor that only counts transactions tells a fraud team what already happened. Each "
        "transaction needs a score the moment it arrives, and the team must know which kinds of fraud it misses.",
        "solution": "An XGBoost classifier trained offline scores every transaction inside Spark Structured "
        "Streaming. Each card's recent history lives in Spark's state store, predictions go to Delta exactly "
        "once, and a monitor checks live precision, recall and input drift against written thresholds.",
        "how": [
            "The threshold is chosen on a validation period; every reported number comes from a later test period no choice has seen.",
            "A Spark test restarts the query and gets the same velocity features as training; CI kills the job with SIGKILL and finds one prediction per Kafka message.",
            "The monitor alerts only when the 95% interval lies below a floor, and flags drift by PSI.",
            "The model is reused by the SEC MCP agent and the fraud investigation agents.",
        ],
        "results": [
            ("96.6% / 96.6%", "precision and recall on the test period (PR-AUC 0.992)"),
            ("4,597 / 4,597", "Kafka messages and predictions after a SIGKILL restart in CI"),
            ("64.2%", "recall on impossible travel, the documented weak spot"),
        ],
        "limits": "Trained on synthetic transactions; impossible travel is partly indistinguishable from real travel.",
        "stack": ["XGBoost", "Spark Structured Streaming", "Delta Lake", "Kafka", "Streamlit"],
        "demo": "https://realtime-fraud-detection-ml.streamlit.app",
        "image": "realtime-fraud-detection-ml",
        "image_alt": "Live scoring dashboard",
    },
    {
        "slug": "realtime-fraud-streaming",
        "group": DATA,
        "name": "Real-time fraud streaming",
        "line": "A streaming pipeline on Delta Lake that survives a crash without losing or repeating a record, with a schema registry and health checks.",
        "headline": ("0", "records lost or duplicated after the job is killed mid-stream and restarted, checked in CI"),
        "problem": "Card fraud happens in seconds, and its signal is in patterns over time. A nightly batch "
        "report sees it a day late.",
        "solution": "Transactions flow from Redpanda through Spark Structured Streaming into Delta Lake tables "
        "and a live dashboard, with event-time windows and watermarks. The event schema lives in a schema "
        "registry that refuses breaking changes; anything that breaks the contract is quarantined with the "
        "reasons. A health check passes or fails the stream and can alert a webhook.",
        "how": [
            "Delta sinks with checkpoints: CI kills the job with SIGKILL, restarts it, and finds every Kafka offset in Bronze exactly once.",
            "Compaction and vacuum run while the stream writes (66 files became 16 with the same rows in CI).",
            "The registry rejects an incompatible schema in CI; a message sent without it lands in quarantine.",
            "Progress of every query is logged; the health check fails within two minutes of the job stopping.",
        ],
        "results": [
            ("0", "duplicate or missing offsets after a crash and restart"),
            ("~2 min", "from the end of a minute to its row in Gold"),
            ("47", "tests, including Spark with Delta on a local session"),
        ],
        "limits": "One broker and local disk; alerts go to a webhook, not a paging service. The public dashboard serves a recorded sample.",
        "stack": ["Redpanda", "Schema Registry", "Spark Structured Streaming", "Delta Lake", "Streamlit"],
        "demo": "https://realtime-fraud-streaming.streamlit.app",
        "image": "realtime-fraud-streaming",
        "image_alt": "Streaming dashboard overview",
    },
    {
        "slug": "supply-chain-risk-intelligence",
        "group": DATA,
        "name": "Supply chain risk intelligence",
        "line": "Delivery delay from cause to decision: causal inference, survival analysis, forecasting, risk and optimization.",
        "headline": ("94.4%", "of the riskiest tenth of orders are actually late, re-checked on the real data in CI"),
        "problem": "“We are often late” is not something operations can act on. They need the cause, the "
        "timing, the volume coming, the orders at risk and what to change.",
        "solution": "Five connected analyses of 180,519 real orders: propensity score matching, survival "
        "models, demand forecasting, a calibrated risk model explained with SHAP, and a linear program that "
        "turns the risk scores into a cheaper shipping allocation.",
        "how": [
            "CI downloads the real dataset (checksum-pinned), validates it against a data contract, re-runs the notebooks and fails if any published number moves.",
            "Causal effect estimated on 35,216 matched pairs, all 78 covariate levels balanced.",
            "The optimization uses out-of-sample risk scores and is stress-tested with 10,000 Monte Carlo runs.",
        ],
        "results": [
            ("1.99 days", "later delivery for Second Class than Standard Class, against the promise"),
            ("33%", "lower forecast error than the naive baseline (MAPE 5.9% vs 8.9%)"),
            ("94.4%", "of the top 10% riskiest orders are late (AUC 0.73)"),
        ],
        "limits": "The optimization saves 0.85% of expected cost on orders the model never saw: real, but small, and reported as such.",
        "stack": ["statsmodels", "lifelines", "Prophet", "XGBoost", "SHAP", "PuLP"],
        "demo": "https://diego-supply-chain-risk.streamlit.app",
        "image": "supply-chain-risk-intelligence",
        "image_alt": "Forecast comparison against the naive baseline",
    },
    {
        "slug": "nyc-tip-mlops",
        "group": DATA,
        "name": "NYC tip MLOps",
        "line": "A monthly retrain on new real data, promotion by a statistical test, a model registry, an API and drift monitoring.",
        "headline": ("+0.010", "AUC for the model trained on August 2026 over the old champion on the same September trips; promoted because the 95% interval is above zero"),
        "problem": "A model is only useful in production if every step around it can be trusted: repeatable "
        "training, a rule for which version is live, features computed the same way in serving, and a "
        "signal when the data changes.",
        "solution": "An MLOps system around a classifier that predicts, when a NYC taxi ride ends and before "
        "payment, whether the tip will be more than 20%: MLflow tracking and registry, a FastAPI service, Evidently drift reports, a "
        "Streamlit operations dashboard, and CI that runs the whole loop including Docker.",
        "how": [
            "No label leakage: no payment field is used, only what is known when the ride ends, which caps the score honestly.",
            "Every month CI finds the newest TLC month, trains a challenger and compares it with the champion on the same out-of-time month; it is promoted only if the paired-bootstrap interval of the gain is above zero.",
            "A test checks that the API computes features exactly as training does.",
        ],
        "results": [
            ("0.625 vs 0.615", "AUC of the new and old champion on 500,000 September 2026 trips"),
            ("4% → 13%", "drift in the share of unknown payment type, caught from 2024 to 2025"),
            ("42", "tests, plus the monthly retrain on real data in CI"),
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
        "line": "A Delta Lake lakehouse over 42 million trips, processed month by month, that separates the congestion fee's effect from winter.",
        "headline": ("−0.4 pts", "change in Manhattan trips per day due to the fee, once winter is taken out; the raw drop was 10.7%"),
        "problem": "Whether New York's 2025 congestion fee changed taxi use: the fee started in January, so a "
        "simple before/after mixes it with winter, and the trip files change schema mid-way and hold invalid records.",
        "solution": "Bronze, Silver and Gold layers in Delta Lake over two Oct-Mar seasons, transformed with DuckDB "
        "and orchestrated by Dagster as monthly partitions. The estimate subtracts what winter did in the season "
        "before the fee, and eleven data-quality checks stop bad data before it reaches the numbers.",
        "how": [
            "Each month is a Dagster partition written with a predicate overwrite: added or redone alone, and redoing it changes nothing.",
            "Tests prove month-by-month and all-at-once builds give identical Gold tables.",
            "The same months a year earlier, without the fee, are the control for the season.",
            "Blocking quality checks stop the run before bad rows reach Gold.",
        ],
        "results": [
            ("−0.4 pts", "trips per day: the 10.7% raw drop is almost all winter"),
            ("−3.6 pts", "trip duration attributable to the fee, with distance unchanged"),
            ("42.1M", "trips in twelve monthly partitions"),
        ],
        "limits": "Assumes winter changes taxi use the same way every year; yellow taxis only.",
        "stack": ["Delta Lake", "DuckDB", "Dagster", "Streamlit"],
        "demo": "https://nyc-taxi-lakehouse.streamlit.app",
        "image": "nyc-taxi-lakehouse",
        "image_alt": "Congestion pricing impact on the dashboard",
    },
    {
        "slug": "olist-cloud-warehouse",
        "group": DATA,
        "name": "Olist cloud warehouse",
        "line": "A BigQuery warehouse fed by a daily change feed, with incremental dbt models, freshness alerts, Terraform and keyless CI.",
        "headline": ("0", "rows of difference between the daily incremental build and a full rebuild, checked on every pull request"),
        "problem": "A warehouse is trusted only if its tables keep their shape, every change is tested before it "
        "reaches analysts, nobody holds a long-lived cloud key, and someone knows what each query costs.",
        "solution": "The Olist marketplace data in BigQuery (Sao Paulo region), arriving the way production data "
        "does: a daily change feed in which orders are bought, shipped, delivered and reviewed on different days. "
        "The fact tables update incrementally, freshness is monitored and failures open an alert. Infrastructure "
        "in Terraform, dbt contracts on every table, and GitHub Actions that authenticate through Workload "
        "Identity Federation as two least-privilege service accounts.",
        "how": [
            "The 2016-2018 history is replayed one day per real day; each batch replaces its own raw partition, so reruns and catch-ups after an outage are idempotent.",
            "The fact tables rebuild only the purchase months with a changed order and swap them in with copy jobs, since the sandbox has no MERGE.",
            "Every pull request replays 31 days in throwaway datasets, builds incrementally and from scratch, and fails unless both hold the same rows.",
            "Freshness is checked after every deploy and every six hours; a failure opens a GitHub issue, and a runbook says what to do.",
            "Terraform creates the datasets, two service accounts, the federation trust and a one-permission custom role.",
        ],
        "results": [
            ("1 day", "of new data per real day, loaded idempotently, with catch-up after an outage"),
            ("80%+", "fewer bytes read by a one-month question on the partitioned fact table, measured every deploy"),
            ("0", "service account keys: CI uses one-hour tokens from GitHub's OIDC identity"),
        ],
        "limits": "The change feed replays real events rather than a live system, and the data is about 100,000 orders. "
        "The BigQuery sandbox has no Cloud Storage, so Terraform state stays in Cloud Shell and is applied by hand.",
        "stack": ["BigQuery", "Terraform", "dbt", "Workload Identity Federation", "GitHub Actions"],
        "extra_links": [
            ("Project page", "https://diegotddd.github.io/olist-cloud-warehouse/"),
            ("dbt docs", "https://diegotddd.github.io/olist-cloud-warehouse/dbt/"),
        ],
    },
    {
        "slug": "olist-analytics",
        "group": DATA,
        "name": "Olist e-commerce analytics",
        "line": "A tested dbt star schema over 100,000 orders and a Power BI report that measure how much late deliveries hurt reviews.",
        "headline": ("4.29 → 1.81", "average review on time vs. 6 days late; after that it barely moves"),
        "problem": "A marketplace knows late deliveries hurt reviews, but not how much, how quickly, or "
        "whether to reduce the size of delays or prevent them altogether.",
        "solution": "A star schema built with dbt on DuckDB over about 100,000 real Olist orders, with tests "
        "for every business rule, a three-page Power BI report on top of it and a Streamlit dashboard.",
        "how": [
            "15 dbt models and 48 tests run on every change, from the raw files.",
            "The two fact tables are incremental. CI replays the order feed day by day from the event times in the data "
            "and proves they equal a full rebuild at every step; source freshness fails a load over 50 hours old.",
            "The Power BI model (TMDL) and pages (PBIR) are generated as code: 23 DAX measures, a marked date "
            "table, and page texts computed from the data. CI fails if they drift from the committed files.",
            "The report was opened, refreshed and checked in Power BI Desktop; the .pbix is in the repository.",
        ],
        "results": [
            ("6.8%", "of delivered orders arrive late"),
            ("3.73 → 2.68", "average review 1 day late vs. 3 days late: each day in the first week costs rating"),
            ("48", "dbt tests on 15 models"),
        ],
        "limits": "Correlation from observational data; late orders may differ in other ways.",
        "stack": ["dbt", "DuckDB", "Power BI", "DAX", "Streamlit"],
        "demo": "https://diegotddd-olist-analytics.streamlit.app",
        "extra_links": [("Power BI file (.pbix)", "https://github.com/DiegoTDDD/olist-analytics/raw/main/powerbi/OlistEntregas.pbix")],
        "image": "olist-analytics",
        "image_alt": "Power BI page: average review by days late, with the decision it supports",
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
    {
        "slug": "hospcall",
        "group": TEAM,
        "repo": None,
        "name": "Hospcall: nurse-call system for an elder-care home",
        "line": "A call system piloted for six months at a geriatric care association, built by a team of seven UNIVESP students.",
        "headline": ("60", "caregivers registered in a six-month pilot at AGERIP"),
        "my_part": "I worked on every stage with the team: the requirement meetings with the AGERIP staff, "
        "the PostgreSQL data model and audit table, the API and real-time channel, the React screens for "
        "tablets, TVs and admin, deployment and the six-month pilot follow-up.",
        "problem": "At AGERIP, a geriatric care association in São José do Rio Preto, a resident who needed help "
        "depended on a caregiver walking past the room, and the shift record depended on handwritten notes. "
        "Refused calls, hand-overs in the middle of a call and care by staff outside the roster left no trace. "
        "Commercial nurse-call systems need dedicated wiring and maintenance contracts a charity cannot pay for.",
        "solution": "A web system on ordinary hardware: a tablet in each room opens the call, TV panels in the "
        "corridors show it in real time, caregivers check in with a PIN, and the nursing team manages calls, "
        "devices and exports from an admin page. Every administrative intervention is written to an immutable "
        "audit table instead of overwriting the call.",
        "how": [
            "Requirements came from meetings with the general manager, the head nurse and a nurse at AGERIP.",
            "Their feedback changed the product: PIN always available, tablets that register themselves, a TV grid "
            "configured remotely, and the open-time counter removed because it made the staff anxious.",
            "The real-time channel reconnects on its own after a dropped connection, tested under induced failures.",
        ],
        "results": [
            ("56", "calls in the pilot, October 2025 to March 2026, 41 completed"),
            ("≤ 39 ms", "median reconnection of the real-time channel; 67 ms at worst"),
            ("11", "new requirements from the final review meeting with the care team, in May 2026"),
        ],
        "limits": "Three rooms were instrumented and the response time to a call was not recorded, so the pilot "
        "shows adoption and stability, not a faster response. Tests were manual. The code belongs to the team "
        "and is not public.",
        "stack": ["React", "Node.js / Bun", "Express", "PostgreSQL", "Redis", "WebSocket", "Prisma"],
        "image": "hospcall",
        "image_alt": "Corridor TV panel showing six rooms, one with an open call",
    },
    {
        "slug": "iefa-sales-stock",
        "group": TEAM,
        "repo": None,
        "name": "Sales and stock system for a charity shop",
        "line": "A point-of-sale and stock system that the volunteers of IEFA's shop use on every working day, built by a team of eight UNIVESP students.",
        "headline": ("100%", "of the planned features delivered; in use on every working day of the shop since about July 2026"),
        "my_part": "I worked on every stage with the team: the stock count and product registration, the "
        "Django models and MySQL database, the point of sale, the reports and labels, the installation on the "
        "shop's computer and the follow-up with the volunteers, including the stock-exit fix.",
        "problem": "The shop of the Instituto Educacional Francisco de Assis, in São José do Rio Preto, recorded "
        "sales on paper and in notebooks and had no structured stock control. Not every item carried its "
        "price, which led to wrong prices at the counter.",
        "solution": "A Django and MySQL system with a barcode point of sale, products, stock movements, payment "
        "methods, users and sales reports, installed on the shop's Windows computer as a service. Every sale "
        "writes its stock exit automatically, and new stock prints its barcode labels.",
        "how": [
            "The team counted the whole stock, registered every product and printed the labels before go-live.",
            "Watching the volunteers use it added features nobody had asked for: remove an item, cancel a sale, "
            "initial stock in the product form and search everywhere.",
            "A defect in the stock exits of sales was fixed in the code and the missing movements were repaired "
            "with a SQL script.",
        ],
        "results": [
            ("0", "reports of wrong or missing prices since the barcode labels were adopted"),
            ("9", "modules in production: sales, point of sale, stock, products, categories, payments, users, reports, labels"),
            ("2", "reports the volunteers use in their routine: sales by payment method and label printing"),
        ],
        "limits": "Results are observed, not measured: there is no before-and-after count of errors. Tests are "
        "manual, and the volunteers share one login, so actions are not traceable to a person. The code belongs "
        "to the team and is not public.",
        "stack": ["Python", "Django", "MySQL", "Waitress", "WhiteNoise", "NSSM"],
        "image": "iefa-sales",
        "image_alt": "Point of sale with two items read by barcode and the sale total",
    },
]
