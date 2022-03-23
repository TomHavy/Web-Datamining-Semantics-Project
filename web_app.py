from turtle import width
from unittest import result
import streamlit as st
import pandas as pd
from rdflib import Graph
import folium
import openrouteservice as ors
from streamlit_folium import folium_static

st.set_page_config(page_title="VLille spots", page_icon= "🚲", layout="wide")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

RANDOM_SEED = 1

st.title("**VLille spots** 🚴")

g=Graph()
g.parse("project_ontology_rdf_xml_full.owl")
data=g.serialize(format="xml")

var=["nom","adresse","localisation","commune","etat", "etatconnexion","libelle", "nbvelosdispo","nbplacesdispo"]

prefix="""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>
PREFIX ns: <http://www.semanticweb.org/havyt/ontologies/2022/2/project_ontology#>
"""

# region FIRST QUERY:  Display database dynamically

st.subheader("Display database dynamically")

select = st.multiselect("Which variables are you interested in?", var,"nom")

select_=" \nSELECT "
where_="\nWHERE {"

for s in select:
    select_+=f"?{s} "
    where_+=f"\n ?p ns:{s} ?{s} ."

query=prefix+select_ +where_+" }"

result=g.query(query)
result_df=pd.DataFrame(result, columns=result.vars)

# print(query)
st.write(result_df)

# endregion

# region THIRD QUERY: VLille spots with highest number of bike available or available places

st.subheader("\nVLille spots with highest number of bike available or available places")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
select=st.radio("Pick one: ",options=["nbvelosdispo","nbplacesdispo"])

select_=f" \n SELECT ?nom ?libelle ?{select} "
where_="\n WHERE { ?p ns:nom ?nom . ?p ns:libelle ?libelle ."+f" ?p ns:{select} ?{select} . }}"
orderby_=f"ORDER BY DESC(?{select})"

query=prefix+select_+where_+orderby_
print("query:",query)

response=g.query(query)
result_df=pd.DataFrame(response, columns=response.vars)
# print("bindings:",response.bindings)
st.write(result_df)

# endregion

# region FOURTH QUERY: VLille spots with a number of bike available above a defined value

st.subheader("\nVLille spots with a number of bike available above a defined value")

select=st.slider("Pick a number ", max_value=50,min_value=0)

select_=f" \n SELECT ?nom ?localisation ?nbvelosdispo"
where_="\n WHERE { ?p ns:nom ?nom . ?p ns:localisation ?localisation . ?p ns:nbvelosdispo ?nbvelosdispo ."
filter_=f"\n FILTER (?nbvelosdispo > {select})}}"    

query=prefix+select_+where_+filter_
print("query:",query)

response=g.query(query)
result_df=pd.DataFrame(response, columns=response.vars)
# print("bindings:",response.bindings)
st.write(result_df)

# endregion

# region Traverlers' trip and directions on interactive map

st.subheader("Traverlers' trip and directions on interactive map")

private_key="5b3ce3597851110001cf6248af2c67c2173d43bf9806b299e45e1b09"
client=ors.Client(key=private_key)

query=prefix+"""
SELECT ?nom ?libelle ?adresse ?commune ?localisation
WHERE { 
       ?p ns:nom ?nom . 
       ?p ns:libelle ?libelle .
       ?p ns:adresse ?adresse . 
       ?p ns:commune ?commune .
       ?p ns:localisation ?localisation .}"""
response=g.query(query)
result_df=pd.DataFrame(response, columns=response.vars)
libelle=result_df[result_df.columns[1]].astype(int)
# localisation=result_df[result_df.columns[4]]

select_departure=st.number_input("Libelle of spot departure: ", min_value=libelle.min(), max_value=libelle.max())
select_arrival=st.number_input("Libelle of spot arrival: ", min_value=libelle.min(), max_value=libelle.max())

coord_departure=result_df[result_df.columns[4]][libelle==select_departure]
coord_departure=list(coord_departure.values[0].split(","))

coord_arrival=result_df[result_df.columns[4]][libelle==select_arrival]
coord_arrival=list(coord_arrival.values[0].split(","))

coordinates=[[coord_departure[1],coord_departure[0]],[coord_arrival[1],coord_arrival[0]]]

route=client.directions(coordinates=coordinates, profile='cycling-regular',format='geojson', optimize_waypoints=True)

map_directions=folium.Map(location=coord_departure,zoom_start=15)

folium.GeoJson(route,name='route').add_to(map_directions)

folium.LayerControl().add_to(map_directions)

folium_static(map_directions, width=1350)
# endregion

st.header("🚧 Work in progress 🚧")

# region SECOND QUERY: Search VLille spots with specific value

st.subheader("\nSearch VLille spots with specific value")
select = st.text_input('property', 'LILLE')

select_=" \nSELECT "
where_="\nWHERE {"

query=prefix+"""
SELECT ?p ?adresse
WHERE { ?p ns:adresse ?adresse . """+f"?p ns:commune \"{select}\" . }}"


response=g.query(query)
result_df=pd.DataFrame(response, columns=response.vars)
# print("bindings:",response.bindings)
st.write(result_df)
# print(query)

# endregion

# region FIFTH QUERY: Is there a spot in this commune?

st.subheader("\nIs there a spot in this commune?")

select = select=st.radio("Pick one", ["LILLE"])

ask_=f"\nASK {{ ?p ns:commune  \"{select}\"}}"
query1=prefix+ask_

response=g.query(query1)
# print("query1: ",query1)
st.write(response.askAnswer)

# endregion

# region SIXTH QUERY: Describe a VLille spot

  #NOT IMPLEMENTED IN LIBRARY 
st.subheader("\nDescribe a VLille spot")

# select=st.slider("Pick a number ", max_value=200,min_value=0)
# describe_=f"DESCRIBE ?p WHERE {{ ?p ns:libelle {select}}}"
# query=prefix+describe_
# response=g.query(query)
# print(query)
# st.write(response)
st.write("DESCRIBE, not implemented in rdflib library ")

# endregion

# region SEVENTH QUERY: Find VLille spots in trouble (bike supply issue, or not usable (hors-service) ...)

st.subheader("\nFind VLille spots in trouble (bike supply issue, or not usable (hors-service) ...)")

query=prefix+"""
SELECT ?p ?etat ?etatconnexion ?nbvelosdispo
WHERE  {   
         OPTIONAL { ?p ns:nbvelosdispo 0 .
    				?p ns:nbvelosdispo ?nbvelosdispo .
  				    ?p ns:etat ?etat . 
       	 			?p ns:etatconnexion ?etatconnexion .} .
  
         OPTIONAL { ?p ns:nbvelosdispo ?nbvelosdispo .
  				    ?p ns:etat "HORS SERVICE" . 
    				?p ns:etat ?etat . 
       	 			?p ns:etatconnexion ?etatconnexion .} .
  
         OPTIONAL { ?p ns:nbvelosdispo ?nbvelosdispo .
  				    ?p ns:etat ?etat . 
       	 			?p ns:etatconnexion "DISCONNECTED" .
  					?p ns:etatconnexion ?etatconnexion .} .
       }
"""

response=g.query(query)
result_df=pd.DataFrame(response, columns=response.vars)
# print("bindings:",response.bindings)
# print("query: ",query)
st.write(result_df)
# endregion