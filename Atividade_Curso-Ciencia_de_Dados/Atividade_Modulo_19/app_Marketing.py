import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image
import streamlit as st

def main():
    st.set_page_config(page_title="Telemarketing Analysis",
                       page_icon = "img/telemarketing_icon.png",
                       layout="wide",
                       initial_sidebar_state="expanded", 
                       )
    st.write("# Telemarketing Analysis")
    st.markdown("---")
    
    image = Image.open('img/bank_icon.png')
    st.sidebar.image(image,clamp=True, width=200)
    
    bank_raw = pd.read_csv('../../../_EBAC/Material_de_Apoio - Data Science/Material_de_Apoio - Modulo 19/data/input/bank-additional-full.csv', sep=';')

    bank = bank_raw.copy()
    agree = st.checkbox('Show original dataset')

    if agree:
        st.write('## Original Dataset')
        st.write(bank_raw.head())

    # IDADES
    max_age = int(bank.age.max())
    min_age = int(bank.age.min())
    idades = st.sidebar.slider(label='Idade', 
                        min_value = min_age,
                        max_value = max_age, 
                        value = (min_age, max_age),
                        step = 1)
    st.sidebar.write('Ages:', idades)
    st.sidebar.write('Min age:', idades[0])
    st.sidebar.write('Max age:', idades[1])

    bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
    
    st.write('## Filtered Dataset')
    st.write(bank.head())
    st.markdown("---")

    # # PLOTS    
    fig, ax = plt.subplots(1, 2, figsize = (5,3))

    bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
    sns.barplot(x = bank_raw_target_perc.index, 
                y = 'y',
                data = bank_raw_target_perc, 
                ax = ax[0])
    ax[0].bar_label(ax[0].containers[0])
    ax[0].set_title('Dados brutos',
                    fontweight ="bold")
    
    bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
    bank_target_perc = bank_target_perc.sort_index()
    sns.barplot(x = bank_target_perc.index, 
                y = 'y', 
                data = bank_target_perc, 
                ax = ax[1])
    ax[1].bar_label(ax[1].containers[0])
    ax[1].set_title('Dados filtrados',
                    fontweight ="bold")
    
    st.write('## Proporção de aceite')

    st.pyplot(plt)
    
if __name__ == '__main__':
    main()