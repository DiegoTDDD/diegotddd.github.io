"""Everything on the site that is not a project: profile, skills, education and the
interface text, in Portuguese (default) and English. Also the filter categories and the CI
workflow of each project, used for the live status badges."""

AVATAR = "https://avatars.githubusercontent.com/u/183739024?v=4&s=320"
GITHUB_PROFILE = "https://github.com/DiegoTDDD"
EMAIL = "diegoleonardo380@gmail.com"
WHATSAPP = "https://wa.me/5517981857271"
PHONE = {"pt": "(17) 98185-7271", "en": "+55 17 98185-7271"}

# The three cases the home page opens with, each proving a different skill.
FEATURED = ["olist-cloud-warehouse", "freight-intelligence", "fraud-investigation-agents"]

# Filter categories for the project list.
CATEGORIES = {
    "llm": {"pt": "LLMs e agentes", "en": "LLMs and agents"},
    "ml": {"pt": "Machine learning", "en": "Machine learning"},
    "mlops": {"pt": "MLOps", "en": "MLOps"},
    "data": {"pt": "Engenharia de dados", "en": "Data engineering"},
    "streaming": {"pt": "Streaming", "en": "Streaming"},
    "analytics": {"pt": "Análise e estatística", "en": "Analytics and statistics"},
    "team": {"pt": "Com usuários reais", "en": "With real users"},
}

# slug -> (categories, main CI workflow file, or None for team projects without public CI)
META = {
    "fraud-investigation-agents": (["llm"], "tests.yml"),
    "sec-mcp-agent": (["llm"], "tests.yml"),
    "olist-ai-analyst": (["llm", "analytics"], "tests.yml"),
    "llm-guardrails-redteam": (["llm"], "redteam.yml"),
    "llm-evals-observability": (["llm", "mlops"], "gate.yml"),
    "finetune-and-serve": (["llm", "mlops"], "ci.yml"),
    "llm-from-scratch": (["llm", "ml"], "tests.yml"),
    "sec-filings-rag": (["llm"], "tests.yml"),
    "freight-intelligence": (["data", "ml", "analytics"], "ci_pipeline.yml"),
    "realtime-fraud-detection-ml": (["ml", "streaming", "mlops"], "tests.yml"),
    "realtime-fraud-streaming": (["data", "streaming"], "tests.yml"),
    "supply-chain-risk-intelligence": (["analytics", "ml"], "tests.yml"),
    "nyc-tip-mlops": (["ml", "mlops"], "ci.yml"),
    "nyc-taxi-lakehouse": (["data"], "tests.yml"),
    "olist-cloud-warehouse": (["data"], "deploy.yml"),
    "olist-analytics": (["data", "analytics"], "dbt-check.yml"),
    "economic-data-platform": (["data"], "ci_pipeline.yml"),
    "hospcall": (["team"], None),
    "iefa-sales-stock": (["team", "data"], None),
}

PERSON = {
    "name": "Diego Alves",
    "role": {"pt": "Engenheiro de Dados", "en": "Data Engineer"},
    "location": {"pt": "Novo Horizonte, SP, Brasil", "en": "Novo Horizonte, SP, Brazil"},
    "headline": {
        "pt": "Dados confiáveis para decisões, com o resultado medido.",
        "en": "Trustworthy data for decisions, with the result measured.",
    },
    "intro": {
        "pt": "Construo pipelines, warehouses e painéis que respondem a uma decisão de negócio, e mostro o que "
        "medi, inclusive o que não funcionou.",
        "en": "I build pipelines, warehouses and dashboards that answer a business decision, and I report what I "
        "measured, including what did not work.",
    },
    "about": {
        "pt": [
            "Cheguei à engenharia pela análise de dados: SQL, painéis e a pergunta de se um número merece confiança. "
            "Essa pergunta guia como eu construo. Pipelines conferem os dados antes de chegarem a alguém, modelos são "
            "medidos em dados que nunca viram, e agentes são avaliados, rastreados e atacados antes de serem dados "
            "como prontos.",
            "Escrevi cinco livros: uma trilogia em inglês sobre decisões com dados, um livro de negócios e "
            "um guia de ciência de dados de mil páginas, os dois em português. Escrevo em português, inglês e espanhol.",
        ],
        "en": [
            "I came to engineering from data analysis: SQL, dashboards and the question of whether a number can be "
            "trusted. That question shapes how I build. Pipelines check their data before it reaches anyone, models "
            "are measured on data they never saw, and agents are evaluated, traced and attacked before they are "
            "called finished.",
            "I have written five books: a trilogy in English on decisions with data, a business book and "
            "a thousand-page data science guide, both in Portuguese. I write in Portuguese, English and Spanish.",
        ],
    },
}

EDUCATION = [
    {
        "course": {"pt": "Pós-graduação em Ciência de Dados e Big Data Analytics",
                   "en": "Postgraduate, Data Science and Big Data Analytics"},
        "school": "Faculdade IMES",
        "when": {"pt": "concluída em 2026", "en": "completed 2026"},
    },
    {
        "course": {"pt": "Bacharelado em Tecnologia da Informação", "en": "BSc, Information Technology"},
        "school": "UNIVESP",
        "when": {"pt": "conclusão prevista em 2026", "en": "expected 2026"},
    },
    {
        "course": {"pt": "Técnico em Inteligência Artificial", "en": "Technical degree, Artificial Intelligence"},
        "school": "IFNMG",
        "when": {"pt": "conclusão prevista em 2027", "en": "expected 2027"},
    },
    {
        "course": {"pt": "Tecnólogo em Gestão Empresarial", "en": "Technologist, Business Management"},
        "school": "Fatec Catanduva",
        "when": {"pt": "concluído em 2023", "en": "completed 2023"},
    },
]

# Every tool listed here is used in at least one project on the site.
SKILLS = [
    {"group": {"pt": "Linguagens e dados", "en": "Languages and data"},
     "items": ["Python", "SQL", "PySpark", "dbt", "DuckDB", "Polars", "PostgreSQL", "pandas"]},
    {"group": {"pt": "Engenharia de dados", "en": "Data engineering"},
     "items": ["Spark Structured Streaming", "Kafka / Redpanda", "Delta Lake", "Dagster"]},
    {"group": {"pt": "Cloud e infraestrutura", "en": "Cloud and infrastructure"},
     "items": ["Google Cloud", "BigQuery", "Terraform", "IAM e Workload Identity Federation", "Docker", "GitHub Actions"]},
    {"group": {"pt": "Machine learning e estatística", "en": "Machine learning and statistics"},
     "items": ["XGBoost", "scikit-learn", "SHAP", "statsmodels", "lifelines", "Prophet", "PuLP", "MLflow", "Evidently"]},
    {"group": {"pt": "LLMs e agentes", "en": "LLMs and agents"},
     "items": ["PyTorch", "Transformers", "LoRA (PEFT)", "llama.cpp", "Ollama", "MCP", "LangGraph", "Qdrant", "RAGAS",
               "Langfuse", "OpenTelemetry"]},
    {"group": {"pt": "Produto e visualização", "en": "Product and visualization"},
     "items": ["FastAPI", "Streamlit", "Power BI"]},
]

LANGUAGES = {
    "pt": ["Português (nativo)", "Inglês (C2)", "Espanhol (C1)"],
    "en": ["Portuguese (native)", "English (C2)", "Spanish (C1)"],
}

UI = {
    "pt": {
        "lang": "pt-BR", "skip": "Pular para o conteúdo", "nav_projects": "Projetos",
        "nav_skills": "Habilidades", "nav_contact": "Contato", "theme": "Alternar tema claro e escuro",
        "other_lang": "English", "other_lang_label": "Read in English",
        "stat_projects": "projetos com resultados medidos", "stat_team": "em uso por equipes reais",
        "stat_ci": "com testes e checagens no CI", "stat_books": "livros escritos", "see_projects": "Ver projetos",
        "projects": "Projetos", "filter_label": "Filtrar projetos por área", "all": "Todos",
        "case": "Estudo de caso", "code": "Código", "demo": "Demo ao vivo", "group_ai": "Engenharia de IA",
        "group_data": "Engenharia de dados e machine learning", "group_team": "Projetos em equipe, em uso real",
        "featured": "Em destaque", "email": "E-mail", "whatsapp": "WhatsApp",
        "featured_proof": {
            "olist-cloud-warehouse": "Warehouse em BigQuery com Terraform, deploy sem chaves e contratos dbt.",
            "freight-intelligence": "Pipeline de 97,6 milhões de linhas e uma falha de memória em produção resolvida.",
            "fraud-investigation-agents": "Agentes medidos contra uma linha de base: o crítico leva o acerto de 47% a 77%.",
        }, "none": "Nenhum projeto nessa área.", "skills": "Habilidades", "education": "Formação", "languages": "Idiomas",
        "about": "Sobre",
        "contact": "Contato", "contact_text": "Procuro vagas remotas em engenharia de dados, análise de dados e BI. "
        "Pode me chamar por e-mail ou WhatsApp.",
        "no_code": "Código da equipe, não público", "my_part": "Minha parte:",
        "github": "GitHub", "back": "Todos os projetos", "problem": "Problema", "solution": "Solução",
        "how": "Como funciona", "results": "Resultados", "results_caption": "Resultados medidos, do repositório",
        "results_caption_team": "Resultados do relatório final entregue à UNIVESP",
        "limits": "Limites", "stack": "Stack", "prev": "Anterior", "next": "Próximo", "ci": "Status do CI",
        "footer": "Os números deste site vêm do repositório de cada projeto, onde o código que os produziu roda no "
        "CI, e, nos projetos em equipe, do relatório final entregue à UNIVESP.", "source": "Código deste site", "title_suffix": "engenharia de dados e IA",
        "description": "Projetos de engenharia de dados, machine learning e engenharia de IA de Diego Alves, cada um "
        "com resultados medidos.",
        "notfound_title": "Página não encontrada", "notfound_text": "Este endereço não existe neste site.",
        "notfound_link": "Ir para a página inicial",
    },
    "en": {
        "lang": "en", "skip": "Skip to content", "nav_projects": "Projects",
        "nav_skills": "Skills", "nav_contact": "Contact", "theme": "Switch light and dark theme",
        "other_lang": "Português", "other_lang_label": "Ler em português",
        "stat_projects": "projects with measured results", "stat_team": "in use by real teams",
        "stat_ci": "with tests and checks in CI", "stat_books": "books written", "see_projects": "See projects",
        "projects": "Projects", "filter_label": "Filter projects by area", "all": "All",
        "case": "Case study", "code": "Code", "demo": "Live demo", "group_ai": "AI engineering",
        "group_data": "Data engineering and machine learning", "group_team": "Team projects in real use",
        "featured": "Featured", "email": "Email", "whatsapp": "WhatsApp",
        "featured_proof": {
            "olist-cloud-warehouse": "A BigQuery warehouse with Terraform, keyless deploys and dbt contracts.",
            "freight-intelligence": "A 97.6-million-row pipeline and a production memory failure, traced and fixed.",
            "fraud-investigation-agents": "Agents measured against a baseline: the critic lifts accuracy from 47% to 77%.",
        }, "none": "No projects in this area.", "skills": "Skills", "education": "Education", "languages": "Languages",
        "about": "About",
        "contact": "Contact", "contact_text": "I'm looking for remote roles in data engineering, data analysis and BI. "
        "Reach me by email or WhatsApp.",
        "no_code": "Team code, not public", "my_part": "My part:",
        "github": "GitHub", "back": "All projects", "problem": "Problem", "solution": "Solution",
        "how": "How it works", "results": "Results", "results_caption": "Measured results, from the repository",
        "results_caption_team": "Results from the final report delivered to UNIVESP",
        "limits": "Limits", "stack": "Stack", "prev": "Previous", "next": "Next", "ci": "CI status",
        "footer": "The numbers on this site come from each project's repository, where the code that produced them "
        "runs in CI, and, for the team projects, from the final report delivered to UNIVESP.", "source": "Source of this site", "title_suffix": "data and AI engineering",
        "description": "Data engineering, machine learning and AI engineering projects by Diego Alves, each with "
        "measured results.",
        "notfound_title": "Page not found", "notfound_text": "This address does not exist on this site.",
        "notfound_link": "Go to the home page",
    },
}
