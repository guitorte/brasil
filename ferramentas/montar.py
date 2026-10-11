"""Gera as páginas do site a partir dos dados em dados/.

Uso, na raiz do repositório:  python3 ferramentas/montar.py

Lê os modelos em ferramentas/modelos/, embute os dados de cada capítulo e escreve:
  index.html          página de entrada, com as manchetes e o sumário
  mundo/index.html    capítulo "Brasil no mundo"
  v4.html             redireciona para mundo/ (endereço antigo)
O estilo e o motor dos gráficos ficam em assets/estilo.css e assets/graficos.js.
Só usa a biblioteca padrão do Python.
"""
import csv, json, math, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = RAIZ / 'ferramentas' / 'modelos'
SITE = 'https://guitorte.github.io/brasil/'

# Ordem dos capítulos. Os que ainda não têm página própria apontam para a versão completa (v3.html).
CAPS = [
    dict(slug='inflacao', nome='Inflação', link='v3.html#ib-inflacao'),
    dict(slug='poder-de-compra', nome='Poder de compra', link='v3.html#ib-poder'),
    dict(slug='salario-minimo', nome='Salário mínimo', link='v3.html#ib-salario'),
    dict(slug='emprego', nome='Emprego', link='v3.html#ib-emprego'),
    dict(slug='cambio', nome='Valor da moeda', link='v3.html#ib-moeda'),
    dict(slug='mundo', nome='Brasil no mundo', link='mundo/', novo=True),
]


def ler(nome):
    return list(csv.DictReader(open(RAIZ / 'dados' / nome, encoding='utf-8')))


def num(s):
    return float(s) if s not in ('', None) else None


def br(x, d=0):
    s = f'{x:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def preencher(modelo, subs, dados=None):
    s = (MODELOS / modelo).read_text(encoding='utf-8')
    if dados is not None:
        s = s.replace('/*__DATA__*/null', json.dumps(dados, ensure_ascii=False, separators=(',', ':')))
    for k, v in subs.items():
        s = s.replace('{{' + k + '}}', v)
    assert '{{' not in s, s[s.index('{{'):s.index('{{') + 40]
    return s


def escrever(caminho, texto):
    p = RAIZ / caminho
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding='utf-8')
    print('escrito', caminho, len(texto), 'bytes')


# ---------------------------------------------------------------- partes comuns
def barra(raiz, atual=None):
    casa = raiz or './'
    atual_attr = ' aria-current="page"'
    itens = ''.join(
        f'<a href="{raiz}{c["link"]}"{atual_attr if c["slug"] == atual else ""}><b>{i}</b>{c["nome"]}</a>'
        for i, c in enumerate(CAPS, 1))
    return (f'<header class="bar">\n  <a class="brand" href="{casa}">INDICADORES DO BRASIL</a>\n'
            f'  <details class="menu"><summary>Capítulos</summary><nav aria-label="Capítulos">{itens}<hr>'
            f'<a href="{casa}">Página inicial</a><a href="{raiz}v3.html">Versão completa</a></nav></details>\n'
            f'  <div class="progress" aria-hidden="true"><span></span></div>\n</header>')


def navegacao(raiz, slug):
    i = [c['slug'] for c in CAPS].index(slug)
    ant = CAPS[i - 1] if i > 0 else None
    prox = CAPS[i + 1] if i + 1 < len(CAPS) else None
    a = f'<a href="{raiz}{ant["link"]}"><span>← Capítulo anterior</span><b>{ant["nome"]}</b></a>' if ant else ''
    b = (f'<a class="dir" href="{raiz}{prox["link"]}"><span>Próximo capítulo →</span><b>{prox["nome"]}</b></a>' if prox
         else f'<a class="dir" href="{raiz or "./"}"><span>Fim →</span><b>Voltar ao início</b></a>')
    return f'<nav class="next wrap" aria-label="Outros capítulos">{a}{b}</nav>'


# ---------------------------------------------------------------- capítulo Brasil no mundo
def dados_mundo():
    m = 'mundo/'
    wb = collections.defaultdict(dict)
    for r in ler(m + 'banco_mundial.csv'):
        wb[(r['indicador'], r['codigo_pais'])][int(r['ano'])] = float(r['valor'])
    paises = ['BRA', 'WLD', 'LCN', 'USA', 'KOR', 'CHN', 'IND', 'CHL', 'MEX', 'ARG', 'COL', 'PER', 'ZAF', 'TUR', 'IDN']
    nomes = {'BRA': 'Brasil', 'WLD': 'Mundo', 'LCN': 'América Latina', 'USA': 'Estados Unidos', 'KOR': 'Coreia do Sul',
             'CHN': 'China', 'IND': 'Índia', 'CHL': 'Chile', 'MEX': 'México', 'ARG': 'Argentina', 'COL': 'Colômbia',
             'PER': 'Peru', 'ZAF': 'África do Sul', 'TUR': 'Turquia', 'IDN': 'Indonésia'}

    def serie(ind, code, a=1961, b=2025):
        s = wb[(ind, code)]
        return {y: round(s[y], 4) for y in range(a, b + 1) if y in s}

    D = {'nomes': nomes,
         'pc': {c: serie('NY.GDP.PCAP.KD.ZG', c) for c in paises},      # crescimento do PIB por habitante, % ao ano
         'gdp': {c: serie('NY.GDP.MKTP.KD.ZG', c) for c in ('BRA', 'WLD', 'LCN')},
         'tt': serie('TT.PRI.MRCH.XD.WD', 'BRA', 2005, 2024), 'renda': {}, 'share': {'fmi': {}, 'bm': {}, 'usd': {}}}
    for r in ler(m + 'renda_relativa_eua.csv'):
        for k, v in r.items():
            if k != 'ano' and v:
                D['renda'].setdefault(k.replace('pct_eua_', '').upper(), {})[int(r['ano'])] = float(v)
    D['com'] = {int(r['ano']): [float(r['indice_nao_energia_real']), float(r['indice_energia_real'])] for r in ler(m + 'commodities.csv')}
    for r in ler(m + 'fmi_weo.csv'):
        if r['codigo_pais'] == 'BRA' and r['indicador'] == 'PPPSH':
            D['share']['fmi'][int(r['ano'])] = float(r['valor'])
    for r in ler(m + 'brasil_no_mundo.csv'):
        if r['participacao_pib_mundial_ppc']: D['share']['bm'][int(r['ano'])] = float(r['participacao_pib_mundial_ppc'])
        if r['participacao_pib_mundial_usd']: D['share']['usd'][int(r['ano'])] = float(r['participacao_pib_mundial_usd'])

    def idx(code, base=1980, end=2025):
        v = 100.0
        for y in range(base + 1, end + 1):
            v *= 1 + D['pc'][code][y] / 100
        return v

    i = {c: idx(c) for c in ('BRA', 'WLD', 'LCN', 'USA', 'KOR', 'CHN')}
    fmi, ren, usd = D['share']['fmi'], D['renda'], D['share']['usd']
    pct = lambda c, y: br(ren[c][y]) + '%'
    F = {
        'bra_idx': br(i['BRA']), 'bra_pct': '+' + br(i['BRA'] - 100) + '%', 'bra_pct_n': br(i['BRA'] - 100) + '%',
        'bra_14_25': '+' + br((i['BRA'] / idx('BRA', 1980, 2014) - 1) * 100) + '%',
        'wld_idx': br(i['WLD']), 'lcn_idx': br(i['LCN']), 'usa_idx': br(i['USA']),
        'kor_idx': br(i['KOR']), 'kor_mult': br(i['KOR'] / 100), 'chn_idx': br(i['CHN']), 'chn_mult': br(i['CHN'] / 100),
        'bra_eua_1990': pct('BRA', 1990), 'bra_eua_2025': pct('BRA', 2025), 'kor_eua_1990': pct('KOR', 1990), 'kor_eua_2025': pct('KOR', 2025),
        'chn_eua_1990': pct('CHN', 1990), 'chn_eua_2025': pct('CHN', 2025), 'chl_eua_1990': pct('CHL', 1990), 'chl_eua_2025': pct('CHL', 2025),
        'mex_eua_1990': pct('MEX', 1990), 'mex_eua_2025': pct('MEX', 2025),
        'share_1980': br(fmi[1980], 1) + '%', 'share_2025': br(fmi[2025], 1) + '%', 'share_2031': br(fmi[2031], 1) + '%',
        'usd_1990': br(usd[1990], 1) + '%', 'usd_2011': br(usd[2011], 1) + '%', 'usd_2025': br(usd[2025], 1) + '%',
        'dif_2015': br(D['gdp']['BRA'][2015] - D['gdp']['WLD'][2015], 1), 'dif_2016': br(D['gdp']['BRA'][2016] - D['gdp']['WLD'][2016], 1),
        'ne_2002': br(D['com'][2002][0], 1), 'ne_2011': br(D['com'][2011][0], 1), 'ne_2016': br(D['com'][2016][0], 1),
        'tt_2005': br(D['tt'][2005], 1), 'tt_2011': br(D['tt'][2011], 1), 'tt_2024': br(D['tt'][2024], 1),
    }
    # o texto afirma estas coisas; se os dados mudarem, a montagem para aqui
    assert 195 < i['WLD'] < 210, 'o texto diz que o mundo dobrou'
    assert abs(i['LCN'] - i['BRA']) < 10, 'o texto diz que a América Latina ficou perto do Brasil'
    assert i['USA'] > i['WLD'] > i['BRA'], 'o texto diz que os EUA cresceram mais'
    assert ren['MEX'][2025] < ren['MEX'][1990] and ren['ARG'][2025] < ren['ARG'][1990], 'o texto diz que México e Argentina perderam terreno'
    assert D['com'][2011][0] > 1.7 * D['com'][2002][0], 'o texto diz que os preços quase dobraram'
    serie_idx = {c: [(1980, 100.0)] for c in ('BRA', 'WLD')}
    for c in serie_idx:
        v = 100.0
        for y in range(1981, 2026):
            v *= 1 + D['pc'][c][y] / 100
            serie_idx[c].append((y, v))
    return D, F, serie_idx


# ---------------------------------------------------------------- miniaturas da página de entrada
def mini(series, log=False, w=300, h=56):
    """Gráfico de linha pequeno, sem eixos, em SVG estático. series: [(pontos, cor)]."""
    tr = (lambda v: math.log10(v)) if log else (lambda v: v)
    xs = [x for pts, _ in series for x, _ in pts]
    ys = [tr(y) for pts, _ in series for _, y in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    sx = lambda x: 3 + (x - x0) / (x1 - x0) * (w - 6)
    sy = lambda y: h - 5 - (tr(y) - y0) / (y1 - y0) * (h - 10)
    paths = ''.join(
        f'<path d="{"".join(("L" if k else "M") + f"{sx(x):.1f},{sy(y):.1f}" for k, (x, y) in enumerate(pts))}" '
        f'style="fill:none;stroke:{cor};stroke-width:{2.5 if k == len(series) - 1 else 2};vector-effect:non-scaling-stroke;stroke-linejoin:round;stroke-linecap:round"/>'
        for k, (pts, cor) in enumerate(series))
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false">{paths}</svg>'


def inicio(F_mundo, serie_idx):
    infl = {int(r['ano']): r for r in ler('inflacao.csv')}
    sm = {int(r['ano']): r for r in ler('salario_minimo.csv')}
    emp = {int(r['ano']): r for r in ler('emprego.csv')}
    cam = {int(r['ano']): r for r in ler('cambio.csv')}
    mens = {r['mes']: r for r in ler('series_mensais.csv')}

    mult = float(mens['1994-06']['indice_ipca']) / float(mens['1986-01']['indice_ipca'])
    pos_real = {a: num(r['ipca']) for a, r in infl.items() if 1995 <= a <= 2025 and r['periodo'] == 'jan-dez'}
    a_min, a_max = min(pos_real, key=pos_real.get), max(pos_real, key=pos_real.get)
    pico = max((a for a in infl if infl[a]['periodo'] == 'jan-dez'), key=lambda a: num(infl[a]['ipca']))
    pc_ult = max(a for a in infl if num(infl[a]['poder_compra_jul94']) is not None)
    des = {a: num(r['desocupacao_pnadc']) for a, r in emp.items() if num(r['desocupacao_pnadc']) is not None}
    d_max = max(des, key=des.get)
    assert min(des, key=des.get) == 2025, 'o texto diz que 2025 teve a menor desocupação da série'
    assert num(sm[2025]['sm_real_medio']) > 2 * num(sm[1995]['sm_real_medio']), 'o texto diz que o mínimo mais que dobrou'

    f = {
        'pico_ano': str(pico), 'pico_ipca': br(num(infl[pico]['ipca'])) + '%',
        'mult': br(mult / 1e6), 'min_ipca': br(pos_real[a_min], 2) + '%', 'min_ano': str(a_min),
        'max_ipca': br(pos_real[a_max], 2) + '%', 'max_ano': str(a_max),
        'pc_valor': 'R$ ' + br(num(infl[pc_ult]['poder_compra_jul94']), 2),
        'sm_1995': 'R$ ' + br(num(sm[1995]['sm_real_medio'])), 'sm_2025': 'R$ ' + br(num(sm[2025]['sm_real_medio'])),
        'des_max': br(des[d_max], 1) + '%', 'des_max_ano': str(d_max), 'des_2025': br(des[2025], 1) + '%',
        'usd_1995': 'R$ ' + br(num(cam[1995]['cambio_medio_reais']), 2), 'usd_2025': 'R$ ' + br(num(cam[2025]['cambio_medio_reais']), 2),
    }
    c1, gray = 'var(--c1)', 'var(--gray)'
    serie = lambda tab, campo, cond=lambda a, r: True: [(a, num(r[campo])) for a, r in sorted(tab.items()) if num(r[campo]) is not None and cond(a, r)]
    textos = {
        'inflacao': ('A inflação que derreteu o dinheiro',
                     f'De janeiro de 1986 a junho de 1994, os preços se multiplicaram por {f["mult"]} milhões. Depois do Real, a inflação anual ficou entre {f["min_ipca"]} ({f["min_ano"]}) e {f["max_ipca"]} ({f["max_ano"]}).',
                     mini([(serie(infl, 'ipca', lambda a, r: r['periodo'] == 'jan-dez'), c1)], log=True), 'IPCA anual, 1986–2025, em escala logarítmica'),
        'poder-de-compra': ('O que R$ 100 compram',
                            f'R$ 100 de hoje compram o que {f["pc_valor"]} compravam em julho de 1994.',
                            mini([(serie(infl, 'poder_compra_jul94'), c1)]), 'Poder de compra de R$ 100, em reais de julho de 1994'),
        'salario-minimo': ('O salário mínimo ganhou valor',
                           f'Descontada a inflação, o salário mínimo médio foi de {f["sm_1995"]} em 1995 para {f["sm_2025"]} em 2025, em reais de agosto de 2026 (cálculo próprio).',
                           mini([(serie(sm, 'sm_real_medio'), c1)]), 'Salário mínimo real, média anual, 1986–2026'),
        'emprego': ('Desemprego no menor nível desde 2012',
                    f'A desocupação medida pela PNAD Contínua foi de {f["des_max"]} em {f["des_max_ano"]} para {f["des_2025"]} em 2025, a menor da série.',
                    mini([(serie(emp, 'desocupacao_pnadc'), c1)]), 'Taxa de desocupação, PNAD Contínua, 2012–2025'),
        'cambio': ('O real e o dólar',
                   f'O dólar custava em média {f["usd_1995"]} em 1995 e {f["usd_2025"]} em 2025.',
                   mini([(serie(cam, 'cambio_medio_reais', lambda a, r: a >= 1995), c1)]), 'Dólar, taxa média anual em reais, 1995–2026'),
        'mundo': ('Crescemos, mas o mundo cresceu mais',
                  f'Desde 1980, a renda média do brasileiro subiu {F_mundo["bra_pct_n"]}. A do mundo dobrou.',
                  mini([(serie_idx['WLD'], gray), (serie_idx['BRA'], c1)]), 'Renda por habitante, 1980 = 100: Brasil (azul) e mundo (cinza)'),
    }
    cards = []
    for k, c in enumerate(CAPS, 1):
        titulo, resumo, svg, legenda = textos[c['slug']]
        estado = '<span class="estado novo">Novo formato</span>' if c.get('novo') else '<span class="estado">Na versão completa</span>'
        cards.append(f'<a class="cap" href="{c["link"]}"><span class="num">Capítulo {k} · {c["nome"]}</span><h3>{titulo}</h3><p>{resumo}</p>'
                     f'{svg}<small>{legenda}</small><span class="cap-foot"><span class="ir">Ler capítulo →</span>{estado}</span></a>')
    manchetes = [
        ('v3.html#ib-inflacao', f['pico_ipca'], f'foi a inflação de {f["pico_ano"]}, o pico da série. Em 2025, foi de {br(num(infl[2025]["ipca"]), 2)}%.'),
        ('v3.html#ib-poder', f['pc_valor'], 'compravam em julho de 1994 o mesmo que R$ 100 compram hoje.'),
        ('v3.html#ib-salario', f['sm_2025'], f'foi o salário mínimo real médio de 2025, contra {f["sm_1995"]} em 1995.'),
        ('mundo/', F_mundo['bra_pct'], 'foi quanto subiu a renda por pessoa no Brasil desde 1980. A do mundo dobrou.'),
    ]
    heads = ''.join(f'<a class="head" href="{h}"><b>{n}</b><span>{t}</span></a>' for h, n, t in manchetes)
    return preencher('inicio.html', {'barra': barra(''), 'manchetes': heads, 'capitulos': '\n'.join(cards)})


REDIRECT = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Brasil no mundo · Indicadores do Brasil</title><link rel="canonical" href="{site}{alvo}">
<meta http-equiv="refresh" content="0; url={alvo}"><script>location.replace('{alvo}' + location.hash);</script></head>
<body><p>Esta página mudou de endereço: <a href="{alvo}">{alvo}</a>.</p></body></html>
"""

if __name__ == '__main__':
    D, F, serie_idx = dados_mundo()
    escrever('mundo/index.html', preencher('mundo.html', {**F, 'raiz': '../', 'barra': barra('../', 'mundo'), 'navegacao': navegacao('../', 'mundo')}, D))
    escrever('index.html', inicio(F, serie_idx))
    escrever('v4.html', REDIRECT.format(site=SITE, alvo='mundo/'))
