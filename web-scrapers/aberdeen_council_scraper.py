from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datefinder
import re

def get_last_updated(string):
    matches = datefinder.find_dates(string)
    return [match for match in matches][0].strftime("%d/%m/%Y")

def get_file_metadata(string):
    file_meta_regex = re.compile(r"\((.*?)\)")
    file_meta = file_meta_regex.search(string).group().strip()
    file_meta = file_meta.strip("(")
    file_meta = file_meta.strip(")")
    file_meta = re.split(",|\s", string)
    filetype = file_meta[0]
    filesize = file_meta[1].strip()
    return (filetype, filesize)

def get_feeds(soup):
    """Get feeds and construct dictionaries with all the values that will be used for the output csv"""

    #Get table and rows
    table = soup.find('table')
    rows = table.find_all('tr')[1:]

    feeds = []

    # get title and files associated to the feed
    for row in rows:
        tds = row.find_all('td')
        feed = {}
        # Add title and files key
        title = tds[0].string
        feed['title'] = title
        feed['files'] = {}
        # Add files with their links, last updated and filesize.
        files = [a_tag for a_tag in tds[1].find_all('a', href=True)]
        for anchor in files:
            link = anchor.get('href')
            if link.endswith('.kmz') or link.endswith('.csv') or link.endswith('.zip'):
                filename = link.rsplit('/', 1)[-1]
                # get last updated
                last_updated = get_last_updated(anchor.text)
                # get size of file
                filetype, filesize = get_file_metadata(anchor.text)

                feed['files'][filename] = {'link': link, 'filesize': urlopen(link).length, 'last-updated': last_updated, 'filetype': filetype, 'filesize': filesize}
        feeds.append(feed)
    return feeds

def parse_feeds(feeds):
    pass

if __name__ == "__main__":
    ### construct array of feed objects
    req = Request('https://www.aberdeenshire.gov.uk/data/open-data/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    feeds = get_feeds(soup)
    print(feeds)