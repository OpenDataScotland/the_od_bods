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

    total_bytes = -1
    for line in lines:
        bytes_on_this_line = len(line) + 1
        total_bytes += bytes_on_this_line


    return number_of_records, total_bytes
    

def csv_output(header, data): 

    with open('the_od_bods/web-scrapers/output.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

    # write the header
        writer.writerow(header)

    # write the data
        for record in data:
            writer.writerow(record)

if __name__ == "__main__":  
    # Record Headings
    header = ["Title","Owner","PageURL","AssetURL","DateCreated","DateUpdated","FileSize","FileSizeUnit","FileType","NumRecords","OriginalTags","ManualTags","License","Description"]
    data = []

    list_of_files = get_all_files()
    for fi in list_of_files:
        metadata = csv_file_metadata(fi['href'])
        output = [fi.string, "East Ayrshire Council", URL_COUNCIL+URL_PAGE, URL_COUNCIL+fi['href'], "NULL", "NULL", metadata[1], "B", "CSV", "B", metadata[0], "NULL", "Education", "Open Government", "NULL"]     
        data.append(output)

    csv_output(header, data)
    
        

