import filecmp
import os
import re
import csv
import pytest
from .csv_validator import csv_checker
from ..usmart import ProcessorUSMART

test_proc = ProcessorUSMART()


def test_get_datasets():
    owner = "test_owner"
    start_url = "file:///" + os.path.abspath(
        "test/mock_data/usmart/dumfries and galloway.json"
    )
    fname = "test/mock_data/output/usmart/dumfries and galloway.csv"
    expected_fname = "test/mock_data/usmart/expected/dumfries and galloway.csv"
    if os.path.exists(fname):
        os.remove(fname)
    test_proc.get_datasets(owner, start_url, fname)
    with open(fname, "r", newline="") as check_file:
        csv_check_file = csv.reader(check_file)
        assert csv_checker(csv_check_file)
    assert filecmp.cmp(fname, expected_fname)
