#!/bin/bash

conda activate stac_tools_env

. ../../env.sh

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection eocis-chuk-land-vegetation-lai --remove-collection eocis-chuk-land-vegetation-lai
uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection eocis-chuk-land-vegetation-fapar --remove-collection eocis-chuk-land-vegetation-fapar