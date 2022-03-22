from unittest import result
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

st.subheader("FIRST QUERY:  Display database dynamically")

select = st.multiselect("Which variable are you interested in?", var,"nom")

select_=" \nSELECT "
where_="\nWHERE {"

for s in select:
    select_+=f"?{s} "
    where_+=f"\n ?p ns:{s} ?{s} ."

query=prefix+select_ +where_+" }"

result=g.query(query)
result_df=pd.DataFrame(result, columns=result.vars)


print(query)
st.write(result_df)

# endregion

# region SECOND QUERY: Search VLille spots with specific value

st.subheader("SECOND QUERY: Search VLille spots with specific value")
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

# endregion

# region THIRD QUERY: VLille spots with highest number of bike available or available places

st.subheader("\nTHIRD QUERY: VLille spots with highest number of bike available or available places")

select=st.radio("Pick one", ["nbvelosdispo","nbplacesdispo"])

select_=f" \n SELECT ?nom ?{select}"
where_="\n WHERE { ?p ns:nom ?nom ."+f" ?p ns:{select} ?{select} . }}"
orderby_=f"ORDER BY DESC(?{select})"

query=prefix+select_+where_+orderby_
print("query:",query)

response=g.query(query)
result_df=pd.DataFrame(response, columns=response.vars)
# print("bindings:",response.bindings)
st.write(result_df)

# endregion

# region FOURTH QUERY: VLille spots with a number of bike available above a defined value

st.subheader("\n FOURTH QUERY: VLille spots with a number of bike available above a defined value")

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

# region FIFTH QUERY: Is there a spot in this commune?

st.subheader("\n FIFTH QUERY: Is there a spot in this commune?")

select = select=st.radio("Pick one", ["LILLE"])

select_=" \nSELECT "
where_="\nWHERE {"
ask_=f"ASK {{ ?p ns:commune  \"{select}\"}}"
query=prefix+ask_

response=g.query(query)
print(query)
st.write(response.askAnswer)
# endregion

# region SIXTH QUERY: Describe a VLille spot
  #NOT IMPLEMENTED IN LIBRARY 
st.subheader("SIXTH QUERY: Describe a VLille spot")

# select=st.slider("Pick a number ", max_value=200,min_value=0)
# describe_=f"DESCRIBE ?p WHERE {{ ?p ns:libelle {select}}}"
# query=prefix+describe_
# response=g.query(query)
# print(query)
# st.write(response)
st.write("DESCRIBE, not implemented in rdflib library ")
# endregion

# region SEVENTH QUERY: Find VLille spots in trouble (bike supply issue, or not usable (hors-service) ...)

st.subheader("\n SEVENTH QUERY: Find VLille spots in trouble (bike supply issue, or not usable (hors-service) ...)")

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
print("bindings:",response.bindings)
# print("query: ",query)
st.write(result_df)
# endregion