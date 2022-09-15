# Packages: beautifulsoup4, csv, requests, math
import requests
import csv
import re
from bs4 import BeautifulSoup

# Global Variables
ODR_URL = "https://www.sqa.org.uk/sqa/57523.html"


def get_headers():
    """
    Gets headers to make a request from the URL. Optimized so website doesn't think a bot is making a request.

    Args:
        NULL

    Returns:
        headers (Dictionary) : header values
    """
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
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

    with open("../data/scraped-results/output_sqa.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for record in data:
            writer.writerow(record)


def fetch_available_years():
    """
    Fetches links to pages of available years from ODR_URL. It uses the dropdown menu on the 'Data' button.

    Returns:
        list_of_links (List): A list of URLs linking to the pages for each data category.
    """
    dict_of_links = {}
    initial_req = requests.get(ODR_URL, get_headers())
    initial_soup = BeautifulSoup(initial_req.text, "html.parser")
    data_button = initial_soup.find("select", id="selYear")
    dropdown_list = data_button.find_all("option")

    for dropdown_item in dropdown_list:
        # print("dropdown item", dropdown_item, type(dropdown_item), dropdown_item["value"])
        dict_of_links[dropdown_item.contents[0]] = "https://www.sqa.org.uk/sqa/" + dropdown_item["value"]
    print(dict_of_links)
    keys_to_skip = ["--- Select Year ---", "Statistics archive"]
    [dict_of_links.pop(d) for d in keys_to_skip]
    print(dict_of_links)

    return dict_of_links


if __name__ == "__main__":
    # Record Headings
    header = [
        "Title",
        "Owner",
        "PageURL",
        "AssetURL",
        "DateCreated",
        "DateUpdated",
        "FileSize",
        "FileSizeUnit",
        "FileType",
        "NumRecords",
        "OriginalTags",
        "ManualTags",
        "License",
        "Description",
    ]
    data = []

    print("Getting data available years")
    category_links = fetch_available_years()
