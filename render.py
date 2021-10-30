from jinja2 import Environment, FileSystemLoader, Markup
import pandas as pd
from dataclasses import dataclass
from typing import List
from math import isnan
import markdown

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

md = markdown.Markdown()

env = Environment(loader=FileSystemLoader("."))
env.filters['markdown'] = lambda text: Markup(md.convert(text))
template = env.get_template('dataset.md')

for k, ds in data.items():
    page = template.render(d=ds)
    fn = ds.title.replace(" ", "-").replace("/", "\\")
    # ^^ need something better for filnames...
    with open(f"_datasets/{fn}.md", "w") as f:
        f.write(page)
