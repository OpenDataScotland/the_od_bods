"""Generates new Mock and Expected Test data based on current code
to run navigate to root directory and run `python -m tests.generate_new_mock_data`
"""
from urllib import request
import csv
import json
import os

from usmart import ProcessorUSMART
from dcat import ProcessorDCAT
from arcgis import ProcessorARCGIS


def get_urls():
    urls_list = {}
    with open("sources.csv", "r", encoding="utf-8") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            urls_list[row["Name"]] = {
                "url": row["Source URL"],
                "type": row["Processor"],
            }
    return urls_list


def get_json(url):
    req = request.Request(url)
    return json.loads(request.urlopen(req).read().decode())


def save_json(data, location):
    with open(location, "w+", newline="", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def test_get_datasets(name, type):
    match (type):
        case "USMART":
            test_proc = ProcessorUSMART()
        case "dcat":
            test_proc = ProcessorDCAT()
        case "arcgis":
            test_proc = ProcessorARCGIS()
        case "ckan":
            # no python parser implemented
            return ()
    owner = "test_owner"
    outputdir = "tests/mock_data/" + type + "/expected/"
    start_url = "file:///" + os.path.abspath(
        "tests/mock_data/" + type + "/" + name + ".json"
    )
    fname = outputdir + name + ".csv"
    if os.path.exists(fname):
        os.remove(fname)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    test_proc.get_datasets(owner, start_url, fname)


def main():
    url_list = get_urls()

    for name in url_list:
        print(f"-> {name} | {url_list[name]['type']} | {url_list[name]['url']}")
        if url_list[name]["type"] != "ckan":
            location = (
                "tests\\mock_data\\" + url_list[name]["type"] + "\\" + name + ".json"
            )
            json_data = get_json(url_list[name]["url"])
            if url_list[name]["type"] == "arcgis":
                if "next" in json_data["meta"] and json_data["meta"]["next"]:
                    del json_data["meta"]["next"]  # avoids link list urls
            save_json(json_data, location)
            test_get_datasets(name, url_list[name]["type"])


if __name__ == "__main__":
    user_response = (False, True)[
        input(
            "This will replace all test data, are you sure you want to continue? Y/n\n"
        )
        == "Y"
    ]
    if user_response:
        main()
