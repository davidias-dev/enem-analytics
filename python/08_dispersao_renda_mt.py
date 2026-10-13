import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base = pd.read_csv('data/processed/base_analitica_estadual.csv')

ORDEM_REGIOES = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
CORES = {
    'Norte': "#53EE2C",
    'Nordeste': '#EE2C2C',
    'Centro-Oeste': "#B268EE",
    'Sudeste': '#DAA520',
    'Sul': "#28A0F0",
}

fig, ax = plt.subplots(figsize=(9, 6))

for regiao in ORDEM_REGIOES:
    grupo = base[base['REGIAO'] == regiao]
    ax.scatter(
        grupo['PROP_RENDA_ATE_1SM'],
        grupo['MEDIA_MT'],
        color=CORES[regiao],
        edgecolor='black',
        s=60,
        label=regiao,
    )

for _, linha in base.iterrows():
    ax.annotate(
        linha['SG_UF_PROVA'],
        (linha['PROP_RENDA_ATE_1SM'], linha['MEDIA_MT']),
        textcoords='offset points',
        xytext=(5, 4),
        fontsize=8,
    )

ax.set_xlabel('Proporção de participantes com renda familiar de até 1 SM')
ax.set_ylabel('Média da nota de Matemática')
ax.set_title('Renda familiar e nota de Matemática por UF (ENEM 2024)')
ax.legend(title='Região')
ax.grid(alpha=0.3)
ax.spines[['top', 'right']].set_visible(False)

Path('outputs').mkdir(exist_ok=True)
fig.savefig('outputs/dispersao_renda_mt.png', dpi=150, bbox_inches='tight')
plt.show()