
## netcdf2stac configuration file format

Each configuration file is a JSON formatted dictionary, with the following keys (incomplete)

| key               | purpose                                                                          |
|-------------------|----------------------------------------------------------------------------------|
| file_id_attribute | global attribute in each input file that provides a file-unique identifier string |
| global_attrs      | a list of global attributes to copy into the STAC item properties                |
| global_attr_map   | a dictionary mapping dataset global attribute names to STAC item property names  |
| kerchunk_url      | URL pattern for kerchunk assets                                                  |
| thumbnail_url     | URL pattern for thumbnail assets                                                 |
| netcdf_url        | URL pattern for netcdf assets                                                    |
| variable          | a reference variable that can be used to obtain the spatial and temporal extent  |
| dataset_id        | the name of the dataset                                                          |
| defaults=>item    | a dictionary containing metatdata to add to each STAC item properties            |
| kerchunk          | dictionary describing kerchunk configuration (TBC)                               |
| thumbnail         | dictionary describing thumbnail configuration (TBC)                              |

Some example configuration files:

* A set of defaults being developed for all EOCIS files: [eocis-defaults.json](eocis-defaults.json)
* Configration files for EOCIS SST CDRv3: [sst.json](sst.json)