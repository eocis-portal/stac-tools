#!/bin/bash

output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

conda activate stac_tools_env

modifystac --paths $output_folder/eocis-lst-s3a-day/collection.json \
  --attr title "EOCIS Land Surface Temperature from Sentinel 3A daily (day)" \
  --attr links.0.title "EOCIS Land Surface Temperature from Sentinel 3A daily (day)"

modifystac --paths $output_folder/eocis-lst-s3b-day/collection.json \
  --attr title "EOCIS Land Surface Temperature from Sentinel 3B daily (day)" \
  --attr links.0.title "EOCIS Land Surface Temperature from Sentinel 3B daily (day)"

modifystac --paths $output_folder/eocis-lst-s3a-night/collection.json \
  --attr title "EOCIS Land Surface Temperature from Sentinel 3A daily (night)" \
  --attr links.0.title "EOCIS Land Surface Temperature from Sentinel 3A daily (night)"

modifystac --paths $output_folder/eocis-lst-s3b-night/collection.json \
  --attr title "EOCIS Land Surface Temperature from Sentinel 3B daily (night)" \
  --attr links.0.title "EOCIS Land Surface Temperature from Sentinel 3B daily (night)"

modifystac --paths $output_folder/eocis-lst-s3a-day/items/*/*/*.geojson \
  --attr title "EOCIS daily LST 3A day \${properties['datetime'][0:10]}" \
  --attr properties.title "EOCIS daily LST 3A day \${properties['datetime'][0:10]}"

modifystac --paths $output_folder/eocis-lst-s3b-day/items/*/*/*.geojson \
  --attr title "EOCIS daily LST 3B day \${properties['datetime'][0:10]}"  \
  --attr properties.title "EOCIS daily LST 3B day \${properties['datetime'][0:10]}"

modifystac --paths $output_folder/eocis-lst-s3a-night/items/*/*/*.geojson \
  --attr title "EOCIS daily LST 3A night \${properties['datetime'][0:10]}" \
  --attr properties.title "EOCIS daily LST 3A night \${properties['datetime'][0:10]}"

modifystac --paths $output_folder/eocis-lst-s3b-night/items/*/*/*.geojson \
  --attr title "EOCIS daily LST 3B night \${properties['datetime'][0:10]}" \
  --attr properties.title "EOCIS daily LST 3B night \${properties['datetime'][0:10]}"