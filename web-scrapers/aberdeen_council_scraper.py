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

# https://www.geeksforgeeks.org/python-split-camelcase-string-to-individual-strings/
def camel_case_split(str):
    words = [[str[0]]]
  
    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
  
    return [''.join(word) for word in words]

def process_file_titles(file_links):
    """Format title from the name of the file"""
    titles = []

    for file in file_links:
        # files are either snake-case or CamelCase on the website so have to be processed accordingly
        if "_" in file:
            title = file.rsplit('.', 1)[0]
            title = title.replace("_", " ")
            title.title()
            titles.append(title)
        else:
            title = file.rsplit('.', 1)[0]
            title = camel_case_split(title)
            titles.append(title)
    return titles




if __name__ == "__main__":
    ### fetch file URLs
    req = Request('https://www.aberdeenshire.gov.uk/data/open-data/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    file_links = find_files(soup)

    ### process file titles
    titles = process_file_titles(file_links)

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
