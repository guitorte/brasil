# Como o site é montado

O site tem uma página de entrada (`index.html`) e uma página por capítulo (`mundo/index.html`, por enquanto).
As duas são **geradas** a partir dos dados; não edite esses arquivos à mão.

```
python3 ferramentas/montar.py
```

O script só usa a biblioteca padrão do Python. Ele:

1. lê os CSVs em `dados/`;
2. calcula os números citados nos textos e **confere as frases**: se uma atualização dos dados tornar falsa
   uma afirmação (por exemplo, "o mundo dobrou"), a montagem para com uma mensagem dizendo qual;
3. embute em cada página só os dados que ela usa e grava `index.html`, `mundo/index.html` e o
   redirecionamento `v4.html`.

## Onde fica cada coisa

| Arquivo | O que é |
|---|---|
| `ferramentas/montar.py` | o script de montagem e a lista de capítulos (`CAPS`) |
| `ferramentas/modelos/inicio.html` | modelo da página de entrada |
| `ferramentas/modelos/mundo.html` | modelo do capítulo "Brasil no mundo" (textos, cartões e o código próprio do capítulo) |
| `assets/estilo.css` | visual comum: cores, barra do topo, cartões, tabelas, glossário |
| `assets/graficos.js` | motor comum: gráficos em SVG, tabelas com coluna fixa, glossário ao toque, compartilhar e baixar imagem |
| `v3.html` | a versão completa, numa página só; os capítulos ainda não convertidos apontam para ela |

Nos modelos, `{{nome}}` é trocado por um número calculado no script e `/*__DATA__*/null` pelos dados do capítulo.

## Para converter outro capítulo

1. Crie `ferramentas/modelos/<capitulo>.html` a partir de `mundo.html`.
2. Em `montar.py`, escreva uma função que prepare os dados e os números do capítulo, com as checagens das frases.
3. Troque o `link` do capítulo em `CAPS` por `<capitulo>/` e mande gravar a página no fim do script.

# Dossiês: páginas de texto longo (`master/`)

A página `master/` não sai dos dados: é um texto longo, com notas e referências. Ela é montada por
outro script, a partir de um arquivo de texto simples, no visual de enciclopédia/documentação.

```
python3 ferramentas/dossie.py
```

## O que mudar, e onde

| Quero mudar... | Edite | Precisa rodar o script? |
|---|---|---|
| um texto, número, nota, ficha, referência ou definição do glossário | `master/texto.md` | sim, ou deixe o GitHub rodar (abaixo) |
| cores, fontes, espaçamentos, aparência das fichas e etiquetas | `assets/dossie.css` | não, vale na hora |
| a moldura da página (topo, sumário, botões flutuantes) | `ferramentas/modelos/dossie.html` | sim |
| o comportamento (notas ao toque, sumário que sobe de baixo, seção atual) | `assets/dossie.js` | não |

`master/index.html` é gerado: não edite à mão. O texto original em inglês (`.docx` e `.pdf`) fica ao lado, em `master/`.

## A marcação do `texto.md`

O arquivo começa com um cabeçalho entre linhas `---` (`titulo`, `titulo_aba`, `chapeu`, `assinatura` e,
se quiser, `descricao`). Depois vem o texto. Comentários `<!-- ... -->` são ignorados.

| Escreva | Vira |
|---|---|
| `# Visão geral` | uma parte: agrupa as seções seguintes no sumário |
| `## CDBs astronômicos {#cdb}` | uma seção; `{#cdb}` é o endereço (`master/#cdb`). Sem ele, o endereço sai do título |
| `### Atores Centrais` | uma subseção |
| `**negrito**`, `*itálico*` | ênfase |
| `[12]` ou `[62][46]` | nota: o número da referência na lista do fim. Ao toque, a referência sobe numa folha |
| `` `Central` `` | etiqueta colorida. A cor vem do texto; `` `Supervisão\|secundario` `` mostra "Supervisão" com a cor de "secundario" |
| `[texto](#id)` | link |
| `- item` / `1. item` | listas |
| `> texto` | caixa de destaque; uma linha só com `>` separa parágrafos |
| um parágrafo | linhas seguidas; uma linha em branco separa parágrafos |

Blocos especiais começam com `:::nome` e terminam com uma linha só com `:::`.

```
:::fichas
Daniel Vorcaro `Central`
- Papel atribuído (alegado): Comando geral do esquema, segundo o relatório da PF [62].
- Resposta: Nega qualquer prática fraudulenta [9].

Augusto Lima `Central`
- Papel atribuído (alegado): ...
:::
```

| Bloco | Conteúdo |
|---|---|
| `:::fichas` | fichas separadas por linha em branco. 1ª linha: título e, no fim, uma etiqueta opcional. Linhas `- Rótulo: texto` viram campos; o campo "Resposta" ganha fundo próprio |
| `:::esteira` | passos em sequência: o título numa linha, o texto na linha seguinte, linha em branco entre passos |
| `:::barras Título` | uma linha por barra: `rótulo \| valor \| largura em %` |
| `:::quadro Título` | quadro-resumo; o primeiro, antes das seções, vai para o topo da página. Linhas `- Rótulo: texto` |
| `:::indice` | atalhos para todas as fichas da seção, agrupados pelas subseções. Fica vazio no texto: é montado sozinho |
| `:::fluxo Título` | diagrama em três andares. Linhas de legenda logo abaixo do título; depois `entrada:`, `centro:` e `saida:`, cada uma `nome \| descrição \| texto da seta`. Uma linha `apoio:` fica acima da `entrada:` seguinte (no Master, o FGC acima dos poupadores). O nome pode ser um link: `[Blindagem](#cap-4)` |
| `:::glossario` | uma sigla por linha: `FGC: definição`. Formas alternativas com barra: `TCE-RJ \| TCE: definição`. O plural com "s" (CDBs, LFs) é reconhecido sozinho |
| `:::referencias` | a lista de referências, `1. Autor, "Título", veículo, data.`, em ordem e sem pular números |

## O glossário ao toque

Basta escrever a sigla no texto normalmente. Ao montar, o script procura as siglas do bloco `:::glossario` e transforma o
**primeiro uso de cada uma em cada seção** num toque (sublinhado com pontos), que abre a definição numa folha. Títulos de
seção e subseção, notas, etiquetas e referências ficam de fora. Se uma sigla do glossário não aparecer em lugar nenhum,
o script avisa.

## O que o script confere

Antes de gravar, `dossie.py` para com uma mensagem se: uma nota `[n]` não tem a referência `n`; a lista de
referências está fora de ordem ou pula número; um link `#id` não leva a nenhuma seção, subseção ou ficha;
um bloco `:::` não foi fechado. Se uma referência não for citada por nenhuma nota, ele grava e avisa.

## Cores das etiquetas

Em `assets/dossie.css`, procure "O tom vem do texto da etiqueta". Cada linha liga o começo do texto da
etiqueta (sem acentos, com hífens: "Aponta para: A" vira `aponta-para-a`) a uma das cores definidas no topo
do arquivo. Etiqueta sem regra fica cinza.

## Montagem automática no GitHub

O arquivo `.github/workflows/dossies.yml` faz o GitHub rodar o script sozinho. Assim dá para editar o `texto.md` direto no
site do GitHub, até pelo celular, sem rodar nada:

- **num pull request** que mude um `texto.md`, o script só confere. Se houver erro, a verificação fica vermelha e o
  registro (aba Actions) diz a linha a corrigir;
- **no `main`**, ele grava o `index.html` refeito num commit próprio ("Remonta os dossiês a partir do texto.md") e pede ao
  GitHub Pages que publique de novo. Commits feitos pelo próprio workflow não disparam a publicação sozinhos; por isso
  esse pedido. Se ele falhar, a página refeita fica gravada e sai na próxima publicação;
- **à mão**: aba Actions → "Montar dossiês" → Run workflow.

Mudanças só no `assets/dossie.css` ou no `assets/dossie.js` não precisam do script e não acionam o workflow.

## Para criar outro dossiê

1. Crie a pasta, por exemplo `outro/`, com um `outro/texto.md` no mesmo formato.
2. Acrescente `'outro'` à lista `DOSSIES` no topo de `ferramentas/dossie.py`.
3. Rode `python3 ferramentas/dossie.py`.
