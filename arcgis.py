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

#start_url = 'https://opendata.arcgis.com/api/v3/search?filter[tags]=any(renfrewshire)&filter[openData]=true'

start_urls = {
    'renfrew': 'https://opendata.arcgis.com/api/v3/search?catalog[groupIds]=any(79dc9ae7552e4782bf66dadbdf049a0d,bcaad01ef27a4457b9c9406818eaca5d)',
    'argyll_and_bute': 'https://opendata.arcgis.com/api/v3/search?catalog[groupIds]=any(2391aa86db9148d1857671888aefdc5f)',
    'south_ayrshire': 'https://opendata.arcgis.com/api/v3/search?catalog[groupIds]=any(436655c931664e279f675390213d828e)',
    'moray': 'https://opendata.arcgis.com/api/v3/search?catalog[groupIds]=any(b42b8e7bce20408684689845a268e8e6)',
    'highland': 'https://map-highland.opendata.arcgis.com/api/v3/search',
    'north_ayrshire': 'https://maps-north-ayrshire.opendata.arcgis.com/api/v3/search',
    'north_lanarkshire': 'https://gisdata.northlanarkshire.gov.uk/api/v3/search'
    }

def get_datasets(start_url, fname):
    url = start_url

    header = ["Title","Owner","PageURL","AssetURL","DateCreated","DateUpdated","FileSize",
              "FileSizeUnit","FileType","NumRecords","OriginalTags","ManualTags","License",
              "Description"]
    datasets = []

    while True:
        d = get_json(url)
        datasets += d['data']
        if 'next' in d['meta']  and d['meta']['next']:
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
                        "", #Link to data
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
                        "", #Manual tags
                        get_license(e), #license
                        e['attributes'].get('searchDescription', "")
                        ])    

    with open(fname, 'w') as csvf:
        w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in prepped:
            if r[-1]:
                r[-1] = r[-1].replace('\n', ' ')
            w.writerow(r)
                                                                       
                                                                       
# get_datasets(argyll_start_url, "argyll_and_bute.csv")
# get_datasets(south_ayrshire_start_url, "south_ayrshire.csv")
# get_datasets(moray_start_url, "moray.csv")
for name, url in start_urls.items():
    print(name)
    get_datasets(url, os.path.join('data', 'arcgis', name+'.csv'))
