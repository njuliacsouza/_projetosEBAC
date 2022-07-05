import pandas as pd
import matplotlib.pyplot as plt

months = {
    'JAN': 1,    'FEV': 2,    'MAR': 3,
    'ABR': 4,    'MAI': 5,    'JUN': 6,
    'JUL': 7,    'AGO': 8,    'SET': 9,
    'OUT': 10,    'NOV': 11,    'DEZ': 12
}

def MonthlyAnalysis(month: str):
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