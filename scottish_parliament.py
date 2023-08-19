from processor import Processor

DATASETS_LINK = "https://data.parliament.scot/#/datasets"
DATASETS_LICENCE = "Scottish Parliament Copyright Policy"


class ProcessorScottishParliament(Processor):
    """Processor for Scottish Parliament's open data portal"""

    def __init__(self):
        """Base init for type and URL list"""
        super().__init__(type="bespoke_ScottishParliament")

    def build_dataset_resources(self, xml_link, json_link, csv_link, date_updated):
        """Build dataset resources by checking for urls"""
        dataset_resources = []
        if xml_link is not None:
            dataset_resources.append(
                {
                    "fileName": "XML",
                    "fileSize": None,
                    "fileSizeUnit": None,
                    "fileType": "XML",
                    "assetUrl": xml_link,
                    "dateCreated": None,
                    "dateUpdated": date_updated,
                    "numRecords": None,
                }
            )

        if json_link is not None:
            dataset_resources.append(
                {
                    "fileName": "JSON",
                    "fileSize": None,
                    "fileSizeUnit": None,
                    "fileType": "JSON",
                    "assetUrl": json_link,
                    "dateCreated": None,
                    "dateUpdated": date_updated,
                    "numRecords": None,
                }
            )

        if csv_link is not None:
            dataset_resources.append(
                {
                    "fileName": "CSV",
                    "fileSize": None,
                    "fileSizeUnit": None,
                    "fileType": "CSV",
                    "assetUrl": csv_link,
                    "dateCreated": None,
                    "dateUpdated": date_updated,
                    "numRecords": None,
                }
            )

        return dataset_resources

    def get_datasets(self, owner, url, fname):
        """Gets datasets from provided portal and outputs to JSON"""
        print(f"Processing {url}")

        datasets_url = f"{url}api/datasetjson"

        datasets = self.get_json(datasets_url)

        print(f"Found {len(datasets)} datasets")

        prepped_datasets = []

        for dataset in datasets:
            dataset_title = dataset.get("Title", "")
            dataset_owner = owner
            dataset_page_url = DATASETS_LINK
            dataset_date_created = None
            dataset_date_updated = dataset.get("LastUpdated", "")
            dataset_licence = DATASETS_LICENCE
            dataset_description = dataset.get("Description", "")
            dataset_tags = []
            dataset_resources = self.build_dataset_resources(
                dataset.get("XmlLink", None),
                dataset.get("JsonLink", None),
                dataset.get("CsvLink", None),
                dataset_date_updated,
            )

            prepped_datasets.append(
                {
                    "title": dataset_title,
                    "owner": dataset_owner,
                    "pageURL": dataset_page_url,
                    "dateCreated": dataset_date_created,
                    "dateUpdated": dataset_date_updated,
                    "licence": dataset_licence,
                    "description": dataset_description,
                    "tags": dataset_tags,
                    "resources": dataset_resources,
                }
            )

        print(fname)
        processor.write_json(fname, prepped_datasets)


processor = ProcessorScottishParliament()

if __name__ == "__main__":
    processor.process("json")
