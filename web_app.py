import streamlit as st
import pandas as pd
from rdflib import Graph

st.set_page_config(page_title="Real Time Bike spots availability", page_icon= "🚲", layout="wide")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

RANDOM_SEED = 1

st.title("**Real Time Bike spots availability VLille** 🚴")

# st.write("This is an app where you can train a model for predicting the number of bike rented in a day.")
# st.write("""
# Currently Rental bikes are introduced in many urban cities for the enhancement of mobility comfort.
#  It is important to make the rental bike available and accessible to the public at the right time as it lessens the waiting time. 
#  Eventually, providing the city with a stable supply of rental bikes becomes a major concern. 
#  The crucial part is the prediction of bike count required at each hour for the stable supply of rental bikes.

#  ** Data source: ** [Seoul Bike Sharing Demand Data Set](https://archive.ics.uci.edu/ml/datasets/Seoul+Bike+Sharing+Demand)
#  """)

# st.header("***Dataset Loading*** 💻")

# with st.expander("Data informations", expanded=True):
#      st.write("""
#      The dataset must have these columns names in this order.

#         - **Date** : Format DD/MM/YYYY
#         - **Rented Bike Count** : The number of bikes who will be rented
#         - **Hour** : From 0 to 23
#         - **Temperature(°C)** : float value
#         - **Humidity(%)** : float value
#         - **Wind speed (m/s)** : float value
#         - **Visibility (10m)** : float value
#         - **Dew point temperature(°C)** : float value
#         - **Solar Radiation (MJ/m2)** : float value
#         - **Rainfall(mm)** : float value
#         - **Snowfall (cm)** : float value
#         - **Seasons** : Winter, Spring, Summer, Automn
#         - **Holiday** : Holiday or No Holiday
#         - **Functioning Day** : Yes or No
#      """)

uploaded_file = st.file_uploader("Import a owl file.", "owl")

drive_file = st.checkbox("Import the file directly from google drive (option not added yet)")

g=Graph()
g.parse("project_ontology_rdf_xml_full.owl")

data=g.serialize(format="xml")

# st.write(data)

# if drive_file:
#     pass
# else:
#     if uploaded_file:
#         dataset = pd.read_csv("project_ontology_rdf_xml_full.owl")
#         st.write(dataset.sample(9, random_state=RANDOM_SEED))

q="""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>
PREFIX ns: <http://www.semanticweb.org/havyt/ontologies/2022/2/project_ontology#>

SELECT ?nom ?adresse ?commune ?localisation
WHERE { 
       ?p ns:nom ?nom . 
       ?p ns:adresse ?adresse . 
       ?p ns:commune ?commune .
       ?p ns:localisation ?localisation .}

"""
response=pd.DataFrame(columns=["nom","commune","localisation"])
for r in g.query(q):

    # st.write(r["nom"],"|",r["commune"],"|",r["localisation"])
    response=response.append({'nom': r["nom"], 'commune':r["commune"],'localisation':r["localisation"]},ignore_index=True)

st.write("First query: List the instances of the geolocated POI ")
st.write(response)
