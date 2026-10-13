import pandas as pd
from indicadores import resumir_desempenho

ARQUIVO = 'data/raw/RESULTADOS_2024.csv'
AREAS = ['CN', 'CH', 'LC', 'MT']
CHAVE = ['CO_UF_PROVA', 'SG_UF_PROVA']

COLUNAS = list(CHAVE)
for area in AREAS:
    COLUNAS += [f'TP_PRESENCA_{area}', f'NU_NOTA_{area}']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

desempenho_estadual = resumir_desempenho(df, AREAS, CHAVE)
print(desempenho_estadual.shape)

# antigo = pd.read_csv('data/processed/desempenho_estadual.csv')
# novo = desempenho_estadual.sort_values('SG_UF_PROVA').reset_index(drop=True)
# antigo = antigo.sort_values('SG_UF_PROVA').reset_index(drop=True)

# pd.testing.assert_frame_equal(novo[antigo.columns], antigo)
# print('ok: resultados idênticos aos da versão anterior')

desempenho_estadual.to_csv('data/processed/desempenho_estadual.csv', index=False)
print(desempenho_estadual.sort_values('MEDIA_MT', ascending=False))