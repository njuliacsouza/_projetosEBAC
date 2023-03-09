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
    
if __name__ == '__main__':
    main()