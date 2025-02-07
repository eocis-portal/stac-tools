#!/bin/bash

conda activate stac_tools_env

output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

. ../env.sh

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-lst-s3a-day/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-lst-s3b-day/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-lst-s3a-night/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-lst-s3b-night/items/*/*/*.geojson"




