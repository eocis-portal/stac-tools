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
    parser.add_argument("--item-subfolder", help="name of folder for storing items", default="items")
    parser.add_argument("--config-paths", nargs="+", help="path to JSON configuration file(s)", required=True)
    parser.add_argument("--include-kerchunk", action="store_true", help="generate a kerchunk file for each item")
    parser.add_argument("--inline-kerchunk", action="store_true", help="inline kerchunk into each STAC item")
    parser.add_argument("--include-collection-thumbnail", action="store_true",
                        help="generate a thumbnail image for the collection based on the last processed item")
    parser.add_argument("--overwrite-items", action="store_true", help="overwrite item/kerchunk files if they already exist")


    args = parser.parse_args()
    try:
        converter = Netcdf2Stac(base_folder=args.base_folder, auxilary_base_folder=args.auxilary_folder,
                                input_paths=args.input_paths,
                                collection_filename=args.collection_filename, item_subfolder=args.item_subfolder,
                                config_paths=args.config_paths, generate_kerchunk_assets=args.include_kerchunk,
                                inline_kerchunk=args.inline_kerchunk,
                                generate_collection_thumbnail_asset=args.include_collection_thumbnail,
                                overwrite_items=args.overwrite_items)
        converter.run()
    except Exception as ex:
        print(f"Error - {ex}")
        raise

if __name__ == "__main__":
    main()




