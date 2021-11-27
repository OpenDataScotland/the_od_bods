---
schema: default
title: Angus Council Property
organization: Angus Council
notes: >-
    Properties that Angus Council owns or occupies or has owned or occupied or has some other interest in.
resources:
  - name: Angus Council Property WMS
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/inspire:ppt_councilproperties/wms?service=wms&request=getmap
  - format: WMS

  - name: Angus Council Property KML
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/wms/kml?layers=inspire:ppt_councilproperties&mode=download
  - format: KML

  - name: Angus Council Property GEOJSON
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:ppt_councilproperties&outputFormat=application%2Fjson&srsName=EPSG:3857
  - format: GEOJSON

  - name: Angus Council Property CSV
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:ppt_councilproperties&outputFormat=csv
  - format: CSV
license: UK Open Government Licence (OGL)
category:

  - land use
  - planning
  - property
maintainer: Angus Council
maintainer_email: someone@example.com
---