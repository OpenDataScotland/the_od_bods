import json
from urllib import request

def get_thing(site, thing="tag"):
    try:
        with request.urlopen(f"{site}api/3/action/{thing}_list") as page:
            data = json.loads(page.read().decode())
            return data['result']
    except Exception as e:
        print(f"Error with {site}, {thing}:")
        print(e)
        return []
    
sites = {"Aberdeen City": "https://data.aberdeencity.gov.uk/",
         "Dundee": "https://data.dundeecity.gov.uk/",
         "Perth": "https://data.pkc.gov.uk/",
         "Stirling": "https://data.stirling.gov.uk/",
         # "Glasgow": "https://data.glasgow.gov.uk/",
         
         }

# tags = {n: get_thing(site, "tag") for n, site in sites.items()}

groups = {n: get_thing(site, "group") for n, site in sites.items()}

print(groups)


