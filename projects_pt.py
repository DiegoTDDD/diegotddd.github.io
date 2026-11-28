"""Portuguese (pt-BR) text for each project, keyed by slug.

Same facts and numbers as projects.py, in Brazilian Portuguese with decimal commas. build.py
fails if a project is missing here or if the number of results differs from the English entry.
"""

PT = {
    "fraud-investigation-agents": {
        "name": "Agentes de investigação de fraude",
        "line": "Uma equipe de agentes que investiga alertas de fraude em cartão e tem os relatórios conferidos contra as evidências.",
        "headline": ("83%", "dos padrões de fraude identificados corretamente, contra 40% com uma única chamada ao modelo"),
        "problem": "Agentes que investigam alertas de fraude são fáceis de demonstrar e difíceis de confiar: podem apontar "
        "um padrão que os dados não mostram, pular uma checagem ou liberar uma compra fraudulenta com um texto convincente.",
        "solution": "Uma equipe em LangGraph. Um planejador escolhe as checagens, um pesquisador as executa por dois "
        "servidores MCP (atividade do cartão e o modelo de fraude), um relator escreve o veredito citando as evidências, "
        "e um crítico baseado em regras rejeita relatórios que as evidências não sustentam e devolve o trabalho. Roda com "
        "um modelo local de 3B num runner de CPU gratuito.",
        "how": [
            "O código busca todos os números; os modelos de linguagem só decidem o que checar e o que isso significa.",
            "O crítico são regras sobre as evidências, então as decisões dele são reproduzíveis e explicáveis.",
            "Medido em 30 alertas com resposta conhecida, contra o modelo de fraude sozinho, regras simples e uma única chamada ao LLM.",
        ],
        "results": [
            ("83%", "de acerto no padrão de fraude, contra 40% com uma única chamada ao LLM"),
            ("27 de 30", "resumos finais que dizem só o que as evidências mostram, contra 50% com uma única chamada"),
            ("7 de 7", "compras legítimas liberadas, contra 2 de 7 na primeira rodada de avaliação"),
        ],
        "limits": "Os dados são sintéticos. As checagens do crítico sobre o resumo são léxicas, e três relatórios "
        "continuaram rejeitados porque o relator de 3B não conseguiu escrever um resumo aceito.",
        "video_caption": "Uma investigação real gravada na rodada 2 da avaliação: o crítico rejeita o primeiro relatório citando a "
        "regra quebrada, a segunda rodada acerta, e o resultado nos 30 alertas.",
    },
    "sec-mcp-agent": {
        "name": "Agente MCP sobre a SEC",
        "line": "Servidores MCP sobre relatórios da SEC e um modelo de fraude, e um agente cujas citações são conferidas na fonte.",
        "headline": ("17 de 22", "perguntas de avaliação aprovadas na oitava rodada medida (7 na primeira); o código confere se cada resposta diz só o que as ferramentas devolveram"),
        "problem": "Respostas sobre relatórios financeiros só têm valor se cada afirmação puder ser rastreada até a fonte, "
        "e modelos pequenos inventam fontes que parecem reais. Além disso, ferramentas costumam ficar presas a um único "
        "agente, e nada mais consegue usá-las.",
        "solution": "Dois servidores MCP, um sobre relatórios 10-K com busca BM25 e outro sobre o modelo de fraude, e um "
        "agente que responde usando os dois. Cada citação é conferida contra o trecho que diz citar antes de a resposta "
        "ser devolvida. Os mesmos servidores funcionam no Claude Desktop.",
        "how": [
            "Uma citação só passa se o trecho citado estiver no documento recuperado, e todo número da resposta precisa aparecer num trecho citado ou no score de fraude, sem veredito contrário ao do modelo.",
            "Oito rodadas de avaliação num runner de CPU, com cada falha rastreada e corrigida no agente ou nas ferramentas; a avaliação roda de novo toda semana.",
            "A ferramenta de fraude reaproveita o modelo XGBoost do projeto de fraude em tempo real, num commit fixado.",
        ],
        "results": [
            ("17 de 22", "perguntas de avaliação aprovadas na oitava rodada (7 na primeira; 18 na sétima, diferença que é variação entre rodadas)"),
            ("21 de 22", "respostas cujos números e veredito de fraude batem com o que as ferramentas devolveram; a sinalizada cita o trecho errado para um número verdadeiro"),
            ("71", "testes, incluindo os servidores acessados pelo cliente MCP"),
        ],
        "limits": "Um modelo de 3B ainda erra algumas perguntas de várias etapas; o conjunto de avaliação é pequeno; a checagem da resposta é léxica, então um número certo ainda pode ficar ao lado do assunto errado.",
        "video_caption": "Duas respostas gravadas na sexta rodada de avaliação: as chamadas de ferramenta, a resposta e as citações verificadas.",
    },
    "olist-ai-analyst": {
        "name": "Analista de dados com IA (Olist)",
        "line": "Um analista com modelo local que transforma uma pergunta de negócio num memo de decisão, com código conferindo o SQL e cada número.",
        "headline": ("72%", "de 25 perguntas de negócio respondidas com o mesmo resultado do SQL de referência escrito à mão"),
        "problem": "Um modelo escrevendo SQL erra de jeitos que parecem certos: uma consulta que roda mas filtra as "
        "linhas erradas, ou um memo que cita um número que a consulta nunca produziu. A resposta de um analista só "
        "vale se quem decide puder confiar nela.",
        "solution": "Um analista sobre os dados reais do marketplace Olist (99.441 pedidos) que segue os cinco passos "
        "dos livros Data-Driven Decisions: nomear a decisão, confiar no dado, mostrar o trabalho, ler a tendência e "
        "fazer durar. O modelo escreve o SQL e o memo; o código confere o SQL, roda em modo só leitura, lê a "
        "tendência e exige que cada número do memo exista no resultado.",
        "how": [
            "O próprio parser do DuckDB só aceita um SELECT sobre três tabelas de análise, numa conexão só leitura, sem acesso a arquivos ou rede.",
            "Erros voltam para o modelo, até três tentativas; um memo com número fora do resultado ganha uma reescrita e depois é marcado como não verificado.",
            "A tendência é lida pelo código, numa reta ajustada sobre meses completos, nunca descrita pelo modelo.",
            "Uma avaliação com SQL de referência roda toda semana com Ollama num runner de CPU gratuito e publica os resultados.",
        ],
        "results": [
            ("72%", "de acerto na execução em 25 perguntas com qwen2.5-coder 7B na quarta rodada medida (68% na terceira; o ganho é um empate de arredondamento)"),
            ("100%", "dos memos com todos os números encontrados no resultado, ao lado da própria linha quando o memo a nomeia"),
            ("100%", "de SQL válido depois das novas tentativas com a mensagem de erro (88% na primeira)"),
        ],
        "limits": "Um número ligado a uma linha nomeada precisa ser o valor dessa linha, mas frases mais soltas não são "
        "julgadas; as perguntas são poucas e foram escritas pela mesma pessoa que fez o pipeline.",
        "extra_links": [("Resultados da avaliação", "https://github.com/DiegoTDDD/olist-ai-analyst/blob/main/eval/results.md")],
    },
    "llm-guardrails-redteam": {
        "name": "Guardrails e red team para LLMs",
        "line": "Proteções em volta dos dois agentes e uma bateria de ataques que roda a cada pull request.",
        "headline": ("26 de 27", "ataques bloqueados, cada um comprovado contra os agentes sem proteção; um relatado como lacuna"),
        "problem": "Agentes leem documentos e chamam ferramentas, então quem consegue escrever num documento, no nome de "
        "uma loja ou numa pergunta pode tentar manipulá-los. As recusas do próprio modelo não são uma defesa, e os traces "
        "acumulam em silêncio os dados pessoais que os usuários digitam.",
        "solution": "Seis camadas em volta dos agentes, sem alterar o código deles: checagem da entrada, quarentena de "
        "instruções encontradas nos dados, mascaramento de dados pessoais, política de ferramentas, checagem da saída e "
        "traces mascarados. A bateria usa os agentes reais com um modelo que obedece qualquer instrução que vê, então o "
        "bloqueio nunca depende de o modelo recusar.",
        "how": [
            "Cada ataque precisa funcionar sem as proteções e falhar com elas.",
            "Alguns ataques são escritos para escapar da detecção, então as camadas seguintes são testadas sozinhas; "
            "injeções reescritas passam por um classificador treinado local, com limiar definido pela bateria de falsos positivos.",
            "Uma bateria de falsos positivos com dados reais gravados quebra o build se algo legítimo for afetado.",
        ],
        "results": [
            ("26 de 27", "ataques bloqueados: injeção, exfiltração, uso indevido de ferramentas, burla do crítico e logs"),
            ("0 de 283", "textos reais marcados; 0 de 22 perguntas e 0 de 3 investigações alteradas"),
            ("79", "testes; a bateria encontrou um bug nas próprias proteções"),
        ],
        "limits": "Padrões e classificador ainda deixam passar algumas frases: uma instrução reescrita num documento passa "
        "e fica na bateria como lacuna conhecida, e por isso as camadas seguintes são testadas separadamente.",
    },
    "llm-evals-observability": {
        "name": "Avaliação e observabilidade de LLMs",
        "line": "Uma barreira contra regressões a cada pull request e avaliações semanais ao vivo rastreadas no Langfuse.",
        "headline": ("162", "chamadas reais de ferramenta reproduzidas a cada pull request"),
        "problem": "Agentes com modelos locais pequenos falham de jeitos que testes unitários não enxergam: o modelo manda "
        "argumentos que as ferramentas rejeitam, uma resposta nunca termina, uma correção num ponto quebra outro.",
        "solution": "Datasets versionados gravados de execuções reais, uma barreira offline que os reproduz a cada pull "
        "request, execuções semanais ao vivo dos dois agentes rastreadas com OpenTelemetry num Langfuse auto-hospedado, e "
        "um painel público.",
        "how": [
            "Os datasets são imutáveis e versionados com manifesto sha256.",
            "As linhas de base têm tolerâncias medidas a partir da variação entre execuções.",
            "O Langfuse roda dentro do CI com Docker Compose, então o rastreamento é testado de ponta a ponta.",
        ],
        "results": [
            ("162", "chamadas de ferramenta gravadas na barreira offline"),
            ("1", "regressão bloqueada num pull request real"),
            ("0,705", "taxa de acerto ao vivo do agente de relatórios (± 0,15 entre execuções)"),
        ],
        "limits": "Os resultados ao vivo variam entre execuções do mesmo código; a barreira usa tolerâncias em vez de valores exatos.",
        "extra_links": [("Painel", "https://diegotddd.github.io/llm-evals-observability/")],
    },
    "finetune-and-serve": {
        "name": "Fine-tuning e serving",
        "line": "Um modelo de 0,5B ajustado num runner de CPU gratuito para marcar fatos financeiros em frases de 10-K, servido com llama.cpp.",
        "headline": ("0,82", "de F1 em fatos rotulados por auditores, contra 0,65 de um modelo de 3B com exemplos no prompt"),
        "problem": "Extração estruturada costuma ser feita com um modelo grande e um prompt, e cada requisição paga por um "
        "prompt longo, numa API ou num hardware grande o bastante para o modelo. Se um modelo pequeno treinado para essa "
        "única tarefa faz melhor e custa menos é uma questão de medição.",
        "solution": "Fine-tuning com LoRA do Qwen2.5-0.5B em frases de notas de 10-K rotuladas por auditores com conceitos "
        "XBRL (FiNER-139), exportação para GGUF com quantização de 8 e 4 bits, e serving com llama.cpp. A comparação é com "
        "o mesmo modelo e um de 3B usados só com prompt, em qualidade, latência, vazão e custo.",
        "how": [
            "Treino, quantização, avaliação e benchmark num único workflow do GitHub Actions numa CPU de 4 núcleos.",
            "Perda e logits só nos tokens da resposta, para um vocabulário de 152 mil tokens caber na memória.",
            "Todos os modelos servidos pelo mesmo llama-server, com o mesmo schema JSON imposto pela gramática.",
            "Custo de uma VM do tamanho do runner contra o preço de tabela das APIs, com o tamanho de prompt medido.",
        ],
        "results": [
            ("0,82", "de F1 em 4 bits (398 MB), contra 0,65 do Qwen2.5-3B com seis exemplos (ganho de +0,16, intervalo de 95% por bootstrap pareado de +0,10 a +0,23) e 0,19 antes do ajuste"),
            ("3,7×", "as requisições por segundo do modelo de 3B na mesma CPU (1,60 contra 0,43)"),
            ("US$ 35", "por milhão de requisições auto-hospedado em carga total; o Claude Haiku 5.5 a preço de tabela custaria de US$ 45 a US$ 91"),
        ],
        "limits": "Um único treino, interrompido pelo limite de tempo em 79% de uma época; a precisão das APIs nessa "
        "tarefa não foi medida, só o preço.",
        "extra_links": [("Modelo publicado", "https://github.com/DiegoTDDD/finetune-and-serve/releases/tag/model-44606410559")],
    },
    "llm-from-scratch": {
        "name": "LLM do zero",
        "line": "Um modelo no estilo GPT escrito do zero e treinado em relatórios 10-K num runner de CPU gratuito.",
        "headline": ("32,0", "de perplexidade de validação, contra 837 de uma linha de base unigrama"),
        "problem": "A maioria dos projetos com LLM chama uma API ou ajusta o modelo de outra pessoa. Quando algo quebra, "
        "como um tokenizador incompatível, um bug de cache ou uma configuração de amostragem, é preciso entender as peças.",
        "solution": "Cada parte de um transformer só-decodificador construída e testada separadamente: BPE em nível de "
        "byte, atenção causal, laço de treino, amostragem e decodificação com KV cache, treinado nas seções Business, Risk "
        "Factors e MD&A de relatórios 10-K.",
        "how": [
            "Cada componente tem os próprios testes, incluindo um BPE ingênuo como referência para o rápido.",
            "O treino roda no runner gratuito do GitHub Actions, então qualquer pessoa pode reproduzir.",
            "A decodificação com KV cache é conferida para gerar os mesmos tokens que o recálculo completo, também além "
            "do contexto com janela deslizante; a atenção otimizada do PyTorch é medida contra a escrita à mão.",
        ],
        "results": [
            ("32,0", "de perplexidade de validação (837 na linha de base unigrama)"),
            ("5–9×", "mais rápido na geração com KV cache em 224 tokens novos (de 4,97× a 9,19× nas rodadas do benchmark, conforme a CPU do runner), conferido token a token"),
            ("13M", "de caracteres de texto de 10-K no conjunto de treino"),
        ],
        "limits": "Um modelo pequeno treinado numa CPU: aprende o estilo dos relatórios, não fatos.",
        "image_alt": "Curvas de perda de treino e validação",
    },
    "sec-filings-rag": {
        "name": "RAG sobre relatórios da SEC",
        "line": "Perguntas e respostas sobre relatórios 10-K e 10-Q, com as fontes que cada resposta usou.",
        "headline": ("0,78", "de hit@5 com busca híbrida e re-ranqueamento, contra 0,40 da busca densa (intervalo de 95% de 0,68 a 0,88)"),
        "problem": "Analistas precisam de respostas de relatórios longos que possam conferir, não de um resumo sem "
        "rastro até o texto.",
        "solution": "Geração aumentada por recuperação sobre os relatórios de Apple, NVIDIA e JPMorgan: busca híbrida "
        "densa e por palavra-chave, re-ranqueamento, um modelo local pelo Ollama e uma avaliação que roda no GitHub "
        "Actions com RAGAS.",
        "how": [
            "66 perguntas, cada uma gerada de um trecho conhecido, então a recuperação é medida com exatidão.",
            "Seis estratégias de recuperação comparadas pergunta a pergunta com intervalos de 95%; a rodada publica as próprias tabelas no README.",
            "Uma demo pública mostra respostas gravadas do pipeline real.",
        ],
        "results": [
            ("+0,13", "de hit@5 sobre o pipeline denso que ele substituiu, intervalo pareado de 95% de +0,03 a +0,23"),
            ("0,95", "de recall@20 do recuperador híbrido (0,73 na busca densa)"),
            ("66", "perguntas de avaliação, rodadas mensalmente no CI"),
        ],
        "limits": "A busca por palavra-chave com re-ranqueamento pontua mais (0,88) nessas perguntas, que reaproveitam as palavras do trecho de origem; o híbrido fica pelas perguntas parafraseadas, que o conjunto ainda não mede. A demo pública reproduz respostas gravadas, porque um host gratuito não roda Qdrant e Ollama.",
        "image_alt": "O painel respondendo uma pergunta sobre a Apple com as fontes",
    },
    "freight-intelligence": {
        "name": "LogiNexus: inteligência de fretes",
        "line": "Análise de fretes para EUA e Brasil: pipeline de 97,6 milhões de linhas, previsão, otimização e roteirização.",
        "headline": ("97,6M", "de linhas processadas pelo pipeline medallion"),
        "problem": "Planejar fretes exige volumes por corredor e modal, previsões que se sustentam em anos fora do "
        "treino e alocações que respeitam capacidade, a partir de fontes com unidades diferentes e lacunas.",
        "solution": "Um pipeline medallion sobre o Freight Analysis Framework dos EUA e fontes brasileiras de ferrovia, "
        "rodovia, hidrovia, aéreo e dutos, linhas de base de previsão avaliadas, um otimizador de transporte, "
        "roteirização para caminhões e uma API somente leitura documentada.",
        "how": [
            "Camadas Bronze, Silver e Gold com troca de arquivos em etapas e hashes das fontes.",
            "Previsões avaliadas com janelas expansivas e anos de teste reservados.",
            "Roteirização com motores separados para carro e caminhão, respeitando dimensões e peso.",
        ],
        "results": [
            ("97,6M", "de linhas processadas do CSV de origem até a camada Gold"),
            ("5", "modais de transporte brasileiros com histórico observado"),
            ("510", "pares de portos de cabotagem observados, todas as 98 origens revisadas"),
        ],
        "limits": "O host gratuito da demo dorme após 15 minutos; o primeiro acesso pode levar cerca de um minuto.",
        "image_alt": "Visão geral da análise de fretes no painel",
    },
    "realtime-fraud-detection-ml": {
        "name": "Detecção de fraude em tempo real",
        "line": "Um modelo XGBoost pontuando um fluxo Kafka ao vivo, com estado por cartão que sobrevive a restarts, predições gravadas uma única vez e um monitor do modelo.",
        "headline": ("0", "predições faltando ou duplicadas depois de derrubar o job de scoring no meio do fluxo e religar, conferido no CI"),
        "problem": "Um monitor que só conta transações diz ao time de fraude o que já aconteceu. Cada transação precisa "
        "de uma nota no momento em que chega, e o time precisa saber que tipos de fraude o modelo deixa passar.",
        "solution": "Um classificador XGBoost treinado offline pontua cada transação dentro do Spark Structured "
        "Streaming. O histórico recente de cada cartão fica no state store do Spark, as predições vão para o Delta uma "
        "única vez, e um monitor confere precisão, recall e drift dos dados contra limites definidos.",
        "how": [
            "O limiar é escolhido num período de validação; todo número publicado vem de um período de teste posterior, que nenhuma escolha viu.",
            "Um teste com Spark religa a consulta e obtém as mesmas features de velocidade do treino; o CI derruba o job com SIGKILL e encontra uma predição por mensagem do Kafka.",
            "O monitor só alerta quando o intervalo de 95% fica abaixo do piso, e aponta drift por PSI.",
            "O modelo é reaproveitado pelo agente MCP da SEC e pelos agentes de investigação de fraude.",
        ],
        "results": [
            ("96,6% / 96,6%", "de precisão e recall no período de teste (PR-AUC de 0,992)"),
            ("4.597 / 4.597", "mensagens no Kafka e predições depois de um restart com SIGKILL no CI"),
            ("64,2%", "de recall em viagem impossível, o ponto fraco documentado"),
        ],
        "limits": "Treinado em transações sintéticas; viagem impossível é em parte indistinguível de uma viagem real.",
        "image_alt": "Painel de pontuação ao vivo",
    },
    "realtime-fraud-streaming": {
        "name": "Streaming de fraude em tempo real",
        "line": "Um pipeline de streaming em Delta Lake que aguenta uma queda sem perder nem repetir registro, com schema registry e checagem de saúde.",
        "headline": ("0", "registros perdidos ou duplicados depois de derrubar o job no meio do fluxo e religar, conferido no CI"),
        "problem": "Fraude em cartão acontece em segundos, e o sinal está nos padrões ao longo do tempo. Um relatório "
        "em lote noturno enxerga isso com um dia de atraso.",
        "solution": "As transações fluem do Redpanda pelo Spark Structured Streaming até tabelas Delta Lake e um painel "
        "ao vivo, com janelas por tempo do evento e watermarks. O schema dos eventos fica num schema registry que recusa "
        "mudanças incompatíveis; o que quebra o contrato vai para quarentena com os motivos. Uma checagem de saúde aprova "
        "ou reprova o fluxo e pode avisar por webhook.",
        "how": [
            "Gravação em Delta com checkpoints: o CI derruba o job com SIGKILL, religa e encontra cada offset do Kafka na Bronze exatamente uma vez.",
            "Compactação e limpeza rodam com o fluxo gravando (66 arquivos viraram 16, com as mesmas linhas, no CI).",
            "O registry recusa um schema incompatível no CI; uma mensagem enviada sem ele cai na quarentena.",
            "O progresso de cada consulta fica registrado; a checagem de saúde falha em até dois minutos depois que o job para.",
        ],
        "results": [
            ("0", "offsets duplicados ou faltando depois de uma queda e religada"),
            ("~2 min", "do fim de um minuto até a linha dele na Gold"),
            ("47", "testes, incluindo Spark com Delta numa sessão local"),
        ],
        "limits": "Um broker e disco local; os alertas vão para um webhook, não para um serviço de plantão. O painel público mostra uma amostra gravada.",
        "image_alt": "Visão geral do painel de streaming",
    },
    "supply-chain-risk-intelligence": {
        "name": "Inteligência de risco na cadeia de suprimentos",
        "line": "Atraso na entrega da causa à decisão: inferência causal, análise de sobrevivência, previsão, risco e otimização.",
        "headline": ("94,4%", "dos 10% de pedidos mais arriscados realmente atrasam, reconferido nos dados reais no CI"),
        "problem": "“Atrasamos com frequência” não é algo sobre o que a operação consiga agir. Ela precisa da causa, do "
        "momento, do volume que vem, dos pedidos em risco e do que mudar.",
        "solution": "Cinco análises conectadas de 180.519 pedidos reais: pareamento por escore de propensão, modelos de "
        "sobrevivência, previsão de demanda, um modelo de risco calibrado e explicado com SHAP, e uma programação linear "
        "que transforma as notas de risco numa alocação de frete mais barata.",
        "how": [
            "O CI baixa o dataset real (com checksum fixo), valida contra um contrato de dados, roda os notebooks de novo e falha se algum número publicado mudar.",
            "Efeito causal estimado em 35.216 pares pareados, com os 78 níveis de covariáveis balanceados.",
            "A otimização usa notas de risco fora da amostra e é testada sob estresse com 10.000 simulações de Monte Carlo.",
        ],
        "results": [
            ("1,99 dia", "a mais de atraso na Segunda Classe que na Classe Padrão, frente ao prometido"),
            ("33%", "menos erro de previsão que a linha de base ingênua (MAPE de 5,9% contra 8,9%)"),
            ("94,4%", "dos 10% de pedidos mais arriscados atrasam (AUC de 0,73)"),
        ],
        "limits": "A otimização economiza 0,85% do custo esperado em pedidos que o modelo nunca viu: real, mas pequeno, e reportado assim.",
        "image_alt": "Comparação da previsão com a linha de base ingênua",
    },
    "nyc-tip-mlops": {
        "name": "MLOps de gorjetas em NY",
        "line": "Retreino mensal com dados reais novos, promoção por teste estatístico, registro de modelos, uma API e monitoramento de drift.",
        "headline": ("+0,010", "de AUC do modelo treinado em agosto de 2026 sobre o antigo campeão, nas mesmas corridas de setembro; promovido porque o intervalo de 95% fica acima de zero"),
        "problem": "Um modelo só tem valor em produção se cada etapa em volta dele for confiável: treino repetível, uma "
        "regra para qual versão está no ar, features calculadas do mesmo jeito no serving e um sinal quando os dados mudam.",
        "solution": "Um sistema de MLOps em volta de um classificador que prevê, no fim da corrida e antes do pagamento, se uma corrida de táxi em "
        "Nova York vai dar mais de 20% de gorjeta: rastreamento e registro com MLflow, um serviço FastAPI, relatórios de "
        "drift com Evidently, um painel de operação em Streamlit e um CI que roda o ciclo inteiro, inclusive o Docker.",
        "how": [
            "Sem vazamento de rótulo: nenhum dado do pagamento entra, só o que se sabe quando a corrida termina, o que limita a nota de forma honesta.",
            "Todo mês o CI acha o mês mais novo da TLC, treina um desafiante e compara com o campeão no mesmo mês fora do treino; ele só é promovido se o intervalo de bootstrap pareado do ganho ficar acima de zero.",
            "Um teste confere que a API calcula as features exatamente como o treino.",
        ],
        "results": [
            ("0,625 vs 0,615", "de AUC do novo e do antigo campeão em 500.000 corridas de setembro de 2026"),
            ("4% → 13%", "de drift na fatia de tipo de pagamento desconhecido, detectado de 2024 para 2025"),
            ("42", "testes, mais o retreino mensal com dados reais no CI"),
        ],
        "limits": "Gorjeta é difícil de prever a partir dos dados da corrida; o valor do projeto está na engenharia em volta do modelo.",
        "image_alt": "Painel de operação com o modelo no ar",
    },
    "nyc-taxi-lakehouse": {
        "name": "Lakehouse de táxis de NY",
        "line": "Um lakehouse em Delta Lake sobre 42 milhões de corridas, processado mês a mês, que separa o efeito da taxa de congestionamento do efeito do inverno.",
        "headline": ("−0,4 pt", "nas corridas por dia em Manhattan por causa da taxa, tirando o inverno; a queda bruta era de 10,7%"),
        "problem": "Saber se a taxa de congestionamento de 2025 em Nova York mudou o uso de táxis: a taxa começou em janeiro, "
        "então um simples antes e depois mistura a taxa com o inverno, e os arquivos mudam de schema no meio e trazem "
        "registros inválidos.",
        "solution": "Camadas Bronze, Silver e Gold em Delta Lake sobre duas temporadas de outubro a março, transformadas "
        "com DuckDB e orquestradas pelo Dagster em partições mensais. A estimativa desconta o que o inverno fez na "
        "temporada anterior à taxa, e onze checagens de qualidade barram dados ruins antes de chegarem aos números.",
        "how": [
            "Cada mês é uma partição do Dagster gravada com overwrite por predicado: entra ou é refeito sozinho, e refazer não muda nada.",
            "Os testes provam que montar mês a mês ou tudo de uma vez dá as mesmas tabelas Gold.",
            "Os mesmos meses um ano antes, sem a taxa, servem de controle para a estação do ano.",
            "Checagens de qualidade bloqueantes param a execução antes que linhas ruins cheguem à Gold.",
        ],
        "results": [
            ("−0,4 pt", "nas corridas por dia: a queda bruta de 10,7% é quase toda inverno"),
            ("−3,6 pt", "na duração das corridas atribuível à taxa, com a distância igual"),
            ("42,1M", "de corridas em doze partições mensais"),
        ],
        "limits": "Supõe que o inverno muda o uso de táxi do mesmo jeito todo ano; só táxis amarelos.",
        "image_alt": "Impacto da taxa de congestionamento no painel",
    },
    "olist-cloud-warehouse": {
        "name": "Data warehouse na nuvem (Olist)",
        "line": "Um data warehouse no BigQuery alimentado por dados que chegam todo dia, com modelos dbt incrementais, alertas de atraso, Terraform e CI sem chaves.",
        "headline": ("0", "linhas de diferença entre o build incremental diário e um build do zero, conferido em todo pull request"),
        "problem": "Um data warehouse só merece confiança se as tabelas mantêm o formato, se toda mudança é testada "
        "antes de chegar ao analista, se ninguém guarda uma chave de nuvem que não expira e se alguém sabe quanto "
        "cada consulta custa.",
        "solution": "Os dados do marketplace Olist no BigQuery (região de São Paulo), chegando como chegam em "
        "produção: um fluxo diário de mudanças, em que o pedido é comprado, enviado, entregue e avaliado em dias "
        "diferentes. As tabelas fato se atualizam de forma incremental, a atualização dos dados é monitorada e "
        "uma falha abre um alerta. Infraestrutura em Terraform, contratos dbt em todas as tabelas e GitHub "
        "Actions que entram no Google Cloud por Workload Identity Federation, como duas contas de serviço com o "
        "mínimo de permissão.",
        "how": [
            "O histórico de 2016 a 2018 é reproduzido um dia por dia real; cada lote substitui a própria partição no raw, então rodar de novo ou recuperar dias perdidos dá o mesmo resultado.",
            "As tabelas fato reconstroem só os meses de compra com algum pedido alterado e trocam essas partições com jobs de cópia, porque o sandbox não tem MERGE.",
            "Todo pull request reproduz 31 dias em datasets descartáveis, faz o build incremental e o completo, e falha se os dois não tiverem as mesmas linhas.",
            "A atualização dos dados é conferida depois de cada deploy e a cada seis horas; uma falha abre uma issue no GitHub, e um runbook diz o que fazer.",
            "O Terraform cria os datasets, duas contas de serviço, a federação de identidade e um papel customizado com uma única permissão.",
        ],
        "results": [
            ("1 dia", "de dados novos por dia real, carregado sem duplicar e recuperando dias perdidos"),
            ("80%+", "menos bytes lidos numa pergunta de um mês na tabela fato particionada, medido a cada deploy"),
            ("0", "chaves de conta de serviço: o CI usa tokens de uma hora vindos da identidade OIDC do GitHub"),
        ],
        "limits": "O fluxo diário reproduz eventos reais, não um sistema ao vivo, e os dados têm cerca de 100 mil "
        "pedidos. O sandbox do BigQuery não tem Cloud Storage, então o estado do Terraform fica no Cloud Shell e "
        "ele é aplicado à mão.",
        "extra_links": [
            ("Página do projeto", "https://diegotddd.github.io/olist-cloud-warehouse/"),
            ("Documentação dbt", "https://diegotddd.github.io/olist-cloud-warehouse/dbt/"),
        ],
    },
    "olist-analytics": {
        "name": "Analytics de e-commerce da Olist",
        "line": "Um modelo estrela testado em dbt sobre 100 mil pedidos e um relatório em Power BI que medem quanto os atrasos derrubam as avaliações.",
        "headline": ("4,29 → 1,81", "de nota média no prazo contra 6 dias de atraso; depois disso quase não muda"),
        "problem": "Um marketplace sabe que atrasos derrubam as avaliações, mas não quanto, com que rapidez, nem se deve "
        "reduzir o tamanho dos atrasos ou evitá-los por completo.",
        "solution": "Um modelo estrela construído com dbt sobre DuckDB em cerca de 100 mil pedidos reais da Olist, com "
        "testes para cada regra de negócio, um relatório de três páginas em Power BI e um painel em Streamlit.",
        "how": [
            "15 modelos dbt e 48 testes rodam a cada mudança, a partir dos arquivos brutos.",
            "As duas tabelas fato são incrementais. O CI reproduz o fluxo de pedidos dia a dia a partir dos horários dos eventos "
            "nos dados e prova que elas são iguais a uma reconstrução completa em cada passo; a checagem de atualização falha "
            "uma carga com mais de 50 horas.",
            "O modelo do Power BI (TMDL) e as páginas (PBIR) são gerados por código: 23 medidas DAX, tabela de datas "
            "marcada e textos das páginas calculados a partir dos dados. O CI falha se divergirem do que está no repositório.",
            "O relatório foi aberto, atualizado e conferido no Power BI Desktop; o .pbix está no repositório.",
        ],
        "results": [
            ("6,8%", "dos pedidos entregues chegam atrasados"),
            ("3,73 → 2,68", "de nota com 1 dia contra 3 dias de atraso: cada dia da primeira semana custa nota"),
            ("48", "testes dbt em 15 modelos"),
        ],
        "limits": "Correlação a partir de dados observacionais; pedidos atrasados podem diferir em outros aspectos.",
        "image_alt": "Página do Power BI: nota média por dias de atraso, com a decisão que ela apoia",
        "extra_links": [("Arquivo do Power BI (.pbix)", "https://github.com/DiegoTDDD/olist-analytics/raw/main/powerbi/OlistEntregas.pbix")],
    },
    "economic-data-platform": {
        "name": "Plataforma de dados econômicos",
        "line": "ELT de indicadores macroeconômicos brasileiros e de mercado que nunca mostra uma tabela vazia ou pela metade.",
        "headline": ("5", "checagens de qualidade que cada lote precisa passar antes de substituir a camada Gold"),
        "problem": "Fontes públicas de dados econômicos falham de jeitos comuns: limite de requisições, timeout, resposta "
        "vazia, formato alterado. Um painel alimentado direto por elas fica em branco ou mostra números errados sem ninguém notar.",
        "solution": "Uma plataforma ELT que busca indicadores do Banco Central do Brasil e dados do Yahoo Finance com "
        "novas tentativas, confere cada lote antes de ele poder substituir a camada Gold no PostgreSQL, grava de forma "
        "atômica e serve tudo num painel.",
        "how": [
            "Checagens de faixa, nulos, duplicatas, datas futuras e contagem de linhas em cada lote.",
            "Um lote com falha é rejeitado e a Gold mantém os dados anteriores.",
            "Um teste prova num PostgreSQL real que uma inserção com falha desfaz a exclusão.",
        ],
        "results": [
            ("5", "checagens de qualidade em cada lote antes de chegar à Gold"),
            ("3", "tentativas por etapa, com espera em limites de requisição e timeouts"),
            ("1", "transação por atualização: a Gold nunca fica vazia"),
        ],
        "limits": "O painel público lê um retrato da Gold que o CI atualiza todo mês.",
        "image_alt": "Indicadores macroeconômicos no painel",
    },
    "hospcall": {
        "name": "Hospcall: sistema de chamados para uma casa de idosos",
        "line": "Um sistema de chamados usado por seis meses em piloto numa associação geriátrica, feito por uma equipe de sete alunos da UNIVESP.",
        "headline": ("60", "cuidadores cadastrados em seis meses de piloto na AGERIP"),
        "my_part": "Participei de todas as etapas com a equipe: as reuniões de requisitos com a equipe da AGERIP, "
        "o modelo de dados em PostgreSQL e a tabela de auditoria, a API e o canal de tempo real, as telas em React "
        "para tablets, TVs e administração, a implantação e o acompanhamento dos seis meses de piloto.",
        "problem": "Na AGERIP, associação geriátrica de São José do Rio Preto, um morador que precisava de ajuda dependia "
        "de um cuidador passar pelo corredor, e o registro do plantão dependia de anotações no papel. Recusa de atendimento, "
        "troca de plantão no meio de um chamado e atendimento por quem não estava na escala não deixavam registro. Sistemas "
        "comerciais de chamada exigem cabeamento próprio e contrato de manutenção fora do alcance de uma entidade filantrópica.",
        "solution": "Um sistema web em hardware comum: um tablet em cada quarto abre o chamado, painéis de TV nos corredores "
        "mostram tudo em tempo real, o cuidador faz check-in com PIN e a enfermagem gerencia chamados, dispositivos e "
        "exportações numa página administrativa. Toda intervenção administrativa vai para uma tabela de auditoria imutável, "
        "sem sobrescrever o chamado.",
        "how": [
            "Os requisitos vieram de reuniões com a gerente geral, a enfermeira-chefe e uma enfermeira da AGERIP.",
            "O retorno delas mudou o produto: PIN sempre disponível, tablets que se cadastram sozinhos, grade da TV "
            "configurada à distância e o contador de tempo em aberto removido porque deixava a equipe ansiosa.",
            "O canal de tempo real se reconecta sozinho depois de uma queda, testado com falhas provocadas.",
        ],
        "results": [
            ("56", "chamados no piloto, de outubro de 2025 a março de 2026, 41 concluídos"),
            ("≤ 39 ms", "de reconexão mediana do canal de tempo real; 67 ms no pior caso"),
            ("11", "novos requisitos da reunião final de validação com a equipe, em maio de 2026"),
        ],
        "limits": "Três quartos foram instrumentados e o tempo de resposta ao chamado não foi registrado, então o piloto "
        "mostra adoção e estabilidade, não um atendimento mais rápido. Os testes foram manuais. O código é da equipe e "
        "não é público.",
        "image_alt": "Painel de TV do corredor com seis quartos, um deles com chamado aberto",
    },
    "iefa-sales-stock": {
        "name": "Sistema de vendas e estoque de uma loja beneficente",
        "line": "Um sistema de ponto de venda e estoque que as voluntárias da loja do IEFA usam em todo dia de funcionamento, feito por uma equipe de oito alunos da UNIVESP.",
        "headline": ("100%", "das funcionalidades previstas entregues; em uso em todo dia de funcionamento da loja desde cerca de julho de 2026"),
        "my_part": "Participei de todas as etapas com a equipe: a contagem do estoque e o cadastro dos produtos, os "
        "modelos em Django e o banco MySQL, o ponto de venda, os relatórios e as etiquetas, a instalação no "
        "computador da loja e o acompanhamento das voluntárias, incluindo a correção das saídas de estoque.",
        "problem": "A loja do Instituto Educacional Francisco de Assis, em São José do Rio Preto, registrava as vendas em papel "
        "e cadernos e não tinha controle de estoque estruturado. Nem todo produto tinha o preço identificado, o que gerava "
        "preço errado no caixa.",
        "solution": "Um sistema em Django e MySQL com ponto de venda por código de barras, produtos, movimentações de estoque, "
        "formas de pagamento, usuários e relatórios de vendas, instalado como serviço no computador Windows da loja. Cada "
        "venda gera a saída de estoque sozinha, e a entrada de mercadoria imprime as etiquetas.",
        "how": [
            "A equipe contou o estoque inteiro, cadastrou todos os produtos e imprimiu as etiquetas antes de entrar em produção.",
            "Acompanhar as voluntárias usando trouxe funções que ninguém tinha pedido: remover item, cancelar venda, estoque "
            "inicial no cadastro do produto e pesquisa em todas as listas.",
            "Um defeito nas saídas de estoque das vendas foi corrigido no código e as movimentações que faltavam foram "
            "regularizadas com um script SQL.",
        ],
        "results": [
            ("0", "relatos de preço errado ou produto sem preço desde a adoção das etiquetas com código de barras"),
            ("9", "módulos em produção: vendas, PDV, estoque, produtos, categorias, pagamentos, usuários, relatórios e etiquetas"),
            ("2", "relatórios usados na rotina das voluntárias: vendas por forma de pagamento e impressão de etiquetas"),
        ],
        "limits": "Os resultados são observados, não medidos: não há contagem de erros antes e depois. Os testes são manuais, "
        "e as voluntárias usam um login comum, então as ações não são rastreáveis por pessoa. O código é da equipe e não é "
        "público.",
        "image_alt": "Ponto de venda com dois itens lidos pelo código de barras e o total da venda",
    },
}
