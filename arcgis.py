from datetime import datetime
from loguru import logger

try:
    from processor import Processor
except:
    from .processor import Processor


class ProcessorARCGIS(Processor):
    def __init__(self):
        super().__init__(type="arcgis")

    def get_datasets(self, owner, start_url, fname):
        datasets = []

        url = start_url

        while True:
            d = processor.get_json(url)
            if d != "NULL":
                datasets += d["data"]
                if "next" in d["meta"] and d["meta"]["next"]:
                    url = d["meta"]["next"]
                    logger.info("Next {}", url)
                else:
                    break

        logger.info("Found {} datasets", len(datasets))

        prepped = []
        for e in datasets:
            prepped.append(
                [
                    e["attributes"].get("name", ""),
                    e["attributes"].get("source", owner),
                    e.get("links", {}).get("itemPage", ""),
                    "",  # Link to data
                    "",  # FileName
                    datetime.utcfromtimestamp(
                        e["attributes"].get("created", 0) / 1000
                    ).strftime("%Y-%m-%d"),
                    datetime.utcfromtimestamp(
                        e["attributes"].get("modified", 0) / 1000
                    ).strftime("%Y-%m-%d"),
                    # ^^ Should really do something better than defaulting to start of epoch
                    e["attributes"].get("size", ""),
                    "bytes",
                    e["attributes"].get("type", ""),
                    e["attributes"].get("recordCount", ""),
                    ";".join(e["attributes"].get("tags", [])),
                    "",  # Manual tags
                    self.get_license(e),  # license
                    e["attributes"].get("searchDescription", ""),
                ]
            )
        processor.write_csv_and_nested_json(fname, prepped)


processor = ProcessorARCGIS()

if __name__ == "__main__":
    processor.process()
