import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import timeit

from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image
import streamlit as st


@st.cache_data(show_spinner= True)
def load_data(file_data):
    return pd.read_csv(file_data, sep=';')

@st.cache(allow_output_mutation=True)
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

@st.cache_data
def df_toString(df):
    return df.to_csv(index=False)

@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data
    
def main():
    st.set_page_config(page_title="Telemarketing Analysis",
                       page_icon = "img/telemarketing_icon.png",
                       layout="wide",
                       initial_sidebar_state="expanded", 
                       )
    st.write("# Telemarketing Analysis")
    st.write("Here we're going to make an analysis over Banking Telemarketing data.")
    st.write('### Summary')
    st.write('- Dataset')
    st.write('- Distribution plots')
    st.markdown("---")
    
    image = Image.open('img/bank_icon.png')
    st.sidebar.image(image,clamp=True)
    
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv'])
    
    if (data_file_1 is not None):
        start = timeit.default_timer()
        bank_raw = load_data(data_file_1)
        csv = df_toString(bank_raw)
        
        #st.sidebar.write('Time: ', timeit.default_timer() - start)  
        bank = bank_raw.copy()

        st.write("## Dataset")

        show_original_dataset = st.checkbox('Show original dataset')
        
        if show_original_dataset:
            st.write('### Original Dataset')
            st.write(f"We have {len(bank_raw)} instances")
            st.write(bank_raw, use_container_width=True)

        st.sidebar.write('## Filters')
        with st.sidebar.form(key='my_form'):
            submit_button = st.form_submit_button(label='Apply')

            # IDADES
            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider(label='Idade', 
                                min_value = min_age,
                                max_value = max_age, 
                                value = (min_age, max_age),
                                step = 1)


            # PROFISSÕES
            jobs_list = bank.job.unique().tolist()
            jobs_list.append('all')
            jobs_selected =  st.multiselect("Job", jobs_list, ['all'])

            # ESTADO CIVIL
            marital_list = bank.marital.unique().tolist()
            marital_list.append('all')
            marital_selected =  st.multiselect("Marital status", marital_list, ['all'])

            # DEFAULT?
            default_list = bank.default.unique().tolist()
            default_list.append('all')
            default_selected =  st.multiselect("Default", default_list, ['all'])


            # TEM FINANCIAMENTO IMOBILIÁRIO?
            housing_list = bank.housing.unique().tolist()
            housing_list.append('all')
            housing_selected =  st.multiselect("Housing", housing_list, ['all'])


            # TEM EMPRÉSTIMO?
            loan_list = bank.loan.unique().tolist()
            loan_list.append('all')
            loan_selected =  st.multiselect("Loan", loan_list, ['all'])


            # MEIO DE CONTATO?
            contact_list = bank.contact.unique().tolist()
            contact_list.append('all')
            contact_selected =  st.multiselect("Contact", contact_list, ['all'])


            # MÊS DO CONTATO
            month_list = bank.month.unique().tolist()
            month_list.append('all')
            month_selected =  st.multiselect("Contact month", month_list, ['all'])


            # DIA DA SEMANA
            day_of_week_list = bank.day_of_week.unique().tolist()
            day_of_week_list.append('all')
            day_of_week_selected =  st.multiselect("Day of the week", day_of_week_list, ['all'])


            bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                        .pipe(multiselect_filter, 'job', jobs_selected)
                        .pipe(multiselect_filter, 'marital', marital_selected)
                        .pipe(multiselect_filter, 'default', default_selected)
                        .pipe(multiselect_filter, 'housing', housing_selected)
                        .pipe(multiselect_filter, 'loan', loan_selected)
                        .pipe(multiselect_filter, 'contact', contact_selected)
                        .pipe(multiselect_filter, 'month', month_selected)
                        .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
            )



        st.write('### Filtered Dataset')
        st.write(f"We have {len(bank)} instances")
        st.write(bank, use_container_width=True)
        
        csv_filtered = df_toString(bank)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv_filtered,
            file_name='df_csv.csv',
            mime='text/csv',
        )
        

        st.markdown('---')

        ## Plots

        ### Plot of y
        st.write('## Distritution plots')
        st.write('### Distribution of response column')

        fig = make_subplots(1,2)

        bank_raw_target_perc = bank_raw['y'].value_counts(normalize = True).to_frame()*100
        bank_raw_target_perc = bank_raw_target_perc.sort_index()

        fig.add_trace(go.Bar(x = bank_raw_target_perc.index.values, 
                             y = bank_raw_target_perc['y'].values,
                             name='Original data', marker_color="red",
                             ))

        bank_target_perc = bank['y'].value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index()
        fig.add_trace(go.Bar(x = bank_target_perc.index.values, 
                             y = bank_target_perc['y'].values,
                             name='Filtered data', marker_color="blue"
                             ))
        fig.update_layout(title_text="Proportion of acceptance",
                      showlegend=True
                     )

        st.plotly_chart(fig, use_container_width=True)

        ### Plot of numerical columns
        st.write('### Distribution of numerical atributes')
        selected_column = st.selectbox('Column', bank.select_dtypes('number').columns)

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=bank_raw[selected_column], name='Original dataset',marker_color="red"))
        fig.add_trace(go.Histogram(x=bank[selected_column], name='Filtered dataset',marker_color="blue"))

        st.plotly_chart(fig, use_container_width=True)

        ### Plot of categorical columns
        st.write('### Distribution of categorical atributes')
        selected_column_cat = st.selectbox('Column', bank.select_dtypes('object').drop('y', axis=1).columns)

        fig = go.Figure()

        bank_raw_target_perc = bank_raw[selected_column_cat].value_counts(normalize = True).to_frame()*100
        bank_raw_target_perc = bank_raw_target_perc.sort_index()

        fig.add_trace(go.Bar(x = bank_raw_target_perc.index.values, 
                             y = bank_raw_target_perc[selected_column_cat].values,
                             name='Original data',marker_color="red"
                             ))

        bank_target_perc = bank[selected_column_cat].value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index()
        fig.add_trace(go.Bar(x = bank_target_perc.index.values, 
                             y = bank_target_perc[selected_column_cat].values,
                             name='Filtered data',marker_color="blue"
                             ))
        fig.update_layout(title_text="Proportion of acceptance",
                      showlegend=True
                     )

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.write('Upload the dataset!')
    
    
    
if __name__ == '__main__':
    main()