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
# Synthetic Data
         
This page contains all relevant information on synthetic data. What is it, how it is made, what it can be used for and the advantages and risks
associated with synthetic data.
         
For short explanations, have a look at the videos. More detailed explanations are found in the text, as well as in our guidebook on synthetic data.

***
         """)

col1, col2 = st.columns(2)

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


st.write("""
***

#### What is synthetic data?
         
Synthetic data refers to data that is artificially generated rather than obtained by direct measurement or collection from real-world events. This data is produced
using a variety of techiques, including statistical modeling, simulations and algorithms that replicate the characterisics and structures found in real data sets. 
The goal of synthetic data is to create a dataset that contains artificial, but realistic data which looks as close as possible to real data.
         
Synthetic data can take on many forms, just like data collected in the real world: structured data, such as tabular data or other statistical data, or unstructured data,
such as text or even visual data. """)

st.image("WebApp/Visuals/syntheticdata_comp.png", width=700)
         
st.write("""
***
#### What can synthetic data be used for?
         

Synthetic data can be used for various purposes. 

For *government agencies*, synthetic data allows for secure data sharing between departments and with external partners, facilitating collaboration on national security, social welfare or other topics.
In addition, governments could simulate various scenarios with synthetic data, such as the impact of certain policy changes or emergency responses, without exposing sensitive information about citizens.
         
In the *industry*, synthetic data can be a key driver of new innovations. It can be used to test products or optimise processes when real data is proprietary, costly or limited, and without risking data breaches.
         
For *researchers*, synthetic data opens new avenues for conducting research. It allows the study of rare phenomena, the validation of models or simulation of experiments. In addition, when using synthetic data,
researchers can share data with peers globally, enhancing open science practices and accelerating scientific research.


""")

st.write("""
***
#### How is synthetic data made?

There are several methods to generate synthetic data, ranging from statistical models, to machine learning methods or large language models (LLM), such as GPT-4 for textual data.
         
In general, one can distinguish between two types of data generation: one in which no real-world data is available and synthetic data is created completely from scratch, and one in which 
synthetic data is generated based on real-world data.
         
Depending on the approach, one has to either feed the chosen model a list of requirements for the synthetic data (when creating synthetic data froms scratch), or a model is used to learn about
the characteristics and structure of real-world data. Based on the list of requirements or the knowledge gained from real-world data, the model generates a synthetic dataset that should adhere to
the list of requirements of closely resemble real-world data. It is up to the person generating the data to evaluate the generated dataset, based on whether it fulfils all the necessary requirements,
whether it resembles the original data close enough and whether the synthetic data adheres to privacy regulations.

""")
st.image('WebApp/Visuals/syntheticdata__synthesis.png', width=700)

st.write("""
***
#### Our guidebook on the use of synthetic data for scientific research

Our guidebook provides a more comprehensive description of what synthetic data is, how it is generated, its advantages and risks, as well as the process of how we generated realistic synthetic homicide data.
""")

# URL of the PDF file
pdf_url = "https://www.universiteitleiden.nl/binaries/content/assets/governance-and-global-affairs/isga/ehm_coding-manual_nucleus-variables_final.pdf"

# Embed the PDF using an iframe
st.components.v1.html(f'<iframe src="{pdf_url}" width="700" height="1000" type="application/pdf"></iframe>', height=1000)

