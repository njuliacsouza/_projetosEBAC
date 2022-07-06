import pandas as pd
import os
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='SINASC Rondônia',
                    layout='wide', 
                    page_icon='https://img.freepik.com/vetores-gratis/bebe-dos-desenhos-animados-dormindo-em-uma-nuvem_61878-363.jpg'
                )

from pathlib import Path

path_to_file = Path(__file__).parents[0] / 'SINASC_RO_2019.csv'

meses = ['JAN']

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
    st.pyplot(fig=plt)
    return None


def plota_variaveis():
    #MonthlyAnalysis(mes) # cria o dataset a partir de SINASC_RO_2019.csv

    st.markdown("# Análise SINASC")
    st.write('Aqui temos uma análise do dataset ```SINASC_RO_2019.csv``` onde temos informações sobre os nascimentos de bebê em Rondônia no ano de 2019.')
    st.write('Dentro desse arquivo temos também informações sobre a mãe e o pai das crianças nascidas.')
    st.write('Para uma melhor visualização dos períodos de tempo, selecione as datas ao lado.')

    sinasc = pd.read_csv(path_to_file)
    sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)
    
    min_data = sinasc.DTNASC.min()
    max_data = sinasc.DTNASC.max()

    datas = sinasc.DTNASC.unique()
    datas.sort()
        
    data_inicial = pd.to_datetime(st.sidebar.date_input('Defina a data inicial: ', value=min_data, min_value=min_data,  max_value=max_data))
    data_final = pd.to_datetime(st.sidebar.date_input('Defina a data final: ', value=max_data, min_value=min_data,  max_value=max_data))

    st.sidebar.write('Data inicial = ',data_inicial)
    st.sidebar.write('Data final = ',data_final)

    sinasc = sinasc[(sinasc.DTNASC <= data_final) & (sinasc.DTNASC >= data_inicial)]

    if st.checkbox('Mostrar dataset'):
        st.subheader('Dataset')
        st.write(sinasc.head())

    st.write('#### Quantidade de nascimentos de acordo com a data')
    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento', 'data de nascimento')

    st.write('#### Idade da mâe de acordo com a data de nascimento (por sexo)')
    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento',
                      'unstack')

    st.write('#### Média do peso do bebê conforme a data de nascimento')
    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')

    st.write('#### APGAR1 média de acordo com a escolaridade da mãe')
    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'apgar1 medio', 'gestacao', 'sort')
    
    st.write('#### APGAR1 média de acordo com a gestação')
    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')
    
    st.write('#### APGAR15 média de acordo com a gestação')
    plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio', 'gestacao', 'sort')

plota_variaveis()


