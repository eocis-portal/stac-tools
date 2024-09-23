# stac demo

import datetime

from pystac_client import Client
import xarray as xr
import matplotlib.pyplot as plt

# open the STAC endpoint
client = Client.open("https://api.stac.ceda.ac.uk")

# search for SST data, early Jan 2020
search = client.search(
    collections=['eocis-sst-cdrv3'],
    bbox=[
        -180.0,
        -90.0,
        180.0,
         90.0
    ],
    datetime=(datetime.datetime(2020,1,1),datetime.datetime(2020,1,4,12,0,0))
)

# define a helper function that will get the kerchunk url from each stac item
def get_kerchunk_url(from_item):
    for (key,value) in from_item.assets.items():
        if value.media_type == "application/json":
            return value.href
    return None

# go through the items returned from the search, open the dataset via kerchunk, append the dataset to a list
data = []
for item in search.item_collection().items:
    print(item.datetime)
    kurl = get_kerchunk_url(item)
    ds = xr.open_dataset("reference://", engine="zarr", backend_kwargs={
                    "consolidated": False,
                    "storage_options": {"fo": kurl, "remote_protocol": "https","remote_options": {}}
                    })

    data.append(ds.sel(lat=slice(48,61),lon=slice(-12,3)))

# concatenate each dataset's items into a single dataset
ds = xr.concat(data,dim="time")

# take the mean along the time dimension, and plot it
da = ds["analysed_sst"].mean(dim="time")
da.plot()
plt.show()