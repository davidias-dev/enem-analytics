import pandas as pd

ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'
COLUNAS = ['SG_UF_PROVA', 'Q007']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

renda_uf = pd.crosstab(df['SG_UF_PROVA'], df['Q007'], normalize='index')

pd.set_option('display.width', 250)
pd.set_option('display.max_columns', None)

print(renda_uf.round(3))
print(renda_uf.sum(axis=1))