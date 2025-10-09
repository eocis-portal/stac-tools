#!/bin/bash

conda activate stac_tools_env

output_folder=stac-tmp

echo Generating STAC records for eocis-arctic-sea-ice-thickness-monthly

netcdf2stac --base-folder $output_folder/eocis-arctic-sea-ice-thickness-monthly \
    --auxilary-folder $output_folder/eocis-arctic-sea-ice-thickness-monthly-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/arctic_sea_ice/arctic_sea_ice_thickness_grids/L3C/monthly/v1.0/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/arctic_sea_ice/arctic_sea_ice.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items
