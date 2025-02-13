#!/bin/bash

conda activate stac_tools_env

output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

echo Generating STAC records for eocis-aerosol-slstr-monthly-s3a

netcdf2stac --base-folder $output_folder/eocis-aerosol-slstr-monthly-s3a \
    --auxilary-folder $output_folder/eocis-aerosol-slstr-monthly-s3a-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/SU_aerosol/SLSTR/L3C/monthly/v1.14.1/SLSTR-A/*/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/aerosol/aerosol.json ../../configurations/aerosol/aerosol-slstr-monthly-S3A.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items

echo Generating STAC records for eocis-aerosol-slstr-monthly-s3b

netcdf2stac --base-folder $output_folder/eocis-aerosol-slstr-monthly-s3b \
    --auxilary-folder $output_folder/eocis-aerosol-slstr-monthly-s3b-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/SU_aerosol/SLSTR/L3C/monthly/v1.14.1/SLSTR-B/*/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/aerosol/aerosol.json ../../configurations/aerosol/aerosol-slstr-monthly-S3B.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items

echo Generating STAC records for eocis-aerosol-slstr-daily-s3a

netcdf2stac --base-folder $output_folder/eocis-aerosol-slstr-daily-s3a \
    --auxilary-folder $output_folder/eocis-aerosol-slstr-daily-s3a-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/SU_aerosol/SLSTR/L3C/daily/v1.14.1/SLSTR-A/*/*/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/aerosol/aerosol.json ../../configurations/aerosol/aerosol-slstr-daily-S3A.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items

echo Generating STAC records for eocis-aerosol-slstr-daily-s3b

netcdf2stac --base-folder $output_folder/eocis-aerosol-slstr-daily-s3b \
    --auxilary-folder $output_folder/eocis-aerosol-slstr-daily-s3b-aux \
    --input-paths "/neodc/eocis/data/global_and_regional/SU_aerosol/SLSTR/L3C/daily/v1.14.1/SLSTR-B/*/*/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json ../../configurations/aerosol/aerosol.json ../../configurations/aerosol/aerosol-slstr-daily-S3B.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items


