import filecmp
import os
import re
import csv
import pytest
from .conftest import csv_checker
from ..usmart import ProcessorUSMART

test_proc = ProcessorUSMART()


def test_get_datasets():
    owner = "test_owner"
    outputdir = "tests/mock_data/output/usmart/"
    start_url = "file:///" + os.path.abspath(
        "tests/mock_data/usmart/Dumfries and Galloway Council.json"
    )
    fname = outputdir + "Dumfries and Galloway Council.csv"
    expected_fname = "tests/mock_data/usmart/expected/Dumfries and Galloway Council.csv"
    if os.path.exists(fname):
        os.remove(fname)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    test_proc.get_datasets(owner, start_url, fname)
    with open(fname, "r", newline="", encoding="utf-8") as check_file:
        csv_check_file = csv.reader(check_file)
        assert csv_checker(csv_check_file)
    assert filecmp.cmp(fname, expected_fname)
