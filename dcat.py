import copy
from dateutil import parser

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
            
                ds = [
                    e.get("dct:title", ""),
                    e.get("dct:publisher", "").get("foaf:name","").replace(" Mapping", ""),
                    "",  # link to page
                    "",  # Link to data
                    "",  #FileName
                    "",  # date created
                    parser.parse(e.get("dct:issued", "")).date(),
                    "",  # size
                    "",  # size unit
                    "",  # filetype
                    "",  # numrecords                     
                    ";".join(map(str, keywords)), # Keywords (we use map here to make sure everything is a string)
                    "",  # Manual tags
                    "",  # license
                    e.get("dct:description", "").strip("\u200b"),
                ]
                pages = e.get("dcat:distribution")
                for p in pages:
                    if p.get("dct:description", "") == "Web Page":
                        ds[2] = p.get("dcat:accessUrl", "")
                        break
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


def get_license(dataset):
    try:
        return dataset["attributes"]["structuredLicense"]["url"]
    except:
        return ""


processor = ProcessorDCAT()

if __name__ == "__main__":
    processor.process()
