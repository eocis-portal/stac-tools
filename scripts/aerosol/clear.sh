#!/bin/bash

conda activate stac_tools_env

. ../env.sh

for COLLECTION_NAME in eocis-aerosol-slstr-monthly-s3a eocis-aerosol-slstr-monthly-s3b eocis-aerosol-slstr-daily-s3a eocis-aerosol-slstr-daily-s3b \
       eocis-aerosol-atsr-monthly-atsr2 eocis-aerosol-atsr-monthly-aatsr eocis-aerosol-atsr-daily-atsr2 eocis-aerosol-atsr-daily-aatsr
do
  uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --clear-collection $COLLECTION_NAME --remove-collection $COLLECTION_NAME
done