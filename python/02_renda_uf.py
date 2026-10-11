import pandas as pd

ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'
COLUNAS = ['SG_UF_PROVA', 'Q007']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

FAIXAS = {
    'A': 'ATE_1SM', 'B': 'ATE_1SM',
    'C': '1_A_3SM', 'D': '1_A_3SM', 'E': '1_A_3SM', 'F': '1_A_3SM',
    'G': '3_A_5SM', 'H': '3_A_5SM',
    'I': 'ACIMA_5SM', 'J': 'ACIMA_5SM', 'K': 'ACIMA_5SM', 'L': 'ACIMA_5SM',
    'M': 'ACIMA_5SM', 'N': 'ACIMA_5SM', 'O': 'ACIMA_5SM', 'P': 'ACIMA_5SM',
    'Q': 'ACIMA_5SM',
}
ORDEM_FAIXAS = ['ATE_1SM', '1_A_3SM', '3_A_5SM', 'ACIMA_5SM']

df['FAIXA_RENDA'] = df['Q007'].map(FAIXAS)
print(df['FAIXA_RENDA'].isna().sum())

print(df['FAIXA_RENDA'].value_counts(normalize=True)[ORDEM_FAIXAS].round(3))

contagem = pd.crosstab(df['SG_UF_PROVA'], df['FAIXA_RENDA'])[ORDEM_FAIXAS]
print(contagem)

renda_faixas = pd.crosstab(df['SG_UF_PROVA'], df['FAIXA_RENDA'], normalize='index')[ORDEM_FAIXAS]
print(renda_faixas.round(3))
print(renda_faixas.sum(axis=1))