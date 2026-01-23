import json
import xarray as xr

ds = xr.open_dataset("EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-LANDCLASS-MERGED-2001-fv1.1.nc")

colours = ds["lccs_class"].attrs["flag_colors"].split(" ")
values = ds["lccs_class"].attrs["flag_values"].data.tolist()

mapping = {}

for (value, colour) in zip(values, colours):
    mapping[str(value)] = colour.upper()

with open("landclass_colours.json", "w") as f:
    f.write(json.dumps(mapping, indent=4))