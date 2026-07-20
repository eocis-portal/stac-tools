#!/bin/bash

conda activate stac_tools_env

output_folder=stac-tmp

input_paths=/neodc/eocis/data/CHUK/land_surface_temperature/LANDSAT8_TIRS/L2/v1.0/????/??/??/*.nc

echo Generating STAC records for eocis-chuk-lst

netcdf2stac --base-folder $output_folder/eocis-chuk-lst \
    --auxilary-folder $output_folder/eocis-chuk-lst-aux \
    --input-paths $input_paths \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json \
            ../../configurations/chuk_land_surface_temperature/chuk_land_surface_temperature.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --include-item-thumbnails \
    --overwrite-items

