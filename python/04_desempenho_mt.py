import pandas as pd

ARQUIVO = 'data/raw/RESULTADOS_2024.csv'
COLUNAS = ['CO_UF_PROVA', 'SG_UF_PROVA', 'TP_PRESENCA_MT', 'NU_NOTA_MT']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)
df_mt = df[df['TP_PRESENCA_MT'] == 1]

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

df_mt_sem_zero = df_mt[df_mt['NU_NOTA_MT'] > 0]
media_sem_zero = df_mt_sem_zero.groupby('SG_UF_PROVA')['NU_NOTA_MT'].mean()

diferenca = desempenho_mt.set_index('SG_UF_PROVA')['MEDIA_MT'] - media_sem_zero
print(diferenca.abs().max())

df['PRESENTE_MT'] = (df['TP_PRESENCA_MT'] == 1)

presenca_mt = (
    df
    .groupby('SG_UF_PROVA')
    .agg(PROP_PRESENTES_MT=('PRESENTE_MT', 'mean'))
    .reset_index()
)

print(presenca_mt.sort_values('PROP_PRESENTES_MT').round(3))