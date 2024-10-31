from processor import Processor
from urllib import request
from urllib.parse import urljoin
from email.message import Message
from email.parser import HeaderParser
from bs4 import BeautifulSoup
import unicodedata

EXPECTED_LICENCE_TEXT = "This content is available under the Open Government Licence v3.0, except for graphic assets and where otherwise stated"


class ProcessorCroftingCommission(Processor):
    """Processor for Crofting Commission's open data page"""

    def __init__(self):
        """Base init for type and URL list"""
        super().__init__(type="bespoke_CroftingCommission")

    def build_dataset_resource(self, resource_link, base_url):
        """Build dataset resource by checking file size and type"""

        # Build full URL
        resource_link = urljoin(base_url, resource_link)
        print(f"Requesting metadata for {resource_link}")

        # Set default values
        resource_file_name = None
        resource_file_size = None
        resource_file_size_unit = "B"
        resource_file_type = None
        resource_asset_url = resource_link
        resource_date_created = None  # Not provided by publisher
        resource_date_updated = None  # Not provided by publisher
        resource_num_records = None  # TODO

        # Attempt to get file size, name and type
        file_metadata_request = request.Request(resource_link, method="HEAD")

        try:
            with request.urlopen(file_metadata_request) as file_metadata_response:
                # Get the Content-Disposition header, if available to set resource_file_name and resource_file_type
                content_disposition = file_metadata_response.headers.get("Content-Disposition")
                if content_disposition is not None:
                    # Use Python email library to parse header
                    msg = Message()
                    msg.add_header("Content-Disposition", content_disposition)
                    file_name = msg.get_param("filename", header="Content-Disposition")

                    # Remove the datetimestamp from the file name
                    base_name, extension = file_name.rsplit('.', 1)
                    file_name = '_'.join(base_name.split('_')[:-1]) + '.' + extension

                    resource_file_name = file_name
                    resource_file_type = extension
                else:
                    print(
                        "Content-Disposition header not found. Cannot set resource_file_name"
                    )

                # Get the Content-Length header, if available to set resource_file_size
                file_size = file_metadata_response.headers.get("Content-Length")
                if file_size is not None:
                    resource_file_size = int(file_size)
                else:
                    print(
                        "Content-Length header not found. Cannot set resource_file_size"
                    )
        except Exception as e:
            print(f"Failed to get file metadata for {resource_link}: {e}")

        return {
            "fileName": resource_file_name,
            "fileSize": resource_file_size,
            "fileSizeUnit": resource_file_size_unit,
            "fileType": resource_file_type,
            "assetUrl": resource_asset_url,
            "dateCreated": resource_date_created,
            "dateUpdated": resource_date_updated,
            "numRecords": resource_num_records,
        }

    def get_datasets(self, owner, url, fname):
        """Gets datasets from provided portal and outputs to JSON"""
        print(f"Processing {url}")

        # Request page with dataset listing
        page_response = request.urlopen(url)
        page_response_html = page_response.read().decode()

        # Parse the page
        parsed_page = BeautifulSoup(page_response_html, "html.parser")
        page_content_text = parsed_page.select_one("#pagecontent").get_text()
        page_content_text = unicodedata.normalize("NFKD", page_content_text)

        # Confirm the licence
        datasets_licence = "Unknown"
        if EXPECTED_LICENCE_TEXT in page_content_text:
            datasets_licence = "OGL3"
        else:
            print("Licence has changed from OGL3")

        # Get the datasets listing table
        datasets_table = parsed_page.select_one("#pagecontent table")
        datasets_table_rows = [
            tr for tr in datasets_table.find_all("tr") if not tr.find("th")
        ]

        prepped_datasets = []

        for row in datasets_table_rows:
            row_cells = row.find_all("td")

            dataset_title = row_cells[0].get_text()
            dataset_owner = owner
            dataset_page_url = url
            dataset_date_created = None
            dataset_date_updated = None
            dataset_licence = datasets_licence

            lowercase_dataset_title = dataset_title[
                0
            ].lower() + dataset_title.removeprefix(dataset_title[0])
            dataset_description = f"{owner}'s {lowercase_dataset_title}"
            dataset_tags = []

            dataset_url = row_cells[1].find("a")["href"]
            dataset_resources = [self.build_dataset_resource(dataset_url, url)]

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

        processor.write_json(fname, prepped_datasets)


processor = ProcessorCroftingCommission()

if __name__ == "__main__":
    processor.process("json")
