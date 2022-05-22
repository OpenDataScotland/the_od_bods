# Packages: beautifulsoup4, csv, requests, math
import requests
import csv
import math
from bs4 import BeautifulSoup

# Global Variables
URL_COUNCIL = "http://www.moray.gov.uk/"
URL_PAGE = "moray_standard/page_110140.html"

def get_headers():
    """
    Gets headers to make a request from the URL. Optimized so website doesn't think a bot is making a request.

    Args:
        NULL

    Returns:
        headers (Dictionary) : header values
    """       
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    return headers    

def get_all_files():
    """
    Gets lists of tags from webpage. Optimized for .csv files and to get data from td tags.

    Args:
        NULL

    Returns:
        headers (List) : list of titles of table, list of descriptions of table, list of csv files.
    """ 
    url = URL_COUNCIL+URL_PAGE
    req = requests.get(url, get_headers())
    soup = BeautifulSoup(req.content, 'html.parser')
    list_of_files = []

    list_of_titles = soup.select("td:nth-of-type(1)")
    list_of_desc = soup.select("td:nth-of-type(2)")

    list_of_a_tags = soup.find_all("a", href=True)
    for poss in list_of_a_tags:
        if (poss['href'].endswith('csv')):
            list_of_files.append(poss)

    return list_of_titles, list_of_desc, list_of_files        

def csv_file_metadata(file_loc):
    """
    Gets file size and number of record for .csv file. 

    Args:
        file_loc (String): URL for location of file on the internet

    Returns:
        number_of_records (int), total_bytes (int) : total number of records and total number of bytes of .csv files.
    """ 
    text = requests.get(file_loc , get_headers()).text
    lines = text.splitlines()
    data = csv.reader(lines)
    number_of_records = len(list(data))-1

    total_bytes = -1
    for line in lines:
        bytes_on_this_line = len(line) + 1
        total_bytes += bytes_on_this_line


    return number_of_records, total_bytes  

def csv_output(header, data):
    """
    Create output csv file of the final data scrapped from website. 

    Args:
        header (List): A list of header items that are Strings.
        data (List): A list of records. 
    Returns:
        NULL
    """  

    with open('the_od_bods/web-scrapers/output_moray.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for record in data:
            writer.writerow(record)

def convert_size(size_bytes):
    """
    Create human-readable way to display .csv file sizes.

    Source: # https://stackoverflow.com/a/14822210/13940304

    Args:
        size_bytes (int): A list of header items that are Strings.
        data (List): A list of records. 
    Returns:
        tuple (Tuple): a tuple which has the file size and the file unit
    """ 
    if size_bytes == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return ("%s %s" % (s, size_name[i]), size_name[i])

if __name__ == "__main__":
    # Record Headings
    header = ["Title","Owner","PageURL","AssetURL","DateCreated","DateUpdated","FileSize","FileSizeUnit","FileType","NumRecords","OriginalTags","ManualTags","License","Description"]
    data = []

    list_of_titles, list_of_desc, list_of_files = get_all_files()

    counter = 1
    for fi in list_of_files:
        metadata = csv_file_metadata(fi['href'])
        file_size = convert_size(metadata[1])
        output = [list_of_titles[counter].string, "Moray Council", URL_COUNCIL+URL_PAGE, fi['href'], "NULL", "NULL", file_size[0], file_size[1], "CSV", metadata[0], "NULL", list_of_titles[counter].string.replace(" ", ""), "Open Government Licence 3.0 (United Kingdom)", list_of_desc[counter].string]     
        data.append(output)
        counter += 1

    csv_output(header, data)