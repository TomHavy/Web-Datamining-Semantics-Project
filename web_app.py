import streamlit as st
from rdflib import Graph
from queries import *
from functions import maj_datas

st.set_page_config(page_title="Bike stations", page_icon= "🚲", layout="wide")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.title("**Bike stations in Rennes and Lyon** 🚴")

weather_lyon,weather_rennes=maj_datas()

g=Graph()
g.parse("new_project_ontology_rdf_xml_full.owl")
data=g.serialize(format="xml")

prefix="""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>
PREFIX ns:<http://www.semanticweb.org/havyt/ontologies/2022/2/untitled-ontology-14#>
"""

st.write(f"Lyon: \n** Temps :** {weather_lyon['Temps']}, ** Température :** {weather_lyon['Température']}°C, ** Température ressentie :** {weather_lyon['Température ressentie']}°C")
st.write(f"Rennes: \n** Temps :** {weather_rennes['Temps']}, ** Température :** {weather_rennes['Température']}°C, ** Température ressentie :** {weather_rennes['Température ressentie']}°C")

first_query(prefix,g)

second_query(prefix,g)

third_query(prefix,g)       

fourth_query(prefix,g)

interactive_map(prefix,g)

st.header("🚧 Work in progress 🚧")

sixth_query(prefix,g)

seventh_query(prefix,g)
