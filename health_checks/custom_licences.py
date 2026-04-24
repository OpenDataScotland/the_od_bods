import urllib.request, json
import pandas as pd
from loguru import logger

with urllib.request.urlopen("https://opendata.scot/datasets.json") as url:
    datasets = json.load(url)

custom_licenses = pd.Series(
    [d["licence"] for d in datasets if d["licence"].startswith("Custom licence:")]
)

logger.info("{}", custom_licenses.value_counts())
