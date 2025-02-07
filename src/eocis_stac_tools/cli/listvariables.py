import argparse
import xarray as xr
import json

parser = argparse.ArgumentParser()

parser.add_argument("path", help="Path to a sample netcdf4 input file")

args = parser.parse_args()

d = {
}

ds = xr.open_dataset(args.path)
for vname in ds.variables:
    if vname == "latitude" or vname == "longitde":
        pass
    o = {}
    v = ds[vname]
    if "units" in v.attrs:
        o["unit"] = v.attrs["units"]

    if "long_name" in v.attrs:
        o["description"] = v.attrs["long_name"]

    o["type"] = "data"
    o["dimensions"] = v.dims
    d[vname] = o


print(json.dumps({"cube:variables":d},indent=4))

