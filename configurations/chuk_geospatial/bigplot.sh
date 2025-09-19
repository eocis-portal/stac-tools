#!/bin/bash

conda activate netcdfexplorer_env

if [ -f "EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-ELEVATION-MERGED-2023-fv1.0.nc" ];
then
  bigplot --input-path EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-ELEVATION-MERGED-2023-fv1.0.nc \
         --input-variable elevation \
         --output-path EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-ELEVATION-MERGED-2023-fv1.0.png \
         --plot-width 512 --flip --cmap viridis --vmin 0 --vmax 1200 --legend-height 0
fi

if [ -f "EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCOVER-MERGED-2023-fv1.1.nc" ];
then
   bigplot --input-path EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCOVER-MERGED-2023-fv1.1.nc \
         --input-variable land_cover \
         --output-path EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCOVER-MERGED-2023-fv1.1.png \
         --plot-width 512 --flip --cchart landcover_colours.json --vmin 0 --vmax 1200 --legend-height 0
fi
