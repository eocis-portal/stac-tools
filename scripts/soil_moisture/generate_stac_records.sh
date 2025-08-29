#!/bin/bash

conda init

conda activate stac_tools_env

# output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp
output_folder=/home/dev/github/stac-tools/scripts/soil_moisture/outputs
input_paths=/neodc/eocis/data/global_and_regional/soil_moisture_africa
input_paths=/home/dev/github/driafs/data/soil_moisture/*/*/*.nc
echo Generating STAC records for eocis-africa-soil-moisture

netcdf2stac --base-folder $output_folder/eocis-soil-moisture-africa \
    --auxilary-folder $output_folder/eocis-soil-moisture-africa-aux \
    --input-paths $input_paths \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/soil_moisture_africa/soil_moisture_africa.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items

