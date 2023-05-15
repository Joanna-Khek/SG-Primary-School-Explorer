import streamlit as st
import pandas as pd
from src.ui import set_page_config
from src.ui import set_page_container_style
from src.ui import set_local_css
from src.ui import display_main_logo

if __name__ == "__main__":

    set_page_config()
    set_local_css()
    set_page_container_style()
    display_main_logo()

    st.divider()
    st.title("About")
    st.markdown('The goal of this web application is to assist parents in selecting a primary school for their children. \
                <br> \
                <br> \
                The 2022 information in this web application are scraped from various sources below. <br>',
                unsafe_allow_html=True)
    
    with st.expander("School Information", expanded=True):
        st.markdown("**MOE School Finder**: https://www.moe.gov.sg/schoolfinder?journey=Primary%20school", unsafe_allow_html=True)
    with st.expander("School Vacancy Information", expanded=True):
        st.markdown("**P1 Ballot History 2022**: https://sgschooling.com/year/2022/all.html", unsafe_allow_html=True)

    st.markdown("If you would like to provide feedback, please contact me here.")

    with st.expander("Contact Me", expanded=True):
        st.markdown("**Website**: https://joanna-khek.github.io/ \
                    <br> \
                    **Email**: joannakhek@gmail.com", unsafe_allow_html=True)

   