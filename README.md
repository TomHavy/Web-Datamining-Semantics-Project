# 🚲 Web Datamining & Semantics Project

This is a project for the Web Datamining & Semantics course, created by Tom Havyarimana and Oussama El Atrache. The goal of this project is to create an ontology for bike-sharing data in the cities of Lyon and Rennes, and to use this ontology to answer queries about the data.

## 📊 Dataset

We used two datasets for this project, one for Lyon and one for Rennes. These datasets contain information about bike-sharing stations, including their location, the number of bikes and bike slots available, and the date of the last update. We also used an API for weather data to provide additional information in real-time.

## 📚 Ontology

Our ontology includes classes for stations, bikes, and weather, as well as object and data properties to describe the relationships between these classes. We used RDF to represent our ontology, and created individuals to populate the ontology using a Python script.

Specifically, we created 5 classes, including 2 subclasses of the POI (Point Of Interest) class called spotRennes and spotLyon, which contain information about the bike-sharing stations. We also created a class called travelers, which contains information about the users of the bike-sharing system, and a class called trips, which contains information about the trips taken by these users between different bike-sharing stations. We used object properties to link the POI class to other classes in the ontology, and data properties to describe the attributes of each class.

## 🔍 Queries

We used SPARQL to query our ontology and answer questions about the bike-sharing data. Some example queries include:

- What is the current weather at a specific bike-sharing station?
- How many bikes are available at a specific station?
- Which station has the most available bike slots?

We also used the SPARQL query language to create a visualization of the bike-sharing stations on a map, using the GeoSPARQL extension.


## 💻 Solution

Our final solution includes a Python script to populate the ontology, a Jupyter notebook to demonstrate our queries and visualization, and a report detailing our methodology and results.

In order to run the streamlit web page, make sure you have installed the necessary libraries, such as:
- streamlit
- rdflib
- openrouteservice
- folium
- streamlit_folium

Now, to run the streamlit web page, enter "streamlit run .\app\app.py" in a new terminal. A new page on your browser should open.

### 🎬 Demo
![gif_demo_wdms](https://github.com/TomHavy/Web-Datamining-Semantics-Project/assets/67765175/de8eb595-e2f5-4055-ba52-de0f33ec0ee9)


You can also checkout the longer demo video (1min30) by downloading this file at: ".\documents\demo_video.mp4"

## 📂 Project Files

- app\core\functions.py: Contains the script to populate our ontology in RDF/XML format.

- app\app.py: Contains the main code of the web page.

- app\core\queries.py: Contains all the queries present on the web page.

- documents\Rapport_Projet_Web_Datamining_semantics.pdf: Contains the report for this project in french. In it we describe our process for creating the ontology, including how we chose the classes and properties, and how we populated the ontology with data. We also discuss our approach to answering queries using SPARQL, and provide examples of the queries we used to analyze the data.

Authors: Tom HAVYARIMANA - Oussama EL ATRACHE
