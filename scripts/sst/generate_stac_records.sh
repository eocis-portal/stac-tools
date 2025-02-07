#!/bin/bash

conda activate stac_tools_env

# output_folder=stac
output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

netcdf2stac --base-folder $output_folder/sst-cdrv3 \
    --auxilary-folder $output_folder/sst-cdrv3-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/sea_surface_temperature/CDR_v3/Analysis/L4/v3.0.1/*/*/*/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/sst.json \
    --include-kerchunk \
    --include-collection-thumbnail