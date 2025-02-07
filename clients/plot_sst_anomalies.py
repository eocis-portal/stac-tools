# stac demo

import time
import datetime
import os.path

from pystac_client import Client
import xarray as xr
import matplotlib.pyplot as plt
import logging

# define a helper function that will return an xarray dataset given a stac item
def open_dataset_from_stac_item(item):
    for (key, value) in item.assets.items():
        if key == "reference_file":
            return xr.open_mfdataset(["reference://"], engine="zarr", backend_kwargs={
                "consolidated": False,
                "storage_options": {"fo": value.href, "remote_protocol": "https", "remote_options": {}}
            })


    return None

# open the STAC endpoint
client = Client.open("https://api.stac.ceda.ac.uk")

search = client.search(
    collections=['eocis-lst-s3a-day'],
    datetime=(datetime.datetime(2022,12,31,0,0,0),datetime.datetime(2022,12,31,23,59,59))
)

from save import Importer

logging.basicConfig(level=logging.INFO)
for item in search.item_collection().items:
    ds = open_dataset_from_stac_item(item)
    ds = ds.sel(lat=slice(50,60),lon=slice(-15,5))
    print(ds)
    t1 = time.time()
    i = Importer(ds,["lst","ndvi"])
    ds = i.import_dataset()
    ds.to_netcdf("final.nc", encoding={
                    "lst": {"zlib": True, "complevel": 5, "dtype": "float32", "chunksizes":[1,1000,1000]},
                    "ndvi": {"zlib": True, "complevel": 5, "dtype": "float32", "chunksizes": [1, 1000, 1000]}
                })
    i.close()
    t2 = time.time()
    print(int(t2-t1))


