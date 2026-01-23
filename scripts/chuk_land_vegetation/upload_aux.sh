#!/bin/bash

output_folder=stac-tmp

ssh dev@eocis.org rm -Rf /data/stac/eocis-chuk-land-vegetation-lai
ssh dev@eocis.org rm -Rf /data/stac/eocis-chuk-land-vegetation-fapar

ssh dev@eocis.org mkdir /data/stac/eocis-chuk-land-vegetation-lai
ssh dev@eocis.org mkdir /data/stac/eocis-chuk-land-vegetation-fapar

scp -r $output_folder/eocis-chuk-land-vegetation-lai-aux/items dev@eocis.org:/data/stac/eocis-chuk-land-vegetation-lai
scp -r $output_folder/eocis-chuk-land-vegetation-fapar-aux/items dev@eocis.org:/data/stac/eocis-chuk-land-vegetation-fapar
