#!/bin/bash

conda activate stac_tools_env

output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

. ../env.sh

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-slstr-monthly-s3a/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-slstr-monthly-s3b/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-slstr-daily-s3a/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-slstr-daily-s3b/items/*/*/*.geojson"

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-atsr-monthly-aatsr/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-atsr-monthly-atsr2/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-atsr-daily-aatsr/items/*/*/*.geojson"
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-items $output_folder"/eocis-aerosol-atsr-daily-atsr2/items/*/*/*.geojson"



