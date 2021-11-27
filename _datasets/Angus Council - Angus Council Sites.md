---
schema: default
title: Angus Council Sites
organization: Angus Council
notes: >-
    Location of Angus Council owned and managed sites and properties. Includes common good properties.
resources:
  - name: Angus Council Sites WMS
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/inspire:ppt_councilsites/wms?service=WMS&version=1.1.0&request=GetMap
  - format: WMS

  - name: Angus Council Sites KML
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/wms/kml?layers=inspire:ppt_councilsites&mode=download
  - format: KML

  - name: Angus Council Sites GEOJSON
  - url: >-
      http://data.angus.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:ppt_councilsites&outputFormat=application%2Fjson&srsName=EPSG:3857
  - format: GEOJSON
license: UK Open Government Licence (OGL)
category:

  - land use
  - planning
  - property
  - sites
maintainer: Angus Council
maintainer_email: someone@example.com
---