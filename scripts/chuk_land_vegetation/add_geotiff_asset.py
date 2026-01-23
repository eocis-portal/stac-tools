
import glob
import json

for dataset in ["fapar","lai"]:

    paths = glob.glob(f"stac-tmp/eocis-chuk-land-vegetation-{dataset}/**/*.geojson", recursive=True)
    for path in paths:
        print(f"Processing {path}")
        with open(path) as f:
            o = json.loads(f.read())
        data_asset = None
        for key,asset in o["assets"].items():
            if asset["type"] == "application/netcdf":
                data_asset = {
                    "href": f"https://eocis.org/data/land_vegetation/{dataset}/{key}.tif",
                    "type": "image/tiff; application=geotiff",
                    "roles": [
                        "data"
                    ]
                }
        if data_asset is None:
            print("Error - unable to process asset")
        else:
            o["assets"]["data"] = data_asset
            with open(path, "w") as f:
                f.write(json.dumps(o, indent=4))

