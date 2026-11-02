# Dados de comparação

Material bruto para responder a quatro perguntas sobre o Brasil:

1. **Está ruim ou está piorando?** Nível e trajetória são veredictos diferentes.
2. **Comparado com quem?** Com o próprio passado, com países que partiram do mesmo lugar e com o que seria possível.
3. **O capitão ou a maré?** O que dependeu de decisões internas e o que veio de fora.
4. **Quem segurava cada alavanca?** Presidência, Banco Central, Congresso.

Tudo foi baixado das fontes oficiais por `ferramentas/coletar_comparacoes.py`. Cada arquivo tem uma linha
em `fontes_e_indicadores.csv` com a fonte, o código original, a unidade, a data da coleta, a cobertura e
as ressalvas. **Leia a coluna `nota` antes de usar qualquer série.**

## A regra dos pares

O grupo de comparação foi escolhido por uma regra, fixada antes de olhar qualquer resultado:

- pelo menos **10 milhões de habitantes em 1995**; e
- **PIB por habitante em PPC entre 2/3 e 1,5 vez o do Brasil em 1995** (Banco Mundial,
  `NY.GDP.PCAP.PP.KD`, dólares internacionais constantes de 2021).

Passaram 16 países: Argélia, Cazaquistão, Chile, Colômbia, Equador, Hungria, Irã, Malásia, México, Polônia,
Romênia, Rússia, África do Sul, Tailândia, Turquia e Ucrânia. Ficaram de fora, por falta de dado no
ano-base, Afeganistão, Cuba, Coreia do Norte, Venezuela e Iêmen. A tabela completa, com a razão de cada país
em relação ao Brasil, está em `pares.csv`.

Os arquivos de resultados guardam **todos os 75 países com mais de 10 milhões de habitantes em 1995**, e não
só os pares. Assim dá para testar outra faixa de renda ou outro ano-base sem baixar tudo de novo. Os países
da lista anterior do repositório (Argentina, Peru, Coreia do Sul, China, Índia, Indonésia, EUA) também
estão lá, marcados em `pares.csv` na coluna `lista_anterior`.

## Arquivos

| Arquivo | O que tem | Fonte |
|---|---|---|
| `pares.csv` | a regra aplicada a cada país | Banco Mundial (WDI) |
| `renda_universo.csv` | PIB por habitante em PPC e população, 1990–2025, para os 75 países | Banco Mundial (WDI) |
| `pobreza.csv` | pobreza pelas linhas de US$ 3,00, 4,20 e 8,30 por dia (PPC 2021), só anos com pesquisa | Banco Mundial (Poverty and Inequality Platform) |
| `condicoes_de_vida.csv` | expectativa de vida, mortalidade infantil, homicídios, PISA, informalidade | ONU (WPP 2024), UNODC, OCDE via Banco Mundial, OIT |
| `alavancas_brasil.csv` | Selic, IPCA, resultado primário, juros e resultado nominal do setor público, dívidas (mensal) | Banco Central (SGS) |
| `contas_publicas_fmi.csv` | primário, juros pagos, receita, despesa e dívida do governo geral, nos 75 países | FMI (Public Finances in Modern History e Fiscal Monitor) |
| `mare.csv` | juros básicos e título de 10 anos dos EUA (mensal) | Federal Reserve (H.15), via FRED |
| `produtividade.csv` | produto por trabalhador; produtividade total dos fatores, capital humano, horas, capital | OIT; Penn World Table 11.0 |
| `eleitos_1994_2014.csv` | um eleito por linha: governador, senador, deputado federal e estadual | TSE |
| `eleitos_por_partido_1994_2014.csv` | quantos cada partido elegeu, por cargo e eleição | TSE |
| `emendas_por_ano_e_tipo.csv` | emendas parlamentares empenhadas, liquidadas e pagas, 2014–2026 | CGU, Portal da Transparência |

Os dados de 2018 e 2022 do TSE, o crescimento, a inflação, o câmbio, os preços de commodities e os termos
de troca já estavam em `dados/eleicoes/` e `dados/mundo/` e não foram baixados de novo.

## O que ainda falta

| Falta | Por quê | Como completar |
|---|---|---|
| PISA 2022 | A base do Banco Mundial vai só até 2018, e a OCDE não oferece o PISA por API | Copiar das tabelas I.B1.5.4 a I.B1.5.6 do relatório *PISA 2022 Results*, Volume I |
| PISA direto da OCDE | Mesmo motivo; hoje a série vem da reprodução do Banco Mundial | Conferir os anos de 2000 a 2018 com os relatórios da OCDE |
| Pobreza pelas linhas do IBGE | O serviço de metadados do IBGE não respondeu daqui | Tabelas da Síntese de Indicadores Sociais |
| Investimento público | Nenhuma fonte com API cobre o Brasil e os pares no mesmo conceito | Tesouro Nacional (Brasil); FMI, Investment and Capital Stock Dataset (pares) |
| Linha do tempo de presidentes e chefes do Banco Central | Precisa de uma fonte oficial por linha | Biblioteca da Presidência e Banco Central |
| Fatia do orçamento direcionada por emendas | Falta o denominador, a despesa discricionária | Resultado do Tesouro Nacional |
| Equivalência entre siglas antigas e atuais | Fusões e trocas de nome precisam de fonte própria | TSE, registro de partidos |

## Cuidados para comparar

- **Renda ou consumo.** Na pobreza, o Brasil mede renda; muitos pares medem consumo. As duas medidas não são
  equivalentes (coluna `tipo_bem_estar`).
- **Quebras de série.** A troca da PNAD pela PNAD Contínua quebra pobreza e informalidade no Brasil por
  volta de 2012–2016. Compare só dentro do mesmo `periodo_comparavel`.
- **Projeções.** As séries do FMI trazem projeções (coluna `projecao`). Na ONU e na OIT, foram guardados só os
  anos anteriores à publicação de cada revisão.
- **Conceitos fiscais.** O Banco Central mede o setor público consolidado; o FMI mede o governo geral.
  Compare o Brasil com os pares só pelos números do FMI.
- **Valores nominais.** As emendas estão em reais correntes: corrija pela inflação antes de comparar anos.

## Para atualizar

```
python3 ferramentas/coletar_comparacoes.py              # tudo, uns 7 minutos
python3 ferramentas/coletar_comparacoes.py resultados   # só um bloco
```

Blocos: `pares`, `resultados`, `alavancas`, `mare`, `produtividade`, `congresso`, `emendas`. O bloco `pares`
precisa rodar antes dos outros, porque eles leem o universo de países em `pares.csv`.
