import pandas as pd
import os
import matplotlib.pyplot as plt

import sys

meses = sys.argv[1:]

months = {
    'JAN': 1,    'FEV': 2,    'MAR': 3,
    'ABR': 4,    'MAI': 5,    'JUN': 6,
    'JUL': 7,    'AGO': 8,    'SET': 9,
    'OUT': 10,    'NOV': 11,    'DEZ': 12
}

def MonthlyAnalysis(month: str):
    print(month)
    sinasc = pd.read_csv('./input/SINASC_RO_2019.csv', parse_dates=['DTNASC'])
    sinasc = sinasc[sinasc['DTNASC'].dt.month == months[month]]
    sinasc = sinasc[['IDADEMAE', 'SEXO', 'APGAR1', 'APGAR5', 'PESO', 'CONSULTAS', 'DTNASC', 'GESTACAO', 'GRAVIDEZ', 'ESCMAE', 'IDADEPAI']]
    sinasc = sinasc.reset_index(drop=True)

    sinasc.to_csv(f'./input/SINASC_RO_2019_{month}.csv', index=False)

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None

def plota_variaveis(mes):
    MonthlyAnalysis(mes) # cria o dataset a partir de SINASC_RO_2019.csv

    sinasc = pd.read_csv(f'./input/SINASC_RO_2019_{mes}.csv')
    print(sinasc.DTNASC.min(), sinasc.DTNASC.max())

    max_data = sinasc.DTNASC.max()[:7]
    print(max_data)
    os.makedirs('./output/figs/' + max_data, exist_ok=True)

    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento', 'data de nascimento')
    plt.savefig('./output/figs/' + max_data + '/quantidade de nascimento.png')

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento',
                      'unstack')
    plt.savefig('./output/figs/' + max_data + '/media idade mae por sexo.png')

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')
    plt.savefig('./output/figs/' + max_data + '/media peso bebe por sexo.png')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'apgar1 medio', 'gestacao', 'sort')
    plt.savefig('./output/figs/' + max_data + '/media apgar1 por escolaridade mae.png')

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')
    plt.savefig('./output/figs/' + max_data + '/media apgar1 por gestacao.png')

    plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio', 'gestacao', 'sort')
    plt.savefig('./output/figs/' + max_data + '/media apgar5 por gestacao.png')

for mes in meses:
    plota_variaveis(mes)


