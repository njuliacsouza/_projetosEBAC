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
    st.write("Here we're going to make an analysis over Banking Telemarketing data.")
    st.markdown("---")
    
    image = Image.open('img/bank_icon.png')
    st.sidebar.image(image,clamp=True, width=200)
    
    bank_raw = pd.read_csv('../../../_EBAC/Material_de_Apoio - Data Science/Material_de_Apoio - Modulo 19/data/input/bank-additional-full.csv', sep=';')
    bank_raw.sort_values(by='age', inplace=True)
    bank = bank_raw.copy()
    
    st.write("## Dataset")
    
    show_original_dataset = st.checkbox('Show original dataset')

    if show_original_dataset:
        st.write('### Original Dataset')
        st.write(f"We have {len(bank_raw)} instances")
        st.write(bank_raw, use_container_width=True)

    # IDADES
    max_age = int(bank.age.max())
    min_age = int(bank.age.min())
    idades = st.sidebar.slider(label='Age filter', 
                        min_value = min_age,
                        max_value = max_age, 
                        value = (min_age, max_age),
                        step = 1)

    bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
    
    show_filtered_dataset = st.checkbox('Show filtered dataset')

    if show_filtered_dataset:  
        st.write('### Filtered Dataset')
        st.write(f"We have {len(bank)} instances")
        st.write(f"Filtering ages from {idades[0]} to {idades[1]}")
        st.write(bank, use_container_width=True)
        
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
    
    st.write('## Proportion of acceptance')

    st.pyplot(plt)
    
if __name__ == '__main__':
    main()