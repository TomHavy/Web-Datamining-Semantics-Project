import pandas as pd
import streamlit as st
import folium
import openrouteservice as ors
from streamlit_folium import folium_static

def first_query(prefix,g): #FIRST QUERY:  Display database dynamically

    var=["nom","id_station","nb_emplacements","nb_emplacements_dispo","nb_velos_dispo","etat","latitude","longitude","derniere_maj"]

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

    print(query)
    st.write(result_df)

def second_query(prefix,g): #SECOND QUERY: Search for bike stations with specific value

    st.subheader("\nSearch for bike stations with specific value")

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
    select=st.radio("Pick one: ",options=["OPEN","CLOSED","En panne"])

    select_=" \nSELECT "
    where_="\nWHERE {"

    query=prefix+"""
    SELECT ?nom ?id_station ?etat ?latitude ?longitude ?nb_velos_dispo ?nb_emplacements_dispo
    WHERE { 
        ?p ns:nom ?nom . 
        ?p ns:id_station ?id_station .
        ?p ns:etat ?etat .
        ?p ns:nb_velos_dispo ?nb_velos_dispo . 
        ?p ns:nb_emplacements_dispo ?nb_emplacements_dispo . 
        ?p ns:latitude ?latitude . 
        ?p ns:longitude ?longitude ."""+f"?p ns:etat \"{select}\" . }}"

    #       ?p ns:longitude ?longitude .}
    response=g.query(query)
    result_df=pd.DataFrame(response, columns=response.vars)
    # print("bindings:",response.bindings)
    st.write(result_df)
    print(query)

def third_query(prefix,g): #THIRD QUERY: Is there a bike station with this name?

    st.subheader("\nIs there a bike station with this name?")

    select = st.text_input('Bike spot name', "Place Aristide Briand")

    ask_=f"\nASK {{ ?p ns:nom  \"{select}\"}}"
    query1=prefix+ask_

    response=g.query(query1)
    print(query1)
    st.write("Answer: ",response.askAnswer)

def fourth_query(prefix,g): #FOURTH QUERY: Bike stations with at least a particular number of bikes available

    st.subheader("\n Bike stations with at least a particular number of bikes available")

    select=st.slider("Pick a number ", max_value=50,min_value=0)

    select_=f"\nSELECT ?nom ?id_station ?latitude ?longitude ?nb_velos_dispo"
    where_=""" 
        WHERE { 
                ?p ns:nom ?nom . 
                ?p ns:id_station ?id_station .
                ?p ns:nb_velos_dispo ?nb_velos_dispo . 
                ?p ns:latitude ?latitude . 
                ?p ns:longitude ?longitude . """
    filter_=f"\n FILTER (?nb_velos_dispo > {select})}}"    

    query=prefix+select_+where_+filter_
    print("query:",query)

    response=g.query(query)
    result_df=pd.DataFrame(response, columns=response.vars)
    # print("bindings:",response.bindings)
    st.write(result_df)

def fifth_query(prefix,g): #FIFTH QUERY: Find bike stations in trouble (bike supply issue, or not usable (hors-service) ...)

    st.subheader("\nFind bike spots in trouble (bike supply issue, or not usable (hors-service) ...)")

    query=prefix+"""
    SELECT ?nom ?etat ?nb_velos_dispo
    WHERE  {   
            OPTIONAL { 
                    ?p ns:nom ?nom .
                    ?p ns:nb_velos_dispo 0 .
                        ?p ns:nb_velos_dispo ?nb_velos_dispo .
                        ?p ns:etat ?etat . } .
    
            OPTIONAL {       
                    ?p ns:nom ?nom .
                    ?p ns:nb_velos_dispo ?nb_velos_dispo .
                    ?p ns:etat "CLOSED" . 
                        ?p ns:etat ?etat . } .
    
            OPTIONAL {  
                    ?p ns:nom ?nom .
                    ?p ns:nb_velos_dispo ?nb_velos_dispo .
                        ?p ns:etat ?etat . 
                        ?p ns:etat "En panne" .} .
        }
    """

    response=g.query(query)
    result_df=pd.DataFrame(response, columns=response.vars)
    # print("bindings:",response.bindings)
    print("query: ",query)
    st.write(result_df)

def interactive_map(prefix,g): #Traverlers' trip and directions on interactive map

    st.subheader("Traverlers' trip and directions on interactive map")

    private_key="5b3ce3597851110001cf6248af2c67c2173d43bf9806b299e45e1b09"
    client=ors.Client(key=private_key)

    query=prefix+"""
    SELECT ?nom ?id_station ?latitude ?longitude ?nb_velos_dispo ?nb_emplacements_dispo
    WHERE { 
        ?p ns:nom ?nom . 
        ?p ns:id_station ?id_station .
        ?p ns:nb_velos_dispo ?nb_velos_dispo . 
        ?p ns:nb_emplacements_dispo ?nb_emplacements_dispo . 
        ?p ns:latitude ?latitude . 
        ?p ns:longitude ?longitude .}"""

    response=g.query(query)
    result_df=pd.DataFrame(response, columns=response.vars)
    id_station=result_df[result_df.columns[1]].astype(int)
    # localisation=result_df[result_df.columns[4]]

    select_departure=st.number_input("ID of spot departure: ", min_value=id_station.min(), max_value=id_station.max())
    select_arrival=st.number_input("ID of spot arrival: ", min_value=id_station.min(), max_value=id_station.max())

    coord_departure=[]
    coord_departure.append(result_df[result_df.columns[2]][id_station==select_departure].values[0])
    coord_departure.append(result_df[result_df.columns[3]][id_station==select_departure].values[0])

    coord_arrival=[]
    coord_arrival.append(result_df[result_df.columns[2]][id_station==select_arrival].values[0])
    coord_arrival.append(result_df[result_df.columns[3]][id_station==select_arrival].values[0])

    print("coord_departure: ",coord_departure)
    # print("coord_arrival: ",coord_arrival)

    coordinates=[[coord_departure[1],coord_departure[0]],[coord_arrival[1],coord_arrival[0]]]

    route=client.directions(coordinates=coordinates, profile='cycling-regular',format='geojson', optimize_waypoints=True)

    map_directions=folium.Map(location=coord_departure,zoom_start=15)

    folium.GeoJson(route,name='route').add_to(map_directions)

    folium.LayerControl().add_to(map_directions)

    folium_static(map_directions, width=1350)

def sixth_query(prefix,g):# SIXTH QUERY: VLille spots with highest number of bike available or available places

    st.subheader("\nBike stations with highest number of bike available or available places")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
    select=st.radio("Pick one: ",options=["nb_velos_dispo","nb_emplacements_dispo"])

    select_=f"\nSELECT ?nom ?id_station ?{select} "
    where_="\nWHERE { ?p ns:nom ?nom . ?p ns:id_station ?id_station ."+f" ?p ns:{select} ?{select} . }}"
    orderby_=f"\nORDER BY DESC(?{select})"

    query=prefix+select_+where_+orderby_

    # response=g.query(query)
    # result_df=pd.DataFrame(response, columns=response.vars)
    # # print("bindings:",response.bindings)
    # st.write(result_df)

    print("query:",query)

def seventh_query(prefix,g): #SEVENTH QUERY: Describe a VLille spot

    #NOT IMPLEMENTED IN LIBRARY 
    st.subheader("\nDescribe a VLille spot")

    # select=st.slider("Pick a number ", max_value=200,min_value=0)
    # describe_=f"DESCRIBE ?p WHERE {{ ?p ns:libelle {select}}}"
    # query=prefix+describe_
    # response=g.query(query)
    # print(query)
    # st.write(response)
    st.write("DESCRIBE, not implemented in rdflib library ")

