---
schema: default
title: School Catchment Areas
organization: Dundee City Council
notes: Catchment areas of all mainstream schools within the Dundee City Council administrative boundary. Catchments are available for Primary and Secondary, Denominational and Nondenominational schools. Catchment areas are used to help place children resident in that area into their catchment school. 

Children are allocated Priority 1 status for their catchment school. Other children not resident in that catchment area are required to make a placing request for entry into that school.
resources:

  - name: School Catchment Areas ZIP
  - url: http://inspire.dundeecity.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:SCHOOL_CATCHMENTS_PRIMARY&maxFeatures=50&outputFormat=SHAPE-ZIP
  - format: ZIP

  - name: School Catchment Areas GEOJSON
  - url: http://inspire.dundeecity.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:SCHOOL_CATCHMENTS_PRIMARY&maxFeatures=100&outputFormat=application%2Fjson&srsName=EPSG:3857
  - format: GEOJSON

  - name: School Catchment Areas ZIP
  - url: http://inspire.dundeecity.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:SCHOOL_CATCHMENTS_SECONDARY&maxFeatures=100&outputFormat=SHAPE-ZIP
  - format: ZIP

  - name: School Catchment Areas GEOJSON
  - url: http://inspire.dundeecity.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:SCHOOL_CATCHMENTS_SECONDARY&maxFeatures=100&outputFormat=application%2Fjson&srsName=EPSG:3857
  - format: GEOJSON

  - name: School Catchment Areas WMS
  - url: http://inspire.dundeecity.gov.uk/geoserver/inspire/wms?service=WMS&version=1.3.0&request=getCapabilities
  - format: WMS

  - name: School Catchment Areas WFS
  - url: http://inspire.dundeecity.gov.uk/geoserver/inspire/ows?service=wfs&request=getCapabilities
  - format: WFS

license: Open Government Licence 3.0 (United Kingdom)
category:

  - Education


  - 

maintainer: Tim Wisniewski
maintainer_email: tim@timwis.com
---