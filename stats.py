from urllib import request, parse

sparql = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX folder: <http://publishmydata.com/def/ontology/folder/>

SELECT ?uri ?name ?creator ?publisher ?issued ?modified ?licence ?comment ?theme 
WHERE {
  ?uri rdf:type <http://publishmydata.com/def/dataset#Dataset>.    
  OPTIONAL { ?uri rdfs:label ?name. }
  OPTIONAL { ?uri dcterms:publisher/rdfs:label ?publisher.}
  OPTIONAL { ?uri dcterms:creator/rdfs:label ?creator.}
  OPTIONAL { ?uri dcterms:issued ?issued.}
  OPTIONAL { ?uri dcterms:modified ?modified.}
  OPTIONAL { ?uri dcterms:license ?licence.}
  OPTIONAL { ?uri rdfs:comment ?comment.}
  OPTIONAL { 
    ?uri dcat:theme ?themeUri.
    ?themeUri folder:inTree <http://statistics.gov.scot/def/concept/folders/themes>;
              rdfs:label ?theme.
  }
}
"""

data = parse.urlencode({"query": sparql}).encode()
req = request.Request("http://statistics.gov.scot/sparql", data=data)
req.add_header("Accept", "text/csv")
req.add_header("Contect-type", "application/x-www-form-urlencoded")
resp = request.urlopen(req)

print(resp.read().decode())



