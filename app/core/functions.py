import requests

def requestAPI(url):
  req = requests.get(url)
  return req.json()

def recup_datas_lyon(req_lyon):
  features = req_lyon["features"]

  stations = []

  for station in features:
    new_station = {}

    properties = station["properties"]

    new_station["nom"] = properties["name"]
    new_station["id_station"] = properties["number"]
    new_station["nb_emplacements"] = properties["bike_stands"]
    new_station["nb_emplacements_dispo"] = properties["available_bike_stands"]
    new_station["nb_velos_dispo"] = properties["available_bikes"]
    new_station["etat"] = properties["status"]
    new_station["latitude"] = properties["lat"]
    new_station["longitude"] = properties["lng"]
    new_station["derniere_maj"] = properties["last_update"]

    stations.append(new_station)

  return stations

def recup_datas_rennes(req_rennes):
  records = req_rennes["records"]

  stations = []

  for station in records:
    new_station = {}

    fields = station["fields"]
    
    new_station["nom"] = fields["nom"]
    new_station["id_station"] = fields["idstation"]
    new_station["nb_emplacements"] = fields["nombreemplacementsactuels"]
    new_station["nb_emplacements_dispo"] = fields["nombreemplacementsdisponibles"]
    new_station["nb_velos_dispo"] = fields["nombrevelosdisponibles"]
    new_station["etat"] = fields["etat"]
    new_station["latitude"] = fields["coordonnees"][0]
    new_station["longitude"] = fields["coordonnees"][1]
    new_station["derniere_maj"] = fields["lastupdate"] 

    stations.append(new_station)

  return stations


def recup_infos_whether(whether_json):
  whether_informations = {}

  main = whether_json["main"]
  whether_informations["Température"] = main["temp"]
  whether_informations["Température ressentie"] = main["feels_like"]

  whether = whether_json["weather"][0]
  whether_informations["Temps"] = whether["description"]

  return whether_informations


def create_ontologies(datas, subclass):
  
  URL = "http://www.semanticweb.org/havyt/ontologies/2022/2/untitled-ontology-14"
  URL_TYPE = "http://www.w3.org/2001/XMLSchema"

  individuals = []

  for i in range(len(datas)):
    line = datas[i]
    
    line['nom'] = line['nom'].replace("&", "et")
    name = line['nom'].replace("/", "")

    elements_name = name.split()
    name = "_".join([element.capitalize() for element in elements_name])

    individual = ""
    individual += f"  <owl:NamedIndividual rdf:about=\"{URL}#{name}\">\n"
    individual += f"      <rdf:type rdf:resource=\"{URL}#{subclass}\"/>\n"
    individual += f"      <derniere_maj>{line['derniere_maj']}</derniere_maj>\n"
    individual += f"      <etat>{line['etat']}</etat>\n"
    individual += f"      <id_station rdf:datatype=\"{URL_TYPE}#integer\">{line['id_station']}</id_station>\n"
    individual += f"      <latitude rdf:datatype=\"{URL_TYPE}#decimal\">{line['latitude']}</latitude>\n"
    individual += f"      <longitude rdf:datatype=\"{URL_TYPE}#decimal\">{line['longitude']}</longitude>\n"
    individual += f"      <nb_emplacements rdf:datatype=\"{URL_TYPE}#integer\">{line['nb_emplacements']}</nb_emplacements>\n"
    individual += f"      <nb_emplacements_dispo rdf:datatype=\"{URL_TYPE}#integer\">{line['nb_emplacements_dispo']}</nb_emplacements_dispo>\n"
    individual += f"      <nb_velos_dispo rdf:datatype=\"{URL_TYPE}#integer\">{line['nb_velos_dispo']}</nb_velos_dispo>\n"
    individual += f"      <nom>{line['nom']}</nom>\n"
    individual += "   </owl:NamedIndividual>\n"

    individuals.append(individual)

  return individuals

def create_complete_rdf(individus):
    with open('before.txt', 'r') as file:
        before = file.read()

    return "{}\n{}\n</rdf:RDF>".format(before, '\n'.join(individus))


def maj_datas():

    URL_LYON = "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171"
    URL_RENNES = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel"

    WHETHER_API_KEY = "3dfeff6f304e5faa5bbb3f4598a260e3"

    req_lyon = requestAPI(URL_LYON)
    req_rennes = requestAPI(URL_RENNES)

    whether_lyon_req = requestAPI(f"https://api.openweathermap.org/data/2.5/weather?q=Lyon&units=metric&lang=fr&appid={WHETHER_API_KEY}")
    whether_rennes_req = requestAPI(f"https://api.openweathermap.org/data/2.5/weather?q=Rennes&units=metric&lang=fr&appid={WHETHER_API_KEY}")

    whether_lyon = recup_infos_whether(whether_lyon_req)
    whether_rennes = recup_infos_whether(whether_rennes_req)

    lyon_stations = recup_datas_lyon(req_lyon)
    rennes_stations = recup_datas_rennes(req_rennes)


    individuals_lyon = create_ontologies(lyon_stations, "spotLyon")
    individuals_rennes = create_ontologies(rennes_stations, "spotRennes")

    individuals_lyon = "\n\n".join(individuals_lyon)
    individuals_rennes = "\n\n".join(individuals_rennes)

    individus = [individuals_lyon, individuals_rennes]

    file_text = create_complete_rdf(individus)
    with open("project_ontology_rdf_xml.owl", "w") as file:
        file.write(file_text)

    return whether_lyon, whether_rennes 