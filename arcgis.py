from urllib import request, parse
import json

def get_json(url):
    req = request.Request(url)
    return json.loads(request.urlopen(req).read().decode())

start_url = 'https://opendata.arcgis.com/api/v3/search?filter[tags]=any(renfrewshire)&filter[openData]=true'
url = start_url

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
                                                                       
                                                                       
