# to run, in terminal: sh main.sh
# delete old log and create new, empty log
find log.json -type f -delete
find log.md -type f -delete
touch log.json
touch log.md
echo '# pipeline error log' >> log.md
echo '' >> log.md
echo '## Unaccessible Webpages' >> log.md
echo '' >> log.md
echo '|URL | Error Code | Error Reason|' >> log.md
echo '|--- | --- | ---|' >> log.md
# clear folders
find data/arcgis/ -type f -delete
find data/ckan/ -type f -delete
find data/dcat/ -type f -delete
find data/scraped-results/ -type f -delete
find data/USMART/ -type f -delete
find data/merged_output.csv -type f -delete
# run source scripts
python arcgis.py
python usmart.py
python ckan.py
python sparkql_statistics.py
python dcat.py
cd web-scrapers
python aberdeenshire_council_scraper.py
python east_ayrshire_scraper.py
python moray_council_scraper.py
python nls_scraper.py
python sqa_scraper.py
cd ..
# processing
python merge_data.py
python export2jkan.py
echo "main.sh complete"
