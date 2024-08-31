from processor import Processor
import urllib.request
from bs4 import BeautifulSoup

DATASETS_LICENCE = "TODO"


class ProcessorCroftingCommission(Processor):
    """Processor for Crofting Commission's open data page"""

    def __init__(self):
        """Base init for type and URL list"""
        super().__init__(type="bespoke_CroftingCommission")

    def get_datasets(self, owner, url, fname):
        """Gets datasets from provided portal and outputs to JSON"""
        print(f"Processing {url}")

        # Request page with dataset listing
        page_response = urllib.request.urlopen(url)
        page_response_html = page_response.read().decode()

        # Parse the page
        parsed_page = BeautifulSoup(page_response_html, "html.parser")

        # Get the datasets listing table
        datasets_table = parsed_page.select_one("#pagecontent table")
        datasets_table_rows = datasets_table.find_all("tr")

        for row in datasets_table_rows:
            print(row)
                    
        # processor.write_json(fname, prepped_datasets)


processor = ProcessorCroftingCommission()

if __name__ == "__main__":
    processor.process("json")
