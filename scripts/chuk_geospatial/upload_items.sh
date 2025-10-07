#!/bin/bash

. ../../env.sh

output_folder=stac-tmp

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder/"chuk-geospatial/items/*.geojson"





