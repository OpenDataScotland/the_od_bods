from processor import Processor
import requests
from bs4 import BeautifulSoup

class ProcessorShetlandCouncil(Processor):
    """Processor for Shetland Council's open data page"""

    def __init__(self):
        """Base init for type and URL list"""
        super().__init__(type="bespoke_ShetlandCouncil")
   
    def get_datasets(self, owner, url, fname):
        """Gets datasets from provided portal and outputs to JSON"""
        print(f"Processing {url}")

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        datasets_elements = soup.select(".list--downloads li.list__item")

        print(f"Found {len(datasets_elements)} datasets")

        for element in datasets_elements:
            # print("----------")
            # print(element)
            # print("----------")
            title = element.select_one(".download__heading")
            print(title.text)


processor = ProcessorShetlandCouncil()

if __name__ == "__main__":
    processor.process("json")
