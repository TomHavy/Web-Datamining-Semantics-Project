from turtle import width
from unittest import result
import streamlit as st
import pandas as pd
from rdflib import Graph
from queries import *

st.set_page_config(page_title="Bike stations", page_icon= "🚲", layout="wide")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

RANDOM_SEED = 1

st.title("**Bike stations in Rennes and Lyon** 🚴")

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

first_query(prefix,g)

second_query(prefix,g)

third_query(prefix,g)       

fourth_query(prefix,g)

interactive_map(prefix,g)

st.header("🚧 Work in progress 🚧")

sixth_query(prefix,g)

seventh_query(prefix,g)
