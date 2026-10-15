import pandas as pd
from indicadores import resumir_perfil, regiao_da_uf

ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'
CHAVE = ['CO_UF_PROVA', 'SG_UF_PROVA']
COLUNAS = CHAVE + ['IN_TREINEIRO', 'TP_SEXO', 'Q001', 'Q002', 'Q007', 'Q020', 'Q021', 'Q023']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

perfil_estadual = resumir_perfil(df, CHAVE)
perfil_estadual.insert(2, 'REGIAO', regiao_da_uf(perfil_estadual['CO_UF_PROVA']))

antigo = pd.read_csv('data/processed/perfil_estadual.csv')
novo = perfil_estadual.sort_values('SG_UF_PROVA').reset_index(drop=True)
antigo = antigo.sort_values('SG_UF_PROVA').reset_index(drop=True)

pd.testing.assert_frame_equal(novo[antigo.columns], antigo)
print('ok: resultados idênticos aos da versão anterior')

cols = perfil_estadual.filter(like='PROP_ESC')
desc = cols.describe().T
print(desc[['mean', 'std', 'min', 'max']].round(3))

print(perfil_estadual.shape)
perfil_estadual.to_csv('data/processed/perfil_estadual.csv', index=False)