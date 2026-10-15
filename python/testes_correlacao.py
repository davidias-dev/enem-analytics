import pandas as pd

base = pd.read_csv('data/processed/base_analitica_estadual.csv')
ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'

notas = ['MEDIA_CN', 'MEDIA_CH', 'MEDIA_LC', 'MEDIA_MT']
print(base[notas].corr(method='spearman').round(2))

indicadores = [
    'PROP_RENDA_ATE_1SM',
    'PROP_COMPUTADOR_NENHUM',
    'PROP_INTERNET_SIM',
    'PROP_ESC_MAE_SUPERIOR_OU_MAIS',
    'PROP_ESC_PAI_ATE_FUND_INCOMPLETO',
    'PROP_ESCOLA_SO_PUBLICA',
]
print(base[indicadores].corr(method='spearman').round(2))


df = pd.read_csv(
    ARQUIVO,
    sep=';',
    encoding='latin1',
    usecols=['IN_TREINEIRO', 'TP_ST_CONCLUSAO', 'TP_FAIXA_ETARIA'],
)

print(pd.crosstab(df['IN_TREINEIRO'], df['TP_ST_CONCLUSAO']))
print(pd.crosstab(df['TP_FAIXA_ETARIA'], df['IN_TREINEIRO'], normalize='index').round(3))