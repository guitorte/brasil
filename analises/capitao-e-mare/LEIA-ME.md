# O capitão ou a maré?

Testes para separar o que, no desempenho do Brasil desde 1995, acompanha a economia mundial e o que se
descola dela. O método foi gravado em `METODO.md` antes de qualquer número ser calculado (veja a data do
commit). `analise.py` lê só arquivos de `dados/` e grava as tabelas em `resultados/`:

```
python3 analises/capitao-e-mare/analise.py
```

| Tabela | O que mostra |
|---|---|
| `t1_anual.csv`, `t1_blocos.csv`, `t1_blocos_defasados.csv` | crescimento do PIB por habitante em PPC do Brasil contra a mediana dos 16 pares, por ano e por bloco de quatro anos (com e sem um ano de defasagem) |
| `t2_modelo.csv`, `t2_anual.csv`, `t2_blocos.csv` | quanto do crescimento do Brasil o crescimento mundial e os preços de commodities explicam (R²), e o que sobra por bloco |
| `t3_peso_commodities_1995_2004.csv`, `t3_blocos.csv` | o Brasil contra os pares que exportam sobretudo commodities |
| `c4_contabilidade_1995_2019.csv` | produto por trabalhador decomposto em capital, capital humano e produtividade total dos fatores |
| `c5_juros_reais.csv`, `c5_juros_pagos_blocos.csv` | Selic real contra o juro real dos EUA; juros pagos pelo governo contra os pares |
| `c6_investimento_blocos.csv` | investimento em % do PIB contra os pares |
| `c7_emendas_reais.csv` | emendas parlamentares empenhadas, em reais de 2025 |

## Como ler

- Os blocos coincidem com mandatos, mas um bloco abaixo dos pares não prova que o presidente da vez causou
  o resultado: há defasagens, choques que o modelo não mede e alavancas que não estão com a Presidência.
- O bloco 2015–2018 mistura dois governos e não é atribuído a nenhum.
- A produtividade total dos fatores da Penn World Table é um resíduo de modelo. O capital humano mede anos
  de estudo, não a qualidade do ensino; o que a qualidade deixa de fora cai no resíduo.
- Os textos legais e a pesquisa publicada que interpretam esses números entram na redação final, com notas.
