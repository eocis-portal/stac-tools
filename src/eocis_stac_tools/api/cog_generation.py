# MIT License
#
# Copyright (c) 2023-2024 National Centre for Earth Observation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os

import rasterio as rio
import xarray as xr
import numpy as np


def generate_cog(ds: xr.Dataset, variable_name: str, to_path: str, dtype:str = None, nodata_value=None, crs:str=None):
    """
    Save a CHUK dataset to a geotiff

    Args:
        ds: the CHUK dataset
        variable_name: the name of the variable to save from the dataset
        to_path: the path to save the geotiff file to
        dtype: alter the dtype when creating the COG
        nodata_value: the nodata value to use when creating the COG
        crs: the coordinate reference system to use when creating the COG, format EPSG:XXXXX
    """

    ds = ds.copy(deep=True)
    if dtype is not None:
        ds[variable_name] = ds[variable_name].astype(dtype)
    if nodata_value is not None:
        ds[variable_name] = xr.where(np.isnan(ds[variable_name]), nodata_value, ds[variable_name])
        ds[variable_name].rio.write_nodata(nodata_value, inplace=True)
    kwargs = {}
    if dtype is not None:
        kwargs["dtype"] = dtype
    if crs is not None:
        ds.rio.write_crs(crs, inplace=True)
    ds[variable_name].rio.to_raster(to_path,  driver="COG", **kwargs)
    ds.close()

