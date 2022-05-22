from urllib import request, parse
from datetime import datetime
import json
import csv
import os


def get_json(url):
    req = request.Request(url)
    return json.loads(request.urlopen(req).read().decode())


def get_license(dataset):
    try:
        return dataset['attributes']['structuredLicense']['url']
    except:
        return ""


def get_urls():
    urls = {}
    with open('./sources.csv', 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row['Processor'] == 'arcgis':
                urls[row['Name']] = row['Source URL']

    return urls


def get_datasets(start_url, fname):
    url = start_url

    header = ["Title", "Owner", "PageURL", "AssetURL", "DateCreated", "DateUpdated", "FileSize",
              "FileSizeUnit", "FileType", "NumRecords", "OriginalTags", "ManualTags", "License",
              "Description"]
    datasets = []

    while True:
        d = get_json(url)
        datasets += d['data']
        if 'next' in d['meta'] and d['meta']['next']:
            url = d['meta']['next']
            print(f"Next {url}")
        else:
            break

    print(f"Found {len(datasets)} datasets")

    prepped = []
    for e in datasets:
        prepped.append([e['attributes'].get('name', ""),
                        e['attributes'].get('source', ""),
                        e.get('links', {}).get('itemPage', ""),
                        "",  # Link to data
                        datetime.utcfromtimestamp(
                            e['attributes'].get('created', 0)/1000).strftime(
                                '%Y-%m-%d'),
                        datetime.utcfromtimestamp(
                            e['attributes'].get('modified', 0)/1000).strftime(
                                '%Y-%m-%d'),
                        # ^^ Should really do something better than defaulting to start of epoch
                        e['attributes'].get('size', ""),
                        "bytes",
                        e['attributes'].get('type', ""),
                        e['attributes'].get('recordCount', ""),
                        ";".join(e['attributes'].get('tags', [])),
                        "",  # Manual tags
                        get_license(e),  # license
                        e['attributes'].get('searchDescription', "")
                        ])

    with open(fname, 'w') as csvf:
        w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in prepped:
            if r[-1]:
                r[-1] = r[-1].replace('\n', ' ')
            w.writerow(r)


start_urls = get_urls()
for name, url in start_urls.items():
    print(name)
    get_datasets(url, os.path.join('data', 'arcgis', name+'.csv'))
