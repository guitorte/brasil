"""Baixa das fontes oficiais os dados de comparação e grava em dados/comparacoes/.

Uso, na raiz do repositório:  python3 ferramentas/coletar_comparacoes.py [bloco ...]

Blocos (sem argumento, roda todos, nesta ordem):
  pares        regra de seleção dos países de comparação (Banco Mundial)
  resultados   condições de vida: pobreza, saúde, homicídios, aprendizagem, informalidade
  alavancas    juros, contas públicas e investimento público no Brasil; mesmas contas nos pares (FMI)
  mare         o que vem de fora: juros dos EUA
  produtividade  produto por trabalhador (OIT) e produtividade total dos fatores (Penn World Table)
  governos     quem ocupou a Presidência e o Banco Central
  congresso    eleitos por partido para deputado federal e senador, 1994–2014 (TSE)
  emendas      emendas parlamentares ao orçamento federal (Portal da Transparência)

Cada arquivo gravado ganha uma linha em dados/comparacoes/fontes_e_indicadores.csv, com a fonte,
o código original, a unidade, a data da coleta e notas. Só usa a biblioteca padrão do Python.
"""
import csv, json, sys, io, time, zipfile, datetime, collections, urllib.request, urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'dados' / 'comparacoes'
HOJE = datetime.date.today().isoformat()

# ---------------------------------------------------------------------------------------------
# REGRA DOS PARES — fixada antes de olhar qualquer resultado (crescimento, pobreza, etc.).
# Um país entra no grupo de comparação se, no ANO_BASE:
#   1) tinha pelo menos POP_MIN habitantes (Banco Mundial, SP.POP.TOTL); e
#   2) o PIB por habitante em paridade de poder de compra (NY.GDP.PCAP.PP.KD) ficava entre
#      FAIXA[0] e FAIXA[1] vezes o do Brasil. A faixa é simétrica em escala de razão (1/1,5 a 1,5).
# Agregados regionais ficam de fora. Países sem dado no ano-base ficam de fora e são listados.
# Os países que o repositório já usava (dados/mundo/paises.csv) continuam disponíveis, marcados
# como "lista anterior", para manter a continuidade com o capítulo "Brasil no mundo".
ANO_BASE = 1995
POP_MIN = 10_000_000
FAIXA = (1 / 1.5, 1.5)
# ---------------------------------------------------------------------------------------------

WB = 'https://api.worldbank.org/v2'


def baixar(url, tentativas=4, espera=3):
    """Baixa uma URL e devolve os bytes; tenta de novo em erros temporários."""
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'coletar_comparacoes/1.0 (github.com/guitorte/brasil)'})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            if i == tentativas - 1:
                raise RuntimeError(f'falhou ao baixar {url}: {e}') from e
            time.sleep(espera * (i + 1))


def wb_json(caminho, **params):
    """Lê todas as páginas de uma consulta à API do Banco Mundial."""
    params = {'format': 'json', 'per_page': 20000, **params}
    pagina, saida = 1, []
    while True:
        url = f'{WB}/{caminho}?' + urllib.parse.urlencode({**params, 'page': pagina})
        resposta = json.loads(baixar(url))
        meta, dados = resposta[0], (resposta[1] if len(resposta) > 1 else [])
        saida.extend(dados or [])
        if pagina >= int(meta.get('pages', 1)):
            return saida
        pagina += 1


def wb_paises():
    """Países (sem agregados) com código ISO3, nome, região e faixa de renda."""
    out = {}
    for c in wb_json('country'):
        if c['region']['value'] == 'Aggregates':
            continue
        out[c['id']] = dict(nome=c['name'], regiao=c['region']['value'], renda=c['incomeLevel']['value'])
    return out


def wb_indicador_meta(codigo):
    """Nome, definição e fonte de um indicador, como o Banco Mundial os publica."""
    m = json.loads(baixar(f'{WB}/indicator/{codigo}?format=json'))[1][0]
    return dict(nome=m['name'], fonte=m['sourceOrganization'], definicao=m['sourceNote'], base=m['source']['value'])


def wb_serie(codigo, paises='all', anos='1990:2025'):
    """Valores de um indicador: lista de (iso3, ano, valor), só onde há valor."""
    out = []
    for x in wb_json(f'country/{paises}/indicator/{codigo}', date=anos):
        if x['value'] is None:
            continue
        out.append((x['countryiso3code'], int(x['date']), x['value']))
    return out


def gravar(nome, cabecalho, linhas):
    SAIDA.mkdir(parents=True, exist_ok=True)
    with open(SAIDA / nome, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(cabecalho)
        w.writerows(linhas)
    print(f'  gravado {nome}: {len(linhas)} linhas')


FONTES_CAB = ['arquivo', 'fonte', 'codigo', 'indicador', 'unidade', 'nome_original', 'atualizacao',
              'cobertura_brasil', 'nota']


def registrar_fontes(linhas):
    """Substitui no fontes_e_indicadores.csv as linhas dos arquivos tocados por este bloco."""
    caminho = SAIDA / 'fontes_e_indicadores.csv'
    antigas = list(csv.DictReader(open(caminho, encoding='utf-8'))) if caminho.exists() else []
    tocados = {(l['arquivo'], l['codigo']) for l in linhas}
    novas = [l for l in antigas if (l['arquivo'], l['codigo']) not in tocados] + linhas
    with open(caminho, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, FONTES_CAB, lineterminator='\n')
        w.writeheader()
        w.writerows(novas)


def cobertura(serie, iso='BRA'):
    anos = [a for (p, a, v) in serie if p == iso]
    return f'{min(anos)}–{max(anos)}' if anos else 'sem dado'


# =============================================================================================
# 1. PARES
# =============================================================================================

def bloco_pares():
    print('pares: aplicando a regra de seleção')
    paises = wb_paises()
    pop = {p: v for (p, a, v) in wb_serie('SP.POP.TOTL', anos=f'{ANO_BASE}:{ANO_BASE}')}
    renda = {p: v for (p, a, v) in wb_serie('NY.GDP.PCAP.PP.KD', anos=f'{ANO_BASE}:{ANO_BASE}')}
    ref = renda['BRA']
    anteriores = {l['codigo'] for l in csv.DictReader(open(RAIZ / 'dados' / 'mundo' / 'paises.csv', encoding='utf-8'))
                  if l['tipo'] == 'país'}
    linhas = []
    for iso, info in sorted(paises.items(), key=lambda kv: kv[1]['nome']):
        p, r = pop.get(iso), renda.get(iso)
        if p is None or p < POP_MIN:
            continue  # só interessa quem passa no critério de população
        if r is None:
            situacao = 'fora: sem PIB por habitante em PPC no ano-base'
            razao = ''
        else:
            razao = r / ref
            if iso == 'BRA':
                situacao = 'referência'
            elif FAIXA[0] <= razao <= FAIXA[1]:
                situacao = 'par pela regra'
            else:
                situacao = 'fora: renda fora da faixa'
            razao = f'{razao:.3f}'
        linhas.append([iso, info['nome'], info['regiao'], info['renda'], round(p), '' if r is None else f'{r:.1f}',
                       razao, situacao, 'sim' if iso in anteriores else 'não'])
    gravar('pares.csv', ['codigo_pais', 'pais', 'regiao_banco_mundial', 'faixa_renda_atual_banco_mundial',
                         f'populacao_{ANO_BASE}', f'pib_pc_ppc_{ANO_BASE}', 'razao_brasil', 'situacao',
                         'lista_anterior'], linhas)
    m_pop, m_ren = wb_indicador_meta('SP.POP.TOTL'), wb_indicador_meta('NY.GDP.PCAP.PP.KD')
    registrar_fontes([dict(arquivo='pares.csv', fonte=f'Banco Mundial, World Development Indicators (API), {m_ren["fonte"]}',
                           codigo='SP.POP.TOTL; NY.GDP.PCAP.PP.KD', indicador='Regra de seleção dos pares',
                           unidade='pessoas; dólares internacionais constantes de 2021',
                           nome_original=f'{m_pop["nome"]}; {m_ren["nome"]}', atualizacao=HOJE,
                           cobertura_brasil=str(ANO_BASE),
                           nota=(f'Par = população ≥ {POP_MIN:,}'.replace(',', '.') + f' e PIB por habitante em PPC entre {FAIXA[0]:.3f}'.replace('.', ',') + ' e '
                                 f'{FAIXA[1]:.1f}'.replace('.', ',') + f' vezes o do Brasil em {ANO_BASE}. Regra fixada antes de olhar '
                                 'resultados. Só países que passam no critério de população aparecem na tabela. '
                                 'faixa_renda_atual_banco_mundial é a classificação de hoje, não a de '
                                 f'{ANO_BASE}.'))])


# =============================================================================================
# Utilidades comuns aos blocos seguintes
# =============================================================================================

AGREGADOS_WB = {'WLD': 'Mundo', 'LCN': 'América Latina e Caribe', 'UMC': 'Renda média-alta'}


def universo():
    """Países com pelo menos POP_MIN habitantes no ANO_BASE (todos os que aparecem em pares.csv).
    Guardar o universo inteiro, e não só os pares, permite testar outras faixas de renda depois."""
    linhas = list(csv.DictReader(open(SAIDA / 'pares.csv', encoding='utf-8')))
    return {l['codigo_pais']: l['pais'] for l in linhas}


def ler_xlsx(conteudo, aba=None):
    """Lê uma planilha .xlsx só com a biblioteca padrão. Devolve as linhas como listas de valores
    (texto ou número), na ordem das colunas A, B, C..."""
    import xml.etree.ElementTree as ET
    import re
    z = zipfile.ZipFile(io.BytesIO(conteudo))
    ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    compart = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).iter(ns + 'si'):
            compart.append(''.join(t.text or '' for t in si.iter(ns + 't')))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    alvo = {r.get('Id'): r.get('Target') for r in rels}
    folhas = [(s.get('name'), alvo[s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')])
              for s in wb.iter(ns + 'sheet')]
    nome, caminho = next((f for f in folhas if f[0] == aba), folhas[0]) if aba else folhas[0]
    caminho = caminho.lstrip('/')
    caminho = caminho if caminho.startswith('xl/') else 'xl/' + caminho

    def col(ref):
        letras = re.match(r'[A-Z]+', ref).group(0)
        n = 0
        for ch in letras:
            n = n * 26 + ord(ch) - 64
        return n - 1

    for _, el in ET.iterparse(z.open(caminho)):
        if el.tag != ns + 'row':
            continue
        linha = []
        for c in el.iter(ns + 'c'):
            i = col(c.get('r'))
            while len(linha) < i:
                linha.append(None)
            v, t = c.find(ns + 'v'), c.get('t')
            if t == 's' and v is not None:
                val = compart[int(v.text)]
            elif t == 'inlineStr':
                val = ''.join(x.text or '' for x in c.iter(ns + 't'))
            elif v is None:
                val = None
            elif t in ('str', 'e'):
                val = v.text
            else:
                val = float(v.text)
            linha.append(val)
        el.clear()
        yield linha


def ilo_sdmx(fluxo, inicio=1990):
    """Dados de um fluxo SDMX da OIT (todas as áreas), como dicionários."""
    url = f'https://sdmx.ilo.org/rest/data/ILO,{fluxo},1.0/all?startPeriod={inicio}&format=csvfilewithlabels'
    return list(csv.DictReader(io.StringIO(baixar(url).decode('utf-8-sig'))))


def sgs_meta(codigo):
    """Nome, unidade e periodicidade de uma série do Banco Central (SGS), pelo serviço oficial."""
    import re
    import html
    corpo = ('<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
             'xmlns:pub="http://publico.ws.casosdeuso.sgs.pec.bcb.gov.br"><soapenv:Body><pub:getUltimoValorXML>'
             f'<in0>{codigo}</in0></pub:getUltimoValorXML></soapenv:Body></soapenv:Envelope>').encode()
    req = urllib.request.Request('https://www3.bcb.gov.br/wssgs/services/FachadaWSSGS', data=corpo,
                                 headers={'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': '""'})
    with urllib.request.urlopen(req, timeout=60) as r:
        t = html.unescape(r.read().decode('latin-1'))
    pega = lambda k: (re.search(f'<{k}>(.*?)</{k}>', t, re.S) or [None, ''])[1].strip()  # noqa: E731
    return dict(nome=pega('NOME'), unidade=pega('UNIDADE'), periodicidade=pega('PERIODICIDADE'))


def sgs_serie(codigo):
    """Série completa do SGS, em blocos de 10 anos (limite da API para séries diárias)."""
    out, ini = [], 1980
    fim = datetime.date.today().year
    while ini <= fim:
        url = (f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json'
               f'&dataInicial=01/01/{ini}&dataFinal=31/12/{min(ini + 9, fim)}')
        for tentativa in range(5):  # a API às vezes devolve corpo vazio; tenta de novo
            try:
                out += json.loads(baixar(url))
                break
            except RuntimeError as e:
                if '404' in str(e):
                    break
                raise
            except json.JSONDecodeError:
                if tentativa == 4:
                    raise
                time.sleep(5 * (tentativa + 1))
        ini += 10
    return [(datetime.datetime.strptime(x['data'], '%d/%m/%Y').date(), float(x['valor'])) for x in out
            if x['valor'] not in ('', None)]


# =============================================================================================
# 2. RESULTADOS — condições de vida
# =============================================================================================

PIP_LINHAS = (3.00, 4.20, 8.30)  # linhas internacionais do Banco Mundial em US$ PPC de 2021 por dia


def bloco_resultados():
    uni = universo()
    fontes = []

    # --- Pobreza: Poverty and Inequality Platform (Banco Mundial), só anos de pesquisa -----------
    print('resultados: pobreza (PIP)')
    linhas = []
    for linha_pob in PIP_LINHAS:
        dados = json.loads(baixar(f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline={linha_pob}'
                                  '&fill_gaps=false&format=json'))
        for x in dados:
            if x['country_code'] not in uni or x['reporting_level'] != 'national':
                continue
            linhas.append([x['country_code'], uni[x['country_code']], f'{linha_pob:.2f}', x['reporting_year'],
                           round(x['headcount'] * 100, 3), x['welfare_type'], x['survey_acronym'],
                           x['survey_comparability'], x['comparable_spell'], x['estimation_type'],
                           x['distribution_type']])
    linhas.sort(key=lambda l: (l[0], l[2], l[3]))
    gravar('pobreza.csv', ['codigo_pais', 'pais', 'linha_usd_ppc_2021_dia', 'ano', 'pobreza_pct', 'tipo_bem_estar',
                           'pesquisa', 'comparabilidade', 'periodo_comparavel', 'tipo_estimativa', 'tipo_distribuicao'],
           linhas)
    fontes.append(dict(arquivo='pobreza.csv', fonte='Banco Mundial, Poverty and Inequality Platform (API pip/v1)',
                       codigo='headcount; povline = ' + ', '.join(f'{p:.2f}' for p in PIP_LINHAS),
                       indicador='Pessoas abaixo da linha de pobreza internacional',
                       unidade='% da população', nome_original='Poverty headcount ratio', atualizacao=HOJE,
                       cobertura_brasil=cobertura([(l[0], l[3], 0) for l in linhas]),
                       nota=('Só anos com pesquisa (fill_gaps=false) e só o nível nacional. Linhas de US$ 3,00, 4,20 e '
                             '8,30 por dia, em PPC de 2021. ATENÇÃO À COMPARAÇÃO: tipo_bem_estar diz se a pesquisa mede '
                             'renda (income) ou consumo (consumption); o Brasil mede renda, muitos pares medem consumo, '
                             'e as duas medidas não são equivalentes. Dentro de um país, só compare anos com o mesmo '
                             'periodo_comparavel (no Brasil, a troca da PNAD pela PNAD Contínua quebra a série).')))

    # --- Expectativa de vida e mortalidade infantil: ONU, World Population Prospects 2024 ---------
    print('resultados: expectativa de vida e mortalidade infantil (ONU, WPP 2024)')
    url_wpp = ('https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/'
               'WPP2024_Demographic_Indicators_Medium.csv.gz')
    import gzip
    wpp = csv.DictReader(io.StringIO(gzip.decompress(baixar(url_wpp)).decode('utf-8-sig')))
    vida = []
    for r in wpp:
        iso = r['ISO3_code']
        if r['Location'] == 'World':
            iso, nome = 'WLD', AGREGADOS_WB['WLD']
        elif iso in uni:
            nome = uni[iso]
        else:
            continue
        ano = int(float(r['Time']))
        if not 1990 <= ano <= 2023:
            continue
        for var, cod in (('LEx', 'expectativa_vida'), ('IMR', 'mortalidade_infantil')):
            if r[var]:
                vida.append([iso, nome, cod, ano, float(r[var]), 'ONU WPP 2024'])

    # --- Homicídios: UNODC ------------------------------------------------------------------------
    print('resultados: homicídios (UNODC)')
    url_unodc = 'https://data.unodc.org/sites/dataportal.unodc.org/files/2026-07/data_cts_intentional_homicide.xlsx'
    cab = None
    for l in ler_xlsx(baixar(url_unodc), 'data_cts_intentional_homicide'):
        if cab is None:
            if l and l[0] == 'Iso3_code':
                cab = l
            continue
        d = dict(zip(cab, l))
        if (d['Iso3_code'] in uni and d['Indicator'] == 'Victims of intentional homicide' and d['Dimension'] == 'Total'
                and d['Category'] == 'Total' and d['Sex'] == 'Total' and d['Age'] == 'Total'
                and d['Unit of measurement'] == 'Rate per 100,000 population' and 1990 <= int(d['Year']) <= 2025):
            vida.append([d['Iso3_code'], uni[d['Iso3_code']], 'homicidios_100mil', int(d['Year']), d['VALUE'],
                         f'UNODC ({d["Source"]})'])

    # --- Aprendizagem: PISA (OCDE), pela base EdStats do Banco Mundial ------------------------------
    print('resultados: PISA (EdStats)')
    for cod, nome_ind in (('LO.PISA.MAT', 'pisa_matematica'), ('LO.PISA.REA', 'pisa_leitura'),
                          ('LO.PISA.SCI', 'pisa_ciencias')):
        dados = wb_json(f'country/all/indicator/{cod}', date='2000:2025', source=12)
        for x in dados:
            if x['value'] is not None and x['countryiso3code'] in uni:
                vida.append([x['countryiso3code'], uni[x['countryiso3code']], nome_ind, int(x['date']), x['value'],
                             'OCDE PISA via Banco Mundial EdStats'])

    # --- Informalidade: OIT ---------------------------------------------------------------------
    print('resultados: informalidade (OIT)')
    for r in ilo_sdmx('DF_EMP_NIFL_SEX_RT'):
        if r['REF_AREA'] in uni and r['FREQ'] == 'A' and r['SEX'] == 'SEX_T' and r['OBS_VALUE']:
            vida.append([r['REF_AREA'], uni[r['REF_AREA']], 'informalidade_pct', int(r['TIME_PERIOD']),
                         float(r['OBS_VALUE']), 'OIT (' + r['SOURCE'].replace('\n', ' ') + ')'])

    vida.sort(key=lambda l: (l[2], l[0], l[3]))
    gravar('condicoes_de_vida.csv', ['codigo_pais', 'pais', 'indicador', 'ano', 'valor', 'origem'], vida)
    s = lambda ind: [(l[0], l[3], l[4]) for l in vida if l[2] == ind]  # noqa: E731
    fontes += [
        dict(arquivo='condicoes_de_vida.csv', fonte='ONU, Divisão de População, World Population Prospects 2024',
             codigo='expectativa_vida (LEx)', indicador='Expectativa de vida ao nascer', unidade='anos',
             nome_original='Life expectancy at birth, both sexes', atualizacao=HOJE,
             cobertura_brasil=cobertura(s('expectativa_vida')),
             nota=('Arquivo WPP2024_Demographic_Indicators_Medium. Guardados só 1990–2023: a revisão saiu em 2024, '
                   'então os anos seguintes são necessariamente projeções (inferência a partir da data da revisão).')),
        dict(arquivo='condicoes_de_vida.csv', fonte='ONU, Divisão de População, World Population Prospects 2024',
             codigo='mortalidade_infantil (IMR)', indicador='Mortalidade infantil', unidade='óbitos por mil nascidos vivos',
             nome_original='Infant mortality rate', atualizacao=HOJE,
             cobertura_brasil=cobertura(s('mortalidade_infantil')),
             nota=('Estimativa da Divisão de População da ONU. A série oficial dos ODS é a do grupo UN IGME, e a '
                   'diferença não é pequena: em 2023, o México tem 10,3 no WPP e 12,4 na série do IGME reproduzida '
                   'pelo Banco Mundial (conferido na coleta). Aqui se usa o WPP para ter a mesma fonte da expectativa '
                   'de vida; para uma comparação fina de mortalidade infantil, use o IGME.')),
        dict(arquivo='condicoes_de_vida.csv', fonte='UNODC, data_cts_intentional_homicide.xlsx (atualizado em 12/07/2026)',
             codigo='homicidios_100mil', indicador='Vítimas de homicídio intencional', unidade='por 100 mil habitantes',
             nome_original='Victims of intentional homicide; Rate per 100,000 population', atualizacao=HOJE,
             cobertura_brasil=cobertura(s('homicidios_100mil')),
             nota=('Total, sem recorte por sexo ou idade. A coluna origem diz de onde a UNODC tirou o número (CTS = '
                   'questionário aos governos; no Brasil, DATASUS). A UNODC revisa a série: o Banco Mundial ainda '
                   'reproduz uma versão anterior, que dá ao Brasil 20,1 em 2022 contra 21,1 aqui (conferido na coleta).')),
        dict(arquivo='condicoes_de_vida.csv', fonte='OCDE, PISA, pela base Education Statistics (EdStats) do Banco Mundial',
             codigo='LO.PISA.MAT; LO.PISA.REA; LO.PISA.SCI', indicador='Nota média no PISA (matemática, leitura, ciências)',
             unidade='pontos (média da OCDE ≈ 500)', nome_original='PISA: Mean performance on the ... scale',
             atualizacao=HOJE, cobertura_brasil=cobertura(s('pisa_matematica')),
             nota=('NÃO É A FONTE PRIMÁRIA: a OCDE não oferece os resultados do PISA por API; o Banco Mundial os reproduz '
                   '"conforme os relatórios do PISA". A base vai só até o PISA 2018: o PISA 2022 FALTA e deve ser '
                   'acrescentado à mão a partir do relatório da OCDE (PISA 2022 Results, Volume I, tabelas I.B1.5.4 a '
                   'I.B1.5.6). Muitos pares não participam do PISA. Conferir com os relatórios da OCDE antes de citar.')),
        dict(arquivo='condicoes_de_vida.csv', fonte='OIT, ILOSTAT (SDMX), fluxo DF_EMP_NIFL_SEX_RT',
             codigo='EMP_NIFL_RT (SEX_T)', indicador='Taxa de informalidade', unidade='% do emprego total',
             nome_original='Informal employment rate (previous ILO definition - ICLS13)', atualizacao=HOJE,
             cobertura_brasil=cobertura(s('informalidade_pct')),
             nota=('Processado pela OIT a partir das pesquisas nacionais; a coluna origem traz a pesquisa. No Brasil, '
                   'a troca da PNAD pela PNAD Contínua (2015→2016) quebra a série.')),
    ]
    registrar_fontes(fontes)


# =============================================================================================
# 3. ALAVANCAS — o que o governo e o Banco Central controlam
# =============================================================================================

SGS = {  # código: nome curto
    4189: 'selic_anualizada', 433: 'ipca_mes', 5793: 'primario_12m_pct_pib', 5760: 'juros_nominais_12m_pct_pib',
    5727: 'nominal_12m_pct_pib', 4513: 'dlsp_pct_pib', 13762: 'dbgg_pct_pib',
}
FMI_FISCAL = {  # indicador do DataMapper: (nome curto, base)
    'pb': ('primario_pct_pib', 'FPP'), 'ie': ('juros_pagos_pct_pib', 'FPP'), 'rev': ('receita_pct_pib', 'FPP'),
    'exp': ('despesa_pct_pib', 'FPP'), 'd': ('divida_bruta_pct_pib', 'FPP'),
    'GGXONLB_G01_GDP_PT': ('primario_pct_pib', 'FM'), 'GGXCNL_G01_GDP_PT': ('nominal_pct_pib', 'FM'),
}


def bloco_alavancas():
    fontes = []
    print('alavancas: séries do Banco Central (SGS)')
    linhas = []
    for cod, curto in SGS.items():
        meta = sgs_meta(cod)
        serie = sgs_serie(cod)
        if meta['periodicidade'] == 'M':
            linhas += [[curto, cod, d.strftime('%Y-%m'), v] for d, v in serie]
        fontes.append(dict(arquivo='alavancas_brasil.csv', fonte='Banco Central do Brasil, SGS (api.bcb.gov.br)',
                           codigo=str(cod), indicador=curto, unidade=meta['unidade'], nome_original=meta['nome'],
                           atualizacao=HOJE, cobertura_brasil=f'{serie[0][0]:%Y-%m}–{serie[-1][0]:%Y-%m}',
                           nota='Mensal. Nome e unidade lidos do serviço oficial do SGS no momento da coleta.'))
    gravar('alavancas_brasil.csv', ['serie', 'codigo_sgs', 'mes', 'valor'], linhas)

    print('alavancas: contas públicas nos pares (FMI)')
    uni = universo()
    fmi = []
    for cod, (curto, base) in FMI_FISCAL.items():
        # a API devolve todos os países de uma vez; o filtro é feito aqui
        d = json.loads(baixar(f'https://www.imf.org/external/datamapper/api/v1/{cod}'))
        for iso, anos in (d.get('values', {}).get(cod) or {}).items():
            if iso not in uni:
                continue
            for ano, v in anos.items():
                if v is not None and 1990 <= int(ano):
                    # ano corrente em diante ainda não fechou: é projeção do FMI
                    proj = 'sim' if int(ano) >= datetime.date.today().year else 'não'
                    fmi.append([iso, uni.get(iso, iso), curto, base, cod, int(ano), v, proj])
    fmi.sort(key=lambda l: (l[3], l[2], l[0], l[5]))
    gravar('contas_publicas_fmi.csv', ['codigo_pais', 'pais', 'indicador', 'base', 'codigo_fmi', 'ano', 'valor',
                                       'projecao'], fmi)
    meta = json.loads(baixar('https://www.imf.org/external/datamapper/api/v1/indicators'))['indicators']
    for cod, (curto, base) in FMI_FISCAL.items():
        fontes.append(dict(arquivo='contas_publicas_fmi.csv',
                           fonte=('FMI, Public Finances in Modern History (DataMapper)' if base == 'FPP'
                                  else 'FMI, Fiscal Monitor (DataMapper)'),
                           codigo=cod, indicador=curto, unidade=meta[cod].get('unit') or '% do PIB',
                           nome_original=meta[cod].get('label'), atualizacao=HOJE,
                           cobertura_brasil=cobertura([(l[0], l[5], 0) for l in fmi if l[4] == cod]),
                           nota=('Governo geral. FPP é a base histórica (até o último ano fechado); FM é o Fiscal Monitor, '
                                 'que inclui projeções nos anos à frente (coluna projecao = sim a partir do ano da coleta; o último ano '
                                 'fechado ainda pode ser estimativa). Não misture as duas bases na mesma comparação. '
                                 'O resultado do BCB (alavancas_brasil.csv) é do setor público consolidado, conceito '
                                 'diferente: compare o Brasil com os pares só pelos números do FMI.')))
    registrar_fontes(fontes)


# =============================================================================================
# 4. MARÉ — o que vem de fora
# =============================================================================================

FRED = {'FEDFUNDS': 'juros_basicos_eua', 'GS10': 'titulo_10_anos_eua'}


def bloco_mare():
    print('maré: juros dos EUA (Federal Reserve, via FRED)')
    linhas, fontes = [], []
    for cod, curto in FRED.items():
        texto = baixar(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={cod}').decode('utf-8')
        for r in csv.DictReader(io.StringIO(texto)):
            data = r.get('observation_date') or r.get('DATE')
            if r[cod] not in ('', '.') and data >= '1990':
                linhas.append([curto, cod, data[:7], float(r[cod])])
        fontes.append(dict(arquivo='mare.csv', fonte='Federal Reserve, série H.15, distribuída pelo FRED (Fed de St. Louis)',
                           codigo=cod, indicador=curto, unidade='% ao ano',
                           nome_original=('Federal Funds Effective Rate' if cod == 'FEDFUNDS'
                                          else 'Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity'),
                           atualizacao=HOJE, cobertura_brasil='não se aplica',
                           nota=('Média mensal. O FRED reproduz sem alteração a série H.15 da Junta do Federal Reserve. '
                                 'Crescimento mundial e preços de commodities já estão em dados/mundo/.')))
    gravar('mare.csv', ['serie', 'codigo', 'mes', 'valor'], linhas)
    registrar_fontes(fontes)


# =============================================================================================
# 5. PRODUTIVIDADE
# =============================================================================================

PWT_VARS = {'rtfpna': 'ptf_precos_nacionais_constantes', 'ctfp': 'ptf_nivel_eua_igual_1',
            'hc': 'capital_humano', 'emp': 'empregados_milhoes', 'avh': 'horas_por_trabalhador_ano',
            'rgdpo': 'pib_producao_milhoes_usd_2021', 'rnna': 'capital_milhoes_usd_2021'}


def bloco_produtividade():
    uni = universo()
    fontes = []
    print('produtividade: produto por trabalhador (OIT)')
    linhas = []
    for r in ilo_sdmx('DF_GDP_211P_NOC_NB'):
        ano = int(r['TIME_PERIOD'])
        if r['REF_AREA'] in uni and r['FREQ'] == 'A' and r['OBS_VALUE'] and ano <= 2024:
            linhas.append([r['REF_AREA'], uni[r['REF_AREA']], 'produto_por_trabalhador', ano, float(r['OBS_VALUE']),
                           'OIT, estimativas modeladas de nov. 2025'])
    fontes.append(dict(arquivo='produtividade.csv', fonte='OIT, ILOSTAT (SDMX), fluxo DF_GDP_211P_NOC_NB',
                       codigo='GDP_211P_NB', indicador='produto_por_trabalhador',
                       unidade='dólares internacionais constantes de 2021 (PPC) por pessoa ocupada',
                       nome_original='Output per worker, GDP constant 2021 international $ at PPP (ILO modelled estimates)',
                       atualizacao=HOJE, cobertura_brasil=cobertura([(l[0], l[3], 0) for l in linhas]),
                       nota=('Estimativas modeladas de novembro de 2025. A OIT publica a série até 2027; guardados só '
                             'os anos até 2024, porque os seguintes, publicados em 2025, são necessariamente projeções '
                             '(inferência a partir da data da publicação).')))

    print('produtividade: Penn World Table 11.0')
    conteudo = baixar('https://dataverse.nl/api/access/datafile/554105')
    cab = None
    for l in ler_xlsx(conteudo, 'Data'):
        if cab is None:
            cab = l
            continue
        d = dict(zip(cab, l))
        iso = d.get('countrycode')
        if iso not in uni or d.get('year') is None or int(d['year']) < 1990:
            continue
        for var, curto in PWT_VARS.items():
            v = d.get(var)
            if isinstance(v, float):
                linhas.append([iso, uni[iso], curto, int(d['year']), v, 'Penn World Table 11.0'])
    linhas.sort(key=lambda l: (l[2], l[0], l[3]))
    gravar('produtividade.csv', ['codigo_pais', 'pais', 'indicador', 'ano', 'valor', 'origem'], linhas)
    fontes.append(dict(arquivo='produtividade.csv',
                       fonte='Feenstra, Inklaar e Timmer, Penn World Table 11.0, Groningen Growth and Development Centre '
                             '(DataverseNL, doi:10.34894/FABVLR, publicado em 10/10/2025)',
                       codigo='; '.join(PWT_VARS), indicador='; '.join(PWT_VARS.values()),
                       unidade='ver nota', nome_original='; '.join(PWT_VARS), atualizacao=HOJE,
                       cobertura_brasil=cobertura([(l[0], l[3], 0) for l in linhas if l[5].startswith('Penn')]),
                       nota=('rtfpna = produtividade total dos fatores a preços nacionais constantes (índice; compare só '
                             'a trajetória de cada país). ctfp = nível da PTF em PPC correntes, EUA = 1 (compare países '
                             'num mesmo ano). hc = índice de capital humano (anos de estudo e retorno da educação). '
                             'emp em milhões de pessoas; avh em horas por ano; rgdpo e rnna em milhões de US$ de 2021 '
                             '(PPC). A PTF é um resíduo de modelo, não uma medida direta: trate como estimativa.')))
    registrar_fontes(fontes)


# =============================================================================================
# 6. CONGRESSO — eleitos por partido, 1994–2014 (2018 e 2022 já estão em dados/eleicoes/)
# =============================================================================================

ANOS_TSE = (1994, 1998, 2002, 2006, 2010, 2014)
ELEITO = {'ELEITO', 'ELEITO POR QP', 'ELEITO POR MÉDIA', 'MÉDIA'}
CARGOS = {'GOVERNADOR': 'governador', 'SENADOR': 'senador', 'DEPUTADO FEDERAL': 'deputado federal',
          'DEPUTADO ESTADUAL': 'deputado estadual', 'DEPUTADO DISTRITAL': 'deputado distrital'}


def bloco_congresso():
    print('congresso: candidaturas do TSE')
    eleitos = {}
    for ano in ANOS_TSE:
        z = zipfile.ZipFile(io.BytesIO(baixar(
            f'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip')))
        for nome in z.namelist():
            # um arquivo por UF; os arquivos _BR e _BRASIL repetem dados e ficam de fora
            if not nome.endswith('.csv') or nome.endswith(('_BR.csv', '_BRASIL.csv')):
                continue
            for r in csv.DictReader(io.StringIO(z.read(nome).decode('latin-1')), delimiter=';'):
                cargo = CARGOS.get(r['DS_CARGO'])
                # só eleições ordinárias, como em dados/eleicoes/ (as suplementares ficam de fora)
                if cargo and r['DS_SIT_TOT_TURNO'] in ELEITO and 'ORDINÁRIA' in r['NM_TIPO_ELEICAO']:
                    # um candidato aparece uma vez por turno; fica a última situação (2º turno, se houver)
                    chave = (ano, r['SG_UF'], r['SQ_CANDIDATO'])  # em 2002 e 2006 o código se repete entre UFs
                    if chave not in eleitos or r['NR_TURNO'] > eleitos[chave][3]:
                        eleitos[chave] = [ano, r['SG_UF'], cargo, r['NR_TURNO'], r['NR_CANDIDATO'],
                                          r['NM_URNA_CANDIDATO'], r['NM_CANDIDATO'], r['SG_PARTIDO'], r['NR_PARTIDO'],
                                          r['NM_PARTIDO'], r['DS_SIT_TOT_TURNO'], r['DS_SITUACAO_CANDIDATURA']]
    linhas = sorted(eleitos.values(), key=lambda l: (l[0], l[2], l[1], l[5]))
    gravar('eleitos_1994_2014.csv', ['ano', 'uf', 'cargo', 'turno', 'numero', 'nome_urna', 'nome', 'sigla_partido',
                                     'numero_partido', 'nome_partido', 'situacao_tse', 'situacao_candidatura'], linhas)
    cont = collections.defaultdict(lambda: collections.Counter())
    nomes = {}
    for l in linhas:
        cargo = 'deputados_estaduais_distritais' if l[2].startswith('deputado e') or l[2].endswith('distrital') else \
            {'governador': 'governadores', 'senador': 'senadores', 'deputado federal': 'deputados_federais'}[l[2]]
        cont[(l[0], l[7])][cargo] += 1
        nomes[(l[0], l[7])] = (l[8], l[9])
    por_partido = []
    for (ano, sigla), c in sorted(cont.items(), key=lambda kv: (kv[0][0], -sum(kv[1].values()), kv[0][1])):
        por_partido.append([ano, sigla, *nomes[(ano, sigla)], c['governadores'], c['senadores'],
                            c['deputados_federais'], c['deputados_estaduais_distritais'], sum(c.values())])
    gravar('eleitos_por_partido_1994_2014.csv', ['ano', 'sigla_partido', 'numero_partido', 'nome_partido',
                                                 'governadores', 'senadores', 'deputados_federais',
                                                 'deputados_estaduais_distritais', 'total'], por_partido)
    nota = ('Arquivos consulta_cand_<ano>.zip do Portal de Dados Abertos do TSE, um por UF. Eleito = situação ELEITO, '
            'ELEITO POR QP, ELEITO POR MÉDIA ou MÉDIA (a grafia muda de eleição para eleição). Mesmo critério de '
            'dados/eleicoes/, que cobre 2018 e 2022. As siglas são as da época: não há aqui equivalência com os nomes '
            'atuais, porque fusões e trocas de nome exigem fonte própria. O Senado renova 2/3 e 1/3 das cadeiras em '
            'eleições alternadas: a bancada de um partido no Senado soma duas eleições. Eleito não é o mesmo que '
            'bancada no exercício do mandato (suplências, trocas de partido). Conferido na coleta: 513 deputados '
            'federais por eleição, exceto em 1998, quando a base marca 516 como eleitos (os 3 a mais são um registro '
            'sem nome, #NULO#, no ES, e dois no PR com situação de candidatura RENÚNCIA e FALECIDO). Mantido como está na '
            'fonte: decida na análise como tratar esses casos. Só eleições ordinárias; as suplementares (por exemplo, '
            'as de governador do AM e do TO registradas na base de 2014) ficam de fora, como em dados/eleicoes/.')
    registrar_fontes([dict(arquivo=a, fonte='Tribunal Superior Eleitoral, Portal de Dados Abertos (consulta_cand)',
                           codigo='consulta_cand_' + '/'.join(map(str, ANOS_TSE)), indicador=i, unidade=u,
                           nome_original='DS_SIT_TOT_TURNO', atualizacao=HOJE, cobertura_brasil='1994–2014', nota=nota)
                      for a, i, u in (('eleitos_1994_2014.csv', 'Eleitos, um por linha', 'pessoas'),
                                      ('eleitos_por_partido_1994_2014.csv', 'Eleitos por partido e cargo',
                                       'número de eleitos'))])


# =============================================================================================
# 7. EMENDAS — quanto do orçamento federal os parlamentares direcionam
# =============================================================================================

def bloco_emendas():
    print('emendas: Portal da Transparência (CGU)')
    z = zipfile.ZipFile(io.BytesIO(baixar(
        'https://portaldatransparencia.gov.br/download-de-dados/emendas-parlamentares/UNICO')))
    rd = csv.DictReader(io.StringIO(z.read('EmendasParlamentares.csv').decode('latin-1')), delimiter=';')
    campos = ['Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 'Valor Restos A Pagar Inscritos',
              'Valor Restos A Pagar Cancelados', 'Valor Restos A Pagar Pagos']
    soma = collections.defaultdict(lambda: [0.0] * len(campos))
    n = collections.Counter()
    for r in rd:
        k = (int(r['Ano da Emenda']), r['Tipo de Emenda'])
        n[k] += 1
        for i, c in enumerate(campos):
            soma[k][i] += float((r[c] or '0').replace('.', '').replace(',', '.'))
    linhas = [[a, t, n[(a, t)], *[round(v, 2) for v in soma[(a, t)]]] for (a, t) in sorted(soma)]
    gravar('emendas_por_ano_e_tipo.csv', ['ano', 'tipo_emenda', 'registros', 'empenhado_reais', 'liquidado_reais',
                                          'pago_reais', 'restos_a_pagar_inscritos_reais',
                                          'restos_a_pagar_cancelados_reais', 'restos_a_pagar_pagos_reais'], linhas)
    registrar_fontes([dict(arquivo='emendas_por_ano_e_tipo.csv',
                           fonte='Controladoria-Geral da União, Portal da Transparência, download "Emendas parlamentares" '
                                 '(arquivo EmendasParlamentares.csv)',
                           codigo='EmendasParlamentares.csv', indicador='Emendas parlamentares por ano e tipo',
                           unidade='reais correntes (sem correção pela inflação)',
                           nome_original='Valor Empenhado; Valor Liquidado; Valor Pago; Valor Restos A Pagar ...',
                           atualizacao=HOJE, cobertura_brasil=f'{linhas[0][0]}–{linhas[-1][0]}',
                           nota=('Soma das linhas do arquivo por ano da emenda e tipo (individual, de bancada, de '
                                 'comissão, de relator). O ano corrente está incompleto. Valores nominais: corrija pela '
                                 'inflação antes de comparar anos. Pago no ano e restos a pagar pagos são fluxos '
                                 'diferentes; some os dois para ter o desembolso total de um ano de emendas. FALTA o '
                                 'denominador (despesa discricionária do governo federal, do Tesouro Nacional) para '
                                 'calcular a fatia do orçamento direcionada por emendas.'))])


BLOCOS = collections.OrderedDict(pares=bloco_pares, resultados=bloco_resultados, alavancas=bloco_alavancas,
                                 mare=bloco_mare, produtividade=bloco_produtividade, congresso=bloco_congresso,
                                 emendas=bloco_emendas)

if __name__ == '__main__':
    pedidos = sys.argv[1:] or list(BLOCOS)
    for nome in pedidos:
        BLOCOS[nome]()
