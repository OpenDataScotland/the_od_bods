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


fulld = pd.read_csv(
    "data/merged_output.csv", dtype=str, na_filter=False, lineterminator="\n"
)


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
        "CombinedTags",
        "ODSCategories",
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


data = {}
for r in fulld.values:
    id = str(r[ind("PageURL")]) + r[ind("Title")]
    if id not in data:
        ds = Dataset(
            title=r[ind("Title")],
            owner=r[ind("Owner")],
            page_url=r[ind("PageURL")],
            date_created=r[ind("DateCreated")],
            date_updated=r[ind("DateUpdated")].removesuffix(" 00:00:00.000"),
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
            show_name=r[ind("FileName")] if r[ind("FileName")] else r[ind("FileType")],
        )
    )


unknown_lics = []


def license_link(l):
    ogl = [
        "Open Government Licence 3.0 (United Kingdom)",
        "uk-ogl",
        "UK Open Government Licence (OGL)",
        "OGL3",
        "Open Government Licence v3.0",
    ]
    if l in ogl:
        return (
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
        )
    if l == "Creative Commons Attribution Share-Alike 4.0":
        return "https://creativecommons.org/licenses/by-sa/4.0/"
    if l == "Creative Commons Attribution 4.0":
        return "https://creativecommons.org/licenses/by/4.0/"
    if l == "Open Data Commons Open Database License 1.0":
        return "https://opendatacommons.org/licenses/odbl/"

    if not l in unknown_lics:
        unknown_lics.append(l)
        # print("Unknown license: ", l)
    return l


md = markdown.Markdown()

### Replace folder by deleting and writing
shutil.rmtree("../jkan/_datasets/")
os.makedirs("../jkan/_datasets/")


for n, (k, ds) in enumerate(data.items()):
    y = {"schema": "default"}
    y["title"] = ds.title
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
    with open(f"../jkan/_datasets/{fn}.md", "w") as f:
        f.write("---\n")
        f.write(yaml.dump(y))
        f.write("---\n")
