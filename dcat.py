#!/usr/bin/env python3

from urllib import request, parse
from datetime import datetime
import json
import csv
import os
import copy

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
    with open('sources.csv', 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row['Processor'] == 'dcat':
                urls[row['Name']] = row['Source URL']

    return urls


def get_datasets(start_url, fname):
    url = start_url

    header = ["Title", "Owner", "PageURL", "AssetURL", "DateCreated", "DateUpdated", "FileSize",
              "FileSizeUnit", "FileType", "NumRecords", "OriginalTags", "ManualTags", "License",
              "Description"]
    d = get_json(url)
    datasets = d['dcat:dataset']

    print(f"Found {len(datasets)} datasets")

    prepped = []
    for e in datasets:
        ds = [e.get('dct:title', ""),
              e.get('dct:publisher', "").replace(" Mapping", ""),
              "",  # link to page
              "",  # Link to data
              "",  # date created
              e.get('dct:issued', ""),
              "",  # size
              "",  # size unit
              "",  # filetype
              "",  # numrecords
              ";".join(e.get('dcat:keyword', [])),
              "",  # Manual tags
              "",  # license
              e.get('dct:description', "").strip(u'\u200b')
              ]
        pages = e.get('dcat:distribution')
        for p in pages:
            if p.get('dct:description', '') == 'Web Page':
                ds[2] = p.get('dcat:accessUrl', '')
                break
        dsl = []
        for p in pages:
            if p.get('dct:description', '') == 'Web Page':
                continue
            ds[3] = p.get('dcat:accessUrl', '')
            ds[8] = p.get('dct:title', '')
            dsl.append(copy.deepcopy(ds))
        if not dsl:
            dsl.append(ds)
        prepped += dsl

    print(f'{len(prepped)} lines for csv')

    with open(fname, 'w') as csvf:
        w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in prepped:
            if r[-1]:
                r[-1] = r[-1].replace('\n', ' ')
            w.writerow(r)

urls = get_urls()
for name, url in urls.items():
    print(name)
    get_datasets(url, os.path.join('data', 'dcat', name+'.csv'))
