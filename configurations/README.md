
## netcdf2stac configuration file format

Each configuration file is a JSON formatted dictionary, with the following keys:

| key                     | purpose                                                                                              |
|-------------------------|------------------------------------------------------------------------------------------------------|
| stac_collection_id*     | the stac collection id                                                                               |
| title*                  | collection title                                                                                     |
| description             | collection description text                                                                          |
| license*                | a license string                                                                                     |
| defaults.all            | properties to be added to items and collections                                                      |
| defaults.item           | properties to be added to items                                                                      |
| defaults.collection     | properties to be added to the collection                                                             |
| defaults.netcdf_asset   | properties to be added to netcdf assets                                                              |
| defaults.kerchunk_asset | properties to be added to kerchunk assets                                                            |
| file_id_attribute       | global attribute in each input file that provides a file-unique identifier string                    |
| global_attrs            | a list of global attributes to copy into the STAC item properties                                    |
| global_attr_map         | a dictionary mapping dataset global attribute names to STAC item property names                      |
| kerchunk_url*           | URL pattern for kerchunk assets.  The asset filename is appended to this URL.                        |
| thumbnail_url*          | URL pattern for thumbnail assets.  The asset filename is appended to this URL.                       |
| netcdf_url*             | URL pattern for netcdf assets.  The asset filename is appended to this URL.                          |
| variable*               | a reference variable that can be used to obtain the spatial and temporal extent                      |
| dataset_id              | the name of the dataset                                                                              |
| defaults=>item          | a dictionary containing metatdata to add to each STAC item properties                                |
| kerchunk                | dictionary describing kerchunk configuration (TBC)                                                   |
| thumbnail               | dictionary describing thumbnail configuration (TBC)                                                  |
| templated_properties    | templates for generating item properties based on dataset attributes and other metadata              |
 | date_extractor_path     | provide the relative path to python code that will extract datetimes instead of using time/time_bnds |

* these keys are required

Some example configuration files:

* A set of defaults being developed for all EOCIS files: [eocis-defaults.json](eocis-defaults.json)
* Configration files for EOCIS SST CDRv3: [sst.json](sst.json)

### date_extractor_path

This top-level configuration option can be used to create a custom extractor for obtaining dates and date intervals for each STAC item, based on the filepath and xarray dataset

It should only be used if the dataset cannot yied the correct values using the usual time/time_bnds variables

The code should define a `date_extract` function which is passed the file path and xarray dataset and returns a tuple of python datetime objects (start_date, date, end_date) 

For an example implementation see [date_extract.py](chuk_land_vegetation/date_extract.py)


