# Packages: beautifulsoup4, csv, requests
import requests
import csv
from bs4 import BeautifulSoup

def get_headers():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    return headers    



if __name__ == "__main__":
    url = "https://www.east-ayrshire.gov.uk/CouncilAndGovernment/About-the-Council/Information-and-statistics/Open-Data.aspx"
    req = requests.get(url, get_headers())
    soup = BeautifulSoup(req.content, 'html.parser')
    list_of_a_tags = soup.find_all("a", href=True)
    list_of_files = []
    for poss in list_of_a_tags:
        if (poss['href'].endswith('csv')):
            list_of_files.append(poss)
    
    

    res = requests.get(url , get_headers())
    t = res.iter_lines("https://www.east-ayrshire.gov.uk/Resources/CSV/Open-Data-001-Primary-School-Contacts.csv")
    data = csv.reader(t, delimiter=',')
    
    
    titles = []
    owners = []
    urls = []
    for fi in list_of_files:
        titles.append(list_of_files[0].string)
        owners.append("East Ayrshire Council")
        urls.append(url)

