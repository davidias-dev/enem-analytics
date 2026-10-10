import pandas as pd

archive = 'data/raw/PARTICIPANTES_2024.csv'

df = pd.read_csv(
    archive,
    sep=';',
    encoding='latin1',
    nrows=5
)

print(df.shape)
print(df.columns.tolist())