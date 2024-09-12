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

On this page, we showcase the functionality of synthetic data by presenting a synthetic dataset on homicide in the Netherlands.
This dataset is based on the Dutch Homicide Monitor, a detailed dataset on homicides administered by researchers at Leiden University. Read on to find more information on the Dutch Homicide Monitor.
Open-access research related to the Dutch Homicide Monitor and other research on homicide in the Netherlands can found under the tab "Research on Homicide".

To explore the synthetic homicide data, click on the tab "Data Explorer"

How to explore the data: 
1. Select any filter you want to apply (or none)
2. Select the characteristics of homicides you wish to see more about
3. Explore the graphs based on your filters and selection
       
***
""")

# Short introduction to synthetic data, link to videos

tab1, tab2, tab3 = st.tabs(["Dutch Homicide Monitor","Data Explorer","Research on Homicide"])

with tab1:
    st.write(
        """
        The Dutch Homicide Monitor is a dataset that entails detailed information on homicides occuring in the Netherlands since 1992.
        The dataset is administered by violence researchers working at the Institute of Security and Global Affairs at Leiden University, the Netherlands.
        The Dutch Homicide Monitor is part of the European Homicide Monitor initiative, which aims to provide a comparable framework for researchers to collect data on homicides in Europe, and beyond.
        More information about the European Homicide Monitor can be found in [this website](https://www.universiteitleiden.nl/en/research/research-projects/governance-and-global-affairs/european-homicide-monitor#tab-1).
        """)
    
    st.write("#### The Dutch Homicide Monitor")
    dhmvid= open('WebApp/Visuals/SENSYN_DHM_2.mp4', 'rb')
    DHMvid = dhmvid.read()
    st.video(DHMvid)

    st.write("""

             
#### What for information is collected in the Dutch Homicide Monitor?
             
The Dutch Homicide Monitor collects information on the homicide cases, such as the crimescene and time, as well as individual information on victims and perpetrators, such as their age and gender.
Over the years, researchers have collected information on more than 80 characteristics of homicides. An overview of these detailed characteristics can be found in 
[this manual](https://www.universiteitleiden.nl/binaries/content/assets/governance-and-global-affairs/isga/data-protocol-manual-ehm_website.pdf).

Since 2023, the main characteristics have been distilled into a 
[nucleus version](https://www.universiteitleiden.nl/binaries/content/assets/governance-and-global-affairs/isga/ehm_coding-manual_nucleus-variables_final.pdf) of the Dutch Homicide Monitor.
             
The details collected in the Dutch Homicide Monitor allow us to answer the most common questions about the phenomenon of homicide:
             
What happened?
Where and when did the homicide occur?
How was the homicide committed?
Who was involved in the homicide, either as victim or as (suspected) perpetrator?
Why did the homicide occur?
What are the (judicial) consequences?
             
***
             
#### Where do we get this information?

In order to get as much trustworthy and complete information on homicides as possible, we collect data from several sources and combine them into the Dutch Homicide Monitor.
Some of these sources are public, such as news articles, the annual homicide list by Elsevier Magazine, or public court rulings. Other sources are non-public, such as the data received by
the Dutch National Police, the public prosecution office, or forensic health records of (suspected) perpetrators.
             
Combined, these sources provide the most complete and detailed picture of homicide in the Netherlands. 

""")

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

    with tab3:
        st.write("""
This page is a collection of academic research on homicide in the Netherlands.
             
#### Research that features data from the Dutch Homicide Monitor

- Aarten, P.G.M., van Harmelen, A.L., & Liem, M. (2024) Juvenile homicide in the Netherlands. in The Routledge International Handbook of Juvenile Homicide (pp.105-118). Routledge.
- [Krüsselmann, K., Aarten, P.G.M. & Liem, M. (2024). Missing the mark? A typology of lethal and non-lethal firearm violence in the Netherlands. Crime & Delinquency, 00111287241242483](https://journals.sagepub.com/doi/pdf/10.1177/00111287241242483)
- [Suonpää, K., Kivivuori, J., Ahven, A., Granath, S., Markwalder, N., Skott, S., Thomsen, A.H., Walser, S., & Liem, M. (2024). Homicide drop in seven European countries: General or specific across countries and crime types? European Journal of Criminology, 21(1), 3-30](https://journals.sagepub.com/doi/pdf/10.1177/14773708221103799)
- [van Breen, J., Rabolini, A. & Liem, M. (2024). Old habits die hard: assessing the validity of using homicide as an indicator of other violent crime. European Journal of Criminology, 21(3), 452-466](https://journals.sagepub.com/doi/pdf/10.1177/14773708231211170)
- [Aarten, P.G.M., & Liem, M. C. (2023). Unravelling the homicide drop: Disaggregating a 25-year homicide trend in the Netherlands. European journal on criminal policy and research, 29(1), 1-26.](https://link-springer-com.ezproxy.leidenuniv.nl/article/10.1007/s10610-021-09489-0)
- [Krüsselmann, K., Aarten, P.G.M., Granath, S., Kivivuori, J., Markwalder, N., Suonpää, K., Thomsen, A.-H., Walser, S., & Liem, M. (2023). Firearm homicides in Europe: A comparison with non-firearm homicides in five European countries. Global Crime, 24(2), 145-167](https://www.tandfonline.com/doi/pdf/10.1080/17440572.2023.2211513)
- [van Breen, J. & Liem, M. (2023). When it rains it pours? A time-series approach to the relationship between homicide and other adverse health phenomena. Journal of Public Health, 1-6](https://link.springer.com/article/10.1007/s10389-023-01929-x)
- [van Breen, J., ten Voorde, J., & Liem, M. (2023). Understanding ethnic disparities in lethal police incidents in the Netherlands between 2016 and 2020. Homicide Studies, 10887679231208676](https://journals.sagepub.com/doi/full/10.1177/10887679231208676)
- [Liem, M. & Krüsselmann, K. (2022). The way of the gun: Firearm trafficking and its impact on violence in the Netherlands. Brussels: Flemish Peace Institute](https://vlaamsvredesinstituut.eu/wp-content/uploads/2022/11/TARGET_Netherlands5.pdf)
- [Liem, M., Aarten, P.G.M. & Vüllers, J. (2022). From detection to sentencing: a homicide case flow analysis of the Dutch criminal justice system. Policing and society, 32(4), 560-576](https://www.tandfonline.com/doi/pdf/10.1080/10439463.2021.1933484)
- [van Breen, J. & Liem, M. (2022). Clustering of homicide with other adverse health outcomes in the Netherlands. Preventive medicine reports, 30, 101988](https://www.sciencedirect.com/science/article/pii/S2211335522002959)
- [Liem, M., Suonpää, K., Lehti, M., Kivivuori, J., Granath, S., Walser, S., & Killias, M. (2019). Homicide clearance in western Europe. European Journal of Criminology, 16(1), 81-101](https://journals.sagepub.com/doi/full/10.1177/1477370818764840)
- [Ganpat, S. (2017). Comparing characteristics of homicides in Finland, the Netherlands, and Sweden. In The Handbook of Homicide, 308-319](https://repository.derby.ac.uk/download/8b57ba14e85f58f7dd44dc155902cd38c93eb08af32c1dfab5dfe6e20a0793d0/932015/Ganpat%20European%20Homicide%20Monitor_International%20Handbook%20on%20Homicide_editor%20version.pdf)
- [Liem, M., Ganpat, S., Granath, S., Hagstedt, J., Kivivuori, J., Lehti, M., & Nieuwbeerta, P. (2013). Homicide in Finland, the Netherlands, and Sweden: First findings from the European homicide monitor. Homicide Studies, 17(1), 75-95.](https://journals.sagepub.com/doi/full/10.1177/1088767912452130?casa_token=gKCgMOOngQ8AAAAA:rWqFE8knJa047u1YZDs6QWa_APrPmrJ1ZT913m4tCIdPqnrVpPtKYak_ktE8xapEXlIZ9TN5_tZ7)
- [Liem, M., Barber, C., Markwalder, N., Killias, M. & Nieuwbeerta, P. (2011). Homicide-suicide and other violent deaths: An international comparison. Forensic Science International, 207(1-3), 70-76](https://www.sciencedirect.com/science/article/pii/S0379073810004378?casa_token=ABtExmAleqUAAAAA:BpFmdpaLDx6VX9Cei75UUEfACAi6FsnsHJP3qvrY2PvUZxL8v2YeoL4VExmwfx19ZorrHrz3TQ)
- [Granath, S., Hagstedt, J., Kivivuori, J., Lehti, M., Ganpat, S., Liem, M., Nieuwbeerta, P. (2011). Homicide in Finland, the Netherlands and Sweden: A first study on the European Homicide Monitor data. Stockholm: The Swedish National Council for Crime PRevention](https://irep.ntu.ac.uk/id/eprint/28206/1/5724_Ganpat.pdf)
- [Liem, M. & Nieuwbeerta, P. (2010). Homicide followed by suicide: a comparison with homicide and suicide. Suicide and Life-Threatening Behavior, 40(2), 133-145](https://guilfordjournals.com/doi/pdf/10.1521/suli.2010.40.2.133?casa_token=gFZgy9mgnysAAAAA:jXpioPX1aGvXstKZR5fGt_ms5Puw8m2Njn309X-4jXRzo0mtvXlnAaomgEJJWk6ISlhUgujB6Bo)
***
             
#### Other research on homicide in the Netherlands

- [Nieuwbeerta, P., McCall, P.L., Elffers, H., & Wittebrood, K. (2008). Neighborhood characteristics and individual homicide risks: effects of social cohesion, confidence in the police, and socioeconomic disadvantage. Homicide Studies, 12(1), 90-116](https://core.ac.uk/download/pdf/232378147.pdf)
- [Nieuwbeerta, P. (2003). Homicide offenders and their criminal trajectories in the Netherlands. Conference Proceedings of the 2003 Homicide Research Working Group, 41-58](https://hrwg1991.org/wp-content/uploads/2019/07/proceedings_2003.pdf#page=49)
- [Nieuwbeerta, P., & Leistra, G. (2002). Homicide in the Netherlands: A summary of all cases in the period 1992-2001. Proceedings of the 2002 Meeting of the Homicide Research Working Group](https://hrwg1991.org/wp-content/uploads/2019/07/proceedings_2002.pdf#page=233)
- [Smit, P.R., Bijleveld, C., Van der Zee, S. (2001). Homicide in the Netherlands: an exploratory study of the 1998 cases. Homicide Studies, 5(4), 293-310](https://journals.sagepub.com/doi/pdf/10.1177/1088767901005004004)
***
             
#### Other research that features data from European Homicide Monitor

- [Kivivuori, J., Liem, M. & Markwalder, N. (2024). European Homicide Monitor: Research, New Developments, and Future. Journal of Contemporary Criminal Justice, p.10439862241253386](https://journals.sagepub.com/doi/pdf/10.1177/10439862241253386)
- [Liem, M., Ganpat, S., Granath, S., Hagstedt, J., Kivivuori, J., Lehti, M., & Nieuwbeerta, P. (2013). Homicide in Finland, the Netherlands, and Sweden: First findings from the European homicide monitor. Homicide Studies, 17(1), 75-95.](https://journals.sagepub.com/doi/full/10.1177/1088767912452130?casa_token=gKCgMOOngQ8AAAAA:rWqFE8knJa047u1YZDs6QWa_APrPmrJ1ZT913m4tCIdPqnrVpPtKYak_ktE8xapEXlIZ9TN5_tZ7)
- [Granath, S., Hagstedt, J., Kivivuori, J., Lehti, M., Ganpat, S., Liem, M., Nieuwbeerta, P. (2011). Homicide in Finland, the Netherlands and Sweden: A first study on the European Homicide Monitor data. Stockholm: The Swedish National Council for Crime PRevention](https://irep.ntu.ac.uk/id/eprint/28206/1/5724_Ganpat.pdf)          

""")       