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
