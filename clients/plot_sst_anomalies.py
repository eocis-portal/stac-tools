# stac demo

import datetime

from pystac_client import Client
import xarray as xr
import matplotlib.pyplot as plt

# define a helper function that will return an xarray dataset given a stac item
def open_dataset_from_stac_item(item):
    for (key, value) in item.assets.items():
        if key == "reference_file":
            return xr.open_dataset("reference://", engine="zarr", backend_kwargs={
                "consolidated": False,
                "storage_options": {"fo": value.href, "remote_protocol": "https", "remote_options": {}}
            })
    return None

# open the STAC endpoint
client = Client.open("https://api.stac.ceda.ac.uk")

# search for the SST climatology items, one for each day of the year
search = client.search(
        collections=['eocis-sst-cdrv3-climatology']
    )

# for each climatology item, add it to a lookup table
climatology_item_lookup = {}
for item in search.item_collection().items:
    day_of_year = item.properties["day_of_year"]
    climatology_item_lookup[day_of_year] = item

# search for SST data, early Jan 2023
search = client.search(
    collections=['eocis-sst-cdrv3'],
    datetime=(datetime.datetime(2023,1,1,0,0,0),datetime.datetime(2023,1,4,23,59,59))
)

# go through the items returned from the search, calculate the anomalies and add them to a list
data = []
for item in search.item_collection().items:
    sst = open_dataset_from_stac_item(item).analysed_sst.sel(lat=slice(48,61),lon=slice(-12,3)).squeeze()
    day_of_year = item.datetime.timetuple()[7]
    sst_climatology = open_dataset_from_stac_item(climatology_item_lookup[day_of_year]).analysed_sst.sel(lat=slice(48,61),lon=slice(-12,3))
    anomaly = sst - sst_climatology
    data.append(anomaly)

# concatenate data array items into a single dataset
da = xr.concat(data,dim="time")

# take the mean along the time dimension, and plot it
da = da.mean(dim="time")
da.plot()
plt.show()

