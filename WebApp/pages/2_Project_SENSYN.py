import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.bottom_container import bottom
from streamlit_extras.app_logo import add_logo

###### PROJECT SENSYN STREAMLIT #####

def add_logo_sidebar(image_path, image_width):
    st.sidebar.image(image_path, width=image_width)

st.set_page_config(page_title="Project SENSYN",
                   page_icon=":bar_chart:",
                   layout="wide")

add_logo_sidebar('WebApp/Visuals/logo.png', 150)  # Adjust path and width as needed
add_logo_sidebar('WebApp/Visuals/lumc_logo.png', 150)  # Adjust path and width as needed

st.write("""
# Project SENSYN
         
""")

tab1, tab2, tab3, tab4 = st.tabs(["About Project SENSYN","Outputs","The Project Team","Contact"])

with tab1:
    st.write("""
             #### What we do \n 
             
             With project SENSYN, a team of social scientists and data scientists aims to encourage and assist the use of synthetic datasets (a) amongst researchers handling personal and highly sensitive data and (b) for the accessibility of data for the general public. 
             One the one hand, the use of synthetic data is encouraged through a proof-of-concept study synthetic dataset using highly sensitive homicide data from the Netherlands. 
             On the other hand, the project will result in accessible protocols and guidelines for other researchers, as well as online workshops and videos on the use of synthetic data. 
             All outputs of the project, including the synthetic dataset, are available and accessible on this webpage.
             
             ***
             """)
    st.write(""" 
             #### Why we do it \n 
             
             Making data findable, accessible, interoperable and reusable (FAIR) is a pillar of Open Science. Yet, privacy regulations hinder the implementation of FAIR principles in research fields working with sensitive data, such as crime, finances, or public health. Sharing individual-level data is not just crucial for collaborations between research institutions, for enabling replication studies and increase transparency and accountability of research processes, but also to inform policymaking and to engage other stakeholders of the general public in research.
             To overcome the problem of sharing sensitive data, in recent years, the use of differentially private synthetic datasets has emerged as a successful tool to make detailed highly sensitive data more accessible, in particular amongst data scientists. 
             A synthetic dataset is an artificial dataset that has the same statistical properties as the original dataset, but as each datapoint is simulated, they cannot be traced back to individuals protected under privacy regulations. In the context of Open Science, synthetic datasets have been praised for opening new possibilities for the replication of studies and for researchers to share their data under FAIR principles. However, the use of this novel technique is not widespread yet, particularly in the social sciences. 
             In addition, very little attention has been directed at the possibilities of using synthetic datasets to open up research processes and findings to non-academic audiences.
             
             ***""")
    st.write("""
             #### Financing \n 
             
             This project and all of its outputs have been funded by the NWO Open Science Fund (OSF23.1.006).
             ***""")
    
with tab2:
    st.write("""
             #### Guidebook \n 
             The guidebook can be found, read and downloaded on the [Zenodo repository](https://zenodo.org/records/13374278)
             ***
             """)


with tab3:
    st.write("""
             #### Jim Achterberg \n 
             Jim Achterberg is PhD candidate at the Leiden University Medical Center. His PhD research is on machine learning, specifically synthetic data in the field of healthcare.
             ***
             """)
    st.write("""
             #### [Marcel Haas](https://www.lumc.nl/afdelingen/public-health-en-eerstelijnsgeneeskunde/mr-haas/) \n 
             Marcel Haas is assistent professor of data science in population health at the Leiden University Medical Centre. 
             ***
             """)
    st.write("""
             #### [Katharina Krüsselmann](https://www.universiteitleiden.nl/en/staffmembers/katharina-krusselmann#tab-1) \n 
             Katharina Krüsselmann is researcher at the Institute of Security and Global Affairs at Leiden University, where she researches firearm violence and open science.
             ***
             """)
    st.write("""
             #### [Marieke Liem](https://www.universiteitleiden.nl/en/staffmembers/marieke-liem#tab-1) \n 
             Marieke Liem is professor of security and interventions at the Institute of Security and Global Affairs at Leiden University and experienced homicide researcher. 
             ***
             """)
    st.write("""
             #### [Marco Spruit](https://www.universiteitleiden.nl/en/staffmembers/marco-spruit#tab-1) 
             Marco Spruit is professor of advanced data science in population health and is connected both to the Leiden University Medical Center, as well as the Leiden Institute of Advanced Computer Science.
             ***
             """)
with tab4:
    st.write("""
    #### Contact us by mail
    
    For questions related to homicide, please contact Marieke Liem """)
    st.markdown("📧 [m.c.a.liem@fgga.leidenuniv.nl](mailto:m.c.a.liem@fgga.leidenuniv.nl)")
             
    st.write("For questions related to synthetic data, please contact Marcel Haas")
    st.markdown("📧 [m.r.haas@lumc.nl](mailto:m.r.haas@lumc.nl)")
