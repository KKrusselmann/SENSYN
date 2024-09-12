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

On this webapplication, we provide information on what synthetic data is, how it is generated and for which purposes it can be used.
To showcase the functionalities of synthetic data, we generated a synthetic version of the Dutch Homicide Monitor, a database with detailed information on cases, victims and perpetrators of homicides in the Netherlands.

This webapplication, the synthetic dataset and a more [detailed guidebook on synthetic data](https://zenodo.org/records/13752141) are the results of project SENSYN, a project funded by the NWO Open Science Fund.                 
***
""")