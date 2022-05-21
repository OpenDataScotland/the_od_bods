from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_feeds(soup):
    """Get feeds and construct dictionaries with all the values that will be used for the output csv"""

    #Get table and rows
    table = soup.find('table')
    rows = table.find_all('tr')[1:]

    feeds = []

    for row in rows:
        tds = row.find_all('td')
        feed = {}
        # Add title
        title = tds[0].string
        feed['title'] = title
        # Add files
        file_links = [link.get('href') for link in tds[1].find_all('a', href=True)]
        feed['links'] = []
        for link in file_links:
            if link.endswith('.kmz') or link.endswith('.csv') or link.endswith('.zip'):
                feed['links'].append(link)
        feeds.append(feed)
    return feeds

if __name__ == "__main__":
    ### construct array of feed objects
    req = Request('https://www.aberdeenshire.gov.uk/data/open-data/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    feeds = get_feeds(soup)

    ### process file titles
    titles = []

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