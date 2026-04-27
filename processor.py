import urllib.error
from urllib import request, parse
from urllib.error import HTTPError, URLError
import csv
import json
import os
import re
import time
from collections import OrderedDict
from functools import wraps
from loguru import logger

class Processor:
    CAMEL_CASE_FIELD_MAP = {
        "Title": "title",
        "Owner": "owner",
        "PageURL": "pageUrl",
        "AssetURL": "assetUrl",
        "FileName": "fileName",
        "DateCreated": "dateCreated",
        "DateUpdated": "dateUpdated",
        "FileSize": "fileSize",
        "FileSizeUnit": "fileSizeUnit",
        "FileType": "fileType",
        "NumRecords": "numRecords",
        "OriginalTags": "originalTags",
        "ManualTags": "manualTags",
        "License": "license",
        "Description": "description",
        "Source": "source",
        "AssetStatus": "assetStatus",
        "ODSCategories": "odsCategories",
        "ODSCategories_Keywords": "odsCategoriesKeywords",
        "URL": "url",
    }

    RESOURCE_FIELDS = [
        "AssetURL",
        "FileName",
        "FileSize",
        "FileSizeUnit",
        "FileType",
        "NumRecords",
    ]

    # Type should be one of the following: 'dcat', 'arcgis', 'usmart'
    def __init__(self, type):
        self.type = type
        self.header = [
            "Title",
            "Owner",
            "PageURL",
            "AssetURL",
            "FileName",
            "DateCreated",
            "DateUpdated",
            "FileSize",
            "FileSizeUnit",
            "FileType",
            "NumRecords",
            "OriginalTags",
            "ManualTags",
            "License",
            "Description",
        ]
        self.urls = {}

    def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
        """Retry calling the decorated function using an exponential backoff.

        http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
        original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

        :param ExceptionToCheck: the exception to check. may be a tuple of
            exceptions to check
        :type ExceptionToCheck: Exception or tuple
        :param tries: number of times to try (not retry) before giving up
        :type tries: int
        :param delay: initial delay between retries in seconds
        :type delay: int
        :param backoff: backoff multiplier e.g. value of 2 will double the delay
            each retry
        :type backoff: int
        """
        def deco_retry(f):

            @wraps(f)
            def f_retry(*args, **kwargs):
                mtries, mdelay = tries, delay
                while mtries > 1:
                    try:
                        return f(*args, **kwargs)
                    except ExceptionToCheck as e:
                        msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                        logger.warning(msg)
                        time.sleep(mdelay)
                        mtries -= 1
                        mdelay *= backoff
                return f(*args, **kwargs)

            return f_retry  # true decorator

        return deco_retry

    @retry(HTTPError, tries=3, delay=60, backoff=2)
    def urlopen_with_retry(self, req):
        return request.urlopen(req)

    def get_urls(self):
        with open("sources.csv", "r", encoding="utf-8") as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if row["Processor"] == self.type:
                    self.urls[row["Name"]] = row["Source URL"]

    def get_json(self, url):
        req = request.Request(url)
        try:
            resp = self.urlopen_with_retry(req)
            decoded_resp = resp.read().decode()

            return json.loads(decoded_resp)
        except HTTPError as err1:
            logger.exception("{} cannot be accessed. The URL returned: {} {}", url, err1.code, err1.reason)
            error_dict = {
                "url": url,
                "error_code": err1.code,
                "error_reason": err1.reason,
            }
        except URLError as err2:
            logger.exception("{} cannot be accessed. The URL returned: {}", url, err2.reason)
            error_dict = {
                "url": url,
                "error_code": "",
                "error_reason": str(err2.reason),
            }
        with open("log.json", "a") as f:
            json.dump(error_dict, f)
        with open("log.md", "a") as file:
            file.write(
                f'| {error_dict["url"]} | {error_dict["error_code"]} | {error_dict["error_reason"]} | \n'
            )

        return "NULL" 

    def get_license(self, dataset):
        try:
            # Known Licenses info
            allLicenses = [
                "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
                "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
                "http://opendatacommons.org/licenses/odbl/1-0/",
                "Open Data Commons Open Database License 1.0",
                "uk-ogl",
                "UK Open Government Licence (OGL)",
                "Open Government Licence 3.0 (United Kingdom)",
                "OGL3",
                "https://creativecommons.org/licenses/by/4.0/legalcode",
                "Creative Commons Attribution 4.0",
                "https://creativecommons.org/licenses/by-sa/3.0/",
            ]

            # Return License info, If License 'url' key available
            if "url" in dataset["attributes"]["structuredLicense"]:
                return dataset["attributes"]["structuredLicense"]["url"]
            # Check for License in 'text' key and return the license info, if license 'url' key not available
            elif "text" in dataset["attributes"]["structuredLicense"]:
                for license in allLicenses:
                    if license in dataset["attributes"]["structuredLicense"]["text"]:
                        return license
                return ""
            # Return '', if 'url' & 'text' key not available
            else:
                return ""
        except:
            return ""

    def write_csv(self, fname, prepped):
        with open(fname, "w", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            w.writerow(self.header)
            for r in prepped:
                row = list(r)
                if row and row[-1]:
                    row[-1] = row[-1].replace("\n", " ")
                w.writerow(row)

    def write_json(self, fname, prepped):        
        with open(fname, "w", encoding="utf8") as json_file:
            json.dump(self._camelize_json_data(prepped), json_file, indent=4)

    def _to_camel_case(self, field_name):
        if field_name in self.CAMEL_CASE_FIELD_MAP:
            return self.CAMEL_CASE_FIELD_MAP[field_name]

        if "_" in field_name:
            parts = [p for p in field_name.split("_") if p]
        else:
            parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|[0-9]+", field_name)

        if not parts:
            return field_name

        return parts[0].lower() + "".join(part[:1].upper() + part[1:].lower() for part in parts[1:])

    def _camelize_json_data(self, data):
        if isinstance(data, list):
            return [self._camelize_json_data(item) for item in data]

        if isinstance(data, dict):
            return {
                self._to_camel_case(key): self._camelize_json_data(value)
                for key, value in data.items()
            }

        return data

    def _build_nested_datasets(self, prepped, header):
        header_lookup = {field: idx for idx, field in enumerate(header)}
        resource_fields = [field for field in self.RESOURCE_FIELDS if field in header_lookup]
        dataset_fields = [field for field in header if field not in resource_fields]
        datasets = OrderedDict()

        def get_value(row, field_name):
            idx = header_lookup[field_name]
            if idx >= len(row):
                return None
            return row[idx]

        for row in prepped:
            dataset_key = tuple(get_value(row, key) for key in ("Title", "Owner", "PageURL") if key in header_lookup)

            if dataset_key not in datasets:
                datasets[dataset_key] = {
                    self._to_camel_case(field): get_value(row, field)
                    for field in dataset_fields
                }
                datasets[dataset_key]["resources"] = []

            resource = {
                self._to_camel_case(field): get_value(row, field)
                for field in resource_fields
            }
            if resource:
                datasets[dataset_key]["resources"].append(resource)

        return list(datasets.values())

    def write_nested_json(self, fname, prepped, header=None):
        if header is None:
            header = self.header
        nested_datasets = self._build_nested_datasets(prepped, header)
        with open(fname, "w", encoding="utf-8") as json_file:
            json.dump(nested_datasets, json_file, indent=4)

    def write_csv_and_nested_json(self, csv_fname, prepped, header=None):
        if header is None:
            header = self.header
        self.write_csv(csv_fname, prepped)
        json_fname = os.path.splitext(csv_fname)[0] + ".json"
        self.write_nested_json(json_fname, prepped, header)

    def get_datasets(self, owner, url, fname):
        logger.warning("Override this method")

    def process(self, file_type = "csv"):
        self.get_urls()

        for name, url in self.urls.items():
            logger.info("{}", name)
            self.get_datasets(name, url, os.path.join("data", self.type, f"{name}.{file_type}"))
