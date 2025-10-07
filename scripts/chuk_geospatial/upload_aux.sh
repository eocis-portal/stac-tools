#!/bin/bash

output_folder=stac-tmp

scp $output_folder/chuk-geospatial-aux/items/* dev@eocis.org:/data/stac/eocis-chuk-geospatial
