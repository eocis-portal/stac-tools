#!/bin/bash

conda activate chuk_api_env

CHUK_GRID_PATH=EOCIS-CHUK-GRID-100M-v1.0.nc

INPUT_FILE=$1
INPUT_VARIABLE=$2
OUTPUT_FILE=$3

python ~/github/chuk-api/utils/convert_to_tiff.py $INPUT_FILE $INPUT_VARIABLE land_cover $CHUK_GRID_PATH $OUTPUT_FILE