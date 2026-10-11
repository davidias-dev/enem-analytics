import pandas as pd

ARQUIVO = 'data/raw/RESULTADOS_2024.csv'
COLUNAS = ['CO_UF_PROVA', 'SG_UF_PROVA', 'TP_PRESENCA_MT', 'NU_NOTA_MT']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

# print(df.shape)
# print(df['TP_PRESENCA_MT'].value_counts(dropna=False))
print(df.groupby('TP_PRESENCA_MT')['NU_NOTA_MT'].agg(['size', 'count', 'min', 'max']))

print((df['NU_NOTA_MT'] == 0).sum())

df_mt = df[df['TP_PRESENCA_MT'] == 1]
print(df_mt.shape)

desempenho_mt = (
    df_mt
    .groupby(['CO_UF_PROVA', 'SG_UF_PROVA'])
    .agg(
        N_MT=('NU_NOTA_MT', 'count'),
        MEDIA_MT=('NU_NOTA_MT', 'mean'),
        MEDIANA_MT=('NU_NOTA_MT', 'median'),
        DP_MT=('NU_NOTA_MT', 'std'),
    )
    .reset_index()
    .sort_values('MEDIA_MT', ascending=False)
    .reset_index(drop=True)
)

print(desempenho_mt.round(3))
print(desempenho_mt['N_MT'].sum())