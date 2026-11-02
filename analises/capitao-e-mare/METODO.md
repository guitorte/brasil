# O capitão ou a maré? Método fixado antes dos resultados

Escrito e gravado no repositório **antes** de rodar qualquer teste, para que o período, os grupos e os
critérios não sejam escolhidos depois de ver os números. Mudanças posteriores ficam registradas no fim
deste arquivo, com o motivo.

## Pergunta

Quanto do desempenho do Brasil desde 1995 acompanha o que veio de fora (a maré) e quanto se descola dela
(o que sobra para decisões internas: o capitão e a tripulação)?

## Períodos

- Período inteiro: 1995–2024 (último ano fechado nas fontes do Banco Mundial).
- Blocos de quatro anos civis, que coincidem com os mandatos presidenciais: 1995–98, 1999–2002, 2003–06,
  2007–10, 2011–14, 2015–18, 2019–22 e 2023–24 (incompleto). O bloco 2015–18 mistura dois presidentes;
  fica marcado como misto e não é atribuído a nenhum dos dois.
- Defasagem: cada bloco também é lido com um ano de atraso (1996–99, 2000–03…), porque decisões de um
  governo costumam aparecer nos números do seguinte. Os dois cortes são sempre mostrados juntos.

## Medidas da maré

1. **Os pares.** Mediana do crescimento do PIB por habitante em PPC dos 16 países escolhidos pela regra
   de `dados/comparacoes/pares.csv`. Eles enfrentam a mesma economia mundial; a diferença entre o Brasil
   e a mediana deles é a primeira medida do que é próprio do Brasil.
2. **Um modelo simples.** Regressão do crescimento anual do PIB por habitante do Brasil sobre o crescimento
   do PIB por habitante mundial e a variação do índice real de commodities não energéticas (Banco Mundial),
   1996–2024. A parte que o modelo não explica (o resíduo) é a segunda medida. Só dois fatores, para não
   ajustar demais com 29 observações. Relata-se o R² e os coeficientes; o resíduo não é "culpa" de ninguém,
   é só o que a maré medida assim não explica.
3. **Exportadores de commodities.** Subgrupo dos pares cuja exportação de mercadorias foi, em média
   1995–2004, pelo menos 60% de commodities (alimentos, matérias-primas agrícolas, combustíveis, minérios e
   metais; Banco Mundial). Compara o Brasil com quem pegou a mesma onda de preços.

## Medidas do capitão

4. **Contabilidade do crescimento** (Penn World Table 11.0), 1995–2019 (antes da pandemia): crescimento do
   produto por trabalhador decomposto em capital por trabalhador, capital humano e produtividade total dos
   fatores. Brasil contra a mediana dos pares.
5. **Juros.** Selic real (Selic média do ano contra IPCA do ano) e diferença para os juros básicos dos EUA;
   juros pagos pelo governo em % do PIB contra os pares (FMI).
6. **Investimento.** Formação bruta de capital em % do PIB, Brasil contra os pares (Banco Mundial).

## Quem segura cada alavanca

7. Mapa a partir dos textos legais (Constituição e leis complementares, no Planalto): quem decide o orçamento
   e as emendas, as regras fiscais e os juros, e quando isso mudou. Emendas parlamentares em valores reais
   (corrigidas pelo IPCA).

## Leitura

- Correlação não é causa. Um bloco com resíduo negativo diz que a maré medida não explica aquele período,
  não que o presidente da vez o causou.
- O mesmo teste vale para todos os blocos, na mesma ordem e com a mesma régua.
- Onde a pesquisa publicada discorda sobre as causas (por exemplo, da recessão de 2014–16), as posições são
  apresentadas com seus autores, sem escolher a média.

## Mudanças depois de ver os resultados

(nenhuma até agora)
