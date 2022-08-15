import filecmp
import os
import re
import csv
import pytest
from .conftest import csv_checker
from ..arcgis import ProcessorARCGIS

test_proc = ProcessorARCGIS()


def test_get_datasets():
    owner = "test_owner"
    start_url = "file:///" + os.path.abspath("test/mock_data/arcgis/renfrew.json")
    fname = "test/mock_data/output/arcgis/renfrew.csv"
    expected_fname = "test/mock_data/arcgis/expected/renfrew.csv"
    if os.path.exists(fname):
        os.remove(fname)
    test_proc.get_datasets(owner, start_url, fname)
    with open(fname, "r", newline="") as check_file:
        csv_check_file = csv.reader(check_file)
        assert csv_checker(csv_check_file)
    assert filecmp.cmp(fname, expected_fname)
