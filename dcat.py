import copy
from dateutil import parser
from urllib.parse import urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup

try:
    from processor import Processor
except:
    from .processor import Processor


class ProcessorDCAT(Processor):
    def __init__(self):
        super().__init__(type="dcat")

    def get_datasets(self, owner, start_url, fname):
        print(start_url)
        d = processor.get_json(start_url)
        if d != "NULL":

            datasets = d["dcat:dataset"]

            print(f"Found {len(datasets)} datasets")

            prepped = []
            for e in datasets:
                # Get keywords
                keywords = e.get("dcat:keyword", [])

                # If there's only one keyword (e.g. the property returned a string, then stick it in an array)
                if type(keywords) is str:
                    keywords = [keywords]

                # Get common metadata
                title = e.get("dct:title", "")
                owner = e.get("dct:publisher", "").get("foaf:name","")
                original_dataset_link = e.get("@id","")
                date_created = parser.parse(e.get("dct:issued", "")).date()
                date_modified = parser.parse(e.get("dct:modified", "")).date()
                tags = ";".join(
                        map(str, keywords)
                    )
                
                metadata_url= e.get("dct:identifier","")
                license = get_license(metadata_url) # TODO

                description = e.get("dct:description", "").strip("\u200b")

                ds = [
                    e.get("dct:title", ""),
                    e.get("dct:publisher", "").get("foaf:name","").replace(" Mapping", ""),
                    e.get("@id",""),  # Link to page
                    "",  # Link to data
                    "",  # FileName
                    "",  # date created
                    parser.parse(e.get("dct:issued", "")).date(),
                    "",  # size
                    "",  # size unit
                    "",  # filetype
                    "",  # numrecords
                    ";".join(
                        map(str, keywords)
                    ),  # Keywords (we use map here to make sure everything is a string)
                    "",  # Manual tags
                    license,  # license
                    e.get("dct:description", "").strip("\u200b"),
                ]
                pages = e.get("dcat:distribution")
                dsl = []
                for p in pages:
                    if p.get("dct:description", "") == "Web Page":
                        continue
                    ds[3] = p.get("dcat:accessUrl", "")
                    ds[9] = p.get("dct:title", "")
                    dsl.append(copy.deepcopy(ds))
                if not dsl:
                    dsl.append(ds)
                prepped += dsl

            print(f"{len(prepped)} lines for csv")
            processor.write_csv(fname, prepped)


def get_license(metadata_url):
    parsed_url = urlparse(metadata_url)
    dataset_guid = parse_qs(parsed_url.query)['id'][0]

    license_metadata_url = f"https://www.arcgis.com/sharing/rest/content/items/{dataset_guid}?f=json"

    license_metadata = processor.get_json(license_metadata_url)

    return parse_license(license_metadata.get("licenseInfo",""))

# TODO: This probably needs refactored as part of a main license parsing function
def parse_license(license_info):
    if license_info in (None, ""):
        return ""
    
    # Strip HTML
    soup = BeautifulSoup(license_info)
    stripped_license_info = soup.get_text().replace("\t", " ").replace("\r", " ").replace("\n", " ")

    if stripped_license_info in (None, ""):
        return ""

    if any(s.lower() in stripped_license_info.lower() for s in ("Data is being released under Open Government Licence terms", "supplied under the Open Government Licence", "supplied under the Open Government License", "supplied under the Open Government License", "This dataset is available for use under the Open Government Licence", "This dataset is available under the terms of the UK Open Government Licence","http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3","made available under the Open Government Licence", "you do have to adhere to the terms of the Open Government Licence", "We, Stirling Council, publish our mapping datasets under the Open Government Licence", "publish our mapping datasets under the Open Government Licence", "We use the Open Government Licence")):
        return "OGL3"
    
    if stripped_license_info.lower().startswith("open government licence") or stripped_license_info.lower().startswith("open government license") or stripped_license_info.lower().startswith("uk open government licence") or stripped_license_info.lower().startswith("uk open government license"):
        return "OGL3"
    
    if "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3" in stripped_license_info.lower():
        return "OGL3"
    
    if stripped_license_info == "CC-BY-SA":
        return "https://creativecommons.org/licenses/by-sa/3.0/"

    # TODO: Log unknown licenses as warnings
    print(f"UNKNOWN: {stripped_license_info}")

    return "NOT_FOUND: " + stripped_license_info



processor = ProcessorDCAT()

if __name__ == "__main__":
    processor.process()
