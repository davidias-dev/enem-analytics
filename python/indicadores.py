import pandas as pd

FAIXAS_RENDA = {
    'A': 'ATE_1SM', 'B': 'ATE_1SM', # até 1 salário mínimo
    'C': '1_A_3SM', 'D': '1_A_3SM', 'E': '1_A_3SM', 'F': '1_A_3SM', # 1 a 3 salários mínimos
    'G': '3_A_5SM', 'H': '3_A_5SM', #3 a 5 salários mínimos
    'I': 'ACIMA_5SM', 'J': 'ACIMA_5SM', 'K': 'ACIMA_5SM', 'L': 'ACIMA_5SM',
    'M': 'ACIMA_5SM', 'N': 'ACIMA_5SM', 'O': 'ACIMA_5SM', 'P': 'ACIMA_5SM',
    'Q': 'ACIMA_5SM', # acima de 5 salários mínimos
}
ORDEM_FAIXAS_RENDA = ['ATE_1SM', '1_A_3SM', '3_A_5SM', 'ACIMA_5SM']

GRUPOS_INTERNET = {'A': 'NAO', 'B': 'SIM'}

GRUPOS_COMPUTADOR = {
    'A': 'NENHUM',
    'B': 'UM',
    'C': 'DOIS_OU_MAIS', 'D': 'DOIS_OU_MAIS', 'E': 'DOIS_OU_MAIS',
}
ORDEM_COMPUTADOR = ['NENHUM', 'UM', 'DOIS_OU_MAIS']

GRUPO_ESCOLARIDADE = {
    'A': 'ATE_FUND_INCOMPLETO', 'B': 'ATE_FUND_INCOMPLETO', 'C': 'ATE_FUND_INCOMPLETO',
    'D': 'FUND_COMPLETO',
    'E': 'MEDIO_COMPLETO',
    'F': 'SUPERIOR_OU_MAIS', 'G': 'SUPERIOR_OU_MAIS',
    'H': 'NAO_SABE',
}
ORDEM_ESCOLARIDADE = [
    'ATE_FUND_INCOMPLETO', 'FUND_COMPLETO', 'MEDIO_COMPLETO',
    'SUPERIOR_OU_MAIS', 'NAO_SABE',
]

GRUPOS_ESCOLA = {
    'A': 'SO_PUBLICA',
    'B': 'MISTA', 'C': 'MISTA',
    'D': 'SO_PRIVADA_SEM_BOLSA',
    'E': 'SO_PRIVADA_BOLSA_INTEGRAL',
    'F': 'SEM_ENSINO_MEDIO',
}

ORDEM_ESCOLA = [
    'SO_PUBLICA', 'MISTA', 'SO_PRIVADA_SEM_BOLSA',
    'SO_PRIVADA_BOLSA_INTEGRAL', 'SEM_ENSINO_MEDIO',
]

REGIOES = {
    1: 'Norte',
    2: 'Nordeste',
    3: 'Sudeste',
    4: 'Sul',
    5: 'Centro-Oeste',
}


def resumir_area(df, area, chave):
    """Resume a nota de uma área (CN, CH, LC ou MT) por grupo.

    Só entram na média os presentes (TP_PRESENCA_<area> == 1).
    `chave` é uma lista de colunas que define o grupo (UF, município...).    
    """
    presenca = f'TP_PRESENCA_{area}'
    nota = f'NU_NOTA_{area}'

    notas = (
        df[df[presenca] == 1]
        .groupby(chave)[nota]
        .agg(N='count', MEDIA='mean', MEDIANA='median', DP='std')
        .add_suffix(f'_{area}')
    )

    presentes = (
        df.assign(PRESENTE=df[presenca] == 1)
        .groupby(chave)['PRESENTE']
        .mean()
        .rename(f'PROP_PRESENTES_{area}')
    )

    return pd.concat([notas, presentes], axis=1)


def resumir_desempenho(df, areas, chave):
    """Junta o resumo de todas as áreas numa única tabela, uma linha por grupo."""
    tabelas = [resumir_area(df, area, chave) for area in areas]
    return pd.concat(tabelas, axis=1).reset_index()


def proporcoes(df, chave, coluna, prefixo, ordem=None):
    """Proporção de cada categoria de `coluna` dentro de cada grupo."""
    tabela = (
        df.groupby(chave)[coluna]
        .value_counts(normalize=True)
        .unstack(fill_value=0)
        .rename_axis(columns=None)
    )
    if ordem is not None:
        tabela = tabela[ordem]
    return tabela.add_prefix(prefixo)


def proporcoes_agrupadas(df, chave, coluna, mapa, prefixo, ordem):
    """Agrupa as categorias de `coluna` segundo `mapa` e calcula a proporção
    de cada grupo dentro de cada unidade. Só as colunas em `ordem` são mantidas."""
    agrupada = df[coluna].map(mapa)
    if agrupada.isna().any():
        raise ValueError(f'{coluna} tem categorias que não estão no mapa')
    return proporcoes(df.assign(GRUPO=agrupada), chave, 'GRUPO', prefixo, ordem)


def perfil_basico(df, chave):
    """Número de participantes, treineiros e proporção feminina por grupo."""
    return (
        df.assign(FEMININO=df['TP_SEXO'] == 'F')
        .groupby(chave)
        .agg(
            N_PARTICIPANTES=('IN_TREINEIRO', 'size'),
            N_TREINEIROS=('IN_TREINEIRO', 'sum'),
            PROP_TREINEIROS=('IN_TREINEIRO', 'mean'),
            PROP_FEMININO=('FEMININO', 'mean'),
        )
    )


def perfil_renda(df, chave):
    """Proporção de participantes em cada faixa de renda familiar (Q007)."""
    return proporcoes_agrupadas(
        df, chave, 'Q007', FAIXAS_RENDA, 'PROP_RENDA_', ORDEM_FAIXAS_RENDA
    )


def perfil_tecnologia(df, chave):
    """Acesso à internet (Q020) e quantidade de computadores (Q021)."""
    return pd.concat(
        [
            proporcoes_agrupadas(
                df, chave, 'Q020', GRUPOS_INTERNET, 'PROP_INTERNET_', ['SIM']
            ),
            proporcoes_agrupadas(
                df, chave, 'Q021', GRUPOS_COMPUTADOR, 'PROP_COMPUTADOR_', ORDEM_COMPUTADOR
            ),
        ],
        axis=1,
    )


def perfil_escolaridade(df, chave):
    """Escolaridade do pai/homem responsável (Q001) e da mãe/mulher responsável (Q002)."""
    return pd.concat(
        [
            proporcoes_agrupadas(
                df, chave, 'Q001', GRUPO_ESCOLARIDADE, 'PROP_ESC_PAI_', ORDEM_ESCOLARIDADE
            ),
            proporcoes_agrupadas(
                df, chave, 'Q002', GRUPO_ESCOLARIDADE, 'PROP_ESC_MAE_', ORDEM_ESCOLARIDADE
            ),
        ],
        axis=1,
    )


def perfil_escola(df, chave):
    """Tipo de escola cursada no Ensino Médio (Q023)."""
    return proporcoes_agrupadas(
        df, chave, 'Q023', GRUPOS_ESCOLA, 'PROP_ESCOLA_', ORDEM_ESCOLA 
    )


def resumir_perfil(df, chave):
    """Junta todos os indicadores de perfil numa única tabela por grupo."""
    partes = [
        perfil_basico(df, chave),
        perfil_renda(df, chave),
        perfil_tecnologia(df, chave),
        perfil_escolaridade(df, chave),
        perfil_escola(df, chave)
    ]
    return pd.concat(partes, axis=1).reset_index()


def regiao_da_uf(codigo_uf):
    """Região a partir do código da UF (o primeiro dígito, padrão IBGE)."""
    return (codigo_uf // 10).map(REGIOES)