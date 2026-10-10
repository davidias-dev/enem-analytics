import pandas as pd

ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'
COLUNAS = ['CO_UF_PROVA', 'SG_UF_PROVA', 'IN_TREINEIRO', 'TP_SEXO']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

df['FEMININO'] = (df['TP_SEXO'] == 'F')

perfil_uf = (
    df
    .groupby(['CO_UF_PROVA', 'SG_UF_PROVA'])
    .agg(
        N_PARTICIPANTES = ('IN_TREINEIRO', 'size'),
        N_TREINEIROS = ('IN_TREINEIRO', 'sum'),
        PROP_TREINEIROS = ('IN_TREINEIRO', 'mean'),
        PROP_FEMININO = ('FEMININO', 'mean')
    )
    .reset_index()
    .sort_values('N_PARTICIPANTES', ascending=False)
    .reset_index(drop=True)
)

print(perfil_uf)
print(perfil_uf['N_PARTICIPANTES'].sum())
print(perfil_uf['N_TREINEIROS'].sum())
print(perfil_uf[['PROP_TREINEIROS', 'PROP_FEMININO']].describe())
desc = perfil_uf[['PROP_TREINEIROS', 'PROP_FEMININO']].describe()
print(desc.loc['std'] / desc.loc['mean'])
print(df['FEMININO'].mean())