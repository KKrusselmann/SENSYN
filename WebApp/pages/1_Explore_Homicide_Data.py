import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.colors as pcolors
from streamlit_extras.app_logo import add_logo
from streamlit_extras.bottom_container import bottom

###### SYNTHETIC DATA #####

DHM_s = pd.read_csv('WebApp/Data/synthetic_caselevel.csv', encoding='utf-8', dtype={'YEARCOM':'category','PRINCIPAL':'category'})

# Preparation of the dataset for visualization purposes only: re-naming age categories & renaming variable names.

agecat_mapping = {
    '7to17':'7-17',
    '40to64':'40-64',
    '25to39':'25-39',
    '>=65':'65 or older',
    '18to24':'18-24',
    '<=6':'6 or younger',
    'Missing':'Missing'
}

DHM_s['AGE_perp']=DHM_s['AGE_perp'].replace(agecat_mapping)
DHM_s['AGE_vic']=DHM_s['AGE_vic'].replace(agecat_mapping)

# Structure of the page
def add_logo_sidebar(image_path, image_width):
    st.sidebar.image(image_path, width=image_width)

st.set_page_config(page_title="Explore Homicide Data",
                   page_icon=":bar_chart:",
                   layout="wide")

add_logo_sidebar("WebApp/Visuals/logo.png", 150)
add_logo_sidebar("WebApp/Visuals/lumc_logo.png", 150)

# Introduction page
st.write("""
# Explore Homicide Data
***

On this page, you can explore various aspects of homicide in the Netherlands youself.
Due to privacy regulations, the data displayed on this page does not refer to real homicide cases, but is based on synthetic data (see tab "Synthetic Data" for more information).
As a result, slight disparities with official statistics might occur.

To learn more about the data, continue reading. 
To explore the data, click on the tab "Data Explorer"

How to explore the data: 
1. Select any filter you want to apply (or none)
2. Select the characteristics of homicides you wish to see more about
3. Explore the graphs based on your filters and selection
       
***
""")

# Short introduction to synthetic data, link to videos

tab1, tab2 = st.tabs(["Data on this page","Data Explorer"])

with tab1:
    st.write("""
             #### Synthetic Homicide Data: What to know

             Before using the data explorer on the next tab, have a look at the short videos down below that explain what synthetic data actually is
             and how it compares to real-world data. Want a more detailed explanation? Take a look at the tab 'Synthetic Data'.
                
             """)
    col1, col2 =st.columns(2)

    with col1:
        st.write("#### What is synthetic data?")
        syntheticvid= open('WebApp/Visuals/syntheticdata.mp4', 'rb')
        synthvid = syntheticvid.read()
        st.video(synthvid)

    with col2:
        st.write("#### How is synthetic data generated?")
        synthesisvid=open('WebApp/Visuals/datasynthesis.mp4','rb')
        synthesisvide=synthesisvid.read()
        st.video(synthesisvid)

# Main data page: setting filters, figures and dataset

with tab2:
    st.write("#### Filter: Display of information.")
    col1,col2=st.columns(2)
    with col1:
    
        filter_caselevel=st.radio("Do you want the information to be displayed for each...",["homicide case","homicide victim"])
    

    st.write("***")

    st.write("#### Filter: Case characteristics")
    col1,col2=st.columns(2)

    with col1:
        
        filter_modus=st.multiselect("Modus operandi",options=DHM_s['MODUS'].unique())

        filter_crimescene=st.multiselect("Crimescene",options=DHM_s["CRIMESCENE"].unique())
        
        filter_typehom=st.multiselect("Context of the homicide",options=DHM_s["TYPEHOM"].unique())

        filter_solved=st.multiselect("Is the case solved?", options=DHM_s["PROCESS"].unique())

    with col2:

        filter_nrvic = st.radio("Number of Victims:",['No Filter',"Single","Multiple"])

        filter_nrperp = st.radio("Number of Perpetrators:",['No Filter',"Single","Multiple"])

    st.write("***")
    st.write("#### Filter: Individual characteristics")
    col1, col2 = st.columns(2)

    with col1:
        filter_gender_v = st.radio("Gender Victim:",['No Filter',"Male","Female"])
        filter_gender_p = st.radio("Gender Perpetrator:",['No Filter',"Male","Female"])
    
    with col2:
         options_age = DHM_s['AGE_vic'].unique()
         options_sorted = sorted(options_age)
         filter_age_v=st.multiselect("Age of victim",options=options_sorted)
         filter_age_p=st.multiselect("Age of perpetrator",options=options_sorted)
         filter_bc_v=st.multiselect("Birthcountry of victim",options=DHM_s["BIRTHCOUNTRY_vic"].unique())
         filter_bc_p=st.multiselect("Birthcountry of perpetrator",options=DHM_s["BIRTHCOUNTRY_perp"].unique())

    st.write("***")

    def filter_dataset(DHM_s, filter_caselevel, filter_gender_v, filter_gender_p, filter_nrvic, filter_nrperp, filter_age_p, filter_age_v, filter_bc_v, filter_bc_p, filter_modus, filter_solved, filter_crimescene, filter_typehom):
        query_expr = ''
        if filter_caselevel == 'homicide case':
            query_expr += 'PRINCIPAL == "Yes, principal victim" and '
        if filter_gender_v != "No Filter":
            query_expr += f'GENDER_vic == "{filter_gender_v}" and '
        if filter_gender_p != "No Filter":
            query_expr += f'GENDER_perp == "{filter_gender_p}" and '
        if filter_nrvic != "No Filter":
            query_expr += f'NRVIC_cat == "{filter_nrvic}" and '
        if filter_nrperp != "No Filter":
            query_expr += f'NRPERP == "{filter_nrperp}" and '
        if filter_age_p:
            age_p_expr = ' or '.join([f'AGE_perp == "{age_perp}"' for age_perp in filter_age_p])
            query_expr += f'({age_p_expr}) and '
        if filter_age_v:
            age_v_expr = ' or '.join([f'AGE_vic == "{age_vic}"' for age_vic in filter_age_v])
            query_expr += f'({age_v_expr}) and '
        if filter_bc_v:
            bc_v_expr = ' or '.join([f'BIRTHCOUNTRY_vic == "{birthcountry_vic}"' for birthcountry_vic in filter_bc_v])
            query_expr += f'({bc_v_expr}) and '
        if filter_bc_p:
            bc_p_expr = ' or '.join([f'BIRTHCOUNTRY_perp == "{birthcountry_perp}"' for birthcountry_perp in filter_bc_p])
            query_expr += f'({bc_p_expr}) and '
        if filter_modus:
            modus_filter_expr = ' or '.join([f'MODUS == "{modus}"' for modus in filter_modus])
            query_expr += f'({modus_filter_expr}) and '
        if filter_solved:
            solved_filter_expr = ' or '.join([f'PROCESS == "{process}"' for process in filter_solved])
            query_expr += f'({solved_filter_expr}) and '
        if filter_crimescene:
            crimescene_filter_expr = ' or '.join([f'CRIMESCENE == "{crimescene}"' for crimescene in filter_crimescene])
            query_expr += f'({crimescene_filter_expr}) and '
        if filter_typehom:
            typehom_filter_expr = ' or '.join([f'TYPEHOM == "{typehom}"' for typehom in filter_typehom])
            query_expr += f'({typehom_filter_expr}) and '
        if query_expr.endswith(' and '):
            query_expr = query_expr[:-5]
        if query_expr:
            filtered_DHM = DHM_s.query(query_expr)
        else:
            filtered_DHM = DHM_s
        return filtered_DHM
    

    filtered_DHM = filter_dataset(DHM_s, filter_caselevel, filter_gender_v, filter_gender_p, filter_nrvic, filter_nrperp, filter_age_p, filter_age_v, filter_bc_p, filter_bc_v, filter_modus, filter_solved, filter_crimescene, filter_typehom)
    columns_drop = ['TYPE','YEARCOM','NUTS3','SUICIDE','PRINCIPAL']
    filtered_DHM = filtered_DHM.drop(columns=columns_drop)

    st.write("#### Homicide in charts (based on selected filters)")
    st.write("Select one or two variables from the list below. Please note: the filter selected on top of the page apply to the figures below. If you wish to display the graphs for all homicide victims or cases, please reset your filters.")


        # CREATING GRAPHS to be displayed
    color_sequence = pcolors.qualitative.Plotly
    color_map={'Missing':'red'}

    def get_color_map(filtered_DHM, color_map, color_sequence):
        unique_categories = pd.unique(filtered_DHM.values.ravel('K'))
        color_idx = 0
        for category in unique_categories:
            if category not in color_map:
                color_map[category] = color_sequence[color_idx%len(color_sequence)]
                color_idx += 1
        return color_map
    
    color_map = get_color_map(filtered_DHM, color_map, color_sequence)
    

    label_map = {
        'CITY': 'Urban vs rural',
        'TIME': 'Time of day',
        'NRVIC_cat': 'Single vs multiple homicide victims',
        'NRPERP': 'Single vs multiple homicide perpetrators',
        'CRIMESCENE': 'Type of crimescene',
        'MODUS': 'Type of weapon used',
        'TYPEHOM': 'Context of homicide',
        'RELAT': 'Victim-perpetrator relationship',
        'PROCESS': 'Solved vs unsolved homicide',
        'GENDER_vic': 'Gender of victim',
        'GENDER_perp': 'Gender of main perpetrator',
        'AGE_vic': 'Age of victim',
        'AGE_perp': 'Age of main perpetrator',
        'BIRTHCOUNTRY_vic':'Birthcountry of victim',
        'BIRTHCOUNTRY_perp':'Birthcountry of main perpetrator',
        'SUICIDE':'Suicide(attempt) by main perpetrator',
        'Missing': 'Missing Data'
    } 
        
    def plot_pie_graph(filtered_DHM, col):
        pie_filtered_DHM = filtered_DHM[col].value_counts(normalize=True).reset_index()
        pie_filtered_DHM.columns = [col, 'percentage']
        pie_filtered_DHM['percentage'] *= 100
        fig = px.pie(pie_filtered_DHM, names=col, values='percentage', color=col, color_discrete_map=color_map)
        st.plotly_chart(fig)
    
    def plot_count_bar_graph(filtered_DHM, x_col, y_col):
        fig = px.bar(filtered_DHM, x=x_col, color=y_col, barmode='stack', color_discrete_map=color_map)
        st.plotly_chart(fig)

    def plot_percentage_bar_graph(filtered_DHM, x_col, y_col):
        #Calculate percentages
        percentage_filtered_DHM = filtered_DHM.groupby([x_col, y_col]).size().reset_index(name='count')
        percentage_filtered_DHM['percentage'] = percentage_filtered_DHM.groupby(x_col)['count'].transform(lambda x: x / x.sum() * 100)
        fig=px.bar(percentage_filtered_DHM, x=x_col, y='percentage', color=y_col, barmode='stack',color_discrete_map=color_map)
        fig.update_layout(yaxis_title='Percentage')        
        st.plotly_chart(fig)

    

    categorical_columns=filtered_DHM.select_dtypes(include=['object']).columns
    excluded_columns=['NUTS3']
    filtered_columns = [col for col in categorical_columns if col not in excluded_columns]

    col3, col4 =st.columns(2)

    with col3:
        option1=st.selectbox('Select your first variable', options=[label_map[opt] for opt in filtered_columns])
    
    with col4:
        option2=st.selectbox('Select the second variable', options=[label_map[opt] for opt in filtered_columns])
    
    if option1 and option2:
        reverse_label_map = {v: k for k, v in label_map.items()}

        option1 = reverse_label_map.get(option1, option1)
        option2 = reverse_label_map.get(option2, option2)

        if option1 == option2:
            st.subheader(f'{label_map[option1]}')
            plot_pie_graph(filtered_DHM, option1)
        else:
            with col3:
                st.subheader(f'{label_map[option1]}')
                plot_pie_graph(filtered_DHM, option1)

                st.subheader(f'{label_map[option1]} per {label_map[option2]}')
                plot_count_bar_graph(filtered_DHM, option1, option2)

                st.subheader(f'{label_map[option2]} per {label_map[option1]}')
                plot_count_bar_graph(filtered_DHM, option2, option1)
            
            with col4:
                st.subheader(f'{label_map[option2]}')
                plot_pie_graph(filtered_DHM, option2)

                st.subheader(f'{label_map[option1]} per {label_map[option2]} in %')
                plot_percentage_bar_graph(filtered_DHM, option1, option2)

                st.subheader(f'{label_map[option2]} per {label_map[option1]} in %')
                plot_percentage_bar_graph(filtered_DHM, option2, option1)

    st.write("***")
    st.write("#### Homicide cases fitting your selected filters:")

    #Renaming of variable labels for accessibility purposes.
    filtered_DHM.rename(columns=label_map, inplace=True)
    st.write(filtered_DHM)