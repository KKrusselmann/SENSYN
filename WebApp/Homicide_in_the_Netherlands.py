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



###### STREAMLIT HOMICIDE IN THE NETHERLANDS #####

def add_logo_sidebar(image_path, image_width):
    st.sidebar.image(image_path, width=image_width)

st.set_page_config(page_title="Synthetic data on homicide in the Netherlands",
                   page_icon=":knife:",
                   layout="wide")

add_logo_sidebar('WebApp/Visuals/logo.png', 150)  # Adjust path and width as needed
add_logo_sidebar('WebApp/Visuals/lumc_logo.png', 150)  # Adjust path and width as needed


st.write("""
# Synthetic data on homicide in the Netherlands
***
         
This page is meant as an informational hub on synthetic data on homicide in the Netherlands.\n
The information on this page is based on the Dutch Homicide Monitor, which is administered by criminologists at Leiden University.
Due to personal information in the Dutch Homicide Monitor, it is not possible to display details about each homicide case, nor to display all information gathered in the Dutch Homicide Monitor.
If you want to explore detailed homicide data yourself, please have a look at the page **Explore Homicide Data**, which uses a synthetic dataset based on the Dutch Homicide Monitor.
Curious what synthetic data is? Have a look at the page **Synthetic Data**. If you want to know more about the project that enabled us to make synthetic dataset and this webpage, take a look at **Project SENSYN**.
         
Questions about homicides in the Netherlands or the project that are not answered here? Feel free to contact us!
       
***
""")

tab1, tab2 = st.tabs(["Dutch Homicide Monitor","Research"])


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

with tab2:
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
    
