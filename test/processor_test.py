"""tests processor.py
"""
import os
import pytest
from ..processor import Processor


class ValidMockProcessor(Processor):
    """This class represents a super class of processor
    it must contain the function get_datasets to be valid
    """

    def __init__(self):
        super().__init__(type="test")

    def get_datasets(self, owner, url, fname):
        return "getting data"


def test_get_urls():
    """test we can read urls based on type
    currently a rubbish test as we can't spoof the csv were the urls are kept
    """
    mock_processor = ValidMockProcessor()
    mock_processor.get_urls()
    expected_urls = {}
    assert mock_processor.urls == expected_urls


def test_get_json():
    """test we can load local json file (as if it were from a url)"""
    mock_processor = ValidMockProcessor()
    json_data = mock_processor.get_json(
        "file:///" + os.path.abspath("test/mock_data/get_json_data.json")
    )
    assert json_data["test_data"][0]["Title"] == "test_title"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        ),
        (
            "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
            "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
        ),
        (
            "http://opendatacommons.org/licenses/odbl/1-0/",
            "http://opendatacommons.org/licenses/odbl/1-0/",
        ),
        (
            "Open Data Commons Open Database License 1.0",
            "Open Data Commons Open Database License 1.0",
        ),
        ("uk-ogl", "uk-ogl"),
        ("UK Open Government Licence (OGL)", "UK Open Government Licence (OGL)"),
        (
            "Open Government Licence 3.0 (United Kingdom)",
            "Open Government Licence 3.0 (United Kingdom)",
        ),
        ("OGL3", "OGL3"),
        (
            "https://creativecommons.org/licenses/by/4.0/legalcode",
            "https://creativecommons.org/licenses/by/4.0/legalcode",
        ),
        ("Creative Commons Attribution 4.0", "Creative Commons Attribution 4.0"),
        (
            "https://creativecommons.org/licenses/by-sa/3.0/",
            "https://creativecommons.org/licenses/by-sa/3.0/",
        ),
        ("invalid_licence", ""),
        ("OGL3 is my licence", "OGL3"),
        ("we use uk-ogl as our my licence", "uk-ogl"),
    ],
)
def test_get_licence_text(test_input, expected):
    """test licence can be picked out from text"""
    mock_processor = ValidMockProcessor()
    dataset = {"attributes": {"structuredLicense": {"text": ""}}}
    dataset["attributes"]["structuredLicense"]["text"] = test_input
    assert mock_processor.get_license(dataset) == expected


@pytest.mark.parametrize(
    "test_input",
    [
        "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "OGL3",
        "invalid_licence",
    ],
)
def test_get_licence_link(test_input):
    """test licence can be picked out from link"""
    mock_processor = ValidMockProcessor()
    dataset = {"attributes": {"structuredLicense": {"text": "", "url": "test_url"}}}
    dataset["attributes"]["structuredLicense"]["text"] = test_input
    assert mock_processor.get_license(dataset) == "test_url"


def test_get_datasets():
    """test the get_datasets function has been properly attached"""
    mock_processor = ValidMockProcessor()
    name = "test_name"
    url = "test_url"
    fname = "test_file"
    assert mock_processor.get_datasets(name, url, fname) == "getting data"
