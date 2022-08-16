import filecmp
import os
import re
import csv
import pytest
from .conftest import csv_checker
from ..dcat import ProcessorDCAT

test_proc = ProcessorDCAT()


def test_get_datasets():
    owner = "test_owner"
    outputdir = "tests/mock_data/output/dcat/"
    start_url = "file:///" + os.path.abspath("tests/mock_data/dcat/glasgow.json")
    fname = outputdir + "glasgow.csv"
    expected_fname = "tests/mock_data/dcat/expected/glasgow.csv"
    if os.path.exists(fname):
        os.remove(fname)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    test_proc.get_datasets(owner, start_url, fname)
    with open(fname, "r", newline="") as check_file:
        csv_check_file = csv.reader(check_file)
        assert csv_checker(csv_check_file)
    assert filecmp.cmp(fname, expected_fname)
