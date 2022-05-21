from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def find_files(soup):
    """Used to find all kmz, zip or csv files on the webpage"""
    links = [link for link in soup.find_all('a', href=True)]
    file_links = []
    for l in links:
        link = l.get("href")
        if link.endswith('.kmz') or link.endswith('.csv') or link.endswith('.zip'):
            file_links.append(link)
    return file_links


if __name__ == "__main__":
    ### fetch file URLs
    req = Request('https://www.aberdeenshire.gov.uk/data/open-data/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    file_links = find_files(soup)

    ### process file titles
    titles = []

    owners  = []
    page_urls = []
    asset_urls = []
    date_createds = []
    date_updateds = []
    file_sizes = []
    file_size_units = []
    file_types = []
    num_records = []
    original_tags = []
    manual_tags = []
    licenses = []
    descriptions = []