# stac-tools

Utilities to convert the metadata in EOCIS netcdf4 data file(s) to a STAC collection/item JSON file, generating any asset files as required, and uploading them to a STAC catalogue

## Summary

* netcdf2stac - convert EOCIS netcdf4 files to STAC collections/items, guided by one or more configuration files
* post_to_stac - post STAC files to a STAC API

## Dependencies

Suggested environment:

```
conda create -n stac_tools_env python=3.10
conda activate stac_tools_env
conda install xarray netcdf4 pystac pystac-client httpx requests kerchunk h5py aiohttp matplotlib zarr datashader pillow
```

## Installation

Clone the repo and install it in the environment, for example:

```
conda activate stac_tools_env
git clone git@github.com:eocis-portal/stac-tools.git
cd stac-tools
pip install -e .
```

This should install the `netcdf2stac and uploadstac` tools

## Creating STAC files

The tool `netcdf2stac` can be used to generate STAC files from EOCIS (or other) netcdf4 files.

```
netcdf2stac --help 

usage: netcdf2stac.py [-h] [--base-folder BASE_FOLDER]
                      [--input-paths INPUT_PATHS [INPUT_PATHS ...]]
                      [--collection-filename COLLECTION_FILENAME]
                      [--item-subfolder ITEM_SUBFOLDER] --config-paths
                      CONFIG_PATHS [CONFIG_PATHS ...] [--include-kerchunk]
                      [--include-thumbnails] [--overwrite-items]

options:
  -h, --help            show this help message and exit
  --base-folder BASE_FOLDER
                        folder to write STAC items to
  --input-paths INPUT_PATHS [INPUT_PATHS ...]
                        path(s) to netcdf4 file(s)
  --collection-filename COLLECTION_FILENAME
                        name of collection
  --item-subfolder ITEM_SUBFOLDER
                        name of folder for storing items
  --config-paths CONFIG_PATHS [CONFIG_PATHS ...]
                        path to JSON configuration file(s)
  --include-kerchunk    generate a kerchunk file for each item
  --include-thumbnails  generate a thumbnail image for each item
  --overwrite-items     overwrite item/kerchunk files if they already exist
```

### Example - convert EOCIS/ESACCI SST CDRv3 file to STAC, using two configuration files

```
netcdf2stac --base-folder /data/stac/sst-cdrv3 \
    --input-paths "/data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1/2020/*/*/*.nc" \
    --collection-filename collection.json \
    --item-subfolder "items/{year}/{month:02d}/" \
    --config-paths configs/eocis-defaults.json configs/sst.json \
    --include-kerchunk
    --include-thumbnails
```

This will:

* search through all the data files matching pattern `/data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1/2020/*/*/*.nc`
* update and create files under `/data/stac/sst-cdrv3`
* use the configuration files `configs/eocis-defaults.json` and `configs/sst.json` to guide the generation of STAC records
* update or create the file `/data/stac/sst-cdrv3/collection.json`
* update or create STAC item files,kerchunk files and thumbnail images under `/data/stac/sst-cdrv3/items/YYYY/MM/`

note that if multiple configuration files are supplied, they are merged, with later ones taking precedence over earlier ones

### Configuration file format

See [configurations/README](configurations/README.md) for examples and more details

### Testing

run unit tests in the test directory to generate STAC records from small sample netcdf4 EOCIS extracts

run the test/serve.py script to serve any generated STAC JSON records.  URLs for each STAC record should be printed on startup. 

You can paste URLs into the [radiant earth STAC browser](https://radiantearth.github.io/stac-browser/#/)

## Uploading STAC files to a STAC catalogue

Use the tool `uploadstac` to do this.

For example - to upload the collection and item files generated above:

```
uploadstac --url <URL of STAC catalog> --basicauth-username <username> --basicauth-password <password>  --add-collection /data/stac/sst-cdrv3/collection.json --add-items /data/stac/sst-cdrv3/items/*/*/*.geojson
```

Note that if the server authenticates using `oauth2` rather than `HTTP basic auth`, use the following options

```
uploadstac --url <URL of STAC catalog> --oauth2-tokenurl <token-url> --oauth2-clientid <client-id> --oauth2-clientsecret <client-secret>  --add-collection /data/stac/sst-cdrv3/collection.json --add-items /data/stac/sst-cdrv3/items/*/*/*.geojson
```

## Acknowledgements

Thank you to Ag Stephens, Rhys Evans and Jack Leland from the UK Science and Technology Facilities Council (STFC) for their help and advice on developing these tools.  

