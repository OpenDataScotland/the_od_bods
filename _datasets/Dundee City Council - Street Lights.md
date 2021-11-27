---
category:
- lighting,transport,street-assets
license: Open Government Licence 3.0 (United Kingdom)
maintainer: Dundee City Council
maintainer_email: someone@example.com
notes: "The street lighting in Dundee is delivered through the [Street Lighting Partnership](https://www.dundeecity.gov.uk/service-area/city-development/roads-and-transportation/street-lighting).\
  \  \n\nThis dataset includes locations of all street lights in the city that are\
  \ operated by the partnership, and includes details of the light type and column\
  \ height.   \n\nYou can [report a fault](https://my.dundeecity.gov.uk/service/Street_Lighting_Fault___Report_it)\
  \ online - let us know in the comments if you would be interested in an API to report\
  \ faults using the light data this dataset. "
organization: Dundee City Council
resources:
- format: CSV
  name: Street Lights CSV
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?version=2.0.0&service=wfs&request=GetFeature&typeName=opendata:v_street_lights&outputFormat=csv
- format: ZIP
  name: Street Lights ZIP
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?version=2.0.0&service=wfs&request=GetFeature&typeName=opendata:v_street_lights&outputFormat=SHAPE-ZIP
- format: GEOJSON
  name: Street Lights GEOJSON
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?version=2.0.0&service=wfs&request=GetFeature&typeName=opendata:v_street_lights&outputFormat=application/json
- format: WMS
  name: Street Lights WMS
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wms?service=Wms&version=1.3.0&request=getCapabilities
- format: WFS
  name: Street Lights WFS
  url: http://inspire.dundeecity.gov.uk/geoserver/opendata/wfs?service=WFS&version=2.0.0&request=getCapabilities
schema: default
title: Street Lights
---
