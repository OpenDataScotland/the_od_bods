# Packages: beautifulsoup4, csv, requests, math
import requests
import csv
from bs4 import BeautifulSoup

# Global Variables
ODR_URL = "https://data.nls.uk/download/national-library-of-scotland-open-data-register-2019.csv"


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


def csv_output(header, data):
    """
    Create output csv file of the final data scrapped from website.

    Args:
        header (List): A list of header items that are Strings.
        data (List): A list of records.
    Returns:
        NULL
    """

    with open('../data/scraped-results/output_nls.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for record in data:
            writer.writerow(record)


def fetch_page_url(title: str, url: str) -> str:
    """
    Fetches page url for dataset.

    Args:
        title (str): The title of the dataset, from the ODR.
        url (str): A URL for the category the dataset is in.
    Returns:
        pageurl (str): A URL linking to the parent page for the dataset.
    """
    req = requests.get(url, get_headers())
    soup = BeautifulSoup(req.content, "html.parser")

    outer_tags = soup.select("figcaption")

    for outer_tag in outer_tags:
        inner_tag = outer_tag.find(href=True)
        if inner_tag:
            cleaned_title = title.lower().replace(" ", "").replace("'", "’")
            cleaned_contents = str(inner_tag.contents[0]).lower().replace(" ", "")
            if cleaned_title in cleaned_contents:
                return inner_tag["href"]

    return "NULL"


def fetch_page_data(url: str):
    """
    Fetches relevant metadata from page hosting direct link to dataset.

    Args:
        url (str): A URL for the page hosting direct link to dataset.
    Returns:
        asseturl (str): Direct link to the dataset.
        filesize (str): Numerical component for dataset size (usually compressed)
        sizeunit (str): Magnitude component for dataset size (eg KB/MB/GB)
        numrecs (str): Currently nulled: for possibly scraping record numbers from file_contents
    """
    req = requests.get(url, get_headers())
    soup = BeautifulSoup(req.content, "html.parser")
    asseturl = "NULL"
    filesize = "NULL"
    sizeunit = "NULL"
    file_contents = ""
    size_data = ""
    possible_button_text = ["Download full dataset", "Download the dataset", "Download the data", ]

    buttons = soup.find_all("a", class_="wp-block-button__link no-border-radius")
    if not buttons:  # Because one collection's page uses a different button class
        buttons = soup.find("div", class_="wp-block-button is-style-fill")
        buttons = buttons.find_all("a", class_="wp-block-button__link")

    for button in buttons:
        if str(button.contents[0]) in possible_button_text:
            asseturl = button["href"]

    if asseturl[:10] == "/download/":  # Make relative URLs absolute
        asseturl = "https://data.nls.uk" + asseturl

    headlines = soup.find_all("h4")
    for headline in headlines:
        if "All the data" in headline.contents[0]:
            file_contents = headline.find_next("p").contents[0]
            size_data = headline.find_next("strong").contents[0]
            if size_data == "File size: ":
                filesize = headline.find_next("strong").find("strong").contents[0]
                sizeunit = headline.find_next("strong").contents[2][:2]
                size_data = ""

    if not file_contents:
        headlines = soup.find_all("h3")
        for headline in headlines:
            if "All the data" in headline.contents[0]:
                file_contents = headline.find_next("p").contents[0]
                if file_contents[:4] != "File":
                    file_contents = "NULL"
                    break
                size_data = headline.find_next("strong").contents[0]

    if not file_contents:
        headlines = soup.find_all("h3")
        for headline in headlines:
            if "Download the data" in headline.contents[0]:
                file_contents = headline.find_next("p").contents[0]
                if str(file_contents).strip()[:4] != "File":
                    file_contents = "NULL"
                    break
                size_data = headline.find_next("strong").contents[0]

    if size_data:
        filesize = size_data.split()[2]
        sizeunit = size_data.split()[3]

    return asseturl, filesize, sizeunit, "NULL"


if __name__ == "__main__":
    # Record Headings
    header = ["Title", "Owner", "PageURL", "AssetURL", "DateCreated", "DateUpdated", "FileSize", "FileSizeUnit",
              "FileType", "NumRecords", "OriginalTags", "ManualTags", "License", "Description", ]
    data = []
    category_match = {"Digitised material collection": "digitised-collections",
                      "Metadata collection": "metadata-collections",
                      "Spatial data": "map-spatial-data",
                      "Organisational data": "organisational-data"}

    req = requests.get(ODR_URL, get_headers()).content.decode("utf-8")
    csvreader = csv.reader(req.splitlines(), delimiter=",")
    next(csvreader)

    for row in csvreader:
        owner = "National Library of Scotland"
        title = row[0]
        collection = row[1]
        create_date = row[2]
        data_type = row[4]
        nls_license = row[6]

        outer_url = f"https://data.nls.uk/data/{category_match[collection]}/"

        if title == "Encyclopaedia Britannica, 1771-1860":  # Hardcoded because ODR and page has mismatching dates
            pageurl = "https://data.nls.uk/data/digitised-collections/encyclopaedia-britannica/"
        else:
            pageurl = fetch_page_url(title, outer_url)

        if title == "British Army Lists":  # Contains 4 separate download links: temporarily nulled to prevent conflicts
            asset_url = "NULL"
            file_size = "NULL"
            file_unit = "NULL"
            num_recs = "NULL"
        else:
            asset_url, file_size, file_unit, num_recs = fetch_page_data(pageurl)

        output = [title, owner, pageurl, asset_url, create_date, "NULL", file_size, file_unit, data_type, num_recs,
                  "NULL", "NULL", nls_license, "NULL", ]
        data.append(output)

    csv_output(header, data)
