import copy
from processor import Processor

class ProcessorDCAT(Processor):
    def __init__(self):
        super().__init__(type='dcat')

    def get_datasets(self, start_url, fname):
        url = start_url

        header = ["Title", "Owner", "PageURL", "AssetURL", "DateCreated", "DateUpdated", "FileSize",
                "FileSizeUnit", "FileType", "NumRecords", "OriginalTags", "ManualTags", "License",
                "Description"]
        d = processor.get_json(url)
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
        processor.write_csv(fname, header, prepped)


def get_license(dataset):
    try:
        return dataset['attributes']['structuredLicense']['url']
    except:
        return ""




processor = ProcessorDCAT()
processor.process()
