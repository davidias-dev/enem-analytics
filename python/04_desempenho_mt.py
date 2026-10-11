import pandas as pd

ARQUIVO = 'data/raw/RESULTADOS_2024.csv'
COLUNAS = ['CO_UF_PROVA', 'SG_UF_PROVA', 'TP_PRESENCA_MT', 'NU_NOTA_MT']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

print(df.shape)
print(df['TP_PRESENCA_MT'].value_counts(dropna=False))
print(df.groupby('TP_PRESENCA_MT')['NU_NOTA_MT'].agg(['size', 'count', 'min', 'max']))