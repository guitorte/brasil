---
titulo: Golpe com garantia: como funcionava o esquema do Banco Master
titulo_aba: Alugando a garantia: como funcionava a máquina do Banco Master
chapeu: Compilação
assinatura: 30 de outubro de 2026 · **@guitorte**
---

<!--
COMO EDITAR
Este arquivo é o texto inteiro da página master/. Depois de mudar algo, rode na raiz do repositório:

    python3 ferramentas/dossie.py

e o master/index.html é refeito. O visual (cores, fontes, espaços) fica em assets/dossie.css.
O guia completo da marcação está em ferramentas/LEIA-ME.md. Resumo:

  # Parte                    agrupa seções no sumário
  ## Título {#id}            seção; o {#id} é o endereço do link (master/#id)
  ### Subtítulo              subseção
  **negrito**  *itálico*     ênfase
  [12]                       nota: número da referência da lista no fim
  `Etiqueta`                 etiqueta colorida; `Texto|tom` escolhe a cor
  [texto](#id)               link
  - item  /  1. item         listas
  > texto                    caixa de destaque
  :::fichas  ... :::         fichas; 1ª linha = título (+ `Etiqueta`), linhas "- Rótulo: texto";
                             uma linha em branco separa uma ficha da outra
  :::esteira ... :::         passos em sequência: título numa linha, texto na seguinte
  :::barras Título ... :::   barras: "rótulo | valor | largura em %"
  :::quadro Título ... :::   quadro-resumo do topo: "- Rótulo: texto"
  :::indice ... :::          atalhos para as fichas da seção (gerado sozinho)
  :::fluxo Título ... :::    diagrama: linhas apoio:, entrada:, centro:, saida: ("nome | descrição | seta")
  :::glossario ... :::       siglas, "SIGLA: definição"; o 1º uso em cada seção vira toque
  :::referencias ... :::     lista numerada "1. referência"
-->

:::quadro O caso em resumo
- [Liquidação](#cdb): 18 de novembro de 2025, decretada pelo Banco Central [10]
- [Prisão de Vorcaro](#cap-5): 17 de novembro de 2025 [54]
- [Pago pelo FGC](#cdb): cerca de R$ 40,6 bilhões a aproximadamente 800.000 investidores, o maior pagamento da sua história [4]
- [Compras do BRB](#cap-5): R$ 12,2 bilhões brutos, entre janeiro e junho de 2025 [48]
- [Fundos de previdência](#previdencia): 18 fundos, R$ 1,876 bilhão em Letras Financeiras sem cobertura do FGC [96]
- [Gastos de influência](#cap-4): R$ 0,40 a R$ 0,42 bilhão identificados, cerca de 1% do pago pelo FGC
- [Indiciados](#argumento): 15 pessoas no primeiro inquérito da PF, em 28 de outubro de 2026 [8]
- [Situação](#argumento): nenhuma alegação foi julgada em definitivo
:::

# Visão geral

## CDBs astronômicos {#cdb}

Em 2024, os Certificados de Depósito Bancário (CDBs) do Banco Master pagavam até 140% do CDI, chegando a 150% em algumas emissões, enquanto a média do mercado girava em torno de 100% a 107% [1]. Poupadores comuns os compravam por meio de grandes plataformas de investimento, como XP e BTG Pactual [2].

Eles não precisavam confiar no Master. O Fundo Garantidor de Créditos (FGC), financiado principalmente pelos seus bancos associados [5], cobria até R$ 250.000 por CPF ou CNPJ [3]. A taxa agressiva vinha do banco; a segurança vinha do fundo.

Quando o Banco Central decretou a liquidação extrajudicial do Master em 18 de novembro de 2025, o FGC devia cerca de R$ 40,6 bilhões a aproximadamente 800.000 investidores — o maior pagamento da sua história [4]. O recorde anterior, estabelecido pelo Banco Bamerindus em 1997, havia sido de R$ 19,6 bilhões [5].

## Tese resumida {#argumento}

O caso Master é melhor compreendido como uma *fraude de controle* (ou *control fraud*) estruturada sobre uma garantia de depósitos. Economistas utilizam o termo *"saque"* (*looting*): proprietários de uma instituição cujas obrigações são garantidas por terceiros obtêm mais lucro extraindo recursos líquidos e entrando em default do que administrando o negócio de forma sólida [6]. Nos casos examinados classicamente por Akerlof e Romer, o garantidor era usualmente o Estado [6]; aqui, era o FGC, abastecido majoritariamente pelos bancos concorrentes [5]. O saque requer duas condições essenciais: captação garantida e a capacidade de sustentar ativos contábeis inflados acima do seu valor real de mercado [7].

Sob essa ótica, os controladores do Master usaram o FGC para levantar poupança do varejo, inflaram o balanço patrimonial, drenaram o caixa e pagaram por tempo, blindagem e influência. Quando a liquidez minguou, tentaram transferir o buraco financeiro para o Banco de Brasília (BRB), instituição controlada pelo Governo do Distrito Federal. O dinheiro público já havia ingressado anteriormente por meio de regimes próprios de previdência social (RPPS) estaduais e municipais, que compraram papéis do Master desprovidos de cobertura do FGC [96]. Esta leitura constitui inferência analítica do autor a partir das apurações de órgãos reguladores, autoridades policiais e da administração da liquidação.

Nenhuma dessas alegações foi julgada em definitivo em tribunal. Em 28 de outubro de 2026, a Polícia Federal (PF) indiciou 15 pessoas em seu primeiro inquérito, sob suspeitas que incluem organização criminosa, lavagem de capitais e gestão fraudulenta [8]. Vorcaro nega qualquer fraude e classifica sua prisão como injusta [9].

> **Estabelecido:** O Banco Central liquidou o conglomerado em 18 de novembro de 2025, apontando grave crise de liquidez e violações severas das normas do Sistema Financeiro Nacional [10].
>
> **Alegado:** As operações fraudulentas, o desvio de caixa, os pagamentos ilícitos e a coação descritos adiante.
>
> **Desconhecido:** O momento exato em que se iniciou o dolo, quem de fato exercia o comando final, a totalidade das transferências e quanto das evidências digitais resistirá ao escrutínio judicial.

## O esquema em resumo {#maquina}

<!-- Diagrama traduzido da figura "the Master machine" do original em inglês (.docx). -->
:::fluxo Poupadores e fundos de pensão injetavam recursos; as perdas recaíram sobre o FGC, o BRB e os orçamentos públicos.
Funções da máquina conforme alegado pelos investigadores; nada foi julgado em tribunal.
Toque numa caixa para ir à seção correspondente.

apoio: [FGC](#custos) | pagou R$ 40,6 bi | garantia até R$ 250 mil
entrada: [Poupadores](#cap-1) | cerca de 800.000 investidores | CDBs até 140% do CDI
entrada: [Fundos de pensão](#previdencia) | 18 fundos estaduais e municipais | títulos e fundos, sem cobertura do FGC
centro: Banco Master | controlado por um grupo restrito
saida: [Blindagem](#cap-4) | agentes públicos, Congresso, advogados, mídia | pagamentos, cerca de R$ 0,4 bi identificados
saida: [Ativos inflados](#cap-2) | fundos, partes relacionadas, Reag
saida: [Extração](#cap-3) | empresas da família, Super
saida: [Saída: BRB](#cap-5) | carteiras questionadas
saida: [Coação (alegada)](#cap-6) | “A Turma”, milícia privada
:::

:::esteira
1. Poupadores do varejo (~800 mil investidores)
Atraídos por CDBs pagando até 140% do CDI, respaldados pela garantia do FGC até R$ 250 mil por CPF/CNPJ.

2. Fundos de pensão públicos (18 RPPS estaduais e municipais)
Aportaram em Letras Financeiras e fundos estruturados sem cobertura do FGC, em busca de retorno acima de 130% do CDI.

3. O núcleo: Banco Master
Instituição controlada por um grupo restrito, coordenando captação acelerada e operações cruzadas.

4. Ativos inflados
Circuitos estruturados via gestora Reag, carteiras de precatórios e empresas ligadas a sócios, mantendo papéis acima do valor de face.

5. Extração para veículos familiares
Desvios de caixa através de operações com a Super Empreendimentos, fundos (City, Navarra, Astralo 95) e entregas em espécie.

6. A blindagem (aproximadamente R$ 0,4 bilhão)
Pagamentos a agentes públicos, parlamentares, bancas de advocacia de influência e campanhas midiáticas para manter o esquema operando.

7. Coação (alegada)
Uso de grupo apelidado de "A Turma" para monitoramento e intimidação de desafetos, críticos e jornalistas.

8. A rota de saída: o BRB
Tentativa de transferência de ativos estressados/podres para o Banco de Brasília antes do colapso final.
:::

## Quem importava, e quanto {#atores}

Oito pessoas ou grupos operavam o motor da máquina, enquanto um punhado atuava sobre seus pontos de controle. A maioria dos nomes de grande notoriedade figura na periferia: evidenciam o alcance das relações do grupo, mas não explicam o funcionamento técnico da engrenagem.

A classificação adota o papel funcional documentado, e não grau de culpa, fama ou volume financeiro:

- `Central` Captou, inflou, movimentou ou desovou o dinheiro. Sem eles, o motor para.
- `Secundário` Atuou sobre um ponto de controle (fiscalização, regras da garantia, banco comprador ou contenção de críticos), sem integrar o motor.
- `Acessório` Contatos e despesas no entorno do motor, sem ato documentado que altere o curso dos fundos.

*Um pagamento mensal de R$ 500.000 a um supervisor hierarquiza-se acima de um filme de R$ 64 milhões, pois tocou um ponto crítico de controle. A leitura é vertical: quanto mais abaixo o nome se situa, menor seria o impacto de sua ausência sobre as origens e destinos do dinheiro.*

:::indice
:::

### Atores centrais

:::fichas
Daniel Vorcaro `Central`
- Papel atribuído (alegado): Comando geral do esquema, segundo o relatório da PF [62].
- Resposta: Nega qualquer prática fraudulenta e considera a prisão arbitrária e injusta [9].

Augusto Lima `Central`
- Papel atribuído (alegado): Sócio; integrou o núcleo executivo-financeiro; apontado pela PF como arquiteto das carteiras simuladas [62][46].
- Resposta: Nega as irregularidades apontadas [46].

Fabiano Zettel `Central`
- Papel atribuído (alegado): Pivô financeiro: recebeu R$ 485 milhões através da Super Empreendimentos [27].
- Resposta: Não localizada manifestação nos autos públicos.

Antonio Carlos Freixo Jr. (Entre) `Central`
- Papel atribuído (alegado): Gerou aproximadamente R$ 1,3 bilhão em espécie para Vorcaro entre 2020 e 2025 e remeteu US$ 12,3 milhões para a Havengate, segundo delação premiada homologada [84].
- Resposta: Declarou que o acordo de colaboração foi estritamente voluntário [84].

João Carlos Mansur (Reag) `Central`
- Papel atribuído (alegado): Circuitos de fundos de investimento que viabilizaram R$ 11,5 bilhões em operações irregulares, segundo o Banco Central [18][19].
- Resposta: Delação assinada sob apreciação [67]; refuta enfaticamente vínculos com facções criminosas [23].

André Maia e Henrique Peretto (Tirreno, Cartos) `Central`
- Papel atribuído (alegado): Origem das carteiras de crédito sob suspeita de simulação [82]; Maia foi formalmente indiciado [83].
- Resposta: A Cartos afirmou que nunca manteve operações ativas com o Banco Master [82].

Paulo Henrique Costa (BRB) `Central`
- Papel atribuído (alegado): Viabilizou a aquisição das carteiras pelo BRB; colocado pela PF no núcleo estratégico com Vorcaro [50]; suspeito de receber entre R$ 140 milhões e R$ 146,5 milhões [49][87].
- Resposta: Sustenta que as operações não acarretaram prejuízo ao BRB [87].

Henrique Vorcaro e veículos familiares `Central`
- Papel atribuído (alegado): Estruturas de desvio patrimonial através das empresas City, Navarra e fundo Astralo 95; R$ 2,2 bilhões teriam sido ocultados de credores [26][29][89].
- Resposta: Não localizada manifestação nos autos públicos.
:::

### Atores secundários

:::fichas
Ex-fiscais / supervisores do Banco Central `Secundário`
- Papel atribuído (alegado): Recebimento de pagamentos periódicos em troca de informações privilegiadas e proteção institucional, segundo a PF [31].
- Resposta: Não localizada manifestação pública.

Senador Ciro Nogueira (PP) `Secundário`
- Papel atribuído (alegado): Repasses mensais sistemáticos; apresentação de emenda legislativa para ampliar o teto do FGC redigida internamente no Master [33][55].
- Resposta: Rejeita qualquer prática ilícita ou favorecimento indevido [40].

Ibaneis Rocha (então governador do DF) `Secundário`
- Papel atribuído (alegado): Chefe político do acionista controlador do BRB; Costa afirmou à PF que o governador detinha ciência plena das movimentações; não indiciado [85].
- Resposta: Declarou total desconhecimento de fraudes até a decretação da liquidação [86].

Cláudio Castro (então governador do RJ) `Secundário`
- Papel atribuído (alegado): Alinhamento político para viabilizar aportes de ~R$ 3 bilhões do Rioprevidência em títulos e fundos ligados ao Master; viagens e jantar em NY pagos por Vorcaro, segundo a PF [99][100][101].
- Resposta: Nega relacionamento impróprio; alega que os investimentos seguiram critérios técnicos e que não houve custeio pessoal de viagens [102].

Diretores e gestores do Rioprevidência `Secundário`
- Papel atribuído (alegado): Aprovação de alocações bilionárias em desconformidade com o histórico conservador da carteira previdenciária, segundo a PF [103].
- Resposta: A fundação negou irregularidades [98] e informou a recuperação administrativa de R$ 1,4 bilhão [106].

Nelson Tanure `Secundário (central se provado)`
- Papel atribuído (alegado): Suspeita de aportes de capital ocultos via debêntures conversíveis no montante superior a R$ 700 milhões [63].
- Resposta: Nega enfaticamente qualquer participação acionária direta, indireta ou por debêntures [65].

“A Turma” `Secundário`
- Papel atribuído (alegado): Ações de inteligência privada, espionagem de críticos e tentativas de coerção física/moral [58].
- Resposta: A defesa de Vorcaro contesta a existência fática da referida estrutura [61].

Mídia e influenciadores digitais `Secundário`
- Papel atribuído (alegado): Contratação coordenada de ataques institucionais contra diretores do Banco Central; repasse de R$ 51,9 milhões ao portal Metrópoles [35][37].
- Resposta: Publicitário interrogado confirmou a liquidação de pagamentos a influenciadores [37].
:::

### Atores acessórios

:::fichas
Escritório Barci de Moraes `Acessório`
- Papel atribuído (alegado): Contrato de assessoria jurídica somando R$ 80 milhões em 22 parcelas mensais [34].
- Resposta: A banca sustenta a efetiva e regular prestação de serviços jurídicos complexos; a PF não apontou conduta ilícita imputável ao ministro do STF ou à sua esposa [34][41].

Ministro Dias Toffoli (STF) `Acessório`
- Papel atribuído (alegado): Aportes e fluxos de R$ 20 a 35 milhões direcionados a empreendimento hoteleiro (Tayayá) no qual empresa familiar possuía participação societária [71][72].
- Resposta: Nega recebimento de recursos de Vorcaro ou Zettel [71]; ministros da corte classificaram as ilações do relatório como "lixo jurídico" [73].

Ministro Nunes Marques (STF) `Acessório (secundário se mantido elo com votos)`
- Papel atribuído (alegado): Repasse de R$ 6,6 milhões à consultoria que remunerou seu filho; custeio de estadia de Carnaval de R$ 1,45 milhão a "KN"; mensagens sugerindo elo com julgamento de usina ligado a precatórios do Master [74][76].
- Resposta: Nega ter atuado em causas de interesse do Master ou que seu filho tenha recebido verbas do banco [74]; afirma que jamais solicitou contrapartidas a Vorcaro [75].

Procurador-geral da República Paulo Gonet `Acessório`
- Papel atribuído (alegado): Interlocução social mediada por terceiros; ausência de qualquer indício de vantagens financeiras nos autos [78].
- Resposta: Nega intimidade pessoal; Conselho Superior do MPF arquivou apuração preliminar por 5 a 4 [77].

Senador Flávio Bolsonaro (PL) `Acessório`
- Papel atribuído (alegado): Articulação de captação privada para o filme *Dark Horse*; remessa internacional de US$ 12,3 milhões mapeada na Operação Crédito Oculto [84][79].
- Resposta: Qualifica a captação audiovisual como atividade legítima de patrocínio privado [79].

Campanhas eleitorais de 2022 `Acessório`
- Papel atribuído (alegado): Aportes classificados como repasses ilícitos de campanha em proposta de delação rejeitada pelo MPF [38].
- Resposta: Candidatos e legendas citadas rechaçam categoricamente as suspeitas [38].

Nikolas Ferreira, Hugo Motta e Jaques Wagner `Acessório`
- Papel atribuído (alegado): Pedidos pontuais de apoio institucional, comparecimento a eventos e ingressos/cortesias [81][27][21].
- Resposta: Ferreira declarou nunca ter auferido recursos do grupo [81]; outros nomes mantiveram esclarecimentos no âmbito parlamentar.
:::

*Ressalva jurídica: Todas as categorias descritas fundamentam-se em inquéritos policiais e delações ainda não submetidas ao crivo final do contraditório judicial.*

# Como o esquema funcionava

## 1. Captação: alugando a credibilidade do FGC {#cap-1}

A estrutura de captação do Banco Master apoiava-se deliberadamente na garantia do FGC por concepção original. O próprio Daniel Vorcaro declarou à Polícia Federal que o plano de negócios submetido ao Banco Central em 2018 era estritamente amarrado aos limites de garantia do fundo, definindo-o como as "regras do jogo" vigentes [11].

A anomalia chamou a atenção da Comissão de Valores Mobiliários (CVM). O presidente interino da autarquia destacou que um dos primeiros focos de inquietação do mercado foi a utilização ostensiva do FGC pelo banco como alavanca agressiva de funding [12].

Contudo, nem todos os recursos contavam com o colchão do seguro. Dezoito fundos de previdência de servidores públicos estaduais e municipais aplicaram R$ 1,876 bilhão em Letras Financeiras (LFs) emitidas pelo Master — títulos bancários que, por determinação legal, não possuem nenhuma cobertura do FGC [96].

O balanço patrimonial da instituição inflou em velocidade incomum: o patrimônio líquido saltou de R$ 219 milhões em 2021 para R$ 4,7 bilhões em 2024, ano em que o conglomerado divulgou publicamente um lucro líquido contábil de R$ 1 bilhão [13]. As apurações técnicas posteriores colocaram em dúvida a fidedignidade desses números.

A dinâmica matemática revelou-se insustentável. Conforme a PF, a emissão massiva de novos CDBs era consumida para honrar amortizações e juros de aplicadores anteriores, em um mecanismo assemelhado à arquitetura de pirâmide financeira [14]. Uma nota técnica do Banco Central situou o colapso estrutural em novembro de 2024, quando a receita dos ativos do banco perdeu a capacidade de cobrir a remuneração das emissões de CDBs em circulação [15].

## 2. Inflando o balanço {#cap-2}

A segunda função da máquina consistia em atribuir aos ativos da instituição valores fictícios, bastante superiores aos de liquidação. Relatórios da CVM apontam que indícios de triangulação já apareciam desde 2020: ativos eram transferidos de um fundo para outro com sobrepreços e remarcações acentuadas sem justificativa de mercado [12].

Investigação da autarquia apurada pelo *Estadão* revelou que, entre 2022 e 2025, o Master aportou cerca de R$ 2,1 bilhões em dez sociedades empresariais desprovidas de suporte operacional ou capacidade patrimonial que justificasse as avaliações [16]. Peritos constataram também mais de R$ 3,5 bilhões aplicados em fundos administrados pelo próprio Master, dos quais R$ 1,8 bilhão estava lastreado em notas emitidas por empresas ligadas aos sócios [17]. Empréstimos concedidos a essas companhias retornavam à tesouraria do banco sob a forma de compra dos seus próprios CDBs [17].

Nesse ecossistema, a gestora Reag exerceu papel fulcral. O Banco Central informou formalmente ao Tribunal de Contas da União (TCU) que fundos sob gestão da Reag estruturaram esquemas fraudulentos com o Master entre julho de 2023 e julho de 2024 [18], perfazendo um montante suspeito de R$ 11,5 bilhões [19].

Recursos circulavam em questão de minutos através de carteiras geridas pelas mesmas partes, desembocando em papéis de baixíssima liquidez ou desprovidos de valor econômico real — tais como antigas debêntures e títulos do extinto Banco do Estado de Santa Catarina (Besc) [20]. Em sua colaboração, o fundador da Reag, João Carlos Mansur, admitiu que a gestora operava a serviço das demandas do Master desde 2019 [21].

A Reag também entrou na mira da Operação Carbono Oculto, apuração voltada à lavagem de capitais do Primeiro Comando da Capital (PCC), suspeita de branquear até R$ 1 bilhão para a organização criminosa [22]. Mansur rechaçou peremptoriamente qualquer envolvimento com o crime organizado [23].

Nem todas as carteiras eram destituídas de valor. O banco mantinha um volume representativo de precatórios federais e estaduais [2]. Mais tarde, quando tais ativos foram repassados ao BRB, a carteira de crédito consignado Credcesta foi marcada contabilmente com ágio de 45% acima do valor lançado no Master, ao passo que operações de crédito ligadas à Oncoclínicas sofreram baixa de 52% [24].

## 3. Extração: do banco para a família {#cap-3}

A terceira engrenagem voltava-se ao dreno financeiro: transferir a liquidez captada no mercado financeiro para as esferas pessoais de Vorcaro, de parentes e de sócios [25].

O caso com documentação mais detalhada antecedeu a fase crítica de iliquidez. Em 2022, o fundo City, estruturado em torno do Master, pagou R$ 419,9 milhões a empresas vinculadas à família de Vorcaro em troca de direitos creditórios com promessa de recebimento de R$ 798 milhões [26]. O liquidante judicial constatou posteriormente que esses créditos careciam de lastro [26].

Em julho de 2025, o City alienou a totalidade desse pacote à empresa Navarra por R$ 776,9 milhões. O liquidante apurou que o beneficiário econômico da Navarra era o próprio Daniel Vorcaro, através dos fundos Lunar e Astralo 95 [26]. A manobra serviu para camuflar o endividamento do núcleo familiar perante os balanços contábeis [26].

O fluxo de desvios passou sistematicamente pela empresa Super Empreendimentos e Participações. O cunhado de Vorcaro, Fabiano Zettel, recebeu R$ 485 milhões dessa firma entre julho de 2022 e janeiro de 2026; a PF o descreve como figura-chave na tesouraria oculta do grupo [27]. Uma entidade investigada na Operação Carbono Oculto também transferiu R$ 180 milhões à Super [28].

Conforme as autoridades, a blindagem patrimonial prosseguiu mesmo após as primeiras ordens cautelares: ao ter a prisão inicialmente revogada, Vorcaro teria movimentado R$ 2,2 bilhões de credores para conta controlada por seu pai [29]. O Ministério Público Federal em São Paulo sustenta a operação contínua de organização criminosa montada desde meados da década passada; a defesa sustenta que nenhuma movimentação beneficiou ilegalmente parentes ou terceiros [30].

A evasão em espécie atingiu montantes recordes. Antonio Carlos Freixo Jr., titular da Entre Investimentos, afirmou em acordo de delação homologado ter disponibilizado cerca de R$ 1,3 bilhão em papel-moeda vivo a Vorcaro entre 2020 e 2025 [84].

Em março de 2026, a 1ª Vara de Falências de São Paulo determinou o bloqueio patrimonial da Astralo 95 e fundos correlatos, registrando transações atípicas antes do decreto de liquidação, incluindo a drenagem de R$ 285,8 milhões [89]. No exterior, a massa liquidanda move ações nos tribunais dos EUA para reaver uma cobertura avaliada em US$ 25,8 milhões em Miami transferida à ex-esposa em 2024 [90] e obteve a suspensão cautelar da alienação de uma mansão de US$ 32 milhões na Flórida [91].

## 4. A blindagem: comprando tempo, regras e reputação {#cap-4}

Os desembolsos identificados até o momento em favor de autoridades públicas, lideranças políticas, escritórios de advocacia de grande porte e empresas de comunicação totalizam entre **R$ 0,40 bilhão e R$ 0,42 bilhão** — montante equivalente a cerca de 1% do rombo assumido pelo FGC (cálculo discriminado abaixo). O valor monetário representava custo operacional de proteção: as transferências visavam atingir exatamente os centros de decisão que possuíam prerrogativa para frear as operações ou ampliar as fontes do banco.

### Pagamentos e desembolsos mapeados

:::fichas
Ex-chefe de fiscalização do Banco Central `Supervisão|secundario`
- Montante apurado: Pagamentos mensais recorrentes de R$ 500.000.
- Origem da evidência: Relatório circunstanciado da Polícia Federal [31].

Agentes e ex-agentes da Polícia Federal `Inteligência|secundario`
- Montante apurado: Repasses periódicos de até R$ 400.000 mensais.
- Origem da evidência: Inquéritos da própria Corregedoria e PF [32].

Senador Ciro Nogueira (PP) `Congresso|secundario`
- Montante apurado: Entre R$ 300.000 e R$ 500.000 mensais; R$ 18,85 milhões bloqueados por ordem judicial.
- Origem da evidência: Relatórios da PF e quebras de sigilo bancário [33].

Escritório Barci de Moraes `Advocacia|acessorio`
- Montante apurado: R$ 80 milhões pactuados em 22 parcelas (fev/2024 a nov/2025).
- Origem da evidência: Declarações contábeis e fiscais do Banco Master [34].

Estrutura societária do Tayayá Resort `Judiciário / família|acessorio`
- Montante apurado: De R$ 20 milhões a R$ 35 milhões.
- Origem da evidência: Interceptações de diálogos entre Vorcaro e Zettel [71][72].

Consult Consultoria (ligada ao filho de Nunes Marques) `Judiciário / Vínculo|acessorio`
- Montante apurado: R$ 6,6 milhões (ago/2024 a jul/2025).
- Origem da evidência: Relatórios de Inteligência Financeira do Coaf [74].

Hospedagem de Carnaval 2025 ("KN") `Custeio|acessorio`
- Montante apurado: Aproximadamente R$ 1,45 milhão.
- Origem da evidência: Troca de mensagens vinculando a sigla ao ministro [76].

Portal de notícias Metrópoles `Imprensa|secundario`
- Montante apurado: R$ 51,9 milhões.
- Origem da evidência: Mensagens apreendidas pela PF e alertas do Coaf [35].

Site Diário do Centro do Mundo (DCM) `Imprensa|secundario`
- Montante apurado: R$ 50.000 mensais para cessar notas desfavoráveis.
- Origem da evidência: Relatório de mensagens da PF [36].

Criadores de conteúdo / influenciadores `Redes sociais|secundario`
- Montante apurado: Propostas de até R$ 2 milhões por pacote.
- Origem da evidência: Depoimento formal de intermediário de publicidade [37].

Campanhas eleitorais de 2022 `Eleitoral|acessorio`
- Montante apurado: R$ 5 milhões oficiais + R$ 10 milhões em espécie.
- Origem da evidência: Anexo de delação preliminar de Vorcaro [38].

Produção do filme "Dark Horse" (biopic de Jair Bolsonaro) `Audiovisual|acessorio`
- Montante apurado: US$ 12,3 milhões (~R$ 64 milhões).
- Origem da evidência: Colaboração de Freixo; autos da Operação Crédito Oculto [84][39].

Ingressos para senador Jaques Wagner (PT) `Cortesias|acessorio`
- Montante apurado: R$ 63.300 em ingressos de espetáculos.
- Origem da evidência: Termo de colaboração de Mansur [21].

Cláudio Castro (governador do RJ) `Poder Executivo|secundario`
- Montante apurado: Despesas de viagens internacionais e jantar em NY de US$ 13.000 (R$ 66 mil).
- Origem da evidência: Relatórios policiais de interceptação telemática [100][101].
:::

Todos os mencionados refutam com veemência a existência de contrapartidas espúrias. A defesa de Ciro Nogueira nega conduta imprópria [40]. O escritório Barci de Moraes demonstrou ter emitido notas fiscais, atuado em centenas de contenciosos do banco e que a PF não imputou crimes aos sócios [34][41]. O gabinete de Toffoli informou que sua família retirou-se do condomínio hoteleiro em fevereiro de 2025 [71]. Nunes Marques afirmou que nunca julgou demandas favoráveis ao banco e que seu filho recebeu R$ 281.600 por assessoria tributária específica da Consult [74].

Divergências contratuais figuram nos autos: veículos de imprensa apontam contratos de advocacia totalizando até R$ 208 milhões [42] ou R$ 180 milhões [43]. Flávio Bolsonaro, alvo de inquérito aberto pelo STF, afirmou que o apoio a produções culturais segue os ditames estritamente privados [79]. No campo governista, Augusto Lima, ex-sócio de Vorcaro, possuía comprovada interlocução política com dirigentes petistas na Bahia [44].

A penetração institucional operava também em encontros de hospitalidade. Vorcaro promovia jantares para senadores e deputados — como Ciro Nogueira e o deputado Hugo Motta — em mansão de R$ 36 milhões em Brasília registrada pela Super Empreendimentos (a qual seu gabinete afirmou ter alugado) [27]. O PGR Paulo Gonet figurou em trocas de mensagens informais via terceiros tratando de degustações, sem indício de transferências; o Conselho Nacional do MPF arquivou o caso [77][78].

> **Aritmética dos gastos de influência:**
>
> A somatória identifica R$ 140–146,5 mi atribuídos ao ex-presidente do BRB; R$ 80 mi em contratos de advocacia; R$ 64 mi na produção audiovisual; R$ 51,9 mi em portais de mídia; R$ 20–35 mi na estrutura do resort; R$ 18,85 mi bloqueados de liderança partidária; R$ 15 mi em doações eleitorais declaradas/alegadas; R$ 6,6 mi na consultoria e R$ 1,45 mi no Carnaval. Total consolidado: **R$ 0,40 a R$ 0,42 bilhão** (~1% dos R$ 40,6 bilhões pagos pelo FGC). Adicionando-se os R$ 485 milhões cursados por Zettel (com sobreposições parciais), atinge-se cerca de 2% do total.

## 5. A saída: o BRB e a própria garantia {#cap-5}

À medida que a captação de CDBs esfriava em 2024, a estratégia do banco mudou de orientação: em vez de apenas extrair valor, buscou repassar o rombo acumulado a um terceiro com bolsos fundos. A rota de saída desenhada foi o BRB, instituição pública do Distrito Federal.

### Carteiras simuladas

As transações com o BRB ganharam corpo no segundo semestre de 2024 [45]. Os créditos comercializados derivaram da empresa de fachada Tirreno, fundada em dezembro de 2024 e controlada pelo grupo Cartos [46]. O Master apropriou-se dos recebíveis da Tirreno sem efetuar desembolsos e os revendeu na sequência ao banco estatal [47].

Entre janeiro e junho de 2025, o BRB adquiriu R$ 6,7 bilhões dessas carteiras, agregando um ágio contratual de R$ 5,5 bilhões — perfazendo R$ 12,2 bilhões brutos [48]. O relatório da PF estima que o volume total de repasses do BRB para o Master alcançou R$ 17 bilhões [46].

### Dentro do BRB

Conforme os autos, a cúpula do BRB foi formalmente alertada pelos órgãos internos de controle técnico a respeito de inconsistências graves, mas chancelou os negócios [45]. O ex-presidente do banco estatal, Paulo Henrique Costa, é apontado pela PF como destinatário de repasses imobiliários de R$ 140 milhões a R$ 146,5 milhões coordenados por Vorcaro [49][87], integrando o núcleo decisório da operação [50]. Costa afirmou categoricamente não haver evidências de podridão prévia das carteiras [48].

Em oitiva, Costa declarou que o governador Ibaneis Rocha acompanhava passo a passo a saúde financeira da instituição [85]. Ibaneis, que não foi indiciado, reiterou que ignorava as fraudes e atribuiu os atos integralmente à diretoria técnica [86].

### O swap e o rombo efetivo

Com o estrangulamento das operações, aproximadamente R$ 10 bilhões em ativos foram devolvidos ao Master em troca de outros créditos e precatórios, restando R$ 2,6 bilhões inteiramente a descoberto, o que obrigou o Banco Central a exigir provisionamento de 100% pelo BRB [51]. O corpo técnico do BC calcula que a perda final consolidada do BRB ultrapasse R$ 5 bilhões [52]. Os R$ 12,2 bilhões representam a face de negociação, não o prejuízo líquido apurado.

### A tese da defesa

Vorcaro sustenta que as transações não infligiram danos ao patrimônio do BRB, argumentando que entregou ativos reais em substituição com desconto substancial, reivindicando perícia contábil independente [9]. Ele atribui a crise de liquidez do BRB aos desdobramentos açodados das operações ostensivas da PF [88].

### A tentativa de fusão

Documentos judiciais evidenciam que a aquisição societária do Master pelo BRB visava diluir as carteiras fictícias no bojo de uma instituição financeira de grande porte [53]. A operação foi vetada pela Diretoria Colegiada do Banco Central no início de setembro de 2025 [54].

### A própria garantia: mudança no FGC

A PF revelou que a assessoria do Master redigiu a minuta de uma emenda legislativa para quadruplicar o limite máximo de garantia individual do FGC de R$ 250.000 para R$ 1.000.000 por correntista. O texto foi entregue ao gabinete do senador Ciro Nogueira e protocolado integralmente sem supressões [55]. Em gravações, Vorcaro jactou-se de que a alteração "saiu sob encomenda", com potencial de multiplicar por seis a capacidade de captação do banco [56].

### O desfecho

Vorcaro foi detido pela Polícia Federal na noite de 17 de novembro de 2025 [54]. Investigadores informaram à imprensa que sua aeronave particular preparava decolagem rumo a Malta e que o anúncio formal de venda do controle ao Grupo Fictor foi uma encenação para disfarçar a rota de fuga [57].

## Fundos públicos de pensão: combustível, depois um estacionamento {#previdencia}

Os regimes próprios de previdência forneceram capital sem qualquer garantia em duas ondas bem demarcadas: primeiro, como combustível estável de longo prazo; mais tarde, quando a máquina perdeu o compasso, funcionaram como local para depositar papéis depreciados. Constituíram provedores involuntários de liquidez, não o alvo primordial da fraude.

Dezoito dos 2.130 fundos de previdência de estados e municípios do país destinaram R$ 1,876 bilhão à compra de Letras Financeiras do Master entre outubro de 2023 e dezembro de 2024 [96]. As maiores exposições envolveram o Rioprevidência do Rio de Janeiro (R$ 970 milhões), o Amapá Previdência (R$ 400 milhões) e a previdência municipal de Maceió (R$ 97 milhões) [96], atraídos por retornos anunciados de 130% do CDI [98].

:::fichas
Fase 1: out/2023 a jul/2024 `Combustível`
- Onde alocaram: Títulos de Letras Financeiras do próprio banco; papéis do Rio com vencimento estendido para 2033–2034 [96][97].
- Função na máquina: Fornecimento de liquidez sem demanda de resgate por até 10 anos consecutivos.

Fase 2: dez/2024 a out/2025 `Depósito de ativos`
- Onde alocaram: R$ 2,01 bilhões do Rioprevidência injetados em fundos fechados estruturados sob o mesmo controle, contornando travas do CMN [103].
- Função na máquina: Estacionamento e absorção de papéis de liquidez duvidosa após a exaustão da captação primária.

Fase 3: outubro de 2025 `A manobra BRB`
- Onde alocaram: Proposta de permuta das LFs do Rioprevidência por cotas de fundos e direitos creditórios sob lema flagrado: *"Faremos o mesmo em Maceió"* [105].
- Função na máquina: Despejo emergencial de obrigações das contas do banco para os fundos previdenciários às vésperas da intervenção.
:::

### Por que os títulos eram bom combustível?

Um mecanismo que liquida passivos antigos mediante entrada contínua de recursos novos [14] depende de capital paciente, que não realize resgates antecipados. Fundos previdenciários operam em horizontes decenais, movimentam centenas de milhões em assinaturas concentradas e prescindem da trava de R$ 250 mil do FGC, decididos por colegiados reduzidos de diretores politicamente indicados.

### Onde as perdas surgiram

Nos veículos finais, a perda incidiu diretamente no patrimônio dos servidores. Em julho de 2026, a Procuradoria-Geral do Estado do Rio de Janeiro ajuizou ações cíveis buscando recuperar R$ 641,4 milhões. A PGE vinculou R$ 135,1 milhões a operações de especulação com ações da Ambipar e R$ 481,4 milhões a alterações estatutárias nos fundos que suprimiram direitos políticos dos cotistas públicos e prorrogaram a liquidação em mais quatro anos [106].

O Rioprevidência declarou ter resgatado administrativamente R$ 1,4 bilhão de fundo gerido pelo Master em dezembro de 2025 [106]. Seus R$ 970 milhões em títulos de LF permanecem na fila retardatária de credores quirografários da liquidação [104].

### Rioprevidência e Cláudio Castro

A PF fixou o comprometimento total do instituto do Rio entre R$ 3 bilhões e R$ 3,6 bilhões durante o governo Castro [98][99]. Eucherio Lerner Rodrigues assumiu a Diretoria de Investimentos em 4 de outubro de 2023, mesmo dia em que o Banco Master deu entrada formal no pedido de credenciamento financeiro no fundo [103].

O Tribunal de Contas do Estado (TCE-RJ) apurou mais de R$ 2,6 bilhões expostos (ultrapassando 25% de toda a reserva previdenciária estadual), sendo cerca de R$ 1 bilhão aportado após alertas expressos emitidos em maio de 2025 [98]. O órgão proibiu novas alocações em 8 de outubro de 2025 [105].

Peritos transcreveram diálogos mencionando que os aportes refletiam "alinhamento político" com o governador, cronogramas de jantares e custeio de diárias no exterior [99][100], incluindo a conta de US$ 13.000 em restaurante nova-iorquino em maio de 2023 paga por Vorcaro [101]. O ministro André Mendonça considerou o acervo indiciário "consistente e robusto", autorizando busca e apreensão contra Castro em 26 de maio de 2026 [99][98]. Castro reitera que os contatos foram protocolares, que jamais integrou o comitê de investimentos e que o banco não pagou suas viagens [102].

## 6. Coação: “A Turma” (alegada, contestada) {#cap-6}

A PF e despachos judiciais do ministro relator André Mendonça descrevem a estruturação de um aparato coercitivo informal e miliciano operando em favor de Daniel Vorcaro, orçado em aproximadamente R$ 1 milhão mensal [58]. A rede teria obtido acessos ilegais a bancos de dados sigilosos da PF, Interpol e FBI com o objetivo de vigiar jornalistas independentes, agentes fiscais e ex-empregados, conspirando inclusive para simular um roubo com agressão física com o intuito de intimidar um profissional de imprensa [58].

A composição envolveria ex-policiais, milicianos e agentes do jogo do bicho, contando com aportes de R$ 400.000 mensais repassados pelo pai do banqueiro [59]. O chefe operacional do grupo teria recebido R$ 24 milhões ao longo do período apurado [60]. Os advogados do banqueiro protocolaram requerimentos exigindo que a PF comprove pericialmente a existência física da referida milícia [61].

Essa camada elucida o *modus operandi* de coação do grupo, embora não altere os canais de circulação monetária do esquema financeiro.

# O dinheiro

## De onde veio o dinheiro {#origens}

A maior fatia dos recursos do Banco Master originou-se de cidadãos comuns adquirindo CDBs garantidos pelo FGC: aproximadamente dois terços do total de R$ 76 a R$ 86 bilhões mapeados. O BRB respondeu por um quinto; fundos de pensão, patrimônio contábil e dívida subordinada completaram o quadro.

:::barras Participação das fontes de recursos (R$ bilhões)
Depósitos (majoritariamente CDBs / FGC) | R$ 49,3–59,7 bi (65–69%) | 68
Aquisições de carteira pelo BRB | R$ 17,0 bi (20–22%) | 21
Patrimônio líquido declarado (dez/24) | R$ 4,7 bi (5–6%) | 6
Rioprevidência (fundos estruturados) | R$ 2,0 bi (2–3%) | 3
18 fundos de pensão (LFs não cobertas) | R$ 1,9 bi (2%) | 2.5
Dívida subordinada elegível a capital | R$ 0,9 bi (1%) | 1.5
:::

**Divergência contábil:** O Master publicou em dezembro de 2024 um volume de funding institucional de R$ 49,3 bilhões e ativo total de R$ 63 bilhões [115]. Os registros compilados pelo DIEESE no IFData do Banco Central registravam volume sensivelmente maior em depósitos [114]. Essa disparidade reflete a consolidação exclusiva do banco versus o ecossistema coligado. Parte das captações decorria de autofinanciamento: empréstimos concedidos a empresas aliadas regressavam à tesouraria para recompor CDBs [17].

### Os quatro motores da captação

1. **A garantia:** A proteção individual de R$ 250.000 do FGC neutralizava o apetite a risco do aplicador. O correntista não precisava atestar a solidez do Master: a aposta era transferida para a blindagem do sistema [3].
2. **A taxa:** Rendimentos agressivos de até 140% do CDI em prazos de até cinco anos — frente a ofertas médias de 100% dos grandes bancos de varejo [116].
3. **A força de vendas das corretoras:** Relatórios de mercado estimam vendas acumuladas de R$ 26 bilhões pela plataforma XP, R$ 6,7 bilhões pelo BTG Pactual e R$ 2,9 bilhões via Easynvest [116]. Agentes autônomos recebiam comissões antecipadas de cerca de 1,5% em papéis de cinco anos, contra 0,6% em emissões curtas. A XP afirmou que o comissionamento médio habitual situa-se em 0,3% ao ano [116].
4. **O ritmo de crescimento:** O volume depositado dobrou anualmente entre 2021 e 2024, acumulando avanço de sete vezes [114]. Cerca de 98% compunha-se de depósitos a prazo, comparado a 56–68% na média do SFN [114].

As fontes alimentaram o sistema em escada sequencial: o varejo sustentou o ciclo inicial de 2021 a 2024 [114]; os fundos públicos ingressaram no final de 2023 [96][103]; e a injeção do BRB surgiu a partir de 2024 para cobrir a esteira de vencimentos das primeiras rodadas de CDBs [46].

No desenlace, os CDBs garantidos formavam a maior dívida do Master: o FGC arcou com R$ 40,6 bilhões [4], cerca de dois terços dos R$ 59,6 bilhões apurados no balanço de março de 2025 pelo IFData [114].

## Quem pagou, e como {#custos}

A existência do FGC transmitia a impressão de que o custo da falência seria inteiramente privado. Na prática, a conta distribuiu-se de forma difusa entre correntistas de todos os bancos do país, os contribuintes do Distrito Federal e os servidores e orçamentos de 18 municípios e estados.

:::fichas
Poupadores até R$ 250.000 (~800.000 credores)
- O que ocorreu: Reembolsados pelo FGC a partir de janeiro de 2026; atualização dos juros cessou formalmente no ato da decretação de liquidação [4][110].
- Quem paga o prejuízo: Parcialmente ressarcidos, suportando a perda da rentabilidade contratada no período.

Poupadores e empresas acima do teto / títulos sem seguro
- O que ocorreu: Inscritos na fila de credores quirografários da massa falida, após os créditos trabalhistas e fiscais prioritários [111].
- Quem paga o prejuízo: Os próprios credores e correntistas.

Cotistas de fundos imobiliários administrados
- O que ocorreu: Cerca de R$ 610 milhões bloqueados em três FIIs suspensos para negociação [95].
- Quem paga o prejuízo: Os próprios cotistas do varejo, aguardando assembleias judiciais.

Clientes do Will Bank e Banco Pleno
- O que ocorreu: Garantidos e ressarcidos pelo FGC em volumes de R$ 6,3 bilhões e R$ 4,9 bilhões, respectivamente [108].
- Quem paga o prejuízo: Reembolsados pelo fundo garantidor.

Fundos de pensão de servidores públicos (RPPS)
- O que ocorreu: LFs desprovidas de cobertura do FGC; pela Lei Federal 9.717/1998, déficits atuariais de aposentadoria devem ser cobertos pelo tesouro estadual/municipal [97].
- Quem paga o prejuízo: Orçamentos públicos de estados e municípios (contribuintes de serviços e cidadãos em geral).

O Distrito Federal (via BRB)
- O que ocorreu: Provisionamento compulsório de R$ 2,6 bilhões exigido pelo BC [51]; aprovação legislativa de capitalização de até R$ 6,6 bilhões oferecendo 9 imóveis públicos como lastro [107].
- Quem paga o prejuízo: População e patrimônio imobiliário do Distrito Federal.

Clientes bancários e tomadores de crédito em geral
- O que ocorreu: FGC exigiu dos bancos associados a antecipação de cinco anos de contribuições (R$ 32,5 bilhões) para recompor reservas [108].
- Quem paga o prejuízo: Os bancos do sistema e, por repasse de spread bancário, os tomadores de empréstimos [109].

Pessoas cujos nomes foram usados em contratos falsos
- O que ocorreu: Emissão de consignados fraudulentos em nome de cidadãos que nunca solicitaram crédito, atingindo professores da Bahia e PMs do DF [112][113].
- Quem paga o prejuízo: Vítimas lesadas patrimonialmente e moralmente no sistema de crédito.
:::

# Provas e lacunas

## Onde as leituras divergem {#divergencias}

Duas teses fundamentais permanecem em aberto nos tribunais:

### 1. Quando começou o dolo?

- **Hipótese A:** O banco foi desenhado especificamente para extrair patrimônio desde 2019.
- **Hipótese B:** Tratava-se de um modelo agressivo e arriscado que descambou para a fraude quando o aperto de liquidez tornou-se insolúvel.

:::fichas
Sobrepreços de cotas de fundos mapeados desde 2020 `Aponta para: A`
- Fonte: Apurações da CVM [12].

Fundo City pagou R$ 419,9 mi a empresas familiares em 2022 `Aponta para: A`
- Fonte: Registros da CVM e relatórios do liquidante [26].

Reag operando a serviço do Master desde 2019 `Aponta para: A`
- Fonte: Termo de delação de João Carlos Mansur [21].

Estrutura criminosa articulada desde a década passada `Aponta para: A`
- Fonte: Parecer do Ministério Público Federal (SP) [30].

Carteira Credcesta marcada pelo BRB 45% acima da avaliação `Aponta para: B`
- Fonte: Relatório de precificação do BRB [24].

Ruptura definitiva datada pelo Banco Central em nov/2024 `Aponta para: B`
- Fonte: Nota Técnica do Banco Central [15].

Empresa de fachada Tirreno aberta apenas em dez/2024 `Aponta para: B (escalada tardia)`
- Fonte: Inquérito da Polícia Federal [46].

Vorcaro sustenta entrega de ativos próprios com deságio `Aponta para: B`
- Fonte: Manifestações da defesa do banqueiro [9].
:::

*Balanço das teses: A hipótese A apresenta suporte robusto na cronologia de desvios familiares; contudo, a hipótese B não está descartada, dada a existência de ativos reais na base do conglomerado.*

### 2. Quem exercia o controle efetivo?

- **Hipótese A:** Daniel Vorcaro comandava monocraticamente, com sócios em posição subordinada.
- **Hipótese B:** Tratava-se de sociedade com estruturas ocultas de financiamento.

:::fichas
Indiciamento indicando Vorcaro como chefe e Lima no núcleo executivo `Aponta para: A`
- Fonte: Relatório de Indiciamento da PF [62].

Sociedade em 2022: Vorcaro, Lima e empresa ligada a Quadrado `Aponta para: B`
- Fonte: Noticiário financeiro (Brazil Journal) [63].

Aval solidário de Vorcaro, Lima e Quadrado em emissão de dívida `Aponta para: B`
- Fonte: Registros de contencioso judicial [64].

Representação alegando injeção de R$ 700 mi por Tanure `Aponta para: B`
- Fonte: Denúncia formal da Esh Capital [63].

Tanure nega participação societária ou posse de debêntures `Aponta para: A`
- Fonte: Declarações formais do empresário [65].

Lima reuniu-se 7 vezes com diretores do BC em 2025 como CEO `Aponta para: B`
- Fonte: Agendas oficiais de autoridades públicas do BC [66].
:::

*Balanço das teses: Um grupo coeso liderado por Vorcaro é a linha mais respaldada pelas autoridades; a existência de controle oculto de terceiros segue sob disputa.*

## Quanto depende do celular apreendido? {#celular}

A contestação jurídica promovida pelos advogados em relação aos aparelhos telefônicos apreendidos de Vorcaro impacta primordialmente as provas subjetivas de intenção dolosa. O caminho do dinheiro (origem e destino dos fluxos financeiros) permanece demonstrado por registros bancários, cartorários e contábeis independentes.

Em 29 de outubro de 2026, os defensores protocolaram laudo do perito judicial Marcos Monteiro referente ao telefone apreendido em 17 de novembro de 2025 [92]. O exame apontou que 657 arquivos foram alterados e 436 foram gerados em 18 de novembro de 2025 — poucas horas após o recolhimento do aparelho, enquanto sob custódia da Polícia Federal; no cômputo geral, 999 arquivos teriam sofrido modificações, incluindo as bases de dados do WhatsApp [92]. O laudo atesta que os logs não permitem individualizar quem operou o dispositivo ou se as alterações decorreram de inserção acidental de cabo USB para recarga. A PF requereu dilação de 60 dias para perícia técnica oficial [92].

### Grau de vulnerabilidade das provas

:::fichas
Liquidação extrajudicial e pagamentos do FGC `Sem risco`
- Base probatória: Atos regulatórios normativos e extratos bancários [4][10].

Aquisição das carteiras podres pelo BRB `Quase nulo`
- Base probatória: Auditorias do Banco Central e contratos do BRB [46][48].

Desvios familiares (City, Navarra, Astralo 95) `Sem risco`
- Base probatória: Balanços da CVM, ações do liquidante e ordens cíveis [26][89].

Pagamentos a bancas, Metrópoles e Consult `Parcial`
- Base probatória: Relatórios fiscais da Receita e do Coaf (valores seguros; o propósito ilícito depende do celular) [34][35][74].

Repasses internacionais do filme "Dark Horse" `Parcial`
- Base probatória: Delação de Freixo e ordens de câmbio do Coaf [84][80].

Mesadas a parlamentares, mensagens a magistrados e "A Turma" `Alto risco`
- Base probatória: Conversas telemáticas e mensagens de texto nos celulares apreendidos [33][72][76][58].

Aportes dos fundos de previdência e elo político de Castro `Parcial`
- Base probatória: Balanços do Ministério da Previdência e TCE (valores seguros; o elo com Castro depende das mensagens) [96][98][99].
:::

Juristas consultados divergem quanto aos impactos de nulidade da prova digital: parcela dos penalistas defende que a violação da cadeia de custódia contamina exclusivamente as conversas extraídas dos aparelhos violados, permanecendo íntegras as provas fiscais, bancárias e periciais independentes [93].

## O que não sabemos, e o que esclareceria {#aberto}

Seis questões centrais pendem de elucidação formal:

- **A delação homologada da Reag:** O acordo assinado entre a PGR e João Carlos Mansur carece de julgamento homologatório [67]. Sua alegação de que pode mapear R$ 20 bilhões sob custódia de Vorcaro segue sem confirmação [68]. Em 27 de outubro de 2026, a PGR protocolou requerimento de urgência no STF [69].
- **A definição da relatoria no STF:** Desde 12 de setembro de 2026, a presidência do STF retém os autos do inquérito. O ministro Mendonça segue como relator formal, mas com atos obstados; aguarda-se redistribuição regimental [94].
- **O desfecho da perícia telefônica:** O acolhimento ou não da tese de quebra da cadeia de custódia dos celulares [92].
- **Inquéritos secundários além do BRB:** O indiciamento inicial concentrou-se estritamente na compra de créditos pelo BRB [8]. Relatórios conclusivos sobre fundos da Reag, Rioprevidência e blindagem política seguem em fase de elaboração.
- **O laudo contábil da massa liquidanda:** Apurará o valor de liquidação dos recebíveis. A CVM instaurou processo sancionador contra o liquidante por descumprimento de prazos na convocação de cotistas de FIIs com R$ 610 milhões aplicados [95].
- **Oferecimento e recebimento de denúncias:** A formalização ou arquivamento de ações penais pela PGR perante o plenário da Suprema Corte.

> **Limites documentais da análise:** O Banco Central decretou sigilo administrativo de oito anos (com vigência até novembro de 2033) sobre os autos da fiscalização do Master [70]. A eventual tramitação da emenda parlamentar do FGC no Congresso Nacional não foi verificada nesta apuração.

# Sobre esta compilação

## Método {#metodo}

- **Fontes utilizadas:** Reportagens documentadas com base em autos do Banco Central, PF, CVM, Receita Federal, Coaf, administração judicial, decisões do STF e termos preliminares de colaboração premiada, coletadas em 30 e 31 de outubro de 2026. Os autos processuais originais sob segredo de justiça não foram acessados diretamente.
- **Categorização analítica:** Classifica-se como *"Estabelecido"* aquilo que deriva de publicação em diários oficiais, decisões regulatórias formais ou convergência documental irrefutável. Considera-se *"Alegado"* o teor de peças investigativas, delações não sentenciadas e relatórios policiais. Todas as manifestações de defesa localizadas foram expressamente reproduzidas.
- **Concentração documental:** A maior fatia das conclusões decorre de peças da PF, checadas, sempre que viável, com dados paralelos da Receita, Coaf e CVM.
- **Status processual:** Indiciamento policial ou menção em termo de colaboração não equivalem a condenação penal transitada em julgado. Vigora para todos os citados a presunção constitucional de inocência.
- **Inferência:** A formulação de "fraude de controle", a modelagem em esteira e a consolidação dos dados monetários constituem inferências analíticas do autor a partir das evidências colhidas.
- **Critério de exclusão:** Registros pontuais e isolados a respeito da conduta privada de magistrados em confraternizações sociais foram suprimidos por não agregarem relevância à análise dos fluxos monetários.

## Glossário {#glossario}

Siglas usadas no texto. Ao longo da página, o primeiro uso de cada sigla em cada seção vem sublinhado com pontos: toque nele para ver a definição sem sair do lugar. As regras de cobertura do FGC seguem o regulamento do fundo [117]; a definição de CDI segue o glossário da B3 [118].

:::glossario
BC: Banco Central do Brasil. Regula e fiscaliza os bancos e as demais instituições financeiras do país.
BRB: Banco de Brasília, banco público controlado pelo Governo do Distrito Federal.
CDB: Certificado de Depósito Bancário. Título que o banco vende ao investidor para captar dinheiro, com prazo e juros combinados. É um depósito a prazo e, por isso, tem a garantia do FGC, dentro do limite.
CDI: Certificado de Depósito Interbancário. Título que os bancos usam para emprestar dinheiro uns aos outros, em geral por um dia. A média dos juros dessas operações de um dia, a taxa DI calculada pela B3, é chamada no mercado simplesmente de "CDI" e serve de régua para aplicações: render 140% do CDI é render 1,4 vez essa taxa.
CMN: Conselho Monetário Nacional. Fixa as regras do sistema financeiro, entre elas os limites para os fundos de previdência de servidores aplicarem seu dinheiro.
CNPJ: Cadastro Nacional da Pessoa Jurídica, o número de registro das empresas na Receita Federal.
Coaf: Conselho de Controle de Atividades Financeiras, a unidade de inteligência financeira do país. Recebe avisos de operações suspeitas e produz relatórios para as autoridades.
CPF: Cadastro de Pessoas Físicas, o número de registro das pessoas na Receita Federal.
CVM: Comissão de Valores Mobiliários. Regula e fiscaliza o mercado de capitais, incluindo os fundos de investimento.
DIEESE: Departamento Intersindical de Estatística e Estudos Socioeconômicos, instituto de pesquisa mantido por entidades sindicais.
FGC: Fundo Garantidor de Créditos. Entidade privada, sustentada pelas instituições associadas, que devolve ao investidor o dinheiro de depósitos, poupança, CDBs e algumas letras quando o banco quebra. O limite é de R$ 250 mil por pessoa (CPF ou CNPJ) em cada instituição ou conglomerado, e de R$ 1 milhão a cada quatro anos, somando todas.
FII: Fundo de investimento imobiliário. Aplica em imóveis ou em papéis ligados a imóveis; as cotas costumam ser negociadas na bolsa.
IFData: Relatórios do Banco Central com dados selecionados de cada instituição financeira, como balanço e captação.
LF: Letra Financeira. Título de dívida de longo prazo emitido por bancos. Não está entre os investimentos cobertos pelo FGC.
MPF: Ministério Público Federal, o órgão que investiga e acusa crimes na esfera federal.
PCC: Primeiro Comando da Capital, facção criminosa.
PF: Polícia Federal.
PGE: Procuradoria-Geral do Estado, que defende o estado na Justiça; aqui, a do Rio de Janeiro.
PGR: Procuradoria-Geral da República, a chefia do Ministério Público Federal. É quem acusa, no STF, as autoridades julgadas por esse tribunal.
PL: Partido Liberal.
PM: Polícia Militar.
PP: Progressistas, partido político.
PT: Partido dos Trabalhadores.
RPPS: Regime Próprio de Previdência Social. O sistema de aposentadoria dos servidores públicos da União, de um estado ou de um município, com fundo próprio para pagar os benefícios.
SFN: Sistema Financeiro Nacional, o conjunto de instituições, órgãos e regras do mercado financeiro do país.
STF: Supremo Tribunal Federal.
TCE-RJ | TCE: Tribunal de Contas do Estado do Rio de Janeiro. Fiscaliza como o governo estadual e seus órgãos usam o dinheiro público.
TCU: Tribunal de Contas da União. Fiscaliza o uso do dinheiro público federal.
:::

## Referências {#referencias}

*Fontes consultadas entre 30 e 31 de outubro de 2026. "s.d." indica sem data explícita informada no registro original consultado.*

:::referencias
1. “Banco Central decreta liquidação extrajudicial do Banco Master.” Eu Quero Investir, s.d.
2. “Entenda a crise financeira por trás da compra do Banco Master pela BRB.” Jornal Opção, s.d.
3. Guia de ressarcimento do FGC para investidores de CDB do Master. Money Times, s.d.
4. “FGC paga R$ 40,6 bi a 800 mil investidores do Banco Master.” AUVP Analítica, s.d.
5. “FGC vai reembolsar 1,6 milhão de investidores do Banco Master.” Bora Investir (B3), nov. 2025.
6. Akerlof, George A.; Romer, Paul M. “Looting: The Economic Underworld of Bankruptcy for Profit.” Brookings Papers on Economic Activity, 1993, nº 2.
7. “Editors’ Summary.” Brookings Papers on Economic Activity, 1993, nº 2.
8. “Caso Master: PF indicia 15, incluindo Vorcaro, por crimes financeiros.” Band, 28 out. 2026.
9. “Banqueiro do Master nega fraude e critica Banco Central.” SpaceMoney, 30 out. 2026.
10. “BC explica liquidação do Banco Master.” O Antagonista, 18 nov. 2025.
11. “Banco Central impõe sigilo de 8 anos sobre caso Master.” Band, 6 abr. 2026.
12. “CVM admite indícios de fraude no Banco Master desde 2020.” Revista Oeste, s.d.
13. Correio da Manhã, 15 jan. 2026, p. 6 (edição impressa).
14. “Como funcionava o esquema do Banco Master, segundo a investigação.” IstoÉ, s.d.
15. “Como funcionava o esquema do Banco Master, segundo a investigação.” Band / Deutsche Welle, 30 jan. 2026.
16. Cerqueira, Felipe. “Banco Master é suspeito de inflar patrimônio com investimentos fraudulentos, diz CVM.” Jovem Pan, s.d.
17. “Investigação aponta uso de ‘laranjas’ em fundos do Banco Master.” Revista Oeste, s.d.
18. “Banco Central decreta liquidação da Reag Investimentos, envolvida no caso Master.” JOTA, 15 jan. 2026 (via Harvard TagTeam).
19. “Entenda por que operações do Banco Master com a Reag estão sob investigação.” Jornal de Brasília, s.d.
20. “Como funcionava o esquema do Banco Master segundo a investigação.” Band, s.d.
21. “Ex-dono da Reag entrega à PGR proposta de delação premiada.” Poder360, s.d.
22. “Ex-dono da Reag propõe delação e cita Banco Master e PCC.” Rádio Itatiaia, s.d.
23. “Fundador da Reag confirma Master entre clientes e nega ligação com PCC.” Estadão Conteúdo via InfoMoney, s.d.
24. Avaliação dos ativos recebidos do Master pelo BRB (citando Valor Econômico). Let’s Money, s.d.
25. Mandl, Carolina; Felix, Diego. “Como Vorcaro desviava dinheiro do Master para familiares, segundo investigações.” Folhapress via Bem Paraná, s.d.
26. “Vorcaro tentou encobrir rombo de R$ 777 mi após usar Master para financiar empresas de familiares.” InfoMoney, s.d.
27. Rezende, Constança; Marchesini, Lucas. “Cunhado de Vorcaro recebeu R$ 485 milhões de empresa investigada pela PF em caso Master.” Folhapress via TNH1, 21 mar. 2026.
28. Transferência de R$ 180 milhões de fundo investigado na Carbono Oculto para a Super Empreendimentos. Folha de Pernambuco, s.d.
29. Sobre R$ 2,2 bilhões ocultados após liberação judicial. BP Money, s.d.
30. Posicionamento do Ministério Público Federal em SP e resposta da defesa. BP Money, s.d.
31. “PF: ex-chefe de supervisão do BC recebeu R$ 500 mil mensais de Vorcaro.” Folhapress via DGABC, s.d.
32. “PF aponta pagamentos de até R$ 400 mil por mês a agentes ligados ao caso Vorcaro.” Gazeta do Povo, s.d.
33. “Quem é Ciro Nogueira, senador e ex-ministro de Bolsonaro que foi alvo da PF.” CNN Brasil, 7 maio 2026.
34. “Master repassou R$ 80 mi a escritório de mulher de Moraes, mostram documentos.” SBT News, s.d.
35. “Diálogos obtidos pela PF mostram repasse de R$ 51,9 mi de Vorcaro ao portal Metrópoles.” Estadão Conteúdo via Mercado & Consumo, 16 out. 2026.
36. “‘Comprado os caras’: Vorcaro pagou DCM para não criticar Master, diz PF.” Jovem Pan, s.d.
37. “Vorcaro ofereceu dinheiro para influenciadores criticarem o BC nas redes, segundo a PF.” Brasil de Fato, 10 jul. 2026.
38. Sampaio, Carlos Nathan. “Em delação rejeitada, Vorcaro associa doações a Tarcísio e Bolsonaro a propina.” Tribuna do Planalto, 4 set. 2026.
39. “Operação policial contra o crime organizado mira o Banco Genial e esquema ligado a recursos do filme Dark Horse.” Times Brasil, 24 set. 2026.
40. Nota oficial da assessoria de Ciro Nogueira. IstoÉ Dinheiro, 7 maio 2026.
41. Gayoso, Lucas. “PF encontra contrato de R$ 3 milhões por mês entre Vorcaro e escritório de Viviane de Moraes.” Correio da Manhã, set. 2026.
42. Contratos jurídicos totalizando R$ 208 milhões. BP Money, s.d.
43. “Entenda o passo a passo da crise no STF.” Revista Oeste, s.d.
44. “Augusto Lima, ex-sócio do Master, tem ligações com o PT da Bahia.” Poder360, s.d.
45. “PF diz que BRB participou de fraudes em aportes bilionários no Banco Master.” BP Money, s.d.
46. Felix, Diego; Moura, Júlia. “Relatório da PF aponta que BRB comprou R$ 17 bi em créditos falsos do Banco Master.” Folhapress via Bahia Notícias, s.d.
47. “Saiba quem são os 15 primeiros indiciados pela PF sob suspeita de crimes no Banco Master.” TNH1, 29 out. 2026.
48. “‘Não há evidência de que as carteiras do Master eram podres’, diz ex-presidente do BRB.” Revista Oeste, s.d.
49. Sotero, Rafael. “Como funcionava esquema entre Ciro Nogueira e Daniel Vorcaro, segundo a PF.” CNN Brasil, 7 maio 2026.
50. “Caso Master: veja os nomes e as condutas dos 15 indiciados no relatório da PF.” Sem Pauta News, 29 out. 2026.
51. “BC exige provisionamento de mais de R$ 2 bi do BRB por perdas com o Master.” Revista Oeste, s.d.
52. Estimativa técnica do Banco Central sobre prejuízos no BRB. Let’s Money, s.d.
53. “Fraudes do BRB e Master aconteceram mesmo sob olhar do BC.” Revista Oeste, s.d.
54. Côrtes, Gustavo; Sousa, Gabriel de; Ohana, Victor. O Estado de S. Paulo, 16 jan. 2026, p. B2 (via clipping ANFIP).
55. “Senador Ciro Nogueira é alvo de busca da PF no caso Master; primo de Vorcaro é preso.” Money Times, 7 maio 2026.
56. Quinta fase ostensiva da Operação da PF. Sul21, maio 2026.
57. “Vorcaro simulou venda para Fictor para tentar fugir do país, dizem investigadores.” Jornal de Brasília, s.d.
58. “‘Sicários’ de Vorcaro presos pela PF formavam ‘milícia privada’.” Times Brasil, 4 mar. 2026.
59. Bernardes, Alícia; Rocha, Danandra; Mac Cord, Iago. “PF: pai de Vorcaro chefiava milícia.” Correio Braziliense, 15 maio 2026, p. 3.
60. “PF aponta que ‘Sicário’ recebeu R$ 24 milhões de Daniel Vorcaro.” Metrópoles, s.d.
61. “Defesa de Vorcaro pede que PF comprove existência da milícia ‘A Turma’.” Jornal Opção, 5 mar. 2026.
62. “Saiba quem são os 15 primeiros indiciados pela PF sob suspeita de crimes no Banco Master.” Jornal de Brasília, 29 out. 2026.
63. Denúncia da Esh Capital e estrutura societária do Master em 2022. Brazil Journal, s.d.
64. “Do Master ao Voiter: entenda disputa judicial que envolve Augusto Lima.” Poder360, s.d.
65. “Quem é Nelson Tanure, que ganhou relógio de luxo de Vorcaro.” Jovem Pan, s.d.
66. “Augusto Lima, do Banco Pleno, se reuniu 7 vezes com BC em 2025 como CEO do Master.” Estadão Conteúdo via InfoMoney, s.d.
67. Rodrigues, Basília. “Caso Master: PGR assina delação com ex-dono da Reag.” SBT News, s.d.
68. Freire Neto, Moisés. “Delação de ex-dono da Reag põe R$ 20 bilhões do dinheiro de Vorcaro no radar.” Economic News Brasil, 10 set. 2026.
69. “Delação de Mansur, da Reag, ganha pedido de urgência da PGR a Fachin para localizar R$ 20 bilhões de Vorcaro.” Times Brasil, 27 out. 2026.
70. Sigilo de 8 anos imposto sobre autos de liquidação do Master. BP Money, s.d.
71. Relatório da PF sobre repasse de pelo menos R$ 20 milhões a empresa da família de Toffoli. Metrópoles, fev. 2026.
72. “Vorcaro teria sido pressionado por aportes em resort ligado a Toffoli e desembolsado R$ 35 milhões.” Times Brasil, 14 fev. 2026.
73. “PF não mostra ao Supremo conteúdo de 52 celulares do caso Master.” Poder360, s.d.
74. Grandi, Guilherme; Manfrin, Juliet. “Filho de Nunes Marques teria recebido R$ 500 mil do Master, aponta PF.” Gazeta do Povo, 15 set. 2026.
75. “Vorcaro coordenou noitada em triplex para ministro do STF Kassio Nunes Marques, diz revista.” Estadão Conteúdo via O Liberal, 16 out. 2026.
76. Lobianco, Bianca. Estadia de Carnaval 2025 atribuída a "KN". Correio da Manhã, 18 set. 2026.
77. “Conselho do MPF decide arquivar pedido de apuração sobre relação de Gonet e Vorcaro.” Times Brasil, set. 2026.
78. “Mensagem de Gonet para Vorcaro: ‘tomara que tenha charuto e Macallan’.” InfoMoney, set. 2026.
79. Inquérito no STF envolvendo Flávio Bolsonaro no caso Dark Horse. O Hoje, 11 set. 2026.
80. “Flávio mentiu ao menos 43 vezes sobre elo com Vorcaro.” Aos Fatos, s.d.
81. “Nikolas admite contato com Vorcaro, mas nega relação: ‘nunca recebi nenhum tostão’.” Rádio Itatiaia, 3 set. 2026.
82. “Banco Master: quem são os dois empresários alvos da operação da PF, soltos pela Justiça.” Mercado & Consumo, 23 nov. 2025.
83. “Banco Master: quem são os 15 indiciados pela PF no escândalo.” Revista Fórum, 29 out. 2026.
84. Homologação da colaboração de Freixo pelo ministro André Mendonça. Gazeta do Povo, set. 2026.
85. Depoimento de Paulo Henrique Costa envolvendo Ibaneis Rocha. Gazeta do Povo, 9 jul. 2026.
86. “STJ manda para PGR pedido de investigação sobre governador Ibaneis Rocha e caso Master.” SBT News, 4 fev. 2026.
87. Gallo, Gabriela. “Vorcaro volta a negar que Master deu prejuízos financeiros ao BRB.” Correio da Manhã, 15 out. 2026.
88. “Vorcaro diz que crise no BRB é culpa de investigação da PF.” SBT News, 16 out. 2026.
89. “Justiça barra venda de bens ligados ao Banco Master após indícios de desvios.” Economic News Brasil, 18 mar. 2026.
90. Ação judicial da massa liquidanda sobre cobertura de luxo em Miami. Times Brasil, s.d.
91. “Exclusivo: Vorcaro obtém liminar nos EUA que suspende investigação sobre mansão de US$ 32 milhões.” SBT News, 22 maio 2026.
92. “Perícia contratada por Vorcaro aponta alterações em celular de ex-banqueiro.” CNN Brasil, 29 out. 2026.
93. “Especialistas divergem sobre possibilidade de anulação do caso Master.” Rádio Itatiaia, 12 set. 2026.
94. “Ministro Edson Fachin retém processos do caso Master no STF e trava investigações.” Gazeta do Povo, 21 out. 2026.
95. “Alvo da CVM, liquidante do Master mantém R$ 610 milhões em FIIs travados.” NeoFeed, 21 out. 2026.
96. Souza, Amanda. “Banco Master: 18 fundos de previdência tinham investimentos no banco; veja lista.” Times Brasil, 19 nov. 2025.
97. Queiroz, Vitória. “Estados e municípios vão arcar com rombo do Master em fundos de previdência.” CNN Brasil, 9 jan. 2026.
98. “Cláudio Castro: relembre caso dos aportes bilionários do Rioprevidência no Master.” InfoMoney, 26 maio 2026.
99. Muradi, Anna. “Cláudio Castro trocou cúpula do Rioprevidência antes de aportes de R$ 3,6 bilhões no Master, diz PF.” BP Money, 26 maio 2026.
100. “Daniel Vorcaro bancou viagens de Cláudio Castro, diz PF.” CNN Brasil, 26 maio 2026.
101. “Cláudio Castro agradeceu Vorcaro após jantar de R$ 66 mil em Nova York: ‘experiência incrível’.” Times Brasil, 28 maio 2026.
102. “Castro nega relação indevida com Vorcaro e diz que contatos foram institucionais.” InfoMoney, 27 maio 2026.
103. “PF: Rioprev investiu no Master para ‘contornar restrições’.” SBT News, maio 2026.
104. “Entenda como o Rio investiu R$ 3 bi no Master e para onde foi o dinheiro.” CNN Brasil, maio 2026.
105. “Vorcaro discutiu substituir aplicações do Rioprevidência por outros ativos antes da liquidação do Master.” Times Brasil, s.d.
106. Ações da Procuradoria-Geral do Estado do Rio para reaver R$ 641 milhões. Gazeta do Povo, jul. 2026.
107. “Câmara do DF aprova capitalização do BRB com garantia de imóveis públicos.” Rádio Itatiaia, 3 mar. 2026.
108. “FGC antecipa contribuições de bancos para recompor R$ 32,5 bi do rombo deixado pelo Master.” SBT News, 5 mar. 2026.
109. “Liquidações de bancos ligados ao Master devem encarecer crédito para o consumidor.” Diario de Pernambuco, 18 fev. 2026.
110. “FGC deve começar a pagar investidores com CDBs do Master nesta semana.” InfoMoney, jan. 2026.
111. “FGC começa a ressarcir investidores do Banco Master.” Correio da Manhã, jan. 2026.
112. “Diretor do BC revela como identificou fraudes do Banco Master e créditos sem valor vendidos ao BRB.” SBT News, s.d.
113. Correio da Manhã, 2 fev. 2026, p. 6 (edição impressa).
114. DIEESE. “Caso Banco Master: impactos sociais e implicações regulatórias.” Nota Técnica nº 291, 31 mar. 2026 (compilação com dados do IFData/BC).
115. Redação Suno. “Banco Master, em negociação com BRB, divulga balanço com lucro de R$ 1 bi em 2024.” Suno Notícias, 2 abr. 2025.
116. Lucchesi, Cristiane; Piovesana, Matheus; Alvim, Leda. “Colapso do Banco Master levanta debate sobre papel de plataformas como a XP.” Bloomberg News via Bloomberg Línea, 1 dez. 2025.
117. Fundo Garantidor de Créditos. Regulamento do FGC (Anexo II à Resolução CMN nº 4.222, de 23 maio 2013), arts. 1º e 2º. Disponível em [fgc.org.br](https://fgc.org.br/documents/d/asset-library-52554/regulamento-fgc). Acesso em 31 out. 2026.
118. B3. “Taxa DI.” Glossário Bora Investir. Disponível em [borainvestir.b3.com.br](https://borainvestir.b3.com.br/glossario/taxa-di/). Acesso em 31 out. 2026.
:::
