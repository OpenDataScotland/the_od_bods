# Packages: beautifulsoup4, csv, requests, math
import requests
import csv
import re
from bs4 import BeautifulSoup

# Global Variables
ODR_URL = "https://data.nls.uk/"


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


def fetch_category_links():
    """
        Fetches links to data category pages from ODR_URL.

        Returns:
            list_of_links (List): A list of URLs linking to the pages for each data category.
        """
    list_of_links = []
    initial_req = requests.get(ODR_URL, get_headers())
    initial_soup = BeautifulSoup(initial_req.text, "html.parser")
    data_button = initial_soup.find("li", id="menu-item-41")
    dropdown_list = data_button.find_all("li")

    for dropdown_item in dropdown_list:
        a_tag = dropdown_item.find("a")
        link = a_tag.get("href")
        list_of_links.append(link)

    print(list_of_links)
    return list_of_links



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


def fetch_data_page_urls(url: str) -> str:
    """
    Fetches page url for dataset.

    Args:
        title (str): The title of the dataset, from the ODR.
        url (str): A URL for the category the dataset is in.
    Returns:
        pageurl (str): A URL linking to the parent page for the dataset.
    """
    req = requests.get(url, get_headers())  # opens page for each data category
    soup = BeautifulSoup(req.content, "html.parser")

    data_page_urls = []
    captions = soup.select("figcaption")
    # print(captions) # debugging help
    for caption in captions:
        # print(caption) # debugging help
        for tag in caption.find_all("a"):
            data_page_urls.append(tag.get("href"))
    print(data_page_urls)

    return data_page_urls


def fetch_title(page):
    dataset_title = page.find("h1", class_="hestia-title").text
    return dataset_title


def fetch_asset_url(page):
    #print("asset_url", page)
    possible_button_text = ["Download full dataset", "Download the dataset", "Download the data", ]

    buttons = page.find_all("a", class_="wp-block-button__link no-border-radius")
    if not buttons:  # Because one collection's page uses a different button class
        buttons = page.find("div", class_="wp-block-button is-style-fill")
        buttons = buttons.find_all("a", class_="wp-block-button__link")

    for button in buttons:
        if str(button.contents[0]) in possible_button_text:
            asseturl = button["href"]

    if asseturl[:10] == "/download/":  # Make relative URLs absolute
        asseturl = "https://data.nls.uk" + asseturl

    return asseturl


def fetch_create_date(page):
    publication = page.find(string=re.compile("Publication"))
    date = publication.split(" ")[2]
    return date


def fetch_file_size(page):
    filesize = "NULL"
    sizeunit = "NULL"
    file_contents = ""
    size_data = ""

    headlines = page.find_all("h4")
    for headline in headlines:
        if "All the data" in headline.contents[0]:
            file_contents = headline.find_next("p").contents[0]
            size_data = headline.find_next("strong").contents[0]
            if size_data == "File size: ":
                filesize = headline.find_next("strong").find("strong").contents[0]
                sizeunit = headline.find_next("strong").contents[2][:2]
                size_data = ""

    if not file_contents:
        headlines = page.find_all("h3")
        for headline in headlines:
            if "All the data" in headline.contents[0]:
                file_contents = headline.find_next("p").contents[0]
                if file_contents[:4] != "File":
                    file_contents = "NULL"
                    break
                size_data = headline.find_next("strong").contents[0]

    if not file_contents:
        headlines = page.find_all("h3")
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

    return filesize, sizeunit


def fetch_data_type(page):
    list_of_types = []
    content = page.find(string=re.compile("File content"))
    parts = content.split(":")
    files = parts[1].split(";")
    for item in files:
        break_up = item.split(" ")
        file_type = break_up[2]
        amount_recs += amount

    print("parts:", amount_recs, list_of_types)
    return amount_recs, list_of_types


def fetch_num_recs_and_data_types(page):
    amount_recs = 0
    list_of_types = []
    content = page.find(string=re.compile("File content"))
    parts = content.split(":")
    files = parts[1].split(";")

    for item in files:
        break_up = item.split(" ")
        amount = int(break_up[1])
        file_type = break_up[2]
        #print(amount, file_type)
        amount_recs += amount
        list_of_types.append(file_type)

    return list_of_types, amount_recs


def fetch_licenses(page):
    list_of_licenses = []
    figures = page.find_all("figure", class_="wp-block-image is-resized")

    for figure in figures:
        license = figure.find("img").get("alt")
        #print("license:", license)
        list_of_licenses.append(license)

    return list_of_licenses


"""
add explanatory comments to all functions (see original file)

resolve British Army Lists conflict below, maybe same way as in licenses (returning a list, instead of single value)

"""


if __name__ == "__main__":
    # Record Headings
    header = ["Title", "Owner", "PageURL", "AssetURL", "DateCreated", "DateUpdated", "FileSize", "FileSizeUnit",
              "FileType", "NumRecords", "OriginalTags", "ManualTags", "License", "Description", ]
    data = []
    category_match = {"Digitised material collection": "digitised-collections",
                      "Metadata collection": "metadata-collections",
                      "Spatial data": "map-spatial-data",
                      "Organisational data": "organisational-data"}

    print("Getting data categories")
    category_links = fetch_category_links()

    print("Getting data page URLs")
    for category_link in category_links:
        url_list = fetch_data_page_urls(category_link)
        print("Getting data")
        for url in url_list:
            req = requests.get(url, get_headers())
            soup = BeautifulSoup(req.content, "html.parser")
            title = fetch_title(soup)
            print("title:", title)
            owner = "National Library of Scotland"
            pageurl = category_link
            print("pageurl:", pageurl)
            asset_url = fetch_asset_url(soup)
            print("asset_url:", asset_url)
            create_date = fetch_create_date(soup)
            print("create_date:", create_date)
            file_size, file_unit = fetch_file_size(soup)
            print("file_size:", file_size)
            print("file_unit:", file_unit)
            data_type, num_recs = fetch_num_recs_and_data_types(soup)
            print("data_type:", data_type)
            print(("num_recs:", num_recs))
            nls_license = fetch_licenses(soup)
            print("nls_license:", nls_license)

            """if title == "British Army Lists":  # Contains 4 separate download links: temporarily nulled to prevent conflicts
                asset_url = "NULL"
                file_size = "NULL"
                file_unit = "NULL"
                num_recs = "NULL"
            else:"""

            output = [title, owner, pageurl, asset_url, create_date, "NULL", file_size, file_unit, data_type, num_recs,
                      "NULL", "NULL", nls_license, "NULL", ]
            data.append(output)


    print("Outputting to CSV")
    csv_output(header, data)
