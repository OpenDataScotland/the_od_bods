import pandas as pd
from dataclasses import dataclass
from typing import List
from math import isnan
import markdown
import re
import yaml

@dataclass
class DataFile:
    url: str
    size: float
    size_unit: str
    file_type: str

@dataclass
class Dataset:
    title: str
    owner: str
    page_url: str
    date_created: str
    date_updated: str
    original_tags: List[str]
    manual_tags: List[str]
    license: str
    description: str
    num_records: int
    files: List[DataFile]

fulld = pd.read_csv("data/merged_output.csv", dtype=str, na_filter=False)
def ind(name):
    f = ['Unnamed: 0', 'Title', 'Owner', 'PageURL', 'AssetURL', 'DateCreated',
       'DateUpdated', 'FileSize', 'FileSizeUnit', 'FileType', 'NumRecords',
       'OriginalTags', 'ManualTags', 'License', 'Description', 'Source']
    return f.index(name)

def splittags(tags):
    if type(tags) == str:
        if tags == "":
            return []
        return tags.split(';')
    else:
        return []
def makeint(val):
    try:
        return int(val)
    except:
        return None
    
data = {}
for r in fulld.values:
    id = str(r[ind('PageURL')]) + r[ind('Title')]
    if id not in data:
        ds = Dataset(
            title = r[ind('Title')],
            owner = r[ind('Owner')],
            page_url = r[ind('PageURL')],
            date_created = r[ind('DateCreated')],
            date_updated = r[ind('DateUpdated')].removesuffix(' 00:00:00.000'),
            original_tags = splittags(r[ind('OriginalTags')]),
            manual_tags = splittags(r[ind('ManualTags')]),
            license = r[ind('License')],
            description = str(r[ind('Description')]),
            num_records = makeint(r[ind('NumRecords')]),
            files = []
        )
        data[id] = ds
    data[id].files.append(
        DataFile(
            url = r[ind('AssetURL')],
            size = r[ind('FileSize')],
            size_unit = r[ind('FileSizeUnit')],
            file_type = r[ind('FileType')]
        ))
# print(data)
print(len(data), ' records')

def sort_key(d):
    if d.date_updated:
        return d.date_updated
    if d.date_created:
        return d.date_created
    return "0"

unknown_lics = []

def license_link(l):
    ogl = ["Open Government Licence 3.0 (United Kingdom)", "uk-ogl",
           "UK Open Government Licence (OGL)", "OGL3"]
    if l in ogl:
        return "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
    if not l in unknown_lics:
        unknown_lics.append(l)
        print("Unknown license: ", l)
    return l

md = markdown.Markdown()

for k, ds in data.items():
    y = {'schema': 'default'}
    y['title'] = ds.title
    y['organization'] = ds.owner
    y['notes'] = markdown.markdown(ds.description)
    y['resources'] = [{'name': 'Description',
                       'url': ds.page_url,
                       'format': 'html'}] + [{'name': d.file_type,
                                              'url': d.url,
                                              'format': d.file_type} for d in ds.files]
    y['license'] = license_link(ds.license)
    y['category'] = ds.original_tags + ds.manual_tags
    y['maintainer'] = ds.owner
    y['date_created'] = ds.date_created
    y['date_updated'] = ds.date_updated
    y['records'] = ds.num_records
    fn = ds.owner + " - " + ds.title
    fn = re.sub(r'[^\w\s-]', '', fn).strip()
    # ^^ need something better for filnames...
    with open(f"_datasets/{fn}.md", "w") as f:
        f.write("---\n")
        f.write(yaml.dump(y))
        f.write("---\n")
