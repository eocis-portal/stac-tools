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

import xarray as xr
import numpy as np

from eocis_stac_tools.api.cog_generation import generate_cog

parser = argparse.ArgumentParser()
parser.add_argument("input_path")
parser.add_argument("variable_name")
parser.add_argument("output_path")
parser.add_argument("--nodata", default=None)
parser.add_argument("--dtype", default=None)
parser.add_argument("--crs", default=None)

args = parser.parse_args()

nodata_value = None
if args.nodata is not None:
    try:
        nodata_value = int(args.nodata)
    except:
        try:
            nodata_value = float(args.nodata)
        except:
            print("--nodata value must be integer or float")


ds = xr.open_dataset(args.input_path)
generate_cog(ds, args.variable_name, args.output_path, nodata_value=nodata_value, dtype=args.dtype, crs=args.crs)
ds.close()