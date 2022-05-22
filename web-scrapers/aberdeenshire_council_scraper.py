from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datefinder
import csv

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
        title = tds[0].get_text()
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

                feed['files'][filename] = {'link': link, 'filesize': {'value':formatted_fs, 'unit': unit}, 'last-updated': last_updated, 'filetype': filename[-3:].upper()}
        feeds.append(feed)
    return feeds

def parse_feeds(feeds):
    """ Process feeds to be ready for csv ouput """
    proc_feeds = []
    for feed in feeds:
        for datafile in feed['files'].keys():
            formatted_feed = []
            formatted_feed.append(feed['title'])
            formatted_feed.append('Aberdeenshire Council')
            formatted_feed.append('https://www.aberdeenshire.gov.uk/online/open-data/')
            formatted_feed.append(feed['files'][datafile]['link'])
            formatted_feed.append('NULL')
            formatted_feed.append(feed['files'][datafile]['last-updated'])
            formatted_feed.append(feed['files'][datafile]['filesize']['value'])
            formatted_feed.append(feed['files'][datafile]['filesize']['unit'])
            formatted_feed.append(feed['files'][datafile]['filetype'])
            formatted_feed.append('NULL')
            formatted_feed.append(' ')
            formatted_feed.append(' ')
            formatted_feed.append('Open Government')
            formatted_feed.append(' ')
            proc_feeds.append(formatted_feed)
    return proc_feeds

def output(parsed):
    with open('aberdeenshire.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        header = ["Title","Owner","PageURL","AssetURL","DateCreated","DateUpdated","FileSize","FileSizeUnit","FileType","NumRecords","OriginalTags","ManualTags","License","Description"]
        writer.writerow(header)

        # write the data
        for record in parsed:
            writer.writerow(record)


if __name__ == "__main__":
    ### construct array of feed objects
    req = Request('https://www.aberdeenshire.gov.uk/data/open-data/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    feeds = get_feeds(soup)
    parsed = parse_feeds(feeds)
    
    # make csv file
    output(parsed)