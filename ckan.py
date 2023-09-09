import requests
import urllib.parse
from bs4 import BeautifulSoup
from enum import Enum
from processor import Processor

STATUS_BASE_URL = "api/3/action/status_show"
PACKAGE_LIST_URL = "api/3/action/package_list"
PACKAGE_SHOW_URL = "api/3/action/package_show?id="


class KAN_TYPE(Enum):
    """Enum for portal type"""
    CKAN = 1
    DKAN = 2


def get_dkan_license(url):
    """Scrapes license from dataset page as DKAN API does not return license info"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    license_element = soup.select_one(".field-name-field-license")

    return license_element.text or None

def sanitise_resource_url(url):
    """Sometimes DKAN's resource URLs wrap URLs with HTML. This method detects it and strips it out."""
    if url.startswith("<"):        
        soup = BeautifulSoup(url, "html.parser")
        return soup.get_text()

    return url


class ProcessorCKAN_DKAN(Processor):
    def __init__(self):
        super().__init__(type="ckan_or_dkan")

    def get_datasets(self, portal_owner, start_url, fname):
        print(f"Processing {start_url}")

        url = start_url

        ### catch for missing trailing "/" in url
        if url[-1] != "/":
            url = url + "/"

        # Check for portal type as DKAN has a slightly different api schema
        portal_info = processor.get_json(f"{url}{STATUS_BASE_URL}", False)

        portal_type = KAN_TYPE.DKAN if portal_info == "NULL" else KAN_TYPE.CKAN

        datasets = processor.get_json(f"{url}{PACKAGE_LIST_URL}")
        if datasets != "NULL":
            print(f"Found {len(datasets['result'])} datasets")

            prepped = []
            for dataset_name in datasets["result"]:
                dataset_metadata = processor.get_json(
                    f"{url}{PACKAGE_SHOW_URL}{urllib.parse.quote(dataset_name)}"
                )

                print(
                    f"Got {dataset_name} with success status: {dataset_metadata['success']}"
                )

                # DKAN returns an array when requesting a single package, CKAN returns just a single object
                dataset_metadata = (
                    dataset_metadata["result"]
                    if portal_type == KAN_TYPE.CKAN
                    else dataset_metadata["result"][0]
                )

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

                # DKAN (At least in the case of Marine Scotland) doesn't expose license in API returns
                dataset_license = (
                    dataset_metadata.get("license_title","")
                    if portal_type == KAN_TYPE.CKAN
                    else get_dkan_license(dataset_metadata["url"])
                )

                for resource in dataset_metadata.get("resources", []):
                    tags = list(
                        map(lambda x: x["name"], dataset_metadata.get("tags", []))
                    )

                    file_size = 0
                    file_size_unit = "B"

                    if "archiver" in resource and "size" in resource["archiver"]:
                        file_size = resource["archiver"]["size"]
                    elif "size" in resource:
                        if isinstance(resource["size"], int) or isinstance(resource["size"], float):
                            file_size = resource["size"]
                        elif resource["size"] is not None and resource["size"].isnumeric():
                            file_size = resource["size"]
                        # Marine Scotland store file sizes as a string with units e.g. "99.99 MB"
                        elif resource["size"] is not None and len(resource["size"]) > 0:
                            split_file_size = resource["size"].split()
                            file_size = float(split_file_size[0])
                            file_size_unit = split_file_size[1].replace("bytes", "B")

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

                    # Some Marine Scotland datasets have "data" as the file type, which is ambiguous and not helpful
                    if file_type == "data":
                        file_type = None                    

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

                    resource_url = sanitise_resource_url(resource["url"])

                    prepped.append(
                        [
                            dataset_metadata["title"],  # Title
                            owner,  # Owner
                            f"{url}dataset/{dataset_name}",  # PageURL
                            resource_url,  # AssetURL
                            resource["name"],  # FileName
                            dataset_metadata["metadata_created"],  # DateCreated
                            dataset_metadata["metadata_modified"],  # DateUpdated
                            file_size,  # FileSize
                            file_size_unit,  # FileSizeUnit
                            file_type,  # FileType
                            None,  # NumRecords
                            ";".join(tags),  # OriginalTags
                            None,  # ManualTags
                            dataset_license,  # License
                            description,  # Description
                        ]
                    )

                processor.write_csv(fname, prepped)


processor = ProcessorCKAN_DKAN()

if __name__ == "__main__":
    processor.process()
