"""The five books Diego wrote. None of them is published yet, and the site says so.
Three are in English (the Data-Driven Decisions trilogy) and two in Portuguese; the language
of each book is shown wherever the book appears. Code snippets are copied from the books."""

# Each book: slug (cover file and anchor), language it is written in, pages, title, subtitle,
# thesis per site language, chapters (in the book's own language) and a short line from it.
BOOKS = [
    {
        "slug": "sql", "lang": "en", "pages": 101, "series": 1,
        "title": "SQL for Decisions", "subtitle": "Data-Driven Decisions, Book One",
        "thesis": {
            "pt": "Como transformar uma decisão real numa pergunta que o banco de dados consegue responder, e a "
            "resposta em algo que uma pessoa pode defender numa reunião. A sintaxe é comum; o livro ensina o hábito "
            "em volta dela: contar com honestidade, desconfiar da fonte e montar a consulta a serviço da decisão.",
            "en": "How to turn a real decision into a question a database can answer, and the answer into something "
            "a person can defend in a meeting. The syntax is ordinary; the book teaches the habit around it: counting "
            "honestly, doubting the source and building the query in service of the decision.",
        },
        "chapters": [
            "The Decision Behind the Query", "Counting Honestly", "Trusting the Source", "Joining Tables Into a Question",
            "Reusable Logic With CTEs", "Ranking and Trends With Window Functions", "Turning Queries Into Models With dbt",
            "Performance When the Data Grows", "The SQL Decision, End to End", "Worked Build, Query by Query",
        ],
        "quote": "A query that runs is easy.",
    },
    {
        "slug": "powerbi", "lang": "en", "pages": 94, "series": 2,
        "title": "Power BI for Decisions", "subtitle": "Data-Driven Decisions, Book Two",
        "thesis": {
            "pt": "Leva a resposta do SQL até um relatório que alguém que não escreveu a consulta consegue abrir, "
            "navegar e usar. O foco está no julgamento em volta dos botões: o que o relatório precisa dizer antes do "
            "primeiro gráfico, o modelo que torna fáceis as perguntas difíceis, e a honestidade que separa um "
            "relatório que esclarece de um que bajula.",
            "en": "Carries the SQL answer into a report that someone who did not write the query can open, navigate "
            "and act on. The focus is the judgment around the buttons: what the report must say before the first "
            "visual, the model that makes hard questions easy, and the honesty that separates a report that clarifies "
            "from one that flatters.",
        },
        "chapters": [
            "Shaping Data With Power Query", "The Star Schema", "Measures That Mean Something",
            "Filter Context, the Idea Behind DAX", "The Chart Catalog as a Method", "Tables That Decide",
            "Designing the Message in Figma", "Telling the Story and Not Lying", "Refreshing and Sharing at Scale",
            "Worked Build, Wireframe to Published",
        ],
        "quote": "A report is only as honest as the data behind it.",
    },
    {
        "slug": "python", "lang": "en", "pages": 94, "series": 3,
        "title": "Python for Decisions", "subtitle": "Data-Driven Decisions, Book Three",
        "thesis": {
            "pt": "Usa Python quando a decisão pede algo que nem a consulta nem o relatório entregam: exploração "
            "aberta, um teste estatístico, uma projeção. O notebook é lido como um argumento, a distribuição é "
            "examinada antes de confiar na média, e uma relação é testada antes de alguém agir em cima dela.",
            "en": "Reaches for Python when the decision needs something neither a query nor a report provides: open "
            "exploration, a statistical test, a projection. The notebook is read as an argument, a distribution is "
            "examined before a mean is trusted, and a relationship is tested before anyone acts on it.",
        },
        "chapters": [
            "The Notebook as a Decision Journal", "Cleaning and Reshaping With pandas", "Distributions and Segments",
            "Relationships and Correlation", "Is It Real? Significance and Confidence", "Time Series and Seasonality",
            "Projection and Scenarios", "Charts That Carry an Argument", "The Python Decision, End to End",
            "Worked Build, A Full Analysis, Cell by Cell",
        ],
        "quote": "A notebook read as an argument.",
    },
    {
        "slug": "negocios", "lang": "pt", "pages": 199,
        "title": "Anotações sobre Negócios", "subtitle": "Reflexões práticas para gerenciar, liderar e fazer acontecer",
        "thesis": {
            "pt": "Oito capítulos sobre o que separa quem transforma uma ideia em negócio de quem apenas tenta: "
            "validar o problema antes da solução, posicionar-se contra concorrentes, liderar times, vender, "
            "reconhecer os próprios vieses ao decidir e entender por que empresas gigantes caem.",
            "en": "Eight chapters on what separates people who turn an idea into a business from those who only try: "
            "validating the problem before the solution, positioning against competitors, leading teams, selling, "
            "spotting your own biases when deciding, and understanding why giant companies fall.",
        },
        "chapters": [
            "Mentalidade e visão", "Validação do problema", "Estratégia competitiva e posicionamento",
            "Inovação e desenvolvimento de produto", "Liderança e gestão de alta performance",
            "Vendas, influência e persuasão", "Vieses cognitivos e tomada de decisões",
            "Escala, inovação e o porquê da queda dos gigantes",
        ],
        "quote": "O que separa quem transforma uma ideia em negócio de verdade de quem apenas tenta?",
    },
    {
        "slug": "canone", "lang": "pt", "pages": 1042,
        "title": "O Cânone da Ciência de Dados Moderna", "subtitle": "Territórios e fundamentos",
        "thesis": {
            "pt": "Um mapa completo do ofício, do Python e da estatística até transformers, MLOps e carreira, escrito "
            "para preencher o espaço entre o livro traduzido denso demais e o tutorial raso demais. Sete partes, "
            "dezenove capítulos e um projeto completo no apêndice.",
            "en": "A complete map of the craft, from Python and statistics to transformers, MLOps and career, written "
            "to fill the gap between the translated textbook that is too dense and the tutorial that is too shallow. "
            "Seven parts, nineteen chapters and a full project in the appendix.",
        },
        "chapters": [],  # shown as the map below
        "quote": "Que o tempo investido aqui sirva ao trabalho que vem em seguida.",
    },
]

# The Cânone's parts, with the page each starts on (from its table of contents) and their chapters.
CANONE_END = 1042
CANONE = [
    {"part": "I", "name": "O Alicerce", "en": "The foundation", "start": 11, "chapters": [
        (1, "A filosofia e o mindset do cientista de dados", 11), (2, "Python essencial e manipulação de arquivos", 60),
        (3, "Matemática fundamental para deep learning", 127), (4, "Excel e sua prática avançada", 191)]},
    {"part": "II", "name": "O Coração Estatístico", "en": "The statistical core", "start": 232, "chapters": [
        (5, "Análise exploratória de dados e visualização científica", 232), (6, "Probabilidade e distribuições", 319),
        (7, "Pensamento bayesiano", 355), (8, "Inferência causal e experimentação", 398)]},
    {"part": "III", "name": "Engenharia de Dados", "en": "Data engineering", "start": 436, "chapters": [
        (9, "Engenharia de dados, com bancos de dados na prática: PostgreSQL e MongoDB", 436),
        (10, "Fluxo canônico de machine learning e regressão", 534),
        (11, "Classificação clássica, árvores e florestas, com AutoML em profundidade", 586)]},
    {"part": "IV", "name": "Machine Learning Supervisionado e Não Supervisionado", "en": "Supervised and unsupervised "
     "machine learning", "start": 668, "chapters": [
        (12, "Não supervisionado e sistemas de recomendação", 668),
        (13, "Séries temporais, com análise prescritiva e otimização", 720)]},
    {"part": "V", "name": "Redes Neurais e a Fronteira da IA", "en": "Neural networks and the AI frontier",
     "start": 803, "chapters": [
        (14, "Aprendizado profundo", 803), (15, "Visão computacional e redes convolucionais", 840),
        (16, "Redes recorrentes e transformers", 874), (17, "Modelos generativos e deep reinforcement learning", 910)]},
    {"part": "VI", "name": "Sistemas de Dados em Escala e Operação de Modelos", "en": "Data systems at scale and "
     "model operations", "start": 947, "chapters": [(18, "Big data, stream processing e MLOps", 947)]},
    {"part": "VII", "name": "Comunicação, Gestão e Carreira", "en": "Communication, management and career",
     "start": 991, "chapters": [(19, "Comunicação, gestão e carreira", 991)]},
    {"part": "A", "name": "Apêndice: Projeto Completo de Data Science", "en": "Appendix: a complete data science "
     "project", "start": 1028, "chapters": []},
]

# One decision, worked through all three books of the trilogy.
DECISION = {
    "pt": {
        "title": "Uma decisão, três ferramentas",
        "intro": "Os três livros resolvem o mesmo caso, cada um com sua ferramenta. Uma linha de produtos fatura "
        "180 mil, está em 47º lugar entre 50 e custa 171 mil para manter. O contrato de fornecimento ainda tem 8 "
        "meses e cobra multa para sair antes. Manter, cortar agora ou encerrar no fim do contrato?",
        "verdict": "A recomendação dos três livros: não pagar a multa. Parar de repor estoque, encerrar a linha no fim "
        "do contrato e revisar a tendência até lá.",
    },
    "en": {
        "title": "One decision, three tools",
        "intro": "All three books solve the same case, each with its own tool. A product line earns 180k, ranks 47th "
        "of 50 and costs 171k to carry. The supply contract has 8 months left and charges a penalty for leaving early. "
        "Keep it, cut it now, or wind it down when the contract ends?",
        "verdict": "The recommendation across the three books: do not pay the penalty. Stop restocking, wind the line "
        "down when the contract ends, and review the trend until then.",
    },
}

TOOLS = [
    {
        "key": "sql", "name": "SQL", "book": "SQL for Decisions", "where": {"pt": "capítulo 9", "en": "chapter 9"},
        "code": """WITH line_sales AS (
     SELECT product_line, SUM(quantity*unit_price) AS revenue
     FROM stg_sales
     WHERE sale_date >= '2023-07-01'
     GROUP BY product_line
),
line_cost AS (
     SELECT product_line, SUM(loaded_cost) AS cost
     FROM stg_costs GROUP BY product_line
)
SELECT s.product_line, s.revenue, c.cost,
          s.revenue - c.cost AS margin
FROM line_sales s
LEFT JOIN line_cost c USING (product_line)
ORDER BY margin;""",
        "result": {"pt": "Mostra que o 47º lugar é de receita, não de lucro: a linha custa 171 mil e ainda deixa 9 mil de margem.",
                   "en": "Shows that 47th place is about revenue, not profit: the line costs 171k and still leaves a 9k margin."},
    },
    {
        "key": "powerbi", "name": "Power BI", "book": "Power BI for Decisions",
        "where": {"pt": "capítulo 10", "en": "chapter 10"},
        "code": "Margin % = DIVIDE ( [Revenue] - [Cost], [Revenue] )",
        "result": {"pt": "Coloca a margem num cartão que qualquer gestor lê: 5,0%, fina, mas ainda positiva.",
                   "en": "Puts the margin on a card any manager can read: 5.0%, thin but still positive."},
    },
    {
        "key": "python", "name": "Python", "book": "Python for Decisions", "where": {"pt": "capítulo 9", "en": "chapter 9"},
        "code": """t_stat, p_val = stats.ttest_ind(margin_pct[:6], margin_pct[6:])
print(f"p = {p_val:.3f}")""",
        "result": {"pt": "p = 0,297: a queda de 5,28% para 4,86% entre os semestres pode ser acaso. Nos cenários até o fim "
                   "do contrato, a margem fica entre 4,07% e 5,87%, sempre positiva, então a multa não se paga.",
                   "en": "p = 0.297: the drop from 5.28% to 4.86% between halves may be chance. In the scenarios to the "
                   "end of the contract the margin stays between 4.07% and 5.87%, always positive, so the penalty does "
                   "not pay off."},
    },
]

# The method the trilogy teaches, and the project on this site where each step shows most.
METHOD = [
    {"pt": "Nomear a decisão", "en": "Name the decision", "slug": "finetune-and-serve",
     "how": {"pt": "Treinar um modelo próprio ou pagar uma API? A pergunta vem antes do código, e a resposta é um volume "
             "mensal a partir do qual a conta muda.",
             "en": "Train a model or pay for an API? The question comes before the code, and the answer is a monthly "
             "volume from which the numbers change."}},
    {"pt": "Confiar no dado", "en": "Trust the data", "slug": "economic-data-platform",
     "how": {"pt": "Cada lote passa por cinco checagens antes de chegar ao painel; se falhar, o painel mantém o último "
             "dado bom.",
             "en": "Every batch passes five checks before it reaches the dashboard; if it fails, the dashboard keeps "
             "the last good data."}},
    {"pt": "Mostrar o trabalho", "en": "Show the work", "slug": "sec-mcp-agent",
     "how": {"pt": "Cada resposta cita o trecho do relatório de onde veio, e a citação é conferida antes de sair.",
             "en": "Every answer cites the passage it came from, and the citation is checked before it goes out."}},
    {"pt": "Ler a tendência", "en": "Read the trend", "slug": "nyc-taxi-lakehouse",
     "how": {"pt": "Antes e depois da taxa de congestionamento, com o aviso de que parte da mudança pode ser sazonal.",
             "en": "Before and after the congestion fee, with the warning that part of the change may be seasonal."}},
    {"pt": "Fazer durar", "en": "Make it last", "slug": "llm-evals-observability",
     "how": {"pt": "Cada mudança é testada contra chamadas gravadas, e uma regressão é barrada antes de ir ao ar.",
             "en": "Every change is tested against recorded calls, and a regression is stopped before it ships."}},
]

UI_BOOKS = {
    "pt": {
        "nav": "Livros", "title": "Livros", "page_title": "Livros",
        "lead": "Escrevi cinco livros, ainda não publicados: uma trilogia em inglês sobre decisões com dados e dois "
        "livros em português, um sobre negócios e outro que percorre a ciência de dados inteira.",
        "shelf_en": "Em inglês", "shelf_pt": "Em português", "trilogy": "Trilogia Data-Driven Decisions",
        "written_in": {"en": "Escrito em inglês", "pt": "Escrito em português"},
        "lang_short": {"en": "Inglês", "pt": "Português"},
        "status": "Inédito", "pages": "páginas", "chapters": "Capítulos", "open": "Ver os cinco livros",
        "map_title": "O mapa do Cânone", "map_lead": "As sete partes do livro, no tamanho real que ocupam nas 1.042 "
        "páginas. Abra uma parte para ver os capítulos.", "page": "p.", "method_title": "O método, nos projetos",
        "method_lead": "A trilogia ensina cinco passos. Cada um aparece num projeto deste site.",
        "see_project": "Ver o projeto", "book_n": "Livro", "of_trilogy": "da trilogia", "tabs": "Ferramenta",
        "description": "Os cinco livros de Diego Alves, ainda não publicados: a trilogia Data-Driven Decisions, em "
        "inglês, e dois livros em português.",
    },
    "en": {
        "nav": "Books", "title": "Books", "page_title": "Books",
        "lead": "I have written five books, not yet published: a trilogy in English on making decisions with data, "
        "and two books in Portuguese, one on business and one that covers the whole of data science.",
        "shelf_en": "In English", "shelf_pt": "In Portuguese", "trilogy": "Data-Driven Decisions trilogy",
        "written_in": {"en": "Written in English", "pt": "Written in Portuguese"},
        "lang_short": {"en": "English", "pt": "Portuguese"},
        "status": "Unpublished", "pages": "pages", "chapters": "Chapters", "open": "See all five books",
        "map_title": "The Cânone, mapped", "map_lead": "The book's seven parts, at the real share of its 1,042 pages "
        "each one takes. Open a part to see its chapters (titles in Portuguese).", "page": "p.",
        "method_title": "The method, in the projects",
        "method_lead": "The trilogy teaches five steps. Each one shows up in a project on this site.",
        "see_project": "See the project", "book_n": "Book", "of_trilogy": "of the trilogy", "tabs": "Tool",
        "description": "Diego Alves's five books, not yet published: the Data-Driven Decisions trilogy, in English, "
        "and two books in Portuguese.",
    },
}

# English translations of the Portuguese titles, so English readers know what each book is.
TITLE_EN = {
    "negocios": "Notes on Business",
    "canone": "The Canon of Modern Data Science",
}
