import filecmp
import os
from os.path import isfile, join
import csv
import pytest
from .conftest import csv_checker
from ..dcat import ProcessorDCAT

test_proc = ProcessorDCAT()


def list_sources(dir):
    sources_path = os.path.abspath(dir)
    sources = [
        f.split(".")[0]
        for f in os.listdir(sources_path)
        if isfile(join(sources_path, f))
    ]
    return sources


@pytest.mark.parametrize("sources", list_sources("tests/mock_data/dcat"))
def test_get_datasets(sources):
    owner = "test_owner"
    outputdir = "tests/mock_data/output/dcat/"
    start_url = "file:///" + os.path.abspath(
        "tests/mock_data/dcat/" + sources + ".json"
    )
    fname = outputdir + sources + ".csv"
    expected_fname = "tests/mock_data/dcat/expected/" + sources + ".csv"
    if os.path.exists(fname):
        os.remove(fname)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    test_proc.get_datasets(owner, start_url, fname)
    with open(fname, "r", newline="", encoding="utf-8") as check_file:
        csv_check_file = csv.reader(check_file)
        assert csv_checker(csv_check_file)
    assert filecmp.cmp(fname, expected_fname)
