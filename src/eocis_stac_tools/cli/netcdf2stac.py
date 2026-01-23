# MIT License
#
# Copyright (c) 2023-2024 National Centre for Earth Observation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Generate STAC item records from EOCIS datasets

Based on: https://github.com/EO-DataHub/eodh-eocis-sprint
"""
import logging
import sys

from ..api.netcdf2stac import Netcdf2Stac

def main():
    logging.basicConfig(level=logging.INFO)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-folder", help="folder to write STAC items to", required=True)
    parser.add_argument("--auxilary-folder", help="folder to write auxilary items to", required=True)
    parser.add_argument("--input-paths", nargs="+", help="path(s) to netcdf4 file(s)", required=True)
    parser.add_argument("--collection-filename", help="name of collection", default="collection.json")
    parser.add_argument("--parent-collection-path", help="path to a parent collection STAC record", default=None)
    parser.add_argument("--item-subfolder", help="name of folder for storing items", default="items")
    parser.add_argument("--config-paths", nargs="+", help="path to JSON configuration file(s)", required=True)
    parser.add_argument("--include-kerchunk", action="store_true", help="generate a kerchunk file for each item")
    parser.add_argument("--inline-kerchunk", action="store_true", help="inline kerchunk into each STAC item")
    parser.add_argument("--include-collection-thumbnail", action="store_true",
                        help="generate a thumbnail image for the collection based on the last processed item")
    parser.add_argument("--include-item-thumbnails", action="store_true", help="generate a thumbnail image for each item")
    parser.add_argument("--overwrite-items", action="store_true", help="overwrite item/kerchunk files if they already exist")
    parser.add_argument("--generate-cog", nargs="+",
                        help="generate cog files for the specified variables", default=[])
    parser.add_argument("--cog-nodata-values", nargs="*",
                        help="specify nodata values for generating cog files, format variable:<value>, for example myvar:-999", default=[])
    parser.add_argument("--cog-dtypes", nargs="*",
                        help="specify dtypes for generating cog files, format variable:<dtype>, for example myvar:int16", default=[])
    parser.add_argument("--cog-crs",
                        help="specify a crs for generating cog files, for example EPSG:27700", default=None)

    args = parser.parse_args()
    try:
        cog_dtypes = {}
        for cog_dtype in args.cog_dtypes:
            (variable,dtype) = cog_dtype.split(":")
            cog_dtypes[variable] = dtype

        cog_nodata_values = {}
        for cog_nodata_value in args.cog_nodata_values:
            (variable,nodata_value) = cog_nodata_value.split(":")
            try:
                nodata_value = int(nodata_value)
            except:
                try:
                    nodata_value = float(nodata_value)
                except:
                    print(f"--cog_nodata_nodata_value: {nodata_value} must be integer or float")
                    sys.exit(0)
            cog_nodata_values[variable] = nodata_value

        converter = Netcdf2Stac(base_folder=args.base_folder, auxilary_base_folder=args.auxilary_folder,
                                input_paths=args.input_paths,
                                collection_filename=args.collection_filename, item_subfolder=args.item_subfolder,
                                parent_collection_path=args.parent_collection_path,
                                config_paths=args.config_paths, generate_kerchunk_assets=args.include_kerchunk,
                                inline_kerchunk=args.inline_kerchunk,
                                generate_collection_thumbnail_asset=args.include_collection_thumbnail,
                                generate_item_thumbnail_assets=args.include_item_thumbnails,
                                overwrite_items=args.overwrite_items,
                                generate_cog=args.generate_cog,
                                cog_nodata_values=cog_nodata_values,
                                cog_dtypes=cog_dtypes,
                                cog_crs=args.cog_crs)
        converter.run()
    except Exception as ex:
        print(f"Error - {ex}")
        raise

if __name__ == "__main__":
    main()




