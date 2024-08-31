from loguru import logger
import utilities
import arcgis
import usmart
import ckan
import sparql_statistics
import dcat
import aberdeenshire_council_scraper
import east_ayrshire_scraper
import moray_council_scraper
import nls_scraper
import sqa_scraper
import scottish_parliament
import crofting_commission

DATASET_PATHS = [
    "data/arcgis/",
    "data/ckan/",
    "data/dcat/",
    "data/scraped-results/",
    "data/USMART/",
    "data/bespoke_ScottishParliament/"
]
FILES_TO_DELETE = [
    "data/merged_output.json",
    "data/merged_output_untidy.json",
    "data/merged_output.json",
    "log.json",
    "log.md",
]

logger.info("Clearing folders")
for path in DATASET_PATHS:
    logger.info(f"Clearing {path}")
    utilities.clear_folder(path)
logger.info("Clearing outputs and logs")
for file in FILES_TO_DELETE:
    logger.info(f"Deleting {file}")
    utilities.safe_delete_file(file)

logger.info("Set up log files")
utilities.init_logs()

logger.info("Running ArcGIS scraper")
arcgis.processor.process()

logger.info("Running USMART scraper")
usmart.processor.process()

logger.info("Running CKAN scraper")
ckan.processor.process()

logger.info("Running SPARQL scraper")
sparql_statistics.processor.process()

logger.info("Running DCAT scraper")
dcat.processor.process()

#logger.info("Running Aberdeenshire Council static scraper")
#aberdeenshire_council_scraper.main()

logger.info("Running East Ayrshire static scraper")
east_ayrshire_scraper.main()

logger.info("Running Moray Council static scraper")
moray_council_scraper.main()

logger.info("Running National Library of Scotland static scraper")
# nls_scraper.main()

logger.info("Running SQA static scraper")
# sqa_scraper.main()

logger.info("Running Scottish Parliament scraper")
scottish_parliament.processor.process("json")

logger.info("Running Crofting Commission scraper")
crofting_commission.processor.process("json")

# logger.info("Merge data")
# merge_data.main()

# logger.info("Exporting to JKAN")
# export2jkan.main()

logger.info("Scraping complete")
