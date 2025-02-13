#!/bin/bash

conda activate stac_tools_env

. ../env.sh

for COLLECTION_NAME in eocis-lst-s3a-day eocis-lst-s3b-day eocis-lst-s3a-night eocis-lst-s3b-night
do
    uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection $COLLECTION_NAME --remove-collection $COLLECTION_NAME
done