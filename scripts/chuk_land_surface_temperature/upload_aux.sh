#!/bin/bash

output_folder=stac-tmp

ssh dev@eocis.org rm -Rf /data/stac/eocis-chuk-lst

ssh dev@eocis.org mkdir /data/stac/eocis-chuk-lst

scp -r $output_folder/eocis-chuk-lst-aux/items dev@eocis.org:/data/stac/eocis-chuk-lst
