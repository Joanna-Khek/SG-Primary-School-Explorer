import streamlit as st
import pandas as pd
from src.ui import plot_overview_sankey
from src.ui import set_local_css, set_page_config

set_page_config()
set_local_css()

st.title("School Type")
st.markdown("There are different types of schools in the Singapore education system. \
            The following are the three main types.",
            unsafe_allow_html=True)

# Information on school type
with st.expander("Government School", expanded=True):
    st.markdown("Government schools offer high quality education such as unique electives, \
                applied subjects and student development programmes at standardised fees.", unsafe_allow_html=True)
with st.expander("Government-Aided School", expanded=True):
    st.markdown("Schools set up by various community organisations \
                to cater to the educational needs of their respective communities. They maintain the same education \
                standards as Government schools and charge standardised fees", unsafe_allow_html=True)
with st.expander("Government-Aided School/ Autonomous", expanded=True):
    st.markdown("They follow the national syllabus, \
                but offer a wider range of programmes that enhance your child’s learning experience \
                and develop their talents.", unsafe_allow_html=True)   

# Sankey Chart
input_category = st.selectbox(label="Select a category to view relationship",
                                options=('School Nature', 'Affiliation', 'GEP'))

if input_category == 'School Nature':
    categories = ['School_Type_Encoded', 'School_Nature_Encoded']
    label_list_word = ['Government School', 'Government-Aided School', 
                        'Government-Aided School / Autonomous',
                        'Co-Ed School', 'Boys School', 'Girls School']

if input_category == 'Affiliation':
    categories = ['School_Type_Encoded', 'Affiliation_Encoded']
    label_list_word = ['Government School', 'Government-Aided School', 'Government-Aided School / Autonomous',
                        'No Affiliation', 'Affiliated']
    
if input_category == 'GEP':
    categories = ['School_Type_Encoded', 'GEP_Encoded']
    label_list_word = ['Government School', 'Government-Aided School', 'Government-Aided School / Autonomous',
                        'No GEP', 'GEP']

plot_overview_sankey(categories, label_list_word)