import pandas as pd

ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'
COLUNAS = ['CO_UF_PROVA', 'SG_UF_PROVA', 'IN_TREINEIRO', 'TP_SEXO', 'Q007']

FAIXAS = {
    'A': 'ATE_1SM', 'B': 'ATE_1SM',
    'C': '1_A_3SM', 'D': '1_A_3SM', 'E': '1_A_3SM', 'F': '1_A_3SM',
    'G': '3_A_5SM', 'H': '3_A_5SM',
    'I': 'ACIMA_5SM', 'J': 'ACIMA_5SM', 'K': 'ACIMA_5SM', 'L': 'ACIMA_5SM',
    'M': 'ACIMA_5SM', 'N': 'ACIMA_5SM', 'O': 'ACIMA_5SM', 'P': 'ACIMA_5SM',
    'Q': 'ACIMA_5SM',
}
ORDEM_FAIXAS = ['ATE_1SM', '1_A_3SM', '3_A_5SM', 'ACIMA_5SM']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)
df['FEMININO'] = (df['TP_SEXO'] == 'F')
df['FAIXA_RENDA'] = df['Q007'].map(FAIXAS)

basicos = (
    df
    .groupby(['CO_UF_PROVA', 'SG_UF_PROVA'])
    .agg(
        N_PARTICIPANTES=('IN_TREINEIRO', 'size'),
        N_TREINEIROS=('IN_TREINEIRO', 'sum'),
        PROP_TREINEIROS=('IN_TREINEIRO', 'mean'),
        PROP_FEMININO=('FEMININO', 'mean')
    )
    .reset_index()
)

renda = (
    pd.crosstab(df['SG_UF_PROVA'], df['FAIXA_RENDA'], normalize='index')[ORDEM_FAIXAS]
    .add_prefix('PROP_RENDA_')
    .reset_index()
)

perfil_estadual = (
    basicos
    .merge(renda, on='SG_UF_PROVA', how='left', validate='one_to_one')
    .sort_values('N_PARTICIPANTES', ascending=False)
    .reset_index(drop=True)
)

print(perfil_estadual.shape)
print(perfil_estadual.isna().sum().sum())
print(perfil_estadual)

perfil_estadual.to_csv('data/processed/perfil_estadual.csv', index=False)