from urllib import request, parse
import csv
import json
import os

class Processor:
    # Type should be one of the following: 'dcat', 'arcgis', 'usmart'
    def __init__(self, type):
        self.type = type
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
            return dataset['attributes']['structuredLicense']['url']
        except:
            return ""

    def write_csv(self, fname, header, prepped):
        with open(fname, 'w') as csvf:
            w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL)
            w.writerow(header)
            for r in prepped:
                if r[-1]:
                    r[-1] = r[-1].replace('\n', ' ')
                w.writerow(r)

    def get_datasets(self, url, fname):
        print("Do something")

    def process(self):
        self.get_urls()

        for name, url in self.urls.items():
            print(name)
            self.get_datasets(url, os.path.join('data', self.type, name+'.csv'))
