#!/bin/bash

conda activate stac_tools_env

output_folder=stac-tmp

. ../env.sh

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-collection $output_folder/eocis-chuk-land-vegetation-lai/collection.json
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-collection $output_folder/eocis-chuk-land-vegetation-fapar/collection.json