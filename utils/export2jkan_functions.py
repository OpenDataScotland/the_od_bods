from dataclasses import dataclass
from typing import List


# TODO: This should be moved to a separate module to be used as a standardised class
@dataclass
class DataFile:
    """
    A class to represent a data file with its associated metadata.

    Attributes:
        url (str): The URL where the data file is located.
        size (float): The size of the data file.
        size_unit (str): The unit of measurement for the file size (e.g., MB, GB).
        file_type (str): The type of the data file (e.g., CSV, JSON).
        file_name (str): The name of the data file.
        show_name (str): The display name of the data file.
    """

    url: str
    size: float
    size_unit: str
    file_type: str
    file_name: str
    show_name: str


# TODO: This should be moved to a separate module to be used as a standardised class
@dataclass
class Dataset:
    """
    A class to represent a dataset with its associated metadata.

    Attributes:
        title (str): The title of the dataset.
        owner (str): The owner of the dataset.
        page_url (str): The URL of the dataset's page.
        date_created (str): The creation date of the dataset.
        date_updated (str): The last updated date of the dataset.
        ods_categories (List[str]): The categories of the dataset in the ODS system.
        license (str): The license under which the dataset is released.
        description (str): A description of the dataset.
        num_records (int): The number of records in the dataset.
        files (List[DataFile]): A list of data files associated with the dataset.
    """

    title: str
    owner: str
    page_url: str
    date_created: str
    date_updated: str
    ods_categories: List[str]
    license: str
    description: str
    num_records: int
    files: List[DataFile]


def strip_date_from_iso8601(dataframe, date_columns):
    """
    Strips the date from ISO 8601 formatted datetime strings in specified columns of a DataFrame.
    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the columns to be processed.
        date_columns (list of str): A list of column names in the DataFrame to process.
    Returns:
        None: The function modifies the DataFrame in place.
    """

    for col in date_columns:
        dataframe[col] = dataframe[col].str.split("T").str[0]


# TODO: This really isn't a great way to pull fields now that we're using JSON. We should probably just use the field names directly.
def find_field_index(field_name):
    """
    Returns the index of the given field name in a predefined list of field names.
    Args:
        name (str): The name of the field to find the index for.
    Returns:
        int: The index of the field name in the list.
    Raises:
        ValueError: If the field name is not found in the list.
    """

    field_names = [
        "Title",
        "Owner",
        "PageURL",
        "AssetURL",
        "FileName",
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
        "Source",
        "AssetStatus",
        "ODSCategories",
        "ODSCategories_Keywords",
    ]
    return field_names.index(field_name)


def split_tags(tags):
    """
    Splits a string of tags separated by semicolons into a list of individual tags.
    Args:
        tags (str): A string containing tags separated by semicolons. If an empty string or a non-string type is provided, an empty list is returned.
    Returns:
        list: A list of individual tags. If the input is an empty string or a non-string type, an empty list is returned.
    """

    if type(tags) == str:
        if tags == "":
            return []
        return tags.split(";")
    else:
        return []


def safe_parse_int(potential_integer):
    """
    Safely parses a value to an integer.
    This function attempts to convert the given value to an integer.
    If the conversion fails, it tries to convert the value to a float first and then to an integer.
    If both conversions fail, it returns None.
    Args:
        val: The value to be converted to an integer. It can be of any type that can be cast to an int or float.
    Returns:
        int: The integer representation of the value if conversion is successful.
        None: If the conversion fails.
    """

    try:
        return int(potential_integer)
    except:
        pass
    try:
        return int(float(potential_integer))
    except:
        pass
    return None


# TODO: We should probably pull a live copy of licenses from licenses.yml
# https://github.com/OpenDataScotland/jkan/blob/gh-pages/_data/licenses.yml
def get_licence_url(licence_name):
    """
    Retrieve the URL for a given licence name.
    This function takes a licence name as input and returns the corresponding URL
    if the licence name is known. If the licence name is not recognized, it logs
    the unknown licence and returns the input licence name.
    Args:
        licence_name (str): The name of the licence.
    Returns:
        str: The URL of the licence if known, otherwise the input licence name.
    """

    known_licence_links = {
        "Open Government Licence v2.0": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
        "Open Government Licence v3.0": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "Creative Commons Attribution Share-Alike 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
        "Creative Commons Attribution Share-Alike 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
        "Creative Commons Attribution 4.0 International": "https://creativecommons.org/licenses/by/4.0/",
        "Open Data Commons Open Database License 1.0": "https://opendatacommons.org/licenses/odbl/",
        "Creative Commons CC0": "https://creativecommons.org/share-your-work/public-domain/cc0",
        "Non-Commercial Use Only": "https://rightsstatements.org/page/NoC-NC/1.0/",
        "No Known Copyright": "https://rightsstatements.org/vocab/NKC/1.0/",
        "Public Domain": "https://creativecommons.org/publicdomain/mark/1.0/",
        "Scottish Parliament Copyright Policy": "https://www.parliament.scot/about/copyright",
    }

    # Try and get license URL
    if licence_name in known_licence_links:
        return known_licence_links[licence_name]

    # Log unknown licences
    print(f"Unknown license: {licence_name}")

    # Fallback to returning the licence name
    return licence_name
