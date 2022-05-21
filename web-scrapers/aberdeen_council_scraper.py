import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    page = requests.get("https://www.aberdeenshire.gov.uk/data/open-data/")
    soup = BeautifulSoup(page.content, 'hmtl.parser')