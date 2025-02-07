#!/bin/bash

conda activate stac_tools_env

output_folder=/gws/nopw/j04/eocis_chuk/stac-tmp

. ../env.sh

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --add-collection $output_folder/sst-cdrv3/collection.json
