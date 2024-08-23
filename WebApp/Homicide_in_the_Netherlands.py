###### STREAMLIT #####

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from folium import Choropleth, CircleMarker
from streamlit_folium import folium_static
import geopandas as gpd
from streamlit_extras.app_logo import add_logo
from streamlit_extras.bottom_container import bottom


###### REAL DATA #####

DHM_r = pd.read_csv('WebApp/Data/Hom_Rates.csv', encoding='utf-8', sep=';')
DHM_r = pd.DataFrame(DHM_r)
DHM_r.rename(columns={'Hom_Rate':'Homicide Rate','M_Hom_Rate':'Male Homicide Rate', 'F_Hom_Rate':'Female Homicide Rate'}, inplace=True)
DHM_r.rename(columns={'IPH_Rate':'IPH Rate','Dom_Rate':'Domestic Homicide Rate', 'Crim_Rate':'Criminal Homicide Rate', 'Rob_Rate':'Robbery Homicide Rate', 'Disp_Rate':'Dispute Homicide Rate', 'Oth_Rate':'Other Homicide Rate'}, inplace=True)
DHM_r.columns.values[0]='Year'

DHM_r['Homicide Rate']=DHM_r['Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['Male Homicide Rate']=DHM_r['Male Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['Female Homicide Rate']=DHM_r['Female Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['IPH Rate']=DHM_r['IPH Rate'].str.replace(',','.').astype(float)
DHM_r['Domestic Homicide Rate']=DHM_r['Domestic Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['Criminal Homicide Rate']=DHM_r['Criminal Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['Robbery Homicide Rate']=DHM_r['Robbery Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['Dispute Homicide Rate']=DHM_r['Dispute Homicide Rate'].str.replace(',','.').astype(float)
DHM_r['Other Homicide Rate']=DHM_r['Other Homicide Rate'].str.replace(',','.').astype(float)


###### STREAMLIT HOMICIDE IN THE NETHERLANDS #####

def add_logo_sidebar(image_path, image_width):
    st.sidebar.image(image_path, width=image_width)

st.set_page_config(page_title="Homicide in the Netherlands",
                   page_icon=":knife:",
                   layout="wide")

add_logo_sidebar('WebApp/Visuals/logo.png', 150)  # Adjust path and width as needed
add_logo_sidebar('WebApp/Visuals/lumc_logo.png', 150)  # Adjust path and width as needed

st.write("""
# Homicide in the Netherlands
***
         
This page is meant as an informational hub on homicide in the Netherlands.\n
The information on this page is based on the Dutch Homicide Monitor, which is administered by criminologists at Leiden University.
Due to personal information in the Dutch Homicide Monitor, it is not possible to display details about each homicide case, nor to display all information gathered in the Dutch Homicide Monitor.
If you want to explore detailed homicide data yourself, please have a look at the page **Explore Homicide Data**, which uses a synthetic dataset based on the Dutch Homicide Monitor.
Curious what synthetic data is? Have a look at the page **Synthetic Data**. If you want to know more about the project that enabled us to make synthetic dataset and this webpage, take a look at **Project SENSYN**.
         
Questions about homicides in the Netherlands or the project that are not answered here? Feel free to contact us!
       
***
""")

tab1, tab2, tab3 = st.tabs(["Some Statistics","Dutch Homicide Monitor","Research"])

with tab1:
    st.write("""
 #### Prevalence of Homicide

The homicide rate in the Netherlands has been **declining** steadily since the beginning of the century.\n
In the last five years, on average 110 homicides took place each year, which accounts for **0.6 homicides per 100.000 population**. 
Compared to the global and European average, the Dutch homicide rate is relatively low.       
""")
    fig_hr = px.line(DHM_r, x='Year', y='Homicide Rate', title='Homicide Rate (2001-2020)')
    st.plotly_chart(fig_hr, use_container_width=True)
    st.write("Cite as: Dutch Homicide Monitor (2024)")
    st.write("***")
    st.write("""
#### Homicide throughout the country

The homicide rate across the Dutch provinces varies. The highest homicide rate (2011-2020) is measured in North Holland (0.94 per 100.000 population; the lowest in Gelderland (0.48 per 100.000 population.\n
On the city-level, the most homicides are registered in Amsterdam, followed by Rotterdam, the Hague and Utrecht.

""")
    regions_data = pd.DataFrame({
    'Region': ['Groningen', 'Friesland', 'Drenthe', 'Overijssel', 'Flevoland', 'Zeeland', 'North Holland', 'South Holland', 'Utrecht', 'Gelderland', 'North Brabant', 'Limburg'],
    'Homicide Rate': [0.48, 0.62, 0.53, 0.53, 0.75, 0.71, 0.94, 0.78, 0.62, 0.45, 0.78, 0.82]
})

# Data for cities
    cities_data = pd.DataFrame({
    'City': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht'],
    'Latitude': [52.3676, 51.9225, 52.0705, 52.0907],
    'Longitude': [4.9041, 4.4792, 4.3007, 5.1214],
    'Homicide Rate': [1.99, 1.8, 1.2, 0.94]
})

    geojson_path = 'WebApp/netherlands.geojson'
    gdf = gpd.read_file(geojson_path)

    regions_data['Region'] = regions_data['Region'].astype(str)
    gdf['prov_name'] = gdf['prov_name'].astype(str)

    gdf = gdf.merge(regions_data, left_on='prov_name', right_on='Region')

    m = folium.Map(location=[52.1326, 5.2913], zoom_start=7)

    Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=['Region', 'Homicide Rate'],
        key_on='features.properties.prov_name',
        fill_color='YlOrRd',
        fill_opacity=1.0,
        line_opacity=0.2,
        legend_name='Homicide Rate per Region'
    ).add_to(m)

    # Add CircleMarkers for the cities with size based on homicide rate
    for _, row in cities_data.iterrows():
        CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=row['Homicide Rate'] * 2,  # Adjust size multiplier as needed
            popup=f"{row['City']}: {row['Homicide Rate']}",
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)

    # Display the map in Streamlit
    folium_static(m)
    st.write("Cite as: Dutch Homicide Monitor (2024)")

    st.write("""
    ***
    #### Homicide Types
            
    Most homicides in the Netherlands (2011-2020) occurred in the context of a conflict between (ex) intimate partners or in the context of criminal activities, such as assassinations or fatal rip deals.\n
    Relatively rare are homicides committed during robberies, the killing of children, homicides committed by individuals with a mental health crisis or homicides in the context of nightlife violence.

    """)

    # Data for the pie chart
    data = {
        'Category': [
            'Partner killing', 'Criminal Milieu', 'Missing', 'Other non-criminal',
            'Other', 'Other familial killing', 'Robbery killing',
            'Child killing (family and non-family)', 'Nightlife violence',
            'Killing by mentally disturbed person (non-family)'
        ],
        'Percentage': [
            22.1, 19.5, 12.5, 16.5, 5.3, 6.9, 5.2, 5.3, 2.3, 4.3
        ]
    }

    # Custom color sequence
    color_discrete_map = {
        'Missing': 'red',
        'Partner killing': '#636EFA',  # default Plotly color
        'Criminal Milieu': '#EF553B',  # default Plotly color
        'Other non-criminal': '#00CC96',  # default Plotly color
        'Other': '#AB63FA',  # default Plotly color
        'Other familial killing': '#19D3F3',  # default Plotly color
        'Robbery killing': '#FFA15A',  # default Plotly color
        'Child killing (family and non-family)': '#FF6692',  # default Plotly color
        'Nightlife violence': '#B6E880',  # default Plotly color
        'Killing by mentally disturbed person (non-family)': '#FF97FF'  # default Plotly color
    }
    # Create a pie chart using Plotly
    fig = px.pie(data, names='Category', values='Percentage', color='Category', color_discrete_map=color_discrete_map)

    col1, col2 = st.columns([2, 1])

    # Place the pie chart in the left column
    with col1:
        st.plotly_chart(fig)

    st.write("Cite as: Dutch Homicide Monitor (2024)")
    st.write("""
    ***
    #### Gender of homicide victims and perpetrators
            
    About two-thirds of homicides victims in the Netherlands are male, as are more than 80 percent of the offenders.
            
    """)

    data1 = {
        'Category': ['Male', 'Female', 'Missing'],
        'Percentage': [65.7, 33.4, 0.1]
    }

    data2 ={
        'Category': ['Male','Female','Missing'],
        'Percentage': [84.1,6.7,9.2 ]
    }

    color_discrete_map = {
        'Missing': 'red',
        'Male': '#636EFA',  # default Plotly color
        'Female': '#EF553B'  # default Plotly color
    }

    fig_vic = px.pie(data1, names='Category', values='Percentage', color='Category', title='Gender of homicide victims', color_discrete_map=color_discrete_map)
    fig_perp = px.pie(data2, names='Category', values='Percentage', color='Category', title='Gender of main homicide perpetrator', color_discrete_map=color_discrete_map)

    col1, col2 =st.columns([2,1])

    with col1:
        st.plotly_chart(fig_vic)

    with col2:
        st.plotly_chart(fig_perp)

    st.write("Cite as: Dutch Homicide Monitor (2024)")


with tab2:
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
    
