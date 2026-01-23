#!/bin/bash

input_folder=/neodc/eocis/data/CHUK/geospatial_information/v1.1
# input_folder=.

conda activate stac_tools_env

# output_folder=stac
output_folder=stac-tmp

echo Generating STAC record for Land Class

netcdf2stac --base-folder $output_folder/chuk-geospatial/landclass \
    --auxilary-folder $output_folder/chuk-geospatial-aux \
    --input-paths $input_folder/EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCLASS-MERGED-????-fv1.1.nc \
    --parent-collection-path ../../configurations/chuk_geospatial/chuk_geospatial_collection.json \
    --collection-filename collection.json \
    --item-subfolder "items" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/chuk_geospatial/chuk_geospatial.json ../../configurations/chuk_geospatial/chuk_geospatial_landclass.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --generate-cog lccs_class \
    --cog-nodata-values lccs_class:-1000 \
    --cog-dtypes lccs_class:int16 \
    --cog-crs EPSG:27700
