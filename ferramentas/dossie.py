"""Monta as páginas de texto longo ("dossiês") a partir de um texto.md.

Uso, na raiz do repositório:
    python3 ferramentas/dossie.py            monta todos os dossiês da lista DOSSIES
    python3 ferramentas/dossie.py master     monta só master/

Para cada pasta, lê <pasta>/texto.md e escreve <pasta>/index.html com o modelo
ferramentas/modelos/dossie.html. O visual fica em assets/dossie.css; as notas ao toque,
o sumário em folha e a seção atual ficam em assets/dossie.js.

Antes de gravar, confere o texto: toda nota [n] precisa ter a referência n, a lista de
referências precisa estar numerada em ordem e todo link interno precisa ter destino.
Se algo falhar, a página não é gravada e a mensagem diz o que corrigir.
A marcação aceita está descrita em ferramentas/LEIA-ME.md. Só usa a biblioteca padrão.
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / 'ferramentas' / 'modelos' / 'dossie.html'
DOSSIES = ['master']

NOTAS = re.compile(r'\s*((?:\[\d+\])+)(?!\()')            # [12] ou [12][46], sem link depois
LINK = re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)')            # [texto](#id)
ETIQUETA = re.compile(r'`([^`|]+)(?:\|([\w-]+))?`')         # `Central` ou `Supervisão|secundario`
TITULO = re.compile(r'(#{1,3}) (.+?)(?:\s*\{#([\w-]+)\})?$')  # # Parte, ## Seção {#id}, ### Subseção
ITEM_NUM = re.compile(r'(\d+)\. (.*)$')


class ErroTexto(Exception):
    pass


def slug(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def texto_puro(s):
    """Tira a marcação: serve para o sumário, os atalhos e os endereços."""
    s = LINK.sub(r'\1', s)
    s = NOTAS.sub('', s)
    s = ETIQUETA.sub(r'\1', s)
    return s.replace('**', '').replace('*', '').strip()


def eh_especial(linha):
    return (linha.startswith((':::', '>', '- ')) or TITULO.match(linha) is not None
            or ITEM_NUM.match(linha) is not None)


def separar(linhas):
    """Divide as linhas de um bloco ::: em grupos separados por linha em branco."""
    grupos, atual = [], []
    for l in linhas:
        if l.strip():
            atual.append(l.strip())
        elif atual:
            grupos.append(atual)
            atual = []
    if atual:
        grupos.append(atual)
    return grupos


def blocos(linhas):
    """Lê o texto e devolve os blocos na ordem: (tipo, ..., número da linha)."""
    i, n = 0, len(linhas)
    while i < n:
        l = linhas[i].rstrip()
        if not l.strip():
            i += 1
            continue
        ini = i + 1
        if l.startswith(':::'):
            tipo, _, arg = l[3:].strip().partition(' ')
            j = i + 1
            while j < n and linhas[j].strip() != ':::':
                if linhas[j].startswith(':::') or TITULO.match(linhas[j].rstrip()):
                    raise ErroTexto(f'linha {ini}: o bloco ":::{tipo}" não foi fechado com ":::" antes da linha {j + 1}')
                j += 1
            if j == n:
                raise ErroTexto(f'linha {ini}: o bloco ":::{tipo}" não foi fechado com ":::"')
            yield ('bloco', tipo, arg.strip(), [x.rstrip() for x in linhas[i + 1:j]], ini)
            i = j + 1
            continue
        m = TITULO.match(l)
        if m:
            nivel = {1: 'parte', 2: 'secao', 3: 'subsecao'}[len(m.group(1))]
            yield (nivel, m.group(2).strip(), m.group(3), ini)
            i += 1
            continue
        if l.startswith('>'):
            paras, atual = [], []
            while i < n and linhas[i].startswith('>'):
                t = linhas[i][1:].strip()
                if t:
                    atual.append(t)
                elif atual:
                    paras.append(' '.join(atual))
                    atual = []
                i += 1
            if atual:
                paras.append(' '.join(atual))
            yield ('destaque', paras, ini)
            continue
        if l.startswith('- '):
            itens = []
            while i < n and linhas[i].startswith('- '):
                itens.append(linhas[i][2:].strip())
                i += 1
            yield ('lista', itens, ini)
            continue
        if ITEM_NUM.match(l):
            itens = []
            while i < n and ITEM_NUM.match(linhas[i].rstrip()):
                itens.append(ITEM_NUM.match(linhas[i].rstrip()).group(2).strip())
                i += 1
            yield ('lista-num', itens, ini)
            continue
        par = []
        while i < n and linhas[i].strip() and not (par and eh_especial(linhas[i])):
            par.append(linhas[i].strip())
            i += 1
        yield ('paragrafo', ' '.join(par), ini)


class Dossie:
    def __init__(self, pasta):
        self.pasta = pasta
        self.fonte = RAIZ / pasta / 'texto.md'
        self.ids = set()
        self.links = []          # (destino, linha) dos links internos, conferidos no fim
        self.citacoes = {}       # n -> ids das citações, na ordem do texto
        self.referencias = {}    # n -> texto
        self.linha = 0
        self.glossario = {}      # id -> (formas, definição); formas = siglas que o texto usa
        self.termos_regex = None
        self.marcados = set()    # termos já marcados na seção atual (marca só o primeiro uso)
        self.usados = set()      # termos marcados em alguma parte da página

    # ------------------------------------------------------------ trechos
    def novo_id(self, base):
        i, k = base, 2
        while i in self.ids:
            i, k = f'{base}-{k}', k + 1
        self.ids.add(i)
        return i

    def etiqueta(self, texto, tom=None):
        return f'<span class="etiqueta" data-tom="{tom or slug(texto)}">{texto}</span>'

    def _link(self, m):
        destino = m.group(2)
        if destino.startswith('#'):
            self.links.append((destino[1:], self.linha))
        return f'<a href="{destino}">{m.group(1)}</a>'

    def _notas(self, m):
        partes = []
        for n in map(int, re.findall(r'\d+', m.group(1))):
            usos = self.citacoes.setdefault(n, [])
            cid = f'cit-{n}-{len(usos) + 1}'
            usos.append(cid)
            partes.append(f'<a href="#ref-{n}" id="{cid}">[{n}]</a>')
        return '<sup class="nota">' + ''.join(partes) + '</sup>'

    def inline(self, s, termos=False):
        s = html.escape(s, quote=False)
        s = ETIQUETA.sub(lambda m: self.etiqueta(m.group(1), m.group(2)), s)
        s = LINK.sub(self._link, s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
        s = NOTAS.sub(self._notas, s)
        return self.marcar_termos(s) if termos and self.termos_regex else s

    def marcar_termos(self, s):
        """Liga ao glossário o primeiro uso de cada sigla na seção (fora de links, notas e etiquetas)."""
        partes = re.split(r'(<[^>]+>)', s)
        dentro = 0
        for k, p in enumerate(partes):
            if p.startswith('<'):
                if re.match(r'<(a|sup|span class="etiqueta")[ >]', p):
                    dentro += 1
                elif re.match(r'</(a|sup|span)>', p) and dentro:
                    dentro -= 1
                continue
            if dentro or not p:
                continue

            def troca(m):
                tid = self.forma_para_id[m.group(1)]
                if tid in self.marcados:
                    return m.group(0)
                self.marcados.add(tid)
                self.usados.add(tid)
                return f'<a class="termo" href="#g-{tid}" data-termo="{tid}">{m.group(0)}</a>'
            partes[k] = self.termos_regex.sub(troca, p)
        return ''.join(partes)

    def carregar_glossario(self, linhas):
        """Linhas "SIGLA: definição" ou "SIGLA | OUTRA FORMA: definição"."""
        for l in linhas:
            if not l.strip():
                continue
            nomes, sep, definicao = l.strip().partition(': ')
            if not sep:
                raise ErroTexto(f'a linha "{l}" do glossário precisa ter a forma "SIGLA: definição"')
            formas = [f.strip() for f in nomes.split('|') if f.strip()]
            tid = slug(formas[0])
            if tid in self.glossario:
                raise ErroTexto(f'"{formas[0]}" aparece duas vezes no glossário')
            self.glossario[tid] = (formas, definicao)
        self.forma_para_id = {f: tid for tid, (formas, _) in self.glossario.items() for f in formas}
        alternativas = sorted(self.forma_para_id, key=len, reverse=True)
        self.termos_regex = re.compile(r'(?<![\w-])(' + '|'.join(map(re.escape, alternativas)) + r')s?(?![\w-])')

    def bloco_glossario(self):
        itens = []
        for tid, (formas, definicao) in self.glossario.items():
            self.ids.add(f'g-{tid}')
            itens.append(f'<div id="g-{tid}"><dt>{html.escape(" / ".join(formas), quote=False)}</dt>'
                         f'<dd>{self.inline(definicao)}</dd></div>')
        return '<dl class="glossario">\n' + '\n'.join(itens) + '\n</dl>'

    def bloco_fluxo(self, titulo, linhas):
        """Diagrama em três andares: entradas (com apoios acima delas), o centro e as saídas."""
        legenda, entradas, centro, saidas, apoio = [], [], None, [], None
        for l in linhas:
            if not l.strip():
                continue
            m = re.match(r'(apoio|entrada|centro|saida):\s*(.*)$', l.strip())
            if not m:
                if entradas or centro or saidas or apoio:
                    raise ErroTexto(f'perto da linha {self.linha}: no fluxo, a linha "{l}" precisa começar com apoio:, entrada:, centro: ou saida:')
                legenda.append(l.strip())
                continue
            campos = [c.strip() for c in m.group(2).split('|')] + ['', '']
            caixa = dict(nome=campos[0], desc=campos[1], seta=campos[2])
            if m.group(1) == 'apoio':
                apoio = caixa
            elif m.group(1) == 'entrada':
                entradas.append((apoio, caixa))
                apoio = None
            elif m.group(1) == 'centro':
                centro = caixa
            else:
                saidas.append(caixa)
        if not centro:
            raise ErroTexto(f'perto da linha {self.linha}: o fluxo precisa de uma linha "centro:"')

        def desenha(c, classe=''):
            desc = f'<span>{self.inline(c["desc"])}</span>' if c['desc'] else ''
            return f'<div class="fluxo-caixa{classe}"><b>{self.inline(c["nome"])}</b>{desc}</div>'

        def seta(texto):
            return f'<div class="fluxo-seta">{self.inline(texto)}</div>'

        out = [f'<figure class="fluxo">\n<figcaption><strong>{self.inline(titulo)}</strong>'
               + ''.join(f'<span>{self.inline(x)}</span>' for x in legenda) + '</figcaption>',
               '<div class="fluxo-entradas">']
        for ap, c in entradas:
            partes = [desenha(ap, ' fluxo-apoio'), seta(ap['seta'])] if ap else []
            partes += [desenha(c), seta(c['seta'])]
            out.append('<div class="fluxo-coluna">' + ''.join(partes) + '</div>')
        out += ['</div>', desenha(centro, ' fluxo-centro'), '<div class="fluxo-seta fluxo-ramo"></div>', '<div class="fluxo-saidas">']
        for c in saidas:
            rotulo = f'<div class="fluxo-rotulo">{self.inline(c["seta"])}</div>' if c['seta'] else ''
            out.append('<div class="fluxo-coluna">' + rotulo + desenha(c) + '</div>')
        out += ['</div>', '</figure>']
        return '\n'.join(out)

    # ------------------------------------------------------------ blocos :::
    def bloco_fichas(self, linhas):
        out = ['<div class="fichas">']
        for g in separar(linhas):
            titulo, etiq, tom = g[0], '', None
            m = re.match(r'(.*?)\s*`([^`|]+)(?:\|([\w-]+))?`\s*$', titulo)
            if m:
                titulo, tom = m.group(1), m.group(3) or slug(m.group(2))
                etiq = ' ' + self.etiqueta(html.escape(m.group(2), quote=False), tom)
            fid = self.novo_id('ficha-' + slug(texto_puro(titulo)))
            self.fichas_da_secao.append((self.subsecao, fid, texto_puro(titulo), tom))
            partes = []
            for l in g[1:]:
                if l.startswith('- '):
                    rotulo, sep, valor = l[2:].partition(': ')
                    if not sep:
                        raise ErroTexto(f'perto da linha {self.linha}: o campo "{l}" precisa ter a forma "- Rótulo: texto"')
                    partes.append(f'<p class="campo" data-campo="{slug(rotulo)}"><b>{self.inline(rotulo)}:</b> {self.inline(valor, True)}</p>')
                else:
                    partes.append(f'<p>{self.inline(l, True)}</p>')
            atrib = f' data-tom="{tom}"' if tom else ''
            out.append(f'<article class="ficha" id="{fid}"{atrib}>\n<h4>{self.inline(titulo, True)}{etiq}</h4>\n'
                       + '\n'.join(partes) + '\n</article>')
        out.append('</div>')
        return '\n'.join(out)

    def bloco_esteira(self, linhas):
        itens = []
        for g in separar(linhas):
            corpo = ' '.join(g[1:])
            itens.append(f'<li><strong>{self.inline(g[0])}</strong>' + (f'<p>{self.inline(corpo, True)}</p>' if corpo else '') + '</li>')
        return '<ol class="esteira">\n' + '\n'.join(itens) + '\n</ol>'

    def bloco_barras(self, titulo, linhas):
        out = [f'<figure class="barras">\n<figcaption>{self.inline(titulo)}</figcaption>']
        for l in linhas:
            if not l.strip():
                continue
            partes = [p.strip() for p in l.split('|')]
            if len(partes) != 3:
                raise ErroTexto(f'perto da linha {self.linha}: a barra "{l}" precisa ter a forma "rótulo | valor | largura"')
            rotulo, valor, largura = partes
            try:
                w = float(largura.rstrip('%').replace(',', '.'))
            except ValueError:
                raise ErroTexto(f'perto da linha {self.linha}: largura "{largura}" não é um número')
            out.append(f'<div class="barra"><div class="barra-rotulo"><span>{self.inline(rotulo)}</span><span>{self.inline(valor)}</span></div>'
                       f'<div class="barra-trilho"><span style="width:{w:g}%"></span></div></div>')
        out.append('</figure>')
        return '\n'.join(out)

    def bloco_quadro(self, titulo, linhas):
        linhas_dl = []
        for l in linhas:
            if not l.strip():
                continue
            rotulo, sep, valor = l.lstrip('- ').partition(': ')
            if not sep:
                raise ErroTexto(f'perto da linha {self.linha}: a linha "{l}" do quadro precisa ter a forma "- Rótulo: texto"')
            linhas_dl.append(f'<div><dt>{self.inline(rotulo)}</dt><dd>{self.inline(valor, True)}</dd></div>')
        return (f'<aside class="quadro" aria-label="{html.escape(texto_puro(titulo))}">\n'
                f'<p class="quadro-titulo">{self.inline(titulo)}</p>\n<dl>\n' + '\n'.join(linhas_dl) + '\n</dl>\n</aside>')

    def bloco_referencias(self, linhas):
        for l in linhas:
            if not l.strip():
                continue
            m = ITEM_NUM.match(l.strip())
            if not m:
                raise ErroTexto(f'perto da linha {self.linha}: a referência "{l}" precisa começar com o número, como "12. Autor, título..."')
            n = int(m.group(1))
            if n in self.referencias:
                raise ErroTexto(f'a referência {n} aparece duas vezes')
            self.referencias[n] = m.group(2)
        esperado = list(range(1, len(self.referencias) + 1))
        if sorted(self.referencias) != esperado or list(self.referencias) != esperado:
            raise ErroTexto('as referências precisam estar numeradas em ordem, de 1 em diante, sem pular números')
        for n in self.referencias:
            self.ids.add(f'ref-{n}')
        return '<!--REFERENCIAS-->'

    def lista_referencias(self):
        itens = []
        for n, texto in self.referencias.items():
            usos = self.citacoes.get(n, [])
            if len(usos) == 1:
                volta = f'<a href="#{usos[0]}" aria-label="Voltar à citação">↑</a>'
            elif usos:
                letras = [chr(97 + k) if k < 26 else str(k + 1) for k in range(len(usos))]
                volta = '↑ ' + ' '.join(f'<a href="#{u}" aria-label="Voltar à citação {l}">{l}</a>' for u, l in zip(usos, letras))
            else:
                volta = ''
            itens.append(f'<li id="ref-{n}"><span class="ref-volta">{volta}</span> <span class="ref-txt">{self.inline(texto)}</span></li>')
        return '<ol class="referencias">\n' + '\n'.join(itens) + '\n</ol>'

    def indice(self, fichas):
        grupos = []
        for grupo, fid, titulo, tom in fichas:
            if not grupos or grupos[-1][0] != grupo:
                grupos.append((grupo, tom, []))
            grupos[-1][2].append(f'<li><a href="#{fid}">{html.escape(titulo, quote=False)}</a></li>')
        out = ['<nav class="indice" aria-label="Atalhos desta seção">']
        for grupo, tom, itens in grupos:
            atrib = f' data-tom="{tom}"' if tom else ''
            nome = f'<p>{html.escape(grupo, quote=False)}</p>' if grupo else ''
            out.append(f'<div class="indice-grupo"{atrib}>{nome}<ul>' + ''.join(itens) + '</ul></div>')
        out.append('</nav>')
        return '\n'.join(out)

    # ------------------------------------------------------------ página
    def montar(self):
        texto = self.fonte.read_text(encoding='utf-8')
        texto = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), texto, flags=re.S)
        linhas = texto.split('\n')
        meta = {}
        k = 0
        while k < len(linhas) and not linhas[k].strip():
            k += 1
        if k < len(linhas) and linhas[k].strip() == '---':
            k += 1
            while k < len(linhas) and linhas[k].strip() != '---':
                chave, sep, valor = linhas[k].partition(':')
                if sep:
                    meta[chave.strip()] = valor.strip()
                k += 1
            linhas = [''] * (k + 1) + linhas[k + 1:]
        if 'titulo' not in meta:
            raise ErroTexto('falta "titulo:" no cabeçalho entre as linhas "---"')

        corpo, sumario = [], []
        quadro_topo = ''
        secao_aberta = False
        self.subsecao = None
        self.fichas_da_secao = []
        indice_pendente = False

        todos = list(blocos(linhas))
        for b in todos:
            if b[0] == 'bloco' and b[1] == 'glossario':
                self.linha = b[-1]
                self.carregar_glossario(b[3])

        def fechar_secao():
            nonlocal secao_aberta, indice_pendente
            if secao_aberta:
                if indice_pendente:
                    i = corpo.index('<!--INDICE-->')
                    corpo[i] = self.indice(self.fichas_da_secao)
                corpo.append('</section>')
            secao_aberta, indice_pendente = False, False
            self.subsecao = None
            self.fichas_da_secao = []
            self.marcados = set()

        for b in todos:
            tipo, self.linha = b[0], b[-1]
            if tipo == 'parte':
                fechar_secao()
                pid = self.novo_id('parte-' + slug(texto_puro(b[1])))
                corpo.append(f'<p class="parte" id="{pid}">{self.inline(b[1])}</p>')
                sumario.append((texto_puro(b[1]), []))
            elif tipo == 'secao':
                fechar_secao()
                sid = b[2] or slug(texto_puro(b[1]))
                if sid in self.ids:
                    raise ErroTexto(f'linha {self.linha}: o endereço "#{sid}" já foi usado em outra seção')
                self.ids.add(sid)
                corpo.append(f'<section id="{sid}">\n<h2>{self.inline(b[1])}</h2>')
                if not sumario:
                    sumario.append((None, []))
                sumario[-1][1].append((sid, texto_puro(b[1])))
                secao_aberta = True
            elif tipo == 'subsecao':
                hid = self.novo_id(b[2] or slug(texto_puro(b[1])))
                corpo.append(f'<h3 id="{hid}">{self.inline(b[1])}</h3>')
                self.subsecao = texto_puro(b[1])
            elif tipo == 'paragrafo':
                corpo.append(f'<p>{self.inline(b[1], True)}</p>')
            elif tipo == 'lista':
                corpo.append('<ul>\n' + '\n'.join(f'<li>{self.inline(x, True)}</li>' for x in b[1]) + '\n</ul>')
            elif tipo == 'lista-num':
                corpo.append('<ol>\n' + '\n'.join(f'<li>{self.inline(x, True)}</li>' for x in b[1]) + '\n</ol>')
            elif tipo == 'destaque':
                corpo.append('<div class="destaque">\n' + '\n'.join(f'<p>{self.inline(x, True)}</p>' for x in b[1]) + '\n</div>')
            elif tipo == 'bloco':
                _, nome, arg, conteudo, _ = b
                if nome == 'fichas':
                    corpo.append(self.bloco_fichas(conteudo))
                elif nome == 'esteira':
                    corpo.append(self.bloco_esteira(conteudo))
                elif nome == 'barras':
                    corpo.append(self.bloco_barras(arg, conteudo))
                elif nome == 'quadro':
                    q = self.bloco_quadro(arg, conteudo)
                    if not quadro_topo and not secao_aberta:
                        quadro_topo = q.replace('class="quadro"', 'class="quadro quadro-topo"', 1)
                    else:
                        corpo.append(q)
                elif nome == 'indice':
                    if not secao_aberta:
                        raise ErroTexto(f'linha {self.linha}: ":::indice" precisa ficar dentro de uma seção (depois de um "## Título")')
                    corpo.append('<!--INDICE-->')
                    indice_pendente = True
                elif nome == 'referencias':
                    corpo.append(self.bloco_referencias(conteudo))
                elif nome == 'glossario':
                    corpo.append(self.bloco_glossario())
                elif nome == 'fluxo':
                    corpo.append(self.bloco_fluxo(arg, conteudo))
                else:
                    raise ErroTexto(f'linha {self.linha}: não conheço o bloco ":::{nome}" (os que existem: '
                                    'fichas, esteira, barras, quadro, fluxo, indice, glossario, referencias)')
        fechar_secao()

        # conferências
        sem_ref = sorted(n for n in self.citacoes if n not in self.referencias)
        if sem_ref:
            raise ErroTexto('estas notas não têm referência na lista: ' + ', '.join(f'[{n}]' for n in sem_ref))
        for destino, linha in self.links:
            if destino not in self.ids:
                raise ErroTexto(f'linha {linha}: o link "#{destino}" não leva a nenhuma seção, subseção ou ficha')
        nunca = [n for n in self.referencias if n not in self.citacoes]
        sem_uso = [formas[0] for tid, (formas, _) in self.glossario.items() if tid not in self.usados]

        html_corpo = '\n'.join(corpo)
        if self.referencias:
            html_corpo = html_corpo.replace('<!--REFERENCIAS-->', self.lista_referencias())

        toc = ['<ol class="toc">']
        for parte, secoes in sumario:
            links = ''.join(f'<li><a href="#{sid}">{html.escape(t, quote=False)}</a></li>' for sid, t in secoes)
            if parte:
                toc.append(f'<li class="toc-parte"><span>{html.escape(parte, quote=False)}</span><ol>{links}</ol></li>')
            else:
                toc.append(links)
        toc.append('</ol>')

        descricao = meta.get('descricao', '')
        valores = {
            'titulo': self.inline(meta['titulo']),
            'titulo_aba': html.escape(texto_puro(meta.get('titulo_aba', meta['titulo'])), quote=False),
            'meta_descricao': f'\n<meta name="description" content="{html.escape(descricao)}">' if descricao else '',
            'chapeu': self.inline(meta.get('chapeu', '')),
            'assinatura': self.inline(meta.get('assinatura', '')),
            'quadro': quadro_topo,
            'sumario': '\n'.join(toc),
            'corpo': html_corpo,
            'raiz': '../' * len(Path(self.pasta).parts),
            'fonte': f'{self.pasta}/texto.md',
        }
        modelo = MODELO.read_text(encoding='utf-8')
        faltando = set(re.findall(r'\{\{(\w+)\}\}', modelo)) - set(valores)
        if faltando:
            raise ErroTexto('o modelo pede valores que o script não tem: ' + ', '.join(sorted(faltando)))
        pagina = re.sub(r'\{\{(\w+)\}\}', lambda m: valores[m.group(1)], modelo)
        resumo = dict(secoes=sum(len(s) for _, s in sumario), fichas=sum(1 for i in self.ids if i.startswith('ficha-')),
                      referencias=len(self.referencias), notas=sum(len(u) for u in self.citacoes.values()), nunca=nunca,
                      termos=len(self.glossario), sem_uso=sem_uso)
        return pagina, resumo


def main(pastas):
    ok = True
    for pasta in pastas:
        d = Dossie(pasta)
        try:
            pagina, r = d.montar()
        except ErroTexto as e:
            print(f'ERRO em {pasta}/texto.md: {e}', file=sys.stderr)
            ok = False
            continue
        destino = RAIZ / pasta / 'index.html'
        destino.write_text(pagina, encoding='utf-8')
        print(f'escrito {pasta}/index.html ({len(pagina.encode())} bytes): {r["secoes"]} seções, {r["fichas"]} fichas, '
              f'{r["notas"]} notas, {r["referencias"]} referências, {r["termos"]} termos no glossário')
        if r['nunca']:
            print('  aviso: referências que nenhuma nota cita: ' + ', '.join(map(str, r['nunca'])))
        if r['sem_uso']:
            print('  aviso: siglas do glossário que não aparecem no texto: ' + ', '.join(r['sem_uso']))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or DOSSIES))
