# A amarração do orçamento

Quanto da despesa do governo central é obrigatória, de onde vem essa obrigação (Constituição ou lei) e o
que aconteceu com o investimento. Método em `METODO.md`, gravado antes dos números.

```
python3 analises/amarracao/analise.py
```

| Tabela | O que mostra |
|---|---|
| `a1_composicao_anual.csv` | despesa primária do governo central por grande grupo, % do PIB, 1997–2025; rigidez (parte obrigatória) desde 2008 |
| `a2_blocos.csv` | as mesmas medidas, em média por bloco de mandato |
| `a3_raiz_legal_2025.csv` | as maiores linhas de despesa em 2025 e o artigo da Constituição (ou a lei) que as cria ou protege — classificação própria, para conferir |
| `a4_salario_minimo_e_previdencia.csv` | salário mínimo real contra despesa previdenciária e BPC |

## Como ler

- Só o governo central (Tesouro, Previdência e Banco Central). Estados e municípios ficam de fora.
- A separação entre obrigatórias e discricionárias só existe na série do Tesouro a partir de 2008.
- "Raiz constitucional" quer dizer que a Constituição cria a despesa ou fixa um piso para ela; o tamanho
  quase sempre depende de leis e de decisões de governo (regras de aposentadoria, valor do salário mínimo).
- Rigidez alta e investimento baixo andando juntos não provam que uma coisa causa a outra.
