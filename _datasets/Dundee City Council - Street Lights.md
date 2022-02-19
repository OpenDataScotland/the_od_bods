---
category:
- lighting,transport,street-assets
date_created: '2019-03-19'
date_updated: '2018-02-12'
license: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
maintainer: Dundee City Council
notes: '<p>The street lighting in Dundee is delivered through the <a href="https://www.dundeecity.gov.uk/service-area/city-development/roads-and-transportation/street-lighting">Street
  Lighting Partnership</a>.  </p>

  <p>This dataset includes locations of all street lights in the city that are operated
  by the partnership, and includes details of the light type and column height.   </p>

  <p>You can <a href="https://my.dundeecity.gov.uk/service/Street_Lighting_Fault___Report_it">report
  a fault</a> online - let us know in the comments if you would be interested in an
  API to report faults using the light data this dataset. </p>'
organization: Dundee City Council
original_dataset_link: https://data.dundeecity.gov.uk/dataset/street-lights
records: null
resources:
- format: CSV
  name: CSV
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?version=2.0.0&service=wfs&request=GetFeature&typeName=opendata:v_street_lights&outputFormat=csv
- format: ZIP
  name: ZIP
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?version=2.0.0&service=wfs&request=GetFeature&typeName=opendata:v_street_lights&outputFormat=SHAPE-ZIP
- format: GEOJSON
  name: GEOJSON
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?version=2.0.0&service=wfs&request=GetFeature&typeName=opendata:v_street_lights&outputFormat=application/json
- format: WMS
  name: WMS
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wms?service=Wms&version=1.3.0&request=getCapabilities
- format: WFS
  name: WFS
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?service=WFS&version=2.0.0&request=getCapabilities
schema: default
title: Street Lights
---
