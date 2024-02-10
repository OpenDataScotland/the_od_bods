from processor import Processor
import time

class ProcessorCKAN(Processor):
    def __init__(self):
        super().__init__(type="ckan")

    def get_datasets(self, portal_owner, start_url, fname):
        print(f"Processing {start_url}")

        url = start_url

        ### catch for missing trailing "/" in url
        if url[-1] != "/":
            url = url + "/"

        datasets = processor.get_json(f"{url}api/3/action/package_list")
        if datasets != "NULL":

            print(f"Found {len(datasets['result'])} datasets")

            prepped = []
            for dataset_name in datasets["result"]:

                # Rate limit us a little to avoid abusing the API
                time.sleep(1)
                dataset_metadata = processor.get_json(
                    f"{url}/api/3/action/package_show?id={dataset_name}"
                )

                try:
                    print(
                        f"Got {dataset_name} with success status: {dataset_metadata['success']}"
                    )
                except:
                    print(f"Failed to get metadata for {dataset_name}. Skipping...")
                    continue                

                dataset_metadata = dataset_metadata["result"]

                ### gets provided owner name if exists, else uses the owner of the portal.
                if (
                    "organization" in dataset_metadata
                    and "title" in dataset_metadata["organization"]
                ):
                    owner = dataset_metadata["organization"]["title"]
                else:
                    owner = portal_owner

                # TEMP FIX: PHS uses CKAN org objects as categories for some reason, overwrite them with PHS until we can make an org filtering system
                if portal_owner == "Public Health Scotland":
                    owner = portal_owner

                for resource in dataset_metadata["resources"]:
                    tags = list(map(lambda x: x["name"], dataset_metadata["tags"]))

                    file_size = 0

                    if "archiver" in resource and "size" in resource["archiver"]:
                        file_size = resource["archiver"]["size"]
                    elif "size" in resource:
                        file_size = resource["size"]

                    file_type = ""

                    if resource["format"]:
                        file_type = resource["format"]
                    elif "qa" in resource and "format" in resource["qa"]:
                        file_type = resource["qa"]["format"]
                    elif "resource:format" in resource:
                        file_type = resource["resource:format"]
                    elif "service_type" in resource:
                        file_type = resource["service_type"]
                    elif "is_wfs" in resource and resource["is_wfs"] == "yes":
                        file_type = "WFS"

                    description = dataset_metadata["notes"]

                    # TEMP FIX: PHS, Dundee and Stirling have some unicode chars that break the CSV. Long term we will sort this by using JSON
                    if (
                        portal_owner == "Public Health Scotland"
                        or portal_owner == "Dundee City Council"
                        or portal_owner == "Stirling Council"
                    ):
                        description = (
                            dataset_metadata["notes"].encode("unicode_escape").decode()
                        )

                    prepped.append(
                        [
                            dataset_metadata["title"],  # Title
                            owner,  # Owner
                            f"{url}dataset/{dataset_name}",  # PageURL
                            resource["url"],  # AssetURL
                            resource["name"],  # FileName
                            dataset_metadata["metadata_created"],  # DateCreated
                            dataset_metadata["metadata_modified"],  # DateUpdated
                            file_size,  # FileSize
                            "B",  # FileSizeUnit
                            file_type,  # FileType
                            None,  # NumRecords
                            ";".join(tags),  # OriginalTags
                            None,  # ManualTags
                            dataset_metadata["license_title"],  # License
                            description,  # Description
                        ]
                    )

                processor.write_csv(fname, prepped)


processor = ProcessorCKAN()

if __name__ == "__main__":
    processor.process()
