import pandas as pd
from dataclasses import dataclass
from typing import List
from math import isnan
import markdown
import re
import yaml
import shutil
import os
import urllib
import subprocess


@dataclass
class DataFile:
    url: str
    size: float
    size_unit: str
    file_type: str
    file_name: str
    show_name: str


@dataclass
class Dataset:
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


fulld = pd.read_json("data/merged_output.json", orient="records").fillna("")

### Extraction of date from ISO datetime ISO.
def strip_date_from_iso8601(df_name, col_list):
    for col in col_list:
        df_name[col] = df_name[col].str.split("T").str[0]
    return


strip_date_from_iso8601(fulld, ["DateCreated", "DateUpdated"])


def ind(name):
    f = [
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
    return f.index(name)


def splittags(tags):
    if type(tags) == str:
        if tags == "":
            return []
        return tags.split(";")
    else:
        return []


def makeint(val):
    try:
        return int(val)
    except:
        pass
    try:
        return int(float(val))
    except:
        pass
    return None


def license_link(l):
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

    for key in known_licence_links.keys():
        if l == key:
            return known_licence_links[key]

    unknown_lics = []

    if not l in unknown_lics:
        unknown_lics.append(l)
        # print("Unknown license: ", l)
    return l


def main():
    data = {}
    for r in fulld.values:
        id = str(r[ind("PageURL")]) + r[ind("Title")]
        if id not in data:
            ds = Dataset(
                title=r[ind("Title")],
                owner=r[ind("Owner")],
                page_url=r[ind("PageURL")],
                date_created=r[ind("DateCreated")],
                date_updated=r[ind("DateUpdated")],
                ods_categories=splittags(r[ind("ODSCategories")]),
                license=r[ind("License")],
                description=str(r[ind("Description")]),
                num_records=makeint(r[ind("NumRecords")]),
                files=[],
            )

            # Sort categories to keep consistent when syncing
            ds.ods_categories.sort()

            data[id] = ds
        data[id].files.append(
            DataFile(
                url=r[ind("AssetURL")],
                size=r[ind("FileSize")],
                size_unit=r[ind("FileSizeUnit")],
                file_type=r[ind("FileType")],
                file_name=r[ind("FileName")],
                show_name=r[ind("FileName")]
                if r[ind("FileName")]
                else r[ind("FileType")],
            )
        )

    ### Replace folder by deleting and writing
    print(os.getcwd())
    shutil.rmtree("../jkan/_datasets/")
    os.makedirs("../jkan/_datasets/")
    #print(subprocess.run(['ls', '../jkan/_datasets/'],stdout=subprocess.PIPE))
    #print(subprocess.run(['ls', '../jkan/'],stdout=subprocess.PIPE))

    for n, (k, ds) in enumerate(data.items()):
        y = {"schema": "default"}
        y["title"] = ds.title[0].upper() + ds.title[1:] # Sentence case for presentability
        y["organization"] = ds.owner
        y["notes"] = markdown.markdown(ds.description)
        y["original_dataset_link"] = ds.page_url
        y["resources"] = [
            {"name": d.show_name, "url": d.url, "format": d.file_type}
            for d in ds.files
            if d.url
        ]
        y["license"] = license_link(ds.license)
        y["category"] = ds.ods_categories
        y["maintainer"] = ds.owner
        y["date_created"] = ds.date_created
        y["date_updated"] = ds.date_updated
        y["records"] = ds.num_records
        # fn = f'{ds.owner}-{ds.title}'
        # fn = re.sub(r'[^\w\s-]', '', fn).strip()[:100]
        fn = urllib.parse.quote_plus(f"{(ds.owner).lower()}-{(ds.title).lower()}")
        # fn = {ds.owner}-{ds.title})
        # ^^ need something better for filnames...
        print(f"Writing ../jkan/_datasets/{fn}.md")
        with open(f"../jkan/_datasets/{fn}.md", "w") as f:
            print(os.path.abspath(f.name))
            f.write("---\n")
            f.write(yaml.dump(y))
            f.write("---\n")

if __name__ == "__main__":
    main()