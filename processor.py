from urllib import request, parse
import csv
import json
import os


class Processor:
    # Type should be one of the following: 'dcat', 'arcgis', 'usmart'
    def __init__(self, type):
        self.type = type
        self.header = ["Title", "Owner", "PageURL", "AssetURL", "DateCreated", "DateUpdated", "FileSize",
                       "FileSizeUnit", "FileType", "NumRecords", "OriginalTags", "ManualTags", "License",
                       "Description"]
        self.urls = {}

    def get_urls(self):
        with open('sources.csv', 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if row['Processor'] == self.type:
                    self.urls[row['Name']] = row['Source URL']

    def get_json(self, url):
        req = request.Request(url)
        return json.loads(request.urlopen(req).read().decode())

    def get_license(self, dataset):
        try:
            # Known Licenses info
            allLicenses = ['http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
            'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/',
            'http://opendatacommons.org/licenses/odbl/1-0/',
            'Open Data Commons Open Database License 1.0',
            'uk-ogl', 'UK Open Government Licence (OGL)',
            'Open Government Licence 3.0 (United Kingdom)',
            'OGL3', 'https://creativecommons.org/licenses/by/4.0/legalcode',
            'Creative Commons Attribution 4.0', 'https://creativecommons.org/licenses/by-sa/3.0/'];

            # Return License info, If License 'url' key available
            if('url' in dataset['attributes']['structuredLicense']):
                return dataset['attributes']['structuredLicense']['url']
            # Check for License in 'text' key and return the license info, if license 'url' key not available
            elif('text' in dataset['attributes']['structuredLicense']):
                for license in allLicenses:
                    if(license in dataset['attributes']['structuredLicense']['text']):
                        return license;
                return "";
            # Return '', if 'url' & 'text' key not available
            else:
                return ""
        except:
            return ""

    def write_csv(self, fname, prepped):
        with open(fname, 'w') as csvf:
            w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL)
            w.writerow(self.header)
            for r in prepped:
                if r[-1]:
                    r[-1] = r[-1].replace('\n', ' ')
                w.writerow(r)

    def get_datasets(self, owner, url, fname):
        print("Override this method")

    def process(self):
        self.get_urls()

        for name, url in self.urls.items():
            print(name)
            self.get_datasets(name, url, os.path.join(
                'data', self.type, name+'.csv'))
