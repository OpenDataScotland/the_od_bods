---
schema: default
title: Angus Council Localities
organization: Angus Council
notes: Localities used in the Corporate Address Gazetteer for the generation of addresses.
resources:

  - name: Angus Council Localities WMS
  - url: http://data.angus.gov.uk/geoserver/inspire/inspire:gaz_localities/wms?service=WMS&request=GetMap
  - format: WMS

  - name: Angus Council Localities KML
  - url: http://data.angus.gov.uk/geoserver/inspire/wms/kml?layers=inspire:gaz_localities&mode=download
  - format: KML

  - name: Angus Council Localities GEOJSON
  - url: http://data.angus.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:gaz_localities&outputFormat=application%2Fjson&srsName=EPSG:3857
  - format: GEOJSON

license: UK Open Government Licence (OGL)
category:

  - gazetteer

  - localities

  - towns


  - 

maintainer: Tim Wisniewski
maintainer_email: tim@timwis.com
---