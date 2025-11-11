#!/bin/bash

conda init

conda activate stac_tools_env

output_folder=stac-tmp

# input_paths_lai=/neodc/eocis/data/CHUK/land_vegetation_parameters/15_days/????/100m_gap_filled/1_LAI/*.nc
input_paths_lai=../../configurations/chuk_land_vegetation/data/EOCIS-LAI-L2-CHUK-LEAF-GAP-FILLED-100m-20201216-20201231-V1.nc

echo Generating STAC records for eocis-chuk-land-vegetation-lai

netcdf2stac --base-folder $output_folder/eocis-chuk-land-vegetation-lai \
    --auxilary-folder $output_folder/eocis-chuk-land-vegetation-lai-aux \
    --input-paths $input_paths_lai \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json \
            ../../configurations/chuk_land_vegetation/chuk_land_vegetation.json \
            ../../configurations/chuk_land_vegetation/chuk_land_vegetation_lai.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items

echo Generating STAC records for eocis-chuk-land-vegetation-fapar

# input_paths_fapar=/neodc/eocis/data/CHUK/land_vegetation_parameters/15_days/????/100m_gap_filled/2_FAPAR/*.nc
input_paths_fapar=../../configurations/chuk_land_vegetation/data/EOCIS-FAPAR-L2-CHUK-LEAF-GAP-FILLED-100m-20201216-20201231-V1.nc

netcdf2stac --base-folder $output_folder/eocis-chuk-land-vegetation-fapar \
    --auxilary-folder $output_folder/eocis-chuk-land-vegetation-fapar-aux \
    --input-paths $input_paths_fapar \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths ../../configurations/eocis-defaults.json \
            ../../configurations/chuk_land_vegetation/chuk_land_vegetation.json \
            ../../configurations/chuk_land_vegetation/chuk_land_vegetation_fapar.json \
    --include-kerchunk \
    --include-collection-thumbnail \
    --overwrite-items

