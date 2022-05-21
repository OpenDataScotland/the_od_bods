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
    req = Request('https://www.aberdeenshire.gov.uk/data/open-data/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    print(find_files(soup))