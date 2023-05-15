import streamlit as st
import pandas as pd
from src.ui import plot_cca_by_school_type
from src.ui import plot_cca_by_school_nature
from src.utils import read_data, read_cca_points
from src.ui import set_local_css, set_page_config
from src.ui import show_school_with_cca
from src.ui import show_most_common_cca
from src.ui import show_most_unique_cca
from src.ui import show_all_cca

set_page_config()
set_local_css()

st.title("CCA")

df_school_full, df_school_cca = read_data()
df_school_cca_points, df_cca_points = read_cca_points()

tab1, tab2, tab3, tab4 = st.tabs(['Find school', 'Explore', 'School Type', 'School Nature'])
with tab1:
    st.subheader("Find schools offering a specific CCA")
    input_cca = st.selectbox("Select a CCA", list(df_cca_points.CCA))
    df_school_cca_points, df_cca_points = read_cca_points()
    show_school_with_cca(input_cca, df_school_cca_points)

with tab2:
    st.subheader("Explore CCAs")
    df_school_cca_points, df_cca_points = read_cca_points()

    st.markdown("Points are awarded in a manner such that unique CCAs are assigned higher points. <br> \
                The following explains how points are calculated. <br> \
                1. Calculate the max count of cca (e.g Art and Craft is most common, with 156 schools having this CCA) <br> \
                2. Points = max count of cca - count of cca (e.g There are 10 schools with Choir as CCA. Score for Choir = 156 - 10 = 146)",
                unsafe_allow_html=True)
    
    with st.expander("Top 20 Most Common CCAs", expanded=False):
        show_most_common_cca(df_cca_points)

    with st.expander("Top 20 Most Unique CCAs", expanded=False):
        show_most_unique_cca(df_cca_points)
    
    with st.expander("Show all CCAs and their assigned points", expanded=False):
        show_all_cca(df_cca_points)

with tab3:
    st.subheader("CCA Score by School Type")
    plot_cca_by_school_type(df_school_cca)

with tab4:
    st.subheader("CCA Score by School Nature")
    plot_cca_by_school_nature(df_school_cca)
