import pandas as pd

perfil = pd.read_csv('data/processed/perfil_estadual.csv')
desempenho = pd.read_csv('data/processed/desempenho_estadual.csv')

base = perfil.merge(
    desempenho,
    on=['CO_UF_PROVA', 'SG_UF_PROVA'],
    how='outer',
    validate='one_to_one',
    indicator=True,
)

print(base['_merge'].value_counts())

base = base.drop(columns='_merge')
print(base.shape)

base.to_csv('data/processed/base_analitica_estadual.csv', index=False)