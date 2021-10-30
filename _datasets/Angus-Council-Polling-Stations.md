---
schema: default
title: Angus Council Polling Stations
organization: Angus Council
notes: Location of current Angus Council polling stations.
resources:

  - name: Angus Council Polling Stations WMS
  - url: http://data.angus.gov.uk/geoserver/inspire/inspire:law_pollingstations/wms?service=WMS&request=GetMap
  - format: WMS

  - name: Angus Council Polling Stations KML
  - url: http://data.angus.gov.uk/geoserver/inspire/wms/kml?layers=inspire:law_pollingstations&mode=download
  - format: KML

  - name: Angus Council Polling Stations GEOJSON
  - url: http://data.angus.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:law_pollingstations&outputFormat=application%2Fjson&srsName=EPSG:3857
  - format: GEOJSON

license: UK Open Government Licence (OGL)
category:

  - democracy

  - elections

  - local government

  - polling district

  - polling place

  - station

  - voting


  - 

maintainer: Tim Wisniewski
maintainer_email: tim@timwis.com
---