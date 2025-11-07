#!/bin/bash

. ../../env.sh


# uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection eocis-chuk-geospatial-elevation --remove-collection eocis-chuk-geospatial-elevation
# uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection eocis-chuk-geospatial-builtarea --remove-collection eocis-chuk-geospatial-builtarea
# uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection eocis-chuk-geospatial-landcover --remove-collection eocis-chuk-geospatial-landcover

uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection eocis-chuk-geospatial --remove-collection eocis-chuk-geospatial