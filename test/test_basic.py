import unittest
import os

from eocis_stac_tools.api.netcdf2stac import Netcdf2Stac

test_folder = os.path.split(__file__)[0]

class BasicTest(unittest.TestCase):

    def test_basic(self):
        config_paths = [
            os.path.join(test_folder, "..", "configurations","eocis-defaults.json"),
            os.path.join(test_folder, "..", "configurations", "sst.json"),
            os.path.join(test_folder, "configurations", "sst.json")
        ]

        converter = Netcdf2Stac(
            base_folder="./stac-generated",
            auxilary_base_folder="./stac-generated/aux",
            input_paths=[os.path.join(test_folder,"sst","data","2022","*","*","*.nc")],
            collection_filename="sst-collection.geojson",
            config_paths=config_paths,
            item_subfolder="sst-items/{year}/{month:02d}/",
            generate_netcdf_assets=True,
            generate_kerchunk_assets=True,
            generate_collection_thumbnail_asset=True)

        converter.run()

    def test_basic_sm(self):
        config_paths = [
            os.path.join(test_folder, "..", "configurations","eocis-defaults.json"),
            os.path.join(test_folder, "configurations", "sm.json")
        ]

        converter = Netcdf2Stac(
            base_folder="./stac-generated",
            auxilary_base_folder="./stac-generated/aux",
            input_paths=[os.path.join(test_folder,"sm","data","2024","**","*.nc")],
            collection_filename="sm-collection.geojson",
            config_paths=config_paths,
            item_subfolder="sm-items/{year}/{month:02d}/",
            generate_netcdf_assets=True,
            generate_kerchunk_assets=True)

        converter.run()

    def test_basic_lst(self):
        config_paths = [
            os.path.join(test_folder, "..", "configurations", "eocis-defaults.json"),
            os.path.join(test_folder, "..", "configurations", "lst.json")
        ]

        paths = [
            "/home/dev/Downloads/EOCIS_-LST-L3C-LST-SLSTRA-0.01deg_1DAILY_DAY-20241015000000-fv4.00.nc",
            "/home/dev/Downloads/EOCIS_-LST-L3C-LST-SLSTRA-0.01deg_1DAILY_DAY-20241016000000-fv4.00.nc",
            "/home/dev/Downloads/EOCIS_-LST-L3C-LST-SLSTRA-0.01deg_1DAILY_DAY-20241017000000-fv4.00.nc",
            "/home/dev/Downloads/EOCIS_-LST-L3C-LST-SLSTRA-0.01deg_1DAILY_DAY-20241018000000-fv4.00.nc",
            "/home/dev/Downloads/EOCIS_-LST-L3C-LST-SLSTRA-0.01deg_1DAILY_DAY-20241019000000-fv4.00.nc",
            "/home/dev/Downloads/EOCIS_-LST-L3C-LST-SLSTRA-0.01deg_1DAILY_DAY-20241020000000-fv4.00.nc"]

        converter = Netcdf2Stac(
            base_folder="./stac-generated",
            auxilary_base_folder="./stac-generated/aux",
            input_paths=paths,
            collection_filename="lst-collection.geojson",
            config_paths=config_paths,
            item_subfolder="lst-items/{year}/{month:02d}/",
            generate_netcdf_assets=True,
            generate_kerchunk_assets=True,
            generate_collection_thumbnail_asset=True)

        converter.run()
