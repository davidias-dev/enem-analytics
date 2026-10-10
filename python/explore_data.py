import pandas as pd

arquivo = 'data/raw/PARTICIPANTES_2024.csv'

categoricas = [
    'CO_UF_PROVA', 'SG_UF_PROVA','NU_ANO', 'TP_FAIXA_ETARIA', 'TP_SEXO',
    'TP_COR_RACA', 'TP_ST_CONCLUSAO', 'IN_TREINEIRO', 'Q001', 'Q002', 'Q003',
    'Q004', 'Q005', 'Q006', 'Q007', 'Q020', 'Q021', 'Q022', 'Q023'
]

df = pd.read_csv(
    arquivo,
    sep=';',
    encoding='latin1',
    usecols=categoricas
)

# print(df.shape)
# print(df.head())
# print(df.info())
# print(df.isna().sum())

for col in categoricas:
    print(f'\n--- {col} ---')
    print(df[col].value_counts(dropna=False))