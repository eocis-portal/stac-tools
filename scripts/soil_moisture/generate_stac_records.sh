#!/bin/bash

conda init

conda activate stac_tools_env

output_folder=stac-tmp

input_paths=/neodc/eocis/data/global_and_regional/soil_moisture_africa/v2.3.1/daily/*/*/*.nc

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

