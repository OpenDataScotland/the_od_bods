---
category:
- Weather,Environment
license: Creative Commons Attribution Share-Alike 4.0
maintainer: Dundee City Council
maintainer_email: someone@example.com
notes: 'Weather data, primarily wind, temperature, pressure, humidity, recorded from
  a weather station situated on the top of the University''s tower building. Warning:
  the location is not ideal so the readings may be affected by turbulence, up-drafts,
  or other effects. Readings are taken every minute or every five minutes but there
  may be gaps and the data is not necessarily clean so check for out of range values.


  Units: Temperature (C), Wind (mph), Pressure (mb), Solar Rad (W/m2), Humidity (%),
  Rain (mm)


  Columns: DateTime,rtBaroCurr,rtOutsideTemp,rtWindSpeed,rtWindAvgSpeed,rtWindDir,rtWindDirRose,rtOutsideHum,rtSolarRad,hlWindHiDay,hlWindHiTime

  where rt=real-time and hl=high/low and time is localtime.


  WARNING: the wind direction readings may be incorrect due to a faulty sensor. We
  are working to rectify this.

  WARNING: the hour may show 12: after midnight when it should show 00:

  '
organization: Dundee City Council
resources:
- format: CSV
  name: Dundee Satellite Receiving Station Weather Data CSV
  url: https://data.dundeecity.gov.uk/dataset/a1bf17ec-8894-4989-96eb-aa6e7b31e0ea/resource/0f35ff53-d72f-434c-af99-c545ccbdb5f5/download/dsrs_weather_2017.csv
schema: default
title: Dundee Satellite Receiving Station Weather Data
---
