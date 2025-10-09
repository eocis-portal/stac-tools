# script for masking data according to the land cover dataset
# the masked data is useful for creating plots (see bigplot.sh)

import xarray as xr
import numpy as np

path_landcover = "../../data/EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCOVER-MERGED-2023-fv1.1.nc"
path_builtarea = "../../data/EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-BUILTAREA-MERGED-2023-fv1.1.nc"

ds = xr.open_dataset(path_landcover)

# look for pixels where landcover is not NO DATA and not salt water
land_mask = xr.where(np.logical_and(ds["land_cover"]>0,ds["land_cover"] != 13), True, False)

builtarea = xr.open_dataset(path_builtarea)["urban_area"]
builtarea = builtarea.where(land_mask, np.nan)

builtarea.to_netcdf("built_area_masked.nc")