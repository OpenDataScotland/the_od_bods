from processor import Processor

DATASETS_LINK = "https://data.parliament.scot/#/datasets"


class ProcessorScottishParliament(Processor):
    def __init__(self):
        super().__init__(type="bespoke_ScottishParliament")

    def get_datasets(self, portal_owner, start_url, fname):
        print(f"Processing {start_url}")

        dataset_url = f"{start_url}api/datasetjson"

        datasets = self.get_json(dataset_url)

        print(f"Found {len(datasets)} datasets")

        prepped_datasets = []

        for dataset in datasets:
            dataset_title = dataset.get("Title", "")
            dataset_owner = portal_owner
            dataset_page_url = DATASETS_LINK
            dataset_date_created = None
            dataset_date_updated = dataset.get("LastUpdated", "")
            dataset_license = None
            dataset_description = dataset.get("Description", "")
            dataset_tags = []
            dataset_resources = []

            dataset_xml_link = dataset.get("XmlLink", None)
            dataset_json_link = dataset.get("JsonLink", None)
            dataset_csv_link = dataset.get("CsvLink", None)

            if dataset_xml_link != None:
                dataset_resources.append(
                    {
                        "fileName": "XML",
                        "fileSize": None,
                        "fileSizeUnit": None,
                        "fileType": "XML",
                        "assetUrl": dataset_xml_link,
                        "dateCreated": None,
                        "dateUpdated": dataset_date_updated,
                        "numRecords": None,
                    }
                )

            if dataset_json_link != None:
                dataset_resources.append(
                    {
                        "fileName": "JSON",
                        "fileSize": None,
                        "fileSizeUnit": None,
                        "fileType": "JSON",
                        "assetUrl": dataset_json_link,
                        "dateCreated": None,
                        "dateUpdated": dataset_date_updated,
                        "numRecords": None,
                    }
                )

            if dataset_csv_link != None:
                dataset_resources.append(
                    {
                        "fileName": "CSV",
                        "fileSize": None,
                        "fileSizeUnit": None,
                        "fileType": "CSV",
                        "assetUrl": dataset_csv_link,
                        "dateCreated": None,
                        "dateUpdated": dataset_date_updated,
                        "numRecords": None,
                    }
                )

            prepped_datasets.append(
                {
                    "title": dataset_title,
                    "owner": dataset_owner,
                    "pageURL": dataset_url,
                    "dateCreated": dataset_date_created,
                    "dateUpdated": dataset_date_updated,
                    "license": dataset_license,
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
