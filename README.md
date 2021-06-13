# the_od_bods
Open data has the power to bring about economic, social, environmental, and other benefits for everyone. It should be the fuel of innovation and entrepreneurship, and provide trust and transparency in government. 

But there are barriers to delivering those benefits:

 - Knowking what data is being produced that you can re-use, and 
 - easily finding that data so that you can use it, or join it together with other agencies data. 

In a perfect world we'd have local and national portals publishing or sign-posting data that we all could use. These portals would be rich with metadata and would use open standards at their core. And they would be federated so that data and metadata added at any level could be found further up the tree. 

They'd use common data schemas with a fixed vocabulary which would be used as a standard across the public sector. 

You could start at your kid's school's open data presence and get an open data timetable, or its own-published data. You could move up to the city or shire level and find the same school data alongside other schools' data - or a summation of each of their data. That council would publish their budget that they spend on the school - or the school catchment area or other LA specifics. And if you went up to a national level you'd see all of that data gatherered upwwards - see all Scottish Schools and also see the national data such as SQA results, school inspection reports - all as open data. 

But this is Scotland and we have only had an open data for six years. Looking at the lowest units - the 32 local authorities - only half even have any open data. Of the fourteen health boards none publishes open data. Of the thirty Health and Social Care Partnerships only one has open data. And in 2020 it was found that of and assumed 147 business units comprising Scottish Government (trying getting data of what IS in the Scottish Government) - 120 have published no data. 

And, of course there are no regional or national open data portals. Why would Scottish Government bother - apart from an EU portal report in 2020, that is, from which it was clear that OD done well would benefit the Scottish economy by around £2.21bn per annum?

So there is no national portal. There isn't even one for the seven cities, let alone all 32 councils. Which means no facility to aggregeate open data on, say, planning, across all 32 councils. No way to download all of the bits of the national cycle paths from their custodians. No way to find our how much each spends on taxis etc.

The aim of this project at [CTC23](https://github.com/CodeTheCity/CTC23) is to start collate access to Open Data in Scotland, beginning with cities. 

## Methodology

We started by looking at Scottish Cities' open data portals (where these could be found). One source was the work that [Ian](https://github.com/watty62) did in his last [audit of Scottish Open Data](https://github.com/watty62/SOD/blob/master/Local_authorities.md) . 




## What we are building

- A list of data sources and what they contain
- Script to pull data from existing platforms
   - CKAN
   - ArcGIS
- A front-end to present an aggregation of datasets from all the platforms


## Lessons Learned

- There is a lack of good quality open datasets published by local authorities
- There is no common taxonomy for categorising datasets
- There is no facility to aggregate a common dataset accross all 32 local authorities (e.g. cycle paths)
- There is no centralised, national portal for accessing open data in Scotland
