"""The manager's view of each project: the decision it supports, who uses it, what an error
costs, how it creates value, and its risks. Every claim comes from the project's README; no
revenue or savings figure is invented. Projects with a calculator name it in "calc"."""

BUSINESS = {
    "fraud-investigation-agents": {
        "pt": {
            "decision": "Para cada alerta de fraude: bloquear o cartão ou liberar a compra, e por qual motivo.",
            "users": "Analistas de prevenção à fraude, que hoje investigam cada alerta à mão.",
            "error": "Liberar uma fraude custa o valor da compra; bloquear um cliente legítimo custa atrito e, às vezes, o cliente.",
            "value": "Os agentes fazem a investigação repetitiva e entregam um relatório com as evidências. O analista revisa em vez de investigar do zero, e o crítico impede que um relatório sem prova libere uma fraude.",
            "risk": "Medido em dados sintéticos; o resumo em texto livre não é conferido pelo crítico, então a decisão final continua com o analista.",
        },
        "en": {
            "decision": "For each fraud alert: block the card or clear the purchase, and why.",
            "users": "Fraud prevention analysts, who today investigate each alert by hand.",
            "error": "Clearing a fraud costs the purchase amount; blocking a legitimate customer costs friction and sometimes the customer.",
            "value": "The agents do the repetitive investigation and hand over a report with the evidence. The analyst reviews instead of starting from scratch, and the critic stops an unsupported report from clearing a fraud.",
            "risk": "Measured on synthetic data; the critic does not check the free-text summary, so the final decision stays with the analyst.",
        },
    },
    "sec-mcp-agent": {
        "pt": {
            "decision": "Responder perguntas sobre relatórios financeiros com fontes que alguém pode conferir.",
            "users": "Analistas financeiros e de risco que leem relatórios 10-K.",
            "error": "Uma citação inventada leva a uma decisão baseada num fato que não existe no documento.",
            "value": "Cada citação é conferida contra o trecho original antes de a resposta sair. As ferramentas ficam em servidores MCP reutilizáveis, que qualquer agente ou o Claude Desktop pode usar.",
            "risk": "17 de 22 perguntas certas: um modelo pequeno ainda erra perguntas de várias etapas.",
        },
        "en": {
            "decision": "Answering questions about financial filings with sources someone can check.",
            "users": "Financial and risk analysts who read 10-K filings.",
            "error": "An invented citation leads to a decision based on a fact that is not in the document.",
            "value": "Every citation is checked against the original passage before the answer goes out. The tools live in reusable MCP servers that any agent or Claude Desktop can use.",
            "risk": "17 of 22 questions right: a small model still misses some multi-step questions.",
        },
    },
    "olist-ai-analyst": {
        "pt": {
            "decision": "Qualquer decisão que dependa de um número da operação: onde investir, o que cortar, o que priorizar.",
            "users": "Gestores e áreas de negócio que hoje esperam o time de dados para cada pergunta.",
            "error": "Um número errado num memo bem escrito leva a uma decisão errada com cara de certa.",
            "value": "A pergunta vira memo em cerca de meio minuto, com o SQL e as linhas que sustentam a resposta. Quando o modelo escreve um número que não está no resultado, o memo sai marcado como não verificado em vez de parecer confiável.",
            "risk": "Acerta 68% das perguntas da avaliação; serve como primeiro rascunho para um analista revisar, não como resposta final.",
        },
        "en": {
            "decision": "Any decision that depends on a number from operations: where to invest, what to cut, what to prioritize.",
            "users": "Managers and business teams who today wait for the data team for every question.",
            "error": "A wrong number in a well-written memo leads to a wrong decision that looks right.",
            "value": "A question becomes a memo in about half a minute, with the SQL and rows behind the answer. When the model writes a number that is not in the result, the memo is marked unverified instead of looking trustworthy.",
            "risk": "It gets 68% of the evaluation questions right; it is a first draft for an analyst to review, not a final answer.",
        },
    },
    "llm-guardrails-redteam": {
        "pt": {
            "decision": "Colocar ou não um agente em contato com documentos e usuários externos.",
            "users": "Times de segurança, compliance e quem aprova a ida de IA para produção.",
            "error": "Um agente manipulado pode vazar dados pessoais, chamar ferramentas indevidas ou liberar uma fraude; dados pessoais em logs são risco de LGPD.",
            "value": "Cada ataque conhecido é testado a cada mudança, e o build quebra se um passar ou se algo legítimo for bloqueado. CPF, cartão e e-mail são mascarados antes de chegar aos logs.",
            "risk": "A detecção de injeção usa padrões; ataques novos podem passar, e por isso as outras camadas são testadas sozinhas.",
        },
        "en": {
            "decision": "Whether an agent can be exposed to external documents and users.",
            "users": "Security and compliance teams, and whoever signs off AI going to production.",
            "error": "A manipulated agent can leak personal data, call the wrong tools or clear a fraud; personal data in logs is a privacy-law risk.",
            "value": "Every known attack is tested on every change, and the build fails if one gets through or if anything legitimate is blocked. Card numbers, CPF and e-mail are masked before they reach the logs.",
            "risk": "Injection detection uses patterns; new attacks can get through, which is why the other layers are tested on their own.",
        },
    },
    "llm-evals-observability": {
        "pt": {
            "decision": "Liberar ou não uma mudança num sistema com IA.",
            "users": "Times que mantêm agentes e LLMs em produção.",
            "error": "Uma mudança que piora o agente chega ao usuário sem ninguém perceber.",
            "value": "Cada pull request é testado contra 162 chamadas reais gravadas; uma regressão real já foi barrada antes de ir para o ar. O painel mostra a qualidade ao longo do tempo.",
            "risk": "Resultados ao vivo variam entre execuções; a barreira usa tolerâncias medidas, não valores exatos.",
        },
        "en": {
            "decision": "Whether to ship a change to an AI system.",
            "users": "Teams that run agents and LLMs in production.",
            "error": "A change that makes the agent worse reaches users without anyone noticing.",
            "value": "Every pull request is tested against 162 recorded real calls; a real regression was already stopped before going live. The dashboard shows quality over time.",
            "risk": "Live results vary between runs; the gate uses measured tolerances, not exact values.",
        },
    },
    "finetune-and-serve": {
        "pt": {
            "decision": "Treinar um modelo próprio ou pagar uma API comercial para uma tarefa de extração.",
            "users": "Quem decide orçamento e arquitetura de IA: tech leads, produto e finanças.",
            "error": "Escolher API com volume alto paga caro por requisição; escolher modelo próprio com volume baixo paga uma máquina parada.",
            "value": "O modelo pequeno ajustado acerta mais (0,82 contra 0,65) e custa US$ 35 por milhão de requisições em carga total. A conta mostra a partir de qual volume mensal a máquina própria fica mais barata que cada API.",
            "risk": "A precisão das APIs nessa tarefa não foi medida, só o preço; o custo da VM supõe uso total.",
        },
        "en": {
            "decision": "Train an in-house model or pay a commercial API for an extraction task.",
            "users": "Whoever owns AI budget and architecture: tech leads, product and finance.",
            "error": "Choosing an API at high volume pays a lot per request; choosing your own model at low volume pays for an idle machine.",
            "value": "The small fine-tuned model is more accurate (0.82 against 0.65) and costs $35 per million requests at full load. The numbers show the monthly volume from which your own machine beats each API.",
            "risk": "The APIs' accuracy on this task was not measured, only their price; the VM cost assumes full use.",
        },
        "calc": "finetune",
    },
    "llm-from-scratch": {
        "pt": {
            "decision": "Entender e depurar um LLM em vez de tratá-lo como caixa-preta.",
            "users": "Times técnicos que ajustam, servem ou depuram modelos de linguagem.",
            "error": "Sem entender as peças, um bug de tokenizador ou de cache vira semanas de investigação.",
            "value": "Mostra domínio de cada parte de um modelo de linguagem, com testes, e geração 5,8× mais rápida com o cache.",
            "risk": "É um projeto de aprendizado: o modelo aprende o estilo dos relatórios, não fatos.",
        },
        "en": {
            "decision": "Understanding and debugging an LLM instead of treating it as a black box.",
            "users": "Technical teams that fine-tune, serve or debug language models.",
            "error": "Without understanding the parts, a tokenizer or cache bug turns into weeks of investigation.",
            "value": "Shows command of every part of a language model, with tests, and 5.8× faster generation with the cache.",
            "risk": "A learning project: the model learns the style of filings, not facts.",
        },
    },
    "sec-filings-rag": {
        "pt": {
            "decision": "Encontrar a resposta num relatório de centenas de páginas, com a fonte.",
            "users": "Analistas de investimento, crédito e compliance.",
            "error": "Uma resposta sem fonte não pode ser usada; uma fonte errada leva a uma conclusão errada.",
            "value": "A busca certa aparece entre os 5 primeiros trechos em 80% das perguntas, contra 43% da busca comum, e cada resposta mostra de onde veio.",
            "risk": "A demo pública mostra respostas gravadas, porque o host gratuito não roda o pipeline completo.",
        },
        "en": {
            "decision": "Finding the answer in a filing hundreds of pages long, with its source.",
            "users": "Investment, credit and compliance analysts.",
            "error": "An answer without a source cannot be used; a wrong source leads to a wrong conclusion.",
            "value": "The right passage is in the top 5 for 80% of questions, against 43% for plain search, and every answer shows where it came from.",
            "risk": "The public demo shows recorded answers, because the free host cannot run the full pipeline.",
        },
    },
    "freight-intelligence": {
        "pt": {
            "decision": "Onde, por qual modal e por qual rota mandar carga, e quanto volume esperar.",
            "users": "Planejamento logístico, comercial de fretes e operação de transporte.",
            "error": "Previsão errada gera capacidade ociosa ou falta; rota sem restrição de caminhão gera multa e atraso.",
            "value": "Junta fontes dos EUA e do Brasil num histórico confiável de 97,6 milhões de linhas, com previsão testada em anos reservados, otimização de alocação e roteirização para caminhões.",
            "risk": "A demo gratuita demora para acordar; previsões são linhas de base avaliadas, não promessas de volume.",
        },
        "en": {
            "decision": "Where, by which mode and on which route to ship, and what volume to expect.",
            "users": "Logistics planning, freight sales and transport operations.",
            "error": "A wrong forecast means idle capacity or shortage; a route that ignores truck limits means fines and delays.",
            "value": "Brings US and Brazilian sources into a trusted 97.6-million-row history, with forecasts tested on held-out years, allocation optimization and truck-aware routing.",
            "risk": "The free demo takes time to wake up; forecasts are evaluated baselines, not volume promises.",
        },
    },
    "realtime-fraud-detection-ml": {
        "pt": {
            "decision": "Aprovar ou segurar cada transação de cartão no momento em que ela chega.",
            "users": "Times de prevenção à fraude e de risco em meios de pagamento.",
            "error": "Uma fraude aprovada vira prejuízo; um bloqueio errado irrita um cliente legítimo.",
            "value": "O limiar foi escolhido para manter no máximo 1 alarme falso a cada 20 alertas no conjunto de teste, pegando 96,6% das fraudes. Com menos fraude na base, a proporção de alarmes falsos sobe; a calculadora abaixo mostra quanto. O painel mostra ao vivo quais tipos de fraude escapam.",
            "risk": "Dados sintéticos; a fraude por viagem impossível só é pega em 64,7% dos casos, e isso está documentado.",
        },
        "en": {
            "decision": "Approve or hold each card transaction the moment it arrives.",
            "users": "Fraud prevention and payments risk teams.",
            "error": "An approved fraud becomes a loss; a wrong block annoys a legitimate customer.",
            "value": "The threshold keeps false alarms to at most 1 in 20 alerts on the test set while catching 96.6% of fraud. With less fraud in the data the share of false alarms rises; the calculator below shows by how much. The dashboard shows live which kinds of fraud get through.",
            "risk": "Synthetic data; impossible-travel fraud is caught in only 64.7% of cases, and that is documented.",
        },
        "calc": "fraud",
    },
    "realtime-fraud-streaming": {
        "pt": {
            "decision": "Perceber um ataque de fraude em minutos, não no relatório do dia seguinte.",
            "users": "Monitoramento de fraude e operação de pagamentos.",
            "error": "Descobrir um ataque um dia depois significa um dia inteiro de prejuízo.",
            "value": "Cada minuto vira uma linha com contagens e fraude por padrão cerca de 2 minutos depois, e eventos fora do contrato vão para quarentena com o motivo.",
            "risk": "O painel público mostra uma amostra gravada do fluxo.",
        },
        "en": {
            "decision": "Spotting a fraud attack within minutes, not in the next day's report.",
            "users": "Fraud monitoring and payments operations.",
            "error": "Finding an attack a day late means a full day of losses.",
            "value": "Each minute becomes a row with counts and fraud by pattern about 2 minutes later, and events that break the contract are quarantined with the reason.",
            "risk": "The public dashboard shows a recorded sample of the stream.",
        },
    },
    "supply-chain-risk-intelligence": {
        "pt": {
            "decision": "Quais pedidos priorizar para não atrasar, e qual modalidade de frete usar.",
            "users": "Operações de logística e atendimento ao cliente.",
            "error": "Atraso gera reclamação e reembolso; agir em todos os pedidos custa caro demais.",
            "value": "O modelo separa os 10% de pedidos mais arriscados, dos quais 94,8% realmente atrasam, então a equipe age onde importa. A análise causal mostra que a Segunda Classe atrasa 1,99 dia a mais que a Padrão.",
            "risk": "A otimização de frete economiza só 1,01% do custo esperado, e isso é reportado assim.",
        },
        "en": {
            "decision": "Which orders to prioritize to avoid delays, and which shipping class to use.",
            "users": "Logistics operations and customer service.",
            "error": "Delays bring complaints and refunds; acting on every order costs too much.",
            "value": "The model isolates the riskiest 10% of orders, 94.8% of which are actually late, so the team acts where it matters. The causal analysis shows Second Class runs 1.99 days later than Standard.",
            "risk": "The shipping optimization saves only 1.01% of expected cost, and it is reported as such.",
        },
        "calc": "supply",
    },
    "nyc-tip-mlops": {
        "pt": {
            "decision": "Confiar ou não no modelo que está no ar, e quando trocá-lo.",
            "users": "Times de dados que mantêm modelos em produção.",
            "error": "Um modelo que perdeu a validade continua decidindo sem ninguém saber.",
            "value": "Uma versão nova só entra no ar se for melhor, a API calcula as features igual ao treino, e o drift de dados é detectado (de 4% para 13% de pagamentos desconhecidos).",
            "risk": "O modelo em si é fraco (AUC 0,624); o valor está na engenharia em volta dele.",
        },
        "en": {
            "decision": "Whether to trust the model in production, and when to replace it.",
            "users": "Data teams that run models in production.",
            "error": "A model that went stale keeps deciding without anyone knowing.",
            "value": "A new version goes live only if it is better, the API computes features exactly as training does, and data drift is detected (unknown payments from 4% to 13%).",
            "risk": "The model itself is weak (AUC 0.624); the value is in the engineering around it.",
        },
    },
    "nyc-taxi-lakehouse": {
        "pt": {
            "decision": "Avaliar se uma política pública (a taxa de congestionamento) mudou o comportamento.",
            "users": "Analistas de políticas públicas, mobilidade e planejamento urbano.",
            "error": "Concluir em cima de dados sujos ou incompletos leva a uma avaliação de política errada.",
            "value": "22,3 milhões de corridas limpas e testadas mostram queda de 10,7% nos embarques e de 15,1% na duração das corridas em Manhattan depois da taxa.",
            "risk": "Antes e depois caem em estações diferentes; parte da mudança pode ser sazonal.",
        },
        "en": {
            "decision": "Assessing whether a public policy (the congestion fee) changed behaviour.",
            "users": "Policy, mobility and urban planning analysts.",
            "error": "Concluding from dirty or incomplete data leads to a wrong policy assessment.",
            "value": "22.3 million cleaned, tested trips show pickups down 10.7% and trip duration down 15.1% in Manhattan after the fee.",
            "risk": "Before and after fall in different seasons; part of the change may be seasonal.",
        },
    },
    "olist-analytics": {
        "pt": {
            "decision": "Onde investir em logística: reduzir atrasos grandes ou evitar qualquer atraso.",
            "users": "Operação de marketplace, logística e experiência do cliente.",
            "error": "Investir no problema errado gasta dinheiro sem recuperar as avaliações.",
            "value": "A nota cai de 4,29 para 2,99 já no primeiro dia de atraso, então evitar o atraso vale mais que encurtá-lo. Os números vêm de modelos dbt conferidos por 35 testes.",
            "risk": "Correlação em dados observacionais: pedidos atrasados podem diferir em outros aspectos.",
        },
        "en": {
            "decision": "Where to invest in logistics: shortening long delays or avoiding any delay.",
            "users": "Marketplace operations, logistics and customer experience.",
            "error": "Investing in the wrong problem spends money without recovering ratings.",
            "value": "The rating drops from 4.29 to 2.99 on the very first day late, so avoiding delays is worth more than shortening them. The numbers come from dbt models checked by 35 tests.",
            "risk": "Correlation in observational data: late orders may differ in other ways.",
        },
    },
    "economic-data-platform": {
        "pt": {
            "decision": "Decidir com indicadores econômicos sem medo de o painel estar errado.",
            "users": "Áreas de finanças, tesouraria e planejamento que acompanham IPCA, câmbio e juros.",
            "error": "Um painel vazio ou com número errado leva a decisão errada, e ninguém percebe.",
            "value": "Cada lote passa por 5 checagens antes de entrar; se falhar, o painel mantém o último dado bom. A atualização é atômica: nunca fica pela metade.",
            "risk": "O painel público lê um retrato atualizado todo mês pelo CI.",
        },
        "en": {
            "decision": "Deciding with economic indicators without fearing the dashboard is wrong.",
            "users": "Finance, treasury and planning teams that follow inflation, FX and rates.",
            "error": "An empty or wrong dashboard leads to a wrong decision, and nobody notices.",
            "value": "Every batch passes 5 checks before it goes in; if it fails, the dashboard keeps the last good data. Refreshes are atomic: never half done.",
            "risk": "The public dashboard reads a snapshot the CI refreshes monthly.",
        },
    },
}

LABELS = {
    "pt": {"view": "Visão", "manager": "Gestor", "tech": "Técnica", "decision": "Decisão que apoia",
           "users": "Quem usa", "error": "Quanto custa errar", "value": "Como gera valor", "risk": "Riscos e limites",
           "calc": "Calcule para o seu cenário"},
    "en": {"view": "View", "manager": "Manager", "tech": "Technical", "decision": "Decision it supports",
           "users": "Who uses it", "error": "What an error costs", "value": "How it creates value", "risk": "Risks and limits",
           "calc": "Run your own numbers"},
}
