from wsgiref.validate import validator
import validators
import os
import dateutil.parser
import re
import csv
import pytest
from ..dcat import ProcessorDCAT

test_proc = ProcessorDCAT()


def test_get_datasets():
    owner = "test_owner"
    start_url = "file:///" + os.path.abspath("test/mock_data/dcat/glasgow.json")
    fname = "test/mock_data/output/dcat/glasgow.csv"
    if os.path.exists(fname):
        os.remove(fname)
    test_proc.get_datasets(owner, start_url, fname)
    with open(fname, "r", newline="") as check_file:
        csv_check_file = csv.reader(check_file)
        assert csv_checker(csv_check_file)


def is_valid_string(str_to_check):
    return isinstance(str_to_check, str)


def is_valid_date(date_to_check):
    if date_to_check:
        try:
            dateutil.parser.isoparse(date_to_check)
        except ValueError:
            return False
    return True


def is_valid_number(str_to_check):
    if str_to_check:
        return isinstance(str_to_check, float)
    return True


def is_valid_file_size_unit(str_to_check):
    file_size_units = [
        "",  # blank
        "B",  # Bytes
        "kB",
        "MB",
        "GB",
        "TB",
        "PB",
        "EB",
        "ZB",
        "YB",
        "b",  # bits
        "kb",
        "Mb",
        "Gb",
        "Tb",
        "Pb",
        "Eb",
        "Zb",
        "Yb",
    ]
    return str_to_check in file_size_units


def is_valid_file_type(str_to_check):
    return is_valid_string(str_to_check)


def is_valid_tags(str_to_check):
    return is_valid_string(str_to_check)


def is_valid_licence(str_to_check):
    licences = [
        "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
        "http://opendatacommons.org/licenses/odbl/1-0/",
        "Open Data Commons Open Database License 1.0",
        "uk-ogl",
        "UK Open Government Licence (OGL)",
        "Open Government Licence 3.0 (United Kingdom)",
        "OGL3",
        "https://creativecommons.org/licenses/by/4.0/legalcode",
        "Creative Commons Attribution 4.0",
        "https://creativecommons.org/licenses/by-sa/3.0/",
        "",
    ]
    return str_to_check in licences


def is_valid_url(url_to_check):
    if url_to_check:
        return validators.url(url_to_check)
    return True


def csv_checker(csv_file):
    result = True
    csv_testers = [
        {"title": "Title", "test_func": is_valid_string},
        {"title": "Owner", "test_func": is_valid_string},
        {"title": "PageURL", "test_func": is_valid_url},
        {"title": "AssetURL", "test_func": is_valid_url},
        {"title": "DateCreated", "test_func": is_valid_date},
        {"title": "DateUpdated", "test_func": is_valid_date},
        {"title": "FileSize", "test_func": is_valid_number},
        {"title": "FileSizeUnit", "test_func": is_valid_file_size_unit},
        {"title": "FileType", "test_func": is_valid_file_type},
        {"title": "NumRecords", "test_func": is_valid_number},
        {"title": "OriginalTags", "test_func": is_valid_tags},
        {"title": "ManualTags", "test_func": is_valid_tags},
        {"title": "License", "test_func": is_valid_licence},
        {"title": "Description", "test_func": is_valid_string},
    ]
    header_row = 0
    for row_idx, row in enumerate(csv_file):
        if row_idx != 0:
            for col_idx, cell in enumerate(row):
                assert csv_testers[col_idx]["test_func"](cell)
                # result = False
    return result
