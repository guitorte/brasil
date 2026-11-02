"""A amarração do orçamento: roda as medidas descritas em METODO.md e grava as tabelas em resultados/.

Uso, na raiz do repositório:  python3 analises/amarracao/analise.py
Lê só arquivos de dados/. Só usa a biblioteca padrão do Python.
"""
import csv, statistics as st, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / 'dados'
SAIDA = Path(__file__).resolve().parent / 'resultados'
SAIDA.mkdir(exist_ok=True)
BLOCOS = [(1997, 1998), (1999, 2002), (2003, 2006), (2007, 2010), (2011, 2014), (2015, 2018), (2019, 2022),
          (2023, 2025)]
ROTULO = {1997: 'FHC 1 (1997–98)', 1999: 'FHC 2', 2003: 'Lula 1', 2007: 'Lula 2', 2011: 'Dilma 1',
          2015: 'Dilma 2 / Temer (misto)', 2019: 'Bolsonaro', 2023: 'Lula 3 (até 2025)'}


def ler(c):
    return list(csv.DictReader(open(c, encoding='utf-8')))


def gravar(nome, cab, linhas):
    with open(SAIDA / nome, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(cab)
        w.writerows(linhas)
    print(f'  gravado resultados/{nome}')


r2 = lambda x, d=2: None if x is None else round(x, d)  # noqa: E731

v = collections.defaultdict(dict)
for l in ler(D / 'comparacoes' / 'orcamento_governo_central.csv'):
    v[(l['tabela_rtn'], l['codigo_linha'])][int(l['ano'])] = float(l['pct_pib'])
g = lambda c, a: v[('2.2-A', c)].get(a)  # noqa: E731

# ------------------------------------------------------------------ A1: composição da despesa, ano a ano
print('A1: composição da despesa primária do governo central (% do PIB)')
a1 = []
for a in range(1997, 2026):
    tot, disc = g('4.', a), (g('4.4.2', a) if a >= 2008 else None)
    rig = (1 - disc / tot) * 100 if disc is not None else None
    a1.append([a, r2(tot), r2(g('4.1', a)), r2(g('4.2', a)), r2(g('4.3', a)),
               r2(g('4.4.1', a)) if a >= 2008 else None, r2(disc), r2(g('4.4', a)) if a < 2008 else None,
               r2(g('2.', a)), r2(v[('2.3-A', '1.')].get(a)), r2(rig, 1)])
gravar('a1_composicao_anual.csv', ['ano', 'despesa_primaria_total', 'previdencia', 'pessoal', 'outras_obrigatorias',
                                   'obrigatorias_com_controle_de_fluxo', 'discricionarias',
                                   'executivo_sujeito_a_programacao_antes_de_2008', 'transferencias_reparticao_receita',
                                   'investimento', 'rigidez_pct_da_despesa'], a1)

# ------------------------------------------------------------------ A2: médias por bloco
print('A2: médias por bloco de mandato')
a2 = []
for a, b in BLOCOS:
    anos = range(a, b + 1)
    med = lambda c: st.mean(g(c, y) for y in anos)  # noqa: E731
    disc = [g('4.4.2', y) / g('4.', y) * 100 for y in anos if y >= 2008]
    inv = [v[('2.3-A', '1.')][y] for y in anos if y in v[('2.3-A', '1.')]]
    a2.append([ROTULO[a], r2(med('4.')), r2(med('4.1')), r2(med('4.2')), r2(med('4.3')),
               r2(100 - st.mean(disc), 1) if disc else None, r2(st.mean(inv)) if inv else None, r2(med('2.'))])
gravar('a2_blocos.csv', ['bloco', 'despesa_primaria_total', 'previdencia', 'pessoal', 'outras_obrigatorias',
                         'rigidez_pct_da_despesa', 'investimento', 'transferencias_reparticao_receita'], a2)

# ------------------------------------------------------------------ A3: raiz legal das maiores linhas, 2025
print('A3: raiz legal das maiores linhas de despesa, 2025 (classificação própria)')
RAIZ_LEGAL = [
    ('2.', 'Transferências a estados e municípios', 'Constituição, art. 159 (FPE 21,5% e FPM 22,5% da arrecadação do IR e do IPI)'),
    ('4.1', 'Benefícios previdenciários (INSS)', 'Constituição, art. 201; § 2º: nenhum benefício abaixo do salário mínimo'),
    ('4.2', 'Pessoal e encargos', 'Constituição, art. 37, XV (irredutibilidade) e art. 41 (estabilidade); valores em lei'),
    ('4.3.05', 'BPC (idosos e pessoas com deficiência pobres)', 'Constituição, art. 203, V: um salário mínimo por mês'),
    ('4.3.01', 'Abono salarial e seguro-desemprego', 'Constituição, art. 239 (financiados pelo PIS/Pasep); regras em lei'),
    ('4.3.10', 'Complementação da União ao Fundeb', 'Constituição, art. 212-A, V: no mínimo 23% dos fundos'),
    ('4.4.1', 'Obrigatórias com controle de fluxo (Bolsa Família, saúde, educação e outras)',
     'Em lei; saúde e educação também contam para os pisos dos arts. 198, § 2º, I (15% da RCL) e 212 (18% dos impostos)'),
    ('4.4.2.1', 'Discricionárias: saúde', 'Contam para o piso do art. 198, § 2º, I'),
    ('4.4.2.2', 'Discricionárias: educação', 'Contam para o piso do art. 212'),
    ('4.4.2', 'Discricionárias (total, inclui emendas parlamentares)',
     'Emendas: Constituição, art. 166, §§ 9º, 11 e 12 (individuais até 2% da RCL; bancada até 1%)'),
]
a3 = [[c, nome, r2(g(c, 2025)), art] for c, nome, art in RAIZ_LEGAL]
gravar('a3_raiz_legal_2025.csv', ['codigo_linha_rtn', 'despesa', 'pct_pib_2025', 'raiz_legal'], a3)

# ------------------------------------------------------------------ A4: salário mínimo e despesa indexada
print('A4: salário mínimo real e despesa previdenciária')
sm = {int(l['ano']): float(l['sm_real_medio']) for l in ler(D / 'salario_minimo.csv')
      if l['sm_real_medio'] and l['periodo'] == 'jan-dez'}
a4 = [[a, r2(sm[a]), r2(sm[a] / sm[1997] * 100, 1), r2(g('4.1', a)), r2(g('4.1', a) / g('4.1', 1997) * 100, 1),
       r2(g('4.3.05', a))] for a in range(1997, 2026) if a in sm]
gravar('a4_salario_minimo_e_previdencia.csv', ['ano', 'salario_minimo_real_medio', 'indice_sm_1997_100',
                                               'previdencia_pct_pib', 'indice_previdencia_1997_100', 'bpc_pct_pib'], a4)

# ------------------------------------------------------------------ resumo
x08, x25 = a1[2008 - 1997], a1[2025 - 1997]
print(f'\nRigidez: {x08[10]}% em 2008 → {x25[10]}% em 2025; discricionárias {x08[6]} → {x25[6]} % do PIB; '
      f'investimento {x08[9]} → {x25[9]} % do PIB.')
print(f'Despesa primária: {a1[0][1]} (1997) → {x25[1]} (2025) % do PIB; previdência {a1[0][2]} → {x25[2]}.')
print(f'Salário mínimo real: índice {a4[-1][2]} em 2025 (1997 = 100).')
