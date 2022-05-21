# Packages: beautifulsoup4, csv, requests
import requests
import csv
from bs4 import BeautifulSoup

URL_COUNCIL = "https://www.east-ayrshire.gov.uk/"
URL_PAGE = "CouncilAndGovernment/About-the-Council/Information-and-statistics/Open-Data.aspx"

def get_headers():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    return headers    

def get_all_files():
    url = URL_COUNCIL+URL_PAGE 
    req = requests.get(url, get_headers())
    soup = BeautifulSoup(req.content, 'html.parser')
    list_of_a_tags = soup.find_all("a", href=True)
    list_of_files = []
    for poss in list_of_a_tags:
        if (poss['href'].endswith('csv')):
            list_of_files.append(poss)

    return list_of_files        


def csv_file_metadata(file_loc):
    text = requests.get(URL_COUNCIL+file_loc , get_headers()).text
    lines = text.splitlines()
    data = csv.reader(lines)
    number_of_records = len(list(data))-1
    print(number_of_records)
    return number_of_records
    

def csv_output():
    pass

if __name__ == "__main__":  
    # Record Headings
    titles = []
    owners = []
    urls = []
    asset_urls = []
    date_created = []
    date_updated = [] 
    file_size = []
    file_unit = []
    file_type = []
    num_records = []
    original_tags = []
    manual_tags = []
    lisence = []
    description = [] 
    # Record Headings

    list_of_files = get_all_files()
    for fi in list_of_files:
        titles.append(fi.string)
        owners.append("East Ayrshire Council")
        urls.append(URL_COUNCIL+URL_PAGE)
        asset_urls.append(URL_COUNCIL+fi['href'])
        date_created.append("NULL")
        date_updated.append("NULL")
        file_type.append("CSV")
        
        # File metadata
        num_records.append(csv_file_metadata(fi['href']))

        lisence.append("Open Government")
        description.append("")

    print(titles)
    print(owners)
    print(urls)
    print(asset_urls)
    print(date_created)
    print(date_updated)
    print(file_type)
    print(num_records)
    print(lisence)
    print(description)    
        

