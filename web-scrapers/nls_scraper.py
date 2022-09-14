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

    with open("../data/scraped-results/output_nls.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for record in data:
            writer.writerow(record)


def fetch_category_links():
    """
    Fetches links to data category pages from ODR_URL. It uses the dropdown menu on the 'Data' button.

    Returns:
        list_of_links (List): A list of URLs linking to the pages for each data category.
    """
    initial_req = requests.get(ODR_URL, get_headers())
    initial_soup = BeautifulSoup(initial_req.text, "html.parser")
    data_button = initial_soup.find("li", id="menu-item-41")
    dropdown_list = data_button.find_all("li")

    list_of_links = [
        dropdown_item.find("a").get("href") for dropdown_item in dropdown_list
    ]

    """
    list_of_links = []
    for dropdown_item in dropdown_list:
        a_tag = dropdown_item.find("a")
        link = a_tag.get("href")
        list_of_links.append(link)
    """

    # print(list_of_links) # for logging and debugging
    return list_of_links


def fetch_data_page_urls(url: str) -> list:
    """
    Fetches page urls for datasets in each data category.

    Args:
        url (str): A URL for the category the dataset is in.
    Returns:
        data_page_urls (List): A list of URLs linking to the parent pages for the datasets.
    """
    req = requests.get(url, get_headers())  # opens page for each data category
    soup = BeautifulSoup(req.content, "html.parser")

    data_page_urls = []
    captions = soup.select("figcaption")
    # print(captions) # for debugging
    for caption in captions:
        # print(caption) # for debugging
        for tag in caption.find_all("a"):
            data_page_urls.append(tag.get("href"))

    # print(data_page_urls) # for logging and debugging
    return data_page_urls


def fetch_title(page: BeautifulSoup) -> str:
    """
    Fetches title/name of the specific dataset.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        dataset_title (str): A name of the dataset.
    """
    dataset_title = page.find("h1", class_="hestia-title").text
    return dataset_title


def fetch_asset_urls(page: BeautifulSoup) -> list:
    """
    Fetches urls to the data files of the specific dataset.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        list_of_asseturls (list): A list of urls to the data files of the specific dataset.
    """
    asseturl = "NULL"

    buttons = page.find_all("a", class_="wp-block-button__link no-border-radius")
    if not buttons:  # Because one collection's page uses a different button class
        buttons = page.find("div", class_="wp-block-button is-style-fill")
        if buttons is None:
            buttons = page.find_all("a", class_="wp-block-button__link")
        else:
            buttons = buttons.find_all("a", class_="wp-block-button__link")

    list_of_asseturls = []

    for button in buttons:
        if str(button.contents[0]).lower().__contains__("download"):
            asseturl = button["href"]
            if asseturl[:10] == "/download/":  # Make relative URLs absolute
                asseturl = "https://data.nls.uk" + asseturl
            list_of_asseturls.append(asseturl)

    return list_of_asseturls


def fetch_create_date(page: BeautifulSoup) -> str:
    """
    Fetches the publication date of the specific dataset.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        date (str): A publication date.
    """
    publication = page.find(string=re.compile("Publication"))
    if not publication == None:
        date = publication.split(" ")[2]
    else:
        date = "NULL"
    return date


def fetch_file_size(page: BeautifulSoup) -> list:
    """
    Fetches the file size and size unit of the specific dataset.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        list_of_filesizes (list): A list of lists, each containing the file size and the file size unit.
    """
    filesize = "NULL"
    sizeunit = "NULL"
    file_contents = ""
    size_data = ""
    list_of_filesizes = []

    filesize_strings = page.find_all(string=re.compile("File size"))
    for filesize_string in filesize_strings:
        # print(filesize_string, type(filesize_string))
        filesize = filesize_string.split(":")[1].strip().split(" ")[0:2]
        if filesize == ['']:
            filesize = []
            filesize.append(filesize_string.next.next)
            filesize.append(filesize_string.next.next.next.strip(" ").split(" ")[0])

        list_of_filesizes.append(filesize)
    if list_of_filesizes == []:
        list_of_filesizes.append("unknown")

    # print("list_of_filesizes", list_of_filesizes)

    """
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
    """
    return list_of_filesizes

def fetch_num_recs(page: BeautifulSoup) -> list:
    """
    Fetches the number of files of the specific dataset.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        amount_recs (int): A number of files in the dataset.
    """
    list_num_recs = []
    content = page.find_all(string=re.compile("File content"))
    # print(content)
    for rec in content:
        amount = 0
        amount_recs = 0
        if not rec == None:
            parts = rec.split(":")
            files = parts[1].split(";")

            for item in files:
                break_up = item.strip().split(" ")
                # print("break_up", item, ", ", break_up, ", ", break_up[0].replace(",", "").replace(".", ""))
                amount = int(break_up[0].replace(",", "").replace(".", ""))
                amount_recs += amount
        list_num_recs.append(amount_recs)
    if list_num_recs == []:
        list_num_recs.append("unknown")
    # print(list_num_recs)

    return list_num_recs


def fetch_data_types(page: BeautifulSoup) -> str:
    """
    Fetches the data types of the specific dataset.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        string_of_types (str): A string of file types present in the dataset.
    """
    list_of_types = []
    string_of_types = ""
    content = page.find(string=re.compile("File content"))
    if not content == None:
        parts = content.split(":")
        files = parts[1].split(";")

        for item in files:
            break_up = item.split(" ")
            # print("break_up", break_up)
            file_type = break_up[2:]
            # print("file_type", file_type)
            lowercase_file_types = []
            for item in file_type:
                lowercase_file_type = item.lower().strip(".()")
                lowercase_file_types.append(lowercase_file_type)
            # print("lowercase_file_types", lowercase_file_types)
            list_of_types.append(lowercase_file_types)
            list_of_types = list(
                set(list_of_types)
            )  # make it a list, where each file type is listed just once
            string1 = ", "
            string_of_types = string1.join(list_of_types) # convert list to a string, since python treats "[..]" as string
            # when reading from csv files

    return string_of_types


def fetch_licences(page: BeautifulSoup) -> str:
    """
    Fetches the licences, under which the specific dataset is published.

    Args:
        page (BeautifulSoup object): A BeautifulSoup object for the specific dataset.
    Returns:
        str: A string of licences.
    """
    if not (figures := page.find_all("figure", class_="wp-block-image is-resized")):
        if not (
            figures := page.find_all(
                "figure", class_="wp-block-image size-medium is-resized"
            )
        ):
            if not (
                figures := page.find_all(
                    "figure", class_="wp-block-image size-large is-resized"
                )
            ):
                return []
    return [f.find("a").get("href") for f in figures][0]
    # useful in case we want to treat the case of multiple licences per dataset:
    # list_of_licences = [f.find("a").get("href") for f in figures]
    # return ', '.join(str(licence) for licence in list_of_licences)


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
    category_match = {
        "Digitised material collection": "digitised-collections",
        "Metadata collection": "metadata-collections",
        "Spatial data": "map-spatial-data",
        "Organisational data": "organisational-data",
    }  # this code is probably not required anymore, since
    # category_match only served to assemble the data_page_url. But I kept it for the time being, in case we want to
    # include this in the output_csv.

    print("Getting data categories")
    category_links = fetch_category_links()

    print("Getting data page URLs")
    for category_link in category_links:
        url_list = fetch_data_page_urls(category_link)
        print("Getting data")
        for url in url_list:
            print("Getting " + url)
            req = requests.get(url, get_headers())
            soup = BeautifulSoup(req.content, "html.parser")
            list_of_asset_urls = fetch_asset_urls(soup)
            fetched_file_size = fetch_file_size(soup)
            fetched_num_recs = fetch_num_recs(soup)
            counter = 0
            for asseturl in list_of_asset_urls:
                title = fetch_title(soup)
                # print("title:", title)
                owner = "National Library of Scotland"
                pageurl = url
                # print("pageurl:", pageurl)
                asset_url = asseturl
                #print("asset_url:", asset_url)
                create_date = fetch_create_date(soup)
                # print("create_date:", create_date)
                if fetched_file_size != ["unknown"]:
                    file_size = fetched_file_size[counter][0]
                    file_unit = fetched_file_size[counter][1]
                else:
                    file_size = "unknown"
                    file_unit = "unknown"

                # print("file_size:", file_size)
                # print("file_unit:", file_unit)
                ### fetch_data_types is more accurate & useful, but file extension is consistent with other listings
                data_type = asset_url.rsplit('.',1)[1] #fetch_data_types(soup)
                # print("data_type:", data_type)
                num_recs = fetched_num_recs[counter]
                # print(("num_recs:", num_recs))
                nls_licence = fetch_licences(soup)
                # print("nls_licence:", nls_licence)

                output = [
                    title,
                    owner,
                    pageurl,
                    asset_url,
                    create_date,
                    "NULL",
                    file_size,
                    file_unit,
                    data_type,
                    num_recs,
                    "NULL",
                    "NULL",
                    nls_licence,
                    "NULL",
                ]
                data.append(output)
                counter += 1

    print("Outputting to CSV")
    csv_output(header, data)


"""
still to do:
- 
issues with this scraper:
- if publication date present on webpage, then only year. In the csv it is the complete date
- for two data sets, the file types are not listed the same way as the other pages. Needs to be addressed, if possible
"""
