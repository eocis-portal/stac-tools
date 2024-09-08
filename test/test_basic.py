import unittest
import os

from eocis_stac_tools.api.netcdf2stac import Netcdf2Stac

test_folder = os.path.split(__file__)[0]

class BasicTest(unittest.TestCase):

    def test_basic(self):
        config_paths = [
            os.path.join(test_folder, "configurations","eocis-defaults.json"),
            os.path.join(test_folder, "configurations", "sst.json")
        ]

        converter = Netcdf2Stac(
            base_folder="./stac-generated",
            input_paths=[os.path.join(test_folder,"sst","data","2022","**","**","*.nc")],
            collection_filename="sst-collection.geojson",
            config_paths=config_paths,
            item_subfolder="sst-items/{year}/{month:02d}/",
            generate_netcdf_assets=True,
            generate_kerchunk_assets=True,
            generate_thumbnail_assets=True)

        converter.run()


