#!/bin/bash

# input_folder=/neodc/eocis/data/CHUK/geospatial_information/v1.1
input_folder=/home/dev/github/stac-tools/configurations/chuk_geospatial

conda activate stac_tools_env

# output_folder=stac
output_folder=stac-tmp

echo Generating STAC record for Elevation

netcdf2stac --base-folder $output_folder/chuk-geospatial/elevation \
    --auxilary-folder $output_folder/chuk-geospatial-aux \
    --input-paths $input_folder/EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-ELEVATION-MERGED-2023-fv1.0.nc \
    --parent-collection-path ../../configurations/chuk_geospatial/chuk_geospatial_collection.json \
    --collection-filename collection.json \
    --item-subfolder "items" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/chuk_geospatial/chuk_geospatial.json ../../configurations/chuk_geospatial/chuk_geospatial_elevation.json \
    --include-kerchunk \
    --include-collection-thumbnail

echo Generating STAC record for Land Cover

netcdf2stac --base-folder $output_folder/chuk-geospatial/landcover \
    --auxilary-folder $output_folder/chuk-geospatial-aux \
    --input-paths $input_folder/EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCOVER-MERGED-2023-fv1.1.nc \
    --parent-collection-path ../../configurations/chuk_geospatial/chuk_geospatial_collection.json \
    --collection-filename collection.json \
    --item-subfolder "items" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/chuk_geospatial/chuk_geospatial.json ../../configurations/chuk_geospatial/chuk_geospatial_landcover.json \
    --include-kerchunk \
    --include-collection-thumbnail

echo Generating STAC record for Built Area

netcdf2stac --base-folder $output_folder/chuk-geospatial/builtarea \
    --auxilary-folder $output_folder/chuk-geospatial-aux \
    --input-paths $input_folder/EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-BUILTAREA-MERGED-2023-fv1.1.nc \
    --parent-collection-path ../../configurations/chuk_geospatial/chuk_geospatial_collection.json \
    --collection-filename collection.json \
    --item-subfolder "items" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/chuk_geospatial/chuk_geospatial.json ../../configurations/chuk_geospatial/chuk_geospatial_builtarea.json \
    --include-kerchunk \
    --include-collection-thumbnail
