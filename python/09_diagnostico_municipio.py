import pandas as pd

ARQUIVO = 'data/raw/PARTICIPANTES_2024.csv'
COLUNAS = ['CO_MUNICIPIO_PROVA']

df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS)

n_por_municipio = df.groupby('CO_MUNICIPIO_PROVA').size()

print(n_por_municipio.shape[0])
print(n_por_municipio.describe().round(3))

for minimo in [30, 100, 500]:
    mantidos = n_por_municipio[n_por_municipio >= minimo]
    print(minimo, mantidos.shape[0], round(mantidos.sum() / n_por_municipio.sum(), 3))
