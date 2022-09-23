# Packages: beautifulsoup4, csv, requests, math
import requests
import csv
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
    # print(dict_of_links)
    keys_to_skip = ["--- Select Year ---", "Statistics archive", "Related", "Derived Grades 2003"]
    [dict_of_links.pop(d) for d in keys_to_skip]
    # print(dict_of_links)

    return dict_of_links


def fetch_year_page(link: str) -> BeautifulSoup:
    """
    Fetches the content of pages of available years.

    Returns:
        BeautifulSoup object of the pages.
    """
    req = requests.get(link, get_headers())
    return BeautifulSoup(req.content, "html.parser")


def fetch_datasets(page: BeautifulSoup) -> list:
    """
    Fetches the datasets present on a page.

    Returns:
        list_of_lists_of_datasets (List): A list of datasets present on the specific page.
    """
    list_of_lists_of_datasets = []
    # h1_headline = page.h1.descendants
    # print(h1_headline)
    # unsorted_lists = h1_headline.find_all("ul")
    content = page.find(id="content")
    # print(len(content), content)
    unsorted_lists = content.find_all("ul")
    for unsorted_list in unsorted_lists:
        # print("unsorted_list ", unsorted_list)
        list_of_datasets = unsorted_list.find_all("a")
        list_of_lists_of_datasets.append(list_of_datasets)
    # print("list_of_datasets ", list_of_lists_of_datasets)

    return list_of_lists_of_datasets


def create_title(part1: str, part2: BeautifulSoup) -> str:
    """
    Combines the two inputs into the title of the dataset

    Returns:
        stripped_title (str): A string of dataset's title.
    """
    title_string1 = year + " " + dataset.get_text()
    stripped_title = title_string1.split(" ", 1)[1]
    return stripped_title


def fetch_asset_url(page: BeautifulSoup) -> str:
    """
    Fetches the asset url of the dataset from the BeautifulSoup object.

    Returns:
        url (str): A string of dataset's asset url.
    """
    link = page.get("href")
    if link.startswith("//"):
        url = "https:" + link
    elif link.startswith("files"):
        url = "https://www.sqa.org.uk/sqa/" + link
    elif link.startswith("/sqa"):
        url = "https://www.sqa.org.uk" + link
    else:
        url = link

    return url


def fetch_create_date(page: BeautifulSoup, ul: str) -> str:
    """
    Fetches the create date of the dataset from the BeautifulSoup object.

    Returns:
        date (str): A string of dataset's create date.
    """

    # get the a-tag, which contains the , retrieve xpath (required?), and navigate down the siblings and check for each sibling,
    # if it contains "Date of publication":
    #   return that date
    # elif is <h2>:
    #   return "NULL"

    part = page.find("a", string=ul.get_text())
    # print("part", part, type(part), part.parent.parent.parent)
    find_ul = part.find_parent("ul")
    # print("1", part, part.find_parent("ul"), part.parent.parent.parent)
    # print("2", part, part.find_parents("ul"), part.parent)
    find_siblings = find_ul.next_siblings
    for sibling in find_siblings:
        if "<h2>" in repr(sibling):
            # print("h2", repr(sibling))
            return "NULL"
        elif "Date of publication" in repr(sibling):
            # print("date", repr(sibling))
            fetched_date = sibling.get_text().split(":")[1].strip(" .")
            if fetched_date.startswith(" "):
                print(fetched_date)
            return fetched_date

    return "NULL"

"""
def fetch_file_size(url: str) -> str:
    myfile = requests.get(url)
    statitnfo = os.stat(myfile)
    print(statinfo.st_size)
    size = statinfo.st_size
    try:
        myfile = requests.get(url)
        statinfo = os.stat(myfile)
        print(statinfo.st_size)
        size = statinfo.st_size
    except:
        size = "1"
    return size


def fetch_num_recs(url: str) -> str:
    try:
        loc = (url)  # Giving the location of the file

        wb = xl.open_workbook(loc)  # opening & reading the excel file
        s1 = wb.sheet_by_index(0)  # extracting the worksheet
        s1.cell_value(0, 0)  # initializing cell from the excel file mentioned through the cell position

        print("No. of rows:", s1.nrows)  # Counting & Printing thenumber of rows & columns respectively
        return s1.nrows
    except:
        return "2"
"""


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

    print("Getting available years")
    category_links = fetch_available_years()
    for year in category_links.keys():
        print("Getting", year)
        years_page = fetch_year_page(category_links[year])
        owner = "Scottish Qualifications Authority (SQA)"
        pageurl = category_links[year]
        list_datasets = fetch_datasets(years_page)
        for list in list_datasets[:-3]:
            # print("list", list)
            for dataset in list:
                print("dataset", dataset)
                title = create_title(year, dataset)
                print("title", title)
                asset_url = fetch_asset_url(dataset)
                create_date = fetch_create_date(years_page, dataset)
                file_size = "NULL"
                # file_size = fetch_file_size(asset_url) #function does not work, unless file is saved locally, size retrieved and then deleted
                file_unit = "NULL"
                data_type = dataset.get("href").split(".")[1]
                # print(data_type)
                num_recs = "NULL"
                # num_recs = fetch_num_recs(asset_url) #function does not work, unless file is saved locally, num_recs retrieved and then deleted
                sqa_licence = "unknown" # contact SQA regarding license

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
                    sqa_licence,
                    "NULL",
                ]
                data.append(output)

    print("Outputting to CSV")
    csv_output(header, data)


"""
issues with this scraper:
- year before 2000 don't return a dataset, even though there are unordered lists present"
- in many (all?) years, the last datasets seem to be missing
"""

