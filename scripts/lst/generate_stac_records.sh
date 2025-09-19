#!/bin/bash

conda activate stac_tools_env

# output_folder=stac
output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

echo Generating STAC records for S3A Day

netcdf2stac --base-folder $output_folder/eocis-lst-s3a-day \
    --auxilary-folder $output_folder/eocis-lst-s3a-day-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/land_surface_temperature/SENTINEL3A_SLSTR/L3C/0.01/v4.00/daily/*/*/*/*DAY*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/lst/lst.json ../../configurations/lst/lst-day-A.json \
    --include-kerchunk \
    --include-collection-thumbnail

echo Generating STAC records for S3B Day

netcdf2stac --base-folder $output_folder/eocis-lst-s3b-day \
    --auxilary-folder $output_folder/eocis-lst-s3b-day-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/land_surface_temperature/SENTINEL3B_SLSTR/L3C/0.01/v4.00/daily/*/*/*/*DAY*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/lst/lst.json ../../configurations/lst/lst-day-B.json \
    --include-kerchunk \
    --include-collection-thumbnail

echo Generating STAC records for S3A Night

netcdf2stac --base-folder $output_folder/eocis-lst-s3a-night \
    --auxilary-folder $output_folder/eocis-lst-s3a-night-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/land_surface_temperature/SENTINEL3A_SLSTR/L3C/0.01/v4.00/daily/*/*/*/*NIGHT*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/lst/lst.json ../../configurations/lst/lst-night-A.json \
    --include-kerchunk \
    --include-collection-thumbnail

echo Generating STAC records for S3B Night

netcdf2stac --base-folder $output_folder/eocis-lst-s3b-night \
    --auxilary-folder $output_folder/eocis-lst-s3b-night-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/land_surface_temperature/SENTINEL3B_SLSTR/L3C/0.01/v4.00/daily/*/*/*/*NIGHT*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/lst/lst.json ../../configurations/lst/lst-night-B.json \
    --include-kerchunk \
    --include-collection-thumbnail