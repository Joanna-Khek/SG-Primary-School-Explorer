import streamlit as st
import pandas as pd
from utils import read_data
from ui import phase1_sub_rate, phase2A_sub_rate, phase2B_sub_rate, phase2C_sub_rate
from ui import set_local_css, set_page_config

set_page_config()
set_local_css()

df_school_full, df_school_cca = read_data()

tab1, tab2, tab3, tab4 = st.tabs(["Phase 1", "Phase 2A", "Phase 2B", "Phase 2C"])
with tab1:
    st.subheader("Phase 1")
    with st.expander("Phase 1", expanded=True):
        st.markdown("For a child who has a sibling studying in the primary school", unsafe_allow_html=True)

    phase1_sub_rate(df_school_full)

with tab2:
    st.subheader("Phase 2A")
    with st.expander("Phase 2A", expanded=True):
        st.markdown("""
        Parent or sibling is a former student of the primary school, including those who have joined the alumni association of the primary school as a member <br> \
        <br>Whose parent is a member of the School Advisory or Management Committee <br> \
        <br>Whose parent is a staff member of the primary school <br> \
        <br>From the MOE Kindergarten under the purview of and located within the primary school<br>
        """, unsafe_allow_html=True)
        
    phase2A_sub_rate(df_school_full)

with tab3:
    st.subheader("Phase 2B")
    with st.expander("Phase 2B", expanded=True):
        st.markdown("""
        Whose parent has joined the primary school as a parent volunteer not later than 1 July of the year before P1 registration \
        and has given at least 40 hours of voluntary service to the school by 30 June of the year of P1 registration <br>
        <br> Whose parent is a member endorsed by the church or clan directly connected with the primary school <br>
        <br> Whose parent is endorsed as an active community leader <br>
        <br> We will reserve 20 places in each primary school for Phase 2B to ensure continued access to all primary schools <br>
        <br>Children who gain priority admission into a school under the "Parent is endorsed as an active community leader" eligibility \
            and the school is within 2km of their address used for registration is required to reside at that address for at least 30 months \
            from the start of the P1 Registration Exercise<br>
        """, unsafe_allow_html=True)
    
    phase2B_sub_rate(df_school_full)

with tab4:
    st.subheader("Phase 2C")
    with st.expander("Phase 2C", expanded=True):
        st.markdown("""
        For a child who is not yet registered in a primary school <br>
        <br>We will reserve 40 places in each primary school for Phase 2C to ensure continued open access to all primary schools<br>
        """, unsafe_allow_html=True)
    phase2C_sub_rate(df_school_full)
