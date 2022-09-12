from io import StringIO
from urllib import request, parse
import pandas as pd
from processor import Processor
import os

class ProcessorSparkQL(Processor):
    def __init__(self):
        super().__init__(type="sparkql")

    # SparkQL Dataset Query for API
    def get_sparkql_query(self):
        return """
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

    def get_datasets(self, owner, start_url, fname):

        sparkql = self.get_sparkql_query();
        data = parse.urlencode({"query": sparkql}).encode()

        # API REQUEST
        req = request.Request("http://statistics.gov.scot/sparql", data=data)
        req.add_header("Accept", "text/csv")
        req.add_header("Contect-type", "application/x-www-form-urlencoded")
        resp = request.urlopen(req)

        # Decoding response and adding to pandas dataframe
        respDecode = StringIO(resp.read().decode())
        df = pd.read_csv(respDecode)

        # Dropping Duplicate Datasets by Filtering Latest Issued Dataset
        dfUnique = df.sort_values('issued', ascending=False) \
                        .drop_duplicates(subset='name', keep="first")

        # Renaming Column Names to ODS Format
        dfOds = dfUnique \
                .rename(columns=
                    {
                        'name':'title',
                        'theme':'category',
                        'creator':'organization',
                        'comment':'notes',
                        'issued':'date_created',
                        'modified':'date_updated',
                        'uri':'url'
                    }) \
                .drop(columns = ['publisher'])

        # File Path
        fname = os.path.join("data", "scotgov-datasets-sparkql" + ".csv")
        dfOds.to_csv(fname,index=False);

processor = ProcessorSparkQL()
processor.process()