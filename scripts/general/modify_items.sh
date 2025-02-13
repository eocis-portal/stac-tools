#!/bin/bash

conda activate stac_tools_env

. ../env.sh

path=$1

if [ -z ${path} ];
then
    echo specify path of collection file
else
    uploadstac --url https://api.stac.ceda.ac.uk --oauth2-tokenurl "https://accounts.ceda.ac.uk/realms/ceda/protocol/openid-connect/token" --oauth2-clientid "eocis-stac" --oauth2-clientsecret $CLIENT_SECRET --modify-items $path"/**/*.geojson"
fi