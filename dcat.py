import copy
from typing import List
from dateutil import parser
from loguru import logger
from classes.Dataset import Dataset, Resource

try:
    from processor import Processor
except:
    from .processor import Processor


class ProcessorDCAT(Processor):
    def __init__(self):
        super().__init__(type="dcat")

    def get_datasets(self, owner, start_url, fname):
        logger.info(f"Getting DCAT feed from {start_url} for {owner}")
        current_org_feed = processor.get_json(start_url)

        if current_org_feed in (None, "NULL"):
            logger.error(
                f"Failed to get feed from {start_url} for {owner}. Skipping..."
            )
            return

        feed_datasets = current_org_feed["dcat:dataset"]

        logger.info(f"Found {len(feed_datasets)} datasets for {owner}")

        prepped_datasets = []

        for feed_dataset in feed_datasets:
            title = feed_dataset.get("dct:title", None)
            owner = feed_dataset.get("dct:publisher", None).get("foaf:name", None)
            page_url = feed_dataset.get("@id", None)
            date_created = parser.parse(feed_dataset.get("dct:issued", None)).date()
            date_updated = parser.parse(feed_dataset.get("dct:modified", None)).date()
            license = None # TODO
            description = feed_dataset.get("dct:description", "")
            tags = get_dataset_tags(feed_dataset)
            
            resources = List[Resource]
            feed_dataset_resources = feed_dataset.get("dcat:distribution", None)

            try:
                resources = list(map(map_dataset_resources, feed_dataset_resources))
            except:
                logger.warning("Failed to parse resources for dataset: {title}")

            dataset = Dataset(title, owner, page_url, date_created, date_updated, license, description, tags, resources)

            prepped_datasets.append(
                dataset,
            )

        processor.write_json(fname, prepped_datasets)

    """
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
"""

def get_dataset_tags(dataset):
    tags = dataset.get("dcat:keyword", [])
    # If there's only one keyword (e.g. the property returned a string, then stick it in an array)
    if type(tags) is str:
        tags = [tags]
    return tags;

def map_dataset_resources(dataset_resource):
    file_name = dataset_resource.get("dct:title",None)
    file_type = None # TODO
    asset_url = dataset_resource.get("dcat:accessURL",None).get("@id",None)
    resource = Resource(file_name, file_type, asset_url)
    return resource

processor = ProcessorDCAT()

if __name__ == "__main__":
    processor.process()
