"""O capitão ou a maré? Roda os testes descritos em METODO.md e grava as tabelas em resultados/.

Uso, na raiz do repositório:  python3 analises/capitao-e-mare/analise.py
Lê só arquivos de dados/ (nada é baixado aqui). Só usa a biblioteca padrão do Python.
"""
import csv, math, statistics as st, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / 'dados'
SAIDA = Path(__file__).resolve().parent / 'resultados'
SAIDA.mkdir(exist_ok=True)

BLOCOS = [(1995, 1998), (1999, 2002), (2003, 2006), (2007, 2010), (2011, 2014), (2015, 2018), (2019, 2022),
          (2023, 2024)]
ROTULO = {1995: 'FHC 1', 1999: 'FHC 2', 2003: 'Lula 1', 2007: 'Lula 2', 2011: 'Dilma 1', 2015: 'Dilma 2 / Temer (misto)',
          2019: 'Bolsonaro', 2023: 'Lula 3 (incompleto)'}


def ler(caminho):
    return list(csv.DictReader(open(caminho, encoding='utf-8')))


def gravar(nome, cab, linhas):
    with open(SAIDA / nome, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(cab)
        w.writerows(linhas)
    print(f'  gravado resultados/{nome}')


def r2(x, d=2):
    return None if x is None else round(x, d)


# --------------------------------------------------------------------------------------------- dados
pares_tab = ler(D / 'comparacoes' / 'pares.csv')
PARES = [l['codigo_pais'] for l in pares_tab if l['situacao'] == 'par pela regra']

renda = collections.defaultdict(dict)  # renda[pais][ano] = PIB por habitante em PPC
for l in ler(D / 'comparacoes' / 'renda_universo.csv'):
    if l['indicador'] == 'pib_pc_ppc':
        renda[l['codigo_pais']][int(l['ano'])] = float(l['valor'])


def cagr(serie, a, b):
    """Crescimento médio anual entre o fim do ano a-1 e o fim do ano b (anos a..b inclusive)."""
    if (a - 1) in serie and b in serie:
        return ((serie[b] / serie[a - 1]) ** (1 / (b - a + 1)) - 1) * 100
    return None


# ================================================================ T1: o Brasil contra a mediana dos pares
print('T1: Brasil contra a mediana dos pares, ano a ano e por bloco')
anual = []
for ano in range(1996, 2025):
    br = cagr(renda['BRA'], ano, ano)
    ps = [cagr(renda[p], ano, ano) for p in PARES]
    ps = [x for x in ps if x is not None]
    anual.append([ano, r2(br), r2(st.median(ps)), r2(br - st.median(ps)), len(ps)])
gravar('t1_anual.csv', ['ano', 'brasil_pct', 'mediana_pares_pct', 'diferenca_pp', 'pares_com_dado'], anual)
abaixo = sum(1 for l in anual if l[3] < 0)


def blocos_contra(grupo, nome_arq, defasagem=0):
    out = []
    for a, b in BLOCOS:
        a2, b2 = a + defasagem, min(b + defasagem, 2024)
        if a2 > 2024:
            continue
        br = cagr(renda['BRA'], a2, b2)
        ps = [cagr(renda[p], a2, b2) for p in grupo]
        ps = [x for x in ps if x is not None]
        if br is None or not ps:
            continue
        pos = sorted(ps + [br], reverse=True).index(br) + 1
        out.append([ROTULO[a], f'{a2}–{b2}', r2(br), r2(st.median(ps)), r2(br - st.median(ps)), pos, len(ps) + 1])
    return out


cab_bloco = ['bloco', 'anos', 'brasil_pct_ao_ano', 'mediana_pct_ao_ano', 'diferenca_pp', 'posicao_brasil',
             'paises']
t1b = blocos_contra(PARES, 't1_blocos.csv')
gravar('t1_blocos.csv', cab_bloco, t1b)
t1d = blocos_contra(PARES, 't1_blocos_defasados.csv', defasagem=1)
gravar('t1_blocos_defasados.csv', cab_bloco, t1d)

# ================================================================ T2: modelo simples da maré
print('T2: modelo do crescimento do Brasil sobre a economia mundial e as commodities')
bm = {int(l['ano']): l for l in ler(D / 'mundo' / 'brasil_no_mundo.csv')}
X, Y, anos = [], [], []
for ano in range(1996, 2025):
    try:
        g_br = float(bm[ano]['crescimento_pc_brasil'])
        g_w = float(bm[ano]['crescimento_pc_mundo'])
        com = math.log(float(bm[ano]['indice_commodities_nao_energia_real']) /
                       float(bm[ano - 1]['indice_commodities_nao_energia_real'])) * 100
    except (ValueError, KeyError):
        continue
    X.append([1.0, g_w, com])
    Y.append(g_br)
    anos.append(ano)


def mqo(X, Y):
    """Mínimos quadrados ordinários pelas equações normais (3 coeficientes)."""
    k = len(X[0])
    xtx = [[sum(x[i] * x[j] for x in X) for j in range(k)] for i in range(k)]
    xty = [sum(x[i] * y for x, y in zip(X, Y)) for i in range(k)]
    # eliminação de Gauss
    m = [row[:] + [v] for row, v in zip(xtx, xty)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c:
                f = m[r][c] / m[c][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    beta = [m[i][k] / m[i][i] for i in range(k)]
    prev = [sum(b * x for b, x in zip(beta, xi)) for xi in X]
    res = [y - p for y, p in zip(Y, prev)]
    my = st.mean(Y)
    r2_ = 1 - sum(e * e for e in res) / sum((y - my) ** 2 for y in Y)
    n = len(Y)
    s2 = sum(e * e for e in res) / (n - k)
    # erros-padrão: s2 * (X'X)^-1 (inversa por Gauss-Jordan)
    inv = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(xtx)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(inv[r][c]))
        inv[c], inv[piv] = inv[piv], inv[c]
        d = inv[c][c]
        inv[c] = [v / d for v in inv[c]]
        for r in range(k):
            if r != c:
                f = inv[r][c]
                inv[r] = [a - f * b for a, b in zip(inv[r], inv[c])]
    ep = [math.sqrt(s2 * inv[i][k + i]) for i in range(k)]
    return beta, ep, r2_, res, prev


beta, ep, R2, res, prev = mqo(X, Y)
gravar('t2_modelo.csv', ['termo', 'coeficiente', 'erro_padrao', 't'],
       [[n, r2(b, 3), r2(e, 3), r2(b / e)] for n, b, e in zip(
           ['constante', 'crescimento_pc_mundo', 'variacao_commodities_nao_energia_real_log_pct'], beta, ep)]
       + [['R2', r2(R2, 3), '', ''], ['observacoes', len(Y), '', '']])
gravar('t2_anual.csv', ['ano', 'brasil_pct', 'previsto_pela_mare_pct', 'residuo_pp'],
       [[a, r2(y), r2(p), r2(e)] for a, y, p, e in zip(anos, Y, prev, res)])
resid = dict(zip(anos, res))
t2b = []
for desl in (0, 1):
    for a, b in BLOCOS:
        a2, b2 = max(a + desl, 1996), min(b + desl, 2024)
        vals = [resid[x] for x in range(a2, b2 + 1) if x in resid]
        if vals:
            t2b.append(['com defasagem de 1 ano' if desl else 'sem defasagem', ROTULO[a], f'{a2}–{b2}',
                        r2(st.mean(vals)), len(vals)])
gravar('t2_blocos.csv', ['corte', 'bloco', 'anos', 'residuo_medio_pp', 'anos_com_dado'], t2b)

# ================================================================ T3: exportadores de commodities
print('T3: pares exportadores de commodities')
est = collections.defaultdict(lambda: collections.defaultdict(dict))
for l in ler(D / 'comparacoes' / 'estrutura.csv'):
    est[l['codigo_pais']][l['indicador']][int(l['ano'])] = float(l['valor'])
EXP = ['export_alimentos_pct', 'export_materias_primas_agricolas_pct', 'export_combustiveis_pct',
       'export_minerios_metais_pct']


def peso_commodities(pais, a=1995, b=2004):
    anos = [y for y in range(a, b + 1) if all(y in est[pais][i] for i in EXP)]
    return st.mean(sum(est[pais][i][y] for i in EXP) for y in anos) if anos else None


t3 = []
for p in ['BRA'] + PARES:
    w = peso_commodities(p)
    t3.append([p, r2(w, 1), '' if w is None else ('sim' if w >= 60 else 'não')])
gravar('t3_peso_commodities_1995_2004.csv', ['codigo_pais', 'commodities_pct_exportacoes', 'exportador_de_commodities'],
       t3)
EXPORTADORES = [l[0] for l in t3 if l[2] == 'sim' and l[0] != 'BRA']
t3b = blocos_contra(EXPORTADORES, 't3_blocos.csv')
gravar('t3_blocos.csv', cab_bloco, t3b)

# ================================================================ C4: contabilidade do crescimento (PWT)
print('C4: contabilidade do crescimento, 1995–2019 (Penn World Table)')
pwt = collections.defaultdict(lambda: collections.defaultdict(dict))
for l in ler(D / 'comparacoes' / 'produtividade.csv'):
    if l['origem'].startswith('Penn'):
        pwt[l['codigo_pais']][l['indicador']][int(l['ano'])] = float(l['valor'])


def taxa(serie, a, b):
    return ((serie[b] / serie[a]) ** (1 / (b - a)) - 1) * 100 if a in serie and b in serie else None


def comp(p, a=1995, b=2019):
    x = pwt[p]
    try:
        y_l = {t: x['pib_producao_milhoes_usd_2021'][t] / x['empregados_milhoes'][t] for t in (a, b)}
        k_l = {t: x['capital_milhoes_usd_2021'][t] / x['empregados_milhoes'][t] for t in (a, b)}
    except KeyError:
        return None
    return [taxa(y_l, a, b), taxa(k_l, a, b), taxa(x['capital_humano'], a, b),
            taxa(x['ptf_precos_nacionais_constantes'], a, b)]


c4 = []
for p in ['BRA'] + PARES:
    c = comp(p)
    if c and None not in c:
        c4.append([p] + [r2(v) for v in c])
med = ['mediana dos pares'] + [r2(st.median(l[i] for l in c4 if l[0] != 'BRA')) for i in range(1, 5)]
gravar('c4_contabilidade_1995_2019.csv', ['pais', 'produto_por_trabalhador_pct_ao_ano', 'capital_por_trabalhador_pct_ao_ano',
                                          'capital_humano_pct_ao_ano', 'ptf_pct_ao_ano'], c4 + [med])

# ================================================================ C5: juros
print('C5: juros reais no Brasil e nos EUA; juros pagos pelo governo')
ala = collections.defaultdict(dict)
for l in ler(D / 'comparacoes' / 'alavancas_brasil.csv'):
    ala[l['serie']][l['mes']] = float(l['valor'])
mare = collections.defaultdict(dict)
for l in ler(D / 'comparacoes' / 'mare.csv'):
    mare[l['serie']][l['mes']] = float(l['valor'])
c5 = []
for ano in range(1996, 2026):
    meses = [f'{ano}-{m:02d}' for m in range(1, 13)]
    if not all(m in ala['selic_anualizada'] and m in ala['ipca_mes'] for m in meses):
        continue
    selic = st.mean(ala['selic_anualizada'][m] for m in meses)
    ipca = (math.prod(1 + ala['ipca_mes'][m] / 100 for m in meses) - 1) * 100
    real_br = ((1 + selic / 100) / (1 + ipca / 100) - 1) * 100
    try:
        ff = st.mean(mare['juros_basicos_eua'][m] for m in meses)
        cpi = (mare['inflacao_eua_indice'][f'{ano}-12'] / mare['inflacao_eua_indice'][f'{ano - 1}-12'] - 1) * 100
        real_us = ((1 + ff / 100) / (1 + cpi / 100) - 1) * 100
    except KeyError:
        ff = cpi = real_us = None
    c5.append([ano, r2(selic), r2(ipca), r2(real_br), r2(ff), r2(cpi), r2(real_us),
               r2(real_br - real_us) if real_us is not None else None])
gravar('c5_juros_reais.csv', ['ano', 'selic_media_pct', 'ipca_pct', 'selic_real_pct', 'fed_funds_media_pct',
                              'inflacao_eua_dez_dez_pct', 'juro_real_eua_pct', 'diferenca_real_pp'], c5)
fmi = collections.defaultdict(lambda: collections.defaultdict(dict))
for l in ler(D / 'comparacoes' / 'contas_publicas_fmi.csv'):
    if l['base'] == 'FPP':
        fmi[l['indicador']][l['codigo_pais']][int(l['ano'])] = float(l['valor'])
c5b = []
for a, b in BLOCOS:
    def media(p):
        v = [fmi['juros_pagos_pct_pib'][p].get(y) for y in range(a, b + 1)]
        v = [x for x in v if x is not None]
        return st.mean(v) if v else None
    br = media('BRA')
    ps = [x for x in (media(p) for p in PARES) if x is not None]
    if br is not None and ps:
        c5b.append([ROTULO[a], f'{a}–{b}', r2(br), r2(st.median(ps)), sorted(ps + [br], reverse=True).index(br) + 1,
                    len(ps) + 1])
gravar('c5_juros_pagos_blocos.csv', ['bloco', 'anos', 'brasil_pct_pib', 'mediana_pares_pct_pib', 'posicao_brasil',
                                     'paises'], c5b)

# ================================================================ C6: investimento
print('C6: investimento em % do PIB')
c6 = []
for a, b in BLOCOS:
    def media(p):
        v = [est[p]['investimento_pct_pib'].get(y) for y in range(a, b + 1)]
        v = [x for x in v if x is not None]
        return st.mean(v) if v else None
    br = media('BRA')
    ps = [x for x in (media(p) for p in PARES) if x is not None]
    if br is not None and ps:
        c6.append([ROTULO[a], f'{a}–{b}', r2(br), r2(st.median(ps)), sorted(ps + [br], reverse=True).index(br) + 1,
                   len(ps) + 1])
gravar('c6_investimento_blocos.csv', ['bloco', 'anos', 'brasil_pct_pib', 'mediana_pares_pct_pib', 'posicao_brasil',
                                      'paises'], c6)

# ================================================================ C7: emendas parlamentares em valores reais
print('C7: emendas parlamentares empenhadas, em reais de 2025 (IPCA)')
ipca = {int(l['ano']): float(l['indice_ipca']) for l in ler(D / 'inflacao.csv') if l['indice_ipca']}
c7 = []
for l in ler(D / 'comparacoes' / 'emendas_por_ano_e_tipo.csv'):
    a = int(l['ano'])
    if a in ipca and a <= 2025:
        c7.append([a, l['tipo_emenda'], r2(float(l['empenhado_reais']) / 1e9),
                   r2(float(l['empenhado_reais']) * ipca[2025] / ipca[a] / 1e9)])
gravar('c7_emendas_reais.csv', ['ano', 'tipo_emenda', 'empenhado_bilhoes_nominais', 'empenhado_bilhoes_reais_de_2025'], c7)

# ================================================================ resumo na tela
print(f'\nT1: o Brasil cresceu abaixo da mediana dos pares em {abaixo} de {len(anual)} anos (1996–2024).')
print(f'T2: R² = {R2:.2f}; coeficientes {[round(b, 2) for b in beta]}; erros-padrão {[round(e, 2) for e in ep]}')
print('Exportadores de commodities entre os pares:', EXPORTADORES)
