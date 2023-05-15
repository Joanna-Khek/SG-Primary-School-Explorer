import streamlit as st
import pandas as pd
from ui import plot_overview_sankey
from ui import set_local_css, set_page_config

set_page_config()
set_local_css()

st.title("School Nature")

st.markdown("The primary schools in Singapore are categorised into three different natures.")
with st.expander("Co-Ed School", expanded=False):
    st.empty()
with st.expander("Boys School", expanded=False):
    st.empty()
with st.expander("Girls School", expanded=False):
    st.empty()
    
# Sankey Chart
input_category = st.selectbox(label="Select a category to view relationship",
                                options=('Affiliation', 'GEP'))

if input_category == 'Affiliation':
    categories = ['School_Nature_Encoded', 'Affiliation_Encoded']
    label_list_word = ['Co-Ed School', 'Boys School', 'Girls School',
                        'No Affiliation', 'Affiliated']
    
if input_category == 'GEP':
    categories = ['School_Nature_Encoded', 'GEP_Encoded']
    label_list_word = ['Co-Ed School', 'Boys School', 'Girls School',
                        'No GEP', 'GEP']

plot_overview_sankey(categories, label_list_word)