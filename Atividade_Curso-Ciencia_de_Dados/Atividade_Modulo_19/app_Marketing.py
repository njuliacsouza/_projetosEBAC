import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

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
    st.sidebar.image(image,clamp=True, width=100)
    
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
    job = st.sidebar.multiselect(label = 'Job filter',
                                 options = list(bank.job.unique()),
                                 default=None
                                    )
    marital = st.sidebar.multiselect(label = 'Marital filter',
                                 options = list(bank.marital.unique()),
                                 default=None
                                    )
    education = st.sidebar.multiselect(label = 'Education filter',
                                 options = list(bank.education.unique()),
                                 default=None
                                    )

    bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
    bank = bank.apply(lambda i: i.job.isin(job) if job else i, axis=1).reset_index(drop=True)
    bank = bank.apply(lambda i: i.marital.isin(marital) if marital else i, axis=1).reset_index(drop=True)
    bank = bank.apply(lambda i: i.education.isin(marital) if education else i, axis=1).reset_index(drop=True)
    
    show_filtered_dataset = st.checkbox('Show filtered dataset')

    if show_filtered_dataset:  
        st.write('### Filtered Dataset')
        st.write(f"We have {len(bank)} instances")
        st.write(bank, use_container_width=True)

    ## PLOTS    
    fig = make_subplots(1,2)

    bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
    
    fig.add_trace(go.Bar(x = bank_raw_target_perc.index.values, 
                         y = bank_raw_target_perc.y.values,
                         name='Original data'
                         ))
    
    bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
    bank_target_perc = bank_target_perc.sort_index()
    fig.add_trace(go.Bar(x = bank_raw_target_perc.index.values, 
                         y = bank_raw_target_perc.y.values,
                         name='Filtered data'
                         ))
    fig.update_layout(title_text="Proportion of acceptance",
                  showlegend=True
                 )
    
    st.plotly_chart(fig, use_container_width=True)
    
if __name__ == '__main__':
    main()