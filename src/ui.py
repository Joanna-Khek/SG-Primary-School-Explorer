import pandas as pd
import numpy as np

import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

from PIL import Image
import os 

import plotly.graph_objects as go
import plotly.express as px

from src.utils import read_data, read_cca_points

def set_page_config():
    st.set_page_config(
        page_title = "SG Primary School Explorer",
        page_icon = "🇸🇬",
        layout = "wide",
        initial_sidebar_state = "expanded",
        menu_items = None,
    )

def set_page_container_style() -> None:
    """Set report container style."""

    margins_css = """
    <style>
        /* Configuration of paddings of containers inside main area */
        .main > div {
            max-width: 100%;
            padding-left: 10%;
        }
        /*Font size in tabs */
        button[data-baseweb="tab"] div p {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(margins_css, unsafe_allow_html=True)

def local_css(css_file):
    with open(css_file) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def set_local_css():
    css_file = './stylesheet/style.css'
    local_css(css_file)


def display_main_logo() -> None:
    logo = Image.open("./static/logo.png")
    st.image(logo)


def plot_overview_sankey(categories, label_list_word):
    df_school_full, df_school_cca = read_data()

    # Create a dictionary map for encoding
    school_type_map = {'Government School': 0,
                    'Government-Aided School': 1,
                    'Government-Aided School / Autonomous': 2}
    
    school_nature_map = {'Co-Ed School': 3,
                        'Boys School': 4,
                        'Girls School': 5}

    affiliation_map = {'No': 6,
                    'Yes': 7}

    gep_map = {'No': 8,
            'Yes': 9}
    
    # Encode each column
    extract_columns = categories.copy()
    df_sankey = (df_school_full
                .loc[:, ['Name', 'School_Nature', 'School_Type', 'Affiliation', 'GEP']]
                .assign(School_Nature_Encoded=lambda df_: df_.School_Nature.map(school_nature_map),
                        School_Type_Encoded=lambda df_: df_.School_Type.map(school_type_map),
                        Affiliation_Encoded=lambda df_: df_.Affiliation.map(affiliation_map),
                        GEP_Encoded=lambda df_: df_.GEP.map(gep_map))
                .groupby(categories)['Name'].count()
                .reset_index()
                .rename(columns={'Name': 'Count'})
    )

    # Convert the encoded columns into nodes
    # new_df = pd.DataFrame()
    # for i in range (len(categories)-1):
    #     temp_df = df_sankey[[categories[i], categories[i+1], 'Count']]
    #     temp_df.columns = ['source', 'target', 'count']
    #     new_df = pd.concat([new_df, temp_df])
    new_df = df_sankey.copy()
    new_df.columns = ['source', 'target', 'count']
    new_df = new_df.groupby(['source','target']).agg({'count':'sum'}).reset_index()

    # Convert into source and target 
    label_list = list(np.unique(df_sankey[categories].values))
    source = new_df['source'].apply(lambda x: label_list.index(x))
    target = new_df['target'].apply(lambda x: label_list.index(x))
    count = new_df['count']

    # Plot the Sankey Chart
    label = label_list_word
    link = dict(source = source,
                target = target,
                value = count)
    node = dict(label = label, 
                pad = 50, 
                thickness = 20,
                line = dict(color = "black", width = 0.5))
    data = go.Sankey(link = link, 
                    node = node, 
                    valueformat = ".0f")

    fig = go.Figure(data)
    fig.update_layout(
        hovermode = 'x',
        title="",
        font=dict(size = 12, color = 'black'),
        plot_bgcolor='black',
        #paper_bgcolor='black',
        height=500, 
        width=1000,
    )
    
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

def plot_cca_by_school_type(df_school_cca):
    fig = px.box(df_school_cca,
           x='School_Type',
           y='CCA_Sum_Score',
           points="all",
           width=1200,
           height=800,
           #title="CCA Score by School Type",
           labels={'School_Type':'',
                   'CCA_Sum_Score': 'CCA Score'},
           template="seaborn",
           hover_data = ['Name', 'School_Type'])
    
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

def plot_cca_by_school_nature(df_school_cca):
    fig = px.box(df_school_cca,
           x='School_Nature',
           y='CCA_Sum_Score',
           points="all",
           width=1200,
           height=800,
           #title="CCA Score by School Nature",
           labels={'School_Nature':'',
                   'CCA_Sum_Score': 'CCA Score'},
           template="seaborn",
           hover_data = ['Name', 'School_Type'])
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

def show_school_with_cca(input_cca, df_school_cca_points):
    output = (df_school_cca_points
              .query(f"CCA == '{input_cca}' and Indicator == 1")
              .loc[:,['Name']])
    gb = GridOptionsBuilder.from_dataframe(output)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    gridOptions = gb.build()
    return AgGrid(output, 
                  gridOptions=gridOptions,
                  fit_columns_on_grid_load=True)

def show_most_common_cca(df_cca_points):
    output = (df_cca_points
              .sort_values(by=['Count'], ascending=False)
              .head(20)
    )
    return AgGrid(output, fit_columns_on_grid_load=True)

def show_most_unique_cca(df_cca_points):
    output = (df_cca_points
              .sort_values(by=['Count'], ascending=True)
              .head(20)
    )
    return AgGrid(output, fit_columns_on_grid_load=True)

def show_all_cca(df_cca_points):
    output = (df_cca_points
              .sort_values(by=['Count'], ascending=False)
              .rename(columns={'Count': 'Number of schools with this CCA',
                               'Points': 'Points for this CCA'})
    )
    return AgGrid(output, fit_columns_on_grid_load=True)
 
def phase1_sub_rate(df_school_full):
    
    color_discrete_map = {'Phase1_applied': 'grey',
                      'Phase2A_vac': 'green'}

    fig = px.bar(df_school_full,
        y='Name',
        x=['Phase1_applied', 'Phase2A_vac'],
        custom_data=['Phase1_vac'],
        color_discrete_map = color_discrete_map,
        text_auto='f',
        #title="<b>Phase 1 Subscription Rate</b>",
        labels={'Name': '',
                'value': 'Count'},
        width=1200,
        height=5000)
    fig.update_traces(hovertemplate = "%{value} <br>Total Phase Vacancy: %{customdata[0]}")

    fig.update_layout(legend_title="Legend",
                    yaxis={'categoryorder':'category descending'})
    fig.update_traces(textposition='inside', textfont_color='white')
    newnames = {'Phase1_applied':'Subscribed', 'Phase2A_vac': 'Remaining Vacancy'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    fig.update_layout(hovermode="y unified")
    fig.update_xaxes(visible=False, showticklabels=False)

    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

def phase2A_sub_rate(df_school_full):
    color_discrete_map = {'Phase2A_applied': 'grey',
                      'After_Phase1_2A_vac': 'green'}

    fig = px.bar(df_school_full,
        y='Name',
        x=['Phase2A_applied', 'After_Phase1_2A_vac'],
        custom_data=['Phase2A_vac','Phase2A_oversub_count'],
        color_discrete_map = color_discrete_map,
        text_auto='f',
        #title="<b>Phase 2A Subscription Rate (Count)</b>",
        labels={'Name': ''},
                #'value': 'Count'},
        width=1200,
        height=5000)

    fig.update_traces(hovertemplate = "%{value} <br>Total Phase Vacancy: %{customdata[0]} <br>Oversubscribed: %{customdata[1]}")

    fig.update_layout(legend_title="Legend",
                    yaxis={'categoryorder':'category descending'})
    fig.update_traces(textposition='inside', textfont_color='white')
    newnames = {'Phase2A_applied':'Subscribed', 'After_Phase1_2A_vac': 'Remaining Vacancy'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    fig.update_layout(hovermode="y unified")
    fig.update_xaxes(visible=False, showticklabels=False)

    for i in range(len(df_school_full)):
        if (df_school_full.Phase2A_oversub[i] == 'Yes'):
            fig.add_shape(
                type="circle",
                line_color="red",
                x0=df_school_full.Phase2A_vac[i],
                y0=df_school_full.Name[i],
                x1=df_school_full.Phase2A_vac[i],
                y1=df_school_full.Name[i+1],
                name='Oversub'
            )
            fig.add_annotation(x=df_school_full.Phase2A_vac[i], y=df_school_full.Name[i],
                text=f"Oversub: {df_school_full.Phase2A_oversub_count[i]}",
                showarrow=True,
                arrowhead=1,
                ax=20,
                bordercolor="#c7c7c7",
                bgcolor="#ff7f0e",
                opacity=0.8,
                font=dict(
                        color="#000000"
                        )
                )
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

def phase2B_sub_rate(df_school_full):
    color_discrete_map = {'Phase2B_applied': 'grey',
                      'After_Phase2B_vac': 'green'}

    fig = px.bar(df_school_full,
        y='Name',
        x=['Phase2B_applied', 'After_Phase2B_vac'],
        custom_data=['Phase2B_vac','Phase2B_oversub_count'],
        color_discrete_map = color_discrete_map,
        text_auto='f',
        #title="<b>Phase 2B Subscription Rate (Count)</b>",
        labels={'Name': ''},
                #'value': 'Count'},
        width=1200,
        height=5000)

    fig.update_traces(hovertemplate = "%{value} <br>Total Phase Vacancy: %{customdata[0]} <br>Oversubscribed: %{customdata[1]}")

    fig.update_layout(legend_title="Legend",
                    yaxis={'categoryorder':'category descending'})
    fig.update_traces(textposition='inside', textfont_color='white')
    newnames = {'Phase2B_applied':'Subscribed', 'After_Phase2B_vac': 'Remaining Vacancy'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    fig.update_layout(hovermode="y unified")
    fig.update_xaxes(visible=False, showticklabels=False)

    for i in range(len(df_school_full)):
        if (df_school_full.Phase2B_oversub[i] == 'Yes'):
            fig.add_shape(
                type="circle",
                line_color="red",
                x0=df_school_full.Phase2B_vac[i],
                y0=df_school_full.Name[i],
                x1=df_school_full.Phase2B_vac[i],
                y1=df_school_full.Name[i+1],
                name='Oversub'
            )
            fig.add_annotation(x=df_school_full.Phase2B_vac[i], y=df_school_full.Name[i],
                text=f"Oversub: {df_school_full.Phase2B_oversub_count[i]}",
                showarrow=True,
                arrowhead=1,
                ax=20,
                bordercolor="#c7c7c7",
                bgcolor="#ff7f0e",
                opacity=0.8,
                font=dict(
                        color="#000000"
                        )
                )
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

def phase2C_sub_rate(df_school_full):
    color_discrete_map = {'Phase2C_applied': 'grey',
                      'After_Phase2C_vac': 'green'}

    fig = px.bar(df_school_full,
        y='Name',
        x=['Phase2C_applied', 'After_Phase2C_vac'],
        custom_data=['Phase2C_vac','Phase2C_oversub_count'],
        color_discrete_map = color_discrete_map,
        text_auto='f',
        #title="<b>Phase 2C Subscription Rate (Count)</b>",
        labels={'Name': ''},
                #'value': 'Count'},
        width=1200,
        height=5000)

    fig.update_traces(hovertemplate = "%{value} <br>Total Phase Vacancy: %{customdata[0]} <br>Oversubscribed: %{customdata[1]}")

    fig.update_layout(legend_title="Legend",
                    yaxis={'categoryorder':'category descending'})
    fig.update_traces(textposition='inside', textfont_color='white')
    newnames = {'Phase2C_applied':'Subscribed', 'After_Phase2C_vac': 'Remaining Vacancy'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    fig.update_layout(hovermode="y unified")
    fig.update_xaxes(visible=False, showticklabels=False)

    for i in range(len(df_school_full)):
        if (df_school_full.Phase2C_oversub[i] == 'Yes'):
            fig.add_shape(
                type="circle",
                line_color="red",
                x0=df_school_full.Phase2C_vac[i],
                y0=df_school_full.Name[i],
                x1=df_school_full.Phase2C_vac[i],
                y1=df_school_full.Name[i+1],
                name='Oversub'
            )
            fig.add_annotation(x=df_school_full.Phase2C_vac[i], y=df_school_full.Name[i],
                text=f"Oversub: {df_school_full.Phase2C_oversub_count[i]}",
                showarrow=True,
                arrowhead=1,
                ax=20,
                bordercolor="#c7c7c7",
                bgcolor="#ff7f0e",
                opacity=0.8,
                 font=dict(
                        color="#000000"
                        )
                )
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')
