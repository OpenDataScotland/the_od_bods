from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datefinder
import re

import math

# https://stackoverflow.com/a/14822210/13940304
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return ("%s %s" % (s, size_name[i]), size_name[i])

def get_last_updated(string):
    matches = datefinder.find_dates(string)
    return [match for match in matches][0].strftime("%d/%m/%Y")


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
                filesize = urlopen(link).length
                formatted_fs, unit = convert_size(filesize)

                feed['files'][filename] = {'link': link, 'filesize': {'value':formatted_fs, 'unit': unit}, 'last-updated': last_updated, 'filetype': filename[-3:].upper(), 'filesize': filesize}
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