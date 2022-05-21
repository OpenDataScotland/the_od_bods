from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datefinder

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
        # Add title
        title = tds[0].string
        feed['title'] = title
        # Add files with their links, last updated and filesize.
        files = [a_tag for a_tag in tds[1].find_all('a', href=True)]
        for anchor in files:
            link = anchor.get('href')
            if link.endswith('.kmz') or link.endswith('.csv') or link.endswith('.zip'):
                filename = link.rsplit('/', 1)[-1]
                # get last updated
                last_updated = get_last_updated(anchor.text)

                feed[filename] = {'link': link, 'filesize': urlopen(link).length, 'last-updated': last_updated}
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