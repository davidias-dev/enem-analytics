import pandas as pd

base = pd.read_csv('data/processed/base_analitica_estadual.csv')

colunas = [
    'PROP_RENDA_ATE_1SM',
    'PROP_RENDA_ACIMA_5SM',
    'PROP_TREINEIROS',
    'PROP_PRESENTES_MT',
    'MEDIA_MT',
]

print(base[colunas].corr(method='pearson').round(2))
print(base[colunas].corr(method='spearman').round(2))