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

import datetime
import sys
import os
import hashlib
import json
import uuid
import glob
import logging
import base64

import pystac
import pandas

import xarray as xr
from kerchunk.hdf import SingleHdf5ToZarr
from .thumbnail import Thumbnail

def expand_dt_template(s, dt):
    return s.format(**{
        "year": dt.year,
        "month": dt.month,
        "day": dt.day
    })

def floats(seq):
    return [float(x) for x in seq]

class NCFileInspector:

    def __init__(self, fpath, var_id, config):
        self.config = config
        self.ds = xr.open_dataset(fpath)
        self.var_id = var_id
        self.var = self.ds[var_id]

    def global_attr(self, key):
        return self.ds.attrs.get(key, None)

    def get_var_props(self):
        attrs = self.var.attrs
        vprops = {
            "variable_id": self.var_id,
            "variable_long_name": attrs.get("long_name", None),
            "variable_units": attrs.get("units", None),
            "cf_standard_name": attrs.get("standard_name", None)
        }
        return vprops

    def get_properties(self):
        props = {}
        for key in self.config["global_attrs"]:
            value = self.global_attr(key)
            key = self.config["global_attr_map"].get(key, key)

            if isinstance(value, str) and value.lower() in ("null", "none"):
                value = None

            props[key] = value
        return props

    def get_datetime(self, index=0):
        return pandas.Timestamp(self.ds.time.values[index]).to_pydatetime().replace(tzinfo=datetime.timezone.utc)

    def get_bbox(self):
        # use the geopspatial min/max metdata if present
        geospatial_lat_min = self.ds.attrs.get("geospatial_lat_min", None)
        geospatial_lat_max = self.ds.attrs.get("geospatial_lat_max", None)
        geospatial_lon_min = self.ds.attrs.get("geospatial_lon_min", None)
        geospatial_lon_max = self.ds.attrs.get("geospatial_lon_max", None)
        metadata_valid = True
        for v in [geospatial_lat_min, geospatial_lon_min, geospatial_lat_max, geospatial_lon_max]:
            if v is None:
                metadata_valid = False
        if metadata_valid:
            return floats([geospatial_lon_min, geospatial_lat_min, geospatial_lon_max, geospatial_lat_max])
        # otherwise, extract from the data
        lt = self.ds["lat"]
        ln = self.ds["lon"]
        return floats([ln.min(), lt.min(), ln.max(), lt.max()])

    def get_level(self):
        try:
            levels = self.ds.cf["Z"].values
            return floats([levels[0], levels[-1]])
        except Exception as exc:
            return None

    def get_dataset(self):
        return self.ds



def sha256(fpath):
    # fake hack to not fail if file doesn't exist
    content = open(fpath, "rb").read() if os.path.isfile(fpath) else fpath.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def get_geometry(bbox):
    lon_min = bbox[0]
    lat_min = bbox[1]
    lon_max = bbox[2]
    lat_max = bbox[3]
    return {
        "type": "Polygon",
        "coordinates": [
            [[lon_min, lat_min], [lon_max, lat_min], [lon_max, lat_max], [lon_min, lat_max], [lon_min, lat_min]]
        ]
    }

def get_netcdf_asset_dict(fpath, config, dt):
    d = {
        "href": f"{expand_dt_template(config['netcdf_url'], dt)}{fpath}",
    }
    d.update(config["defaults"]["netcdf_asset"])
    return d

def get_kerchunk_asset_dict(fpath, config, dt):
    d = {
        "href": f"{expand_dt_template(config['kerchunk_url'], dt)}{fpath}",
    }
    d.update(config["defaults"]["kerchunk_asset"])
    return d

def get_thumbnail_asset_dict(fpath, config, dt):
    d = {
        "href": f"{expand_dt_template(config['thumbnail_url'], dt)}{fpath}",
    }
    if "thumbnail_asset" in config["defaults"]:
        d.update(config["defaults"]["thumbnail_asset"])
    return d

def generate_kerchunk(filepath, url, outpath):
    with open(filepath, "rb") as f:
        h5chunks = SingleHdf5ToZarr(f, url, inline_threshold=300)
        with open(outpath, "wb") as of:
            of.write(json.dumps(h5chunks.translate(), indent=4).encode())

class Netcdf2Stac:

    def __init__(self, base_folder, input_paths, config_paths, collection_filename="collection.json", item_subfolder="items",
                 generate_kerchunk_assets=True, inline_kerchunk=False, generate_netcdf_assets=True, generate_thumbnail_assets=True,
                 overwrite_items=False):
        self.base_folder = base_folder
        self.input_paths = input_paths
        self.collection_filename = collection_filename
        self.collection_path = os.path.join(self.base_folder,self.collection_filename)
        self.item_subfolder = item_subfolder
        self.config_paths = config_paths

        self.start_date = None
        self.end_date = None
        self.bbox = None
        self.collection = None

        self.logger = logging.getLogger("Netcdf2Stac")

        self.generate_kerchunk_assets = generate_kerchunk_assets
        self.inline_kerchunk = inline_kerchunk
        self.generate_netcdf_assets = generate_netcdf_assets
        self.generate_thumbnail_assets = generate_thumbnail_assets
        self.overwrite_items = overwrite_items

        def merge(d1, d2):
            # recursively merge configurations d1 and d2, give d2 priority
            if d2 is None:
                return d1
            if d1 is None:
                return d2
            if isinstance(d1, list) and isinstance(d2, list):
                return d1 + d2
            if isinstance(d1, dict) and isinstance(d2, dict):
                all_keys = list(set(list(d1.keys()) + list(d2.keys())))
                merged = {}
                for k in all_keys:
                    merged[k] = merge(d1.get(k, None), d2.get(k, None))
                return merged
            # fallback, ignore d1, return d2
            return d2

        self.config = {}
        for config_path in self.config_paths:
            with open(config_path) as f:
                self.config = merge(self.config, json.loads(f.read()))

        self.climatology_interval = None
        if "climatology_interval" in self.config:
            self.climatology_interval = (datetime.datetime.strptime(self.config["climatology_interval"][0],"%Y-%m-%d"),datetime.datetime.strptime(self.config["climatology_interval"][1],"%Y-%m-%d"))

        if os.path.exists(self.collection_path):
            with open(self.collection_path) as f:
                o = json.loads(f.read())
                self.collection = pystac.Collection.from_dict(o)
                self.start_date = self.collection.extent.temporal.intervals[0][0]
                self.end_date = self.collection.extent.temporal.intervals[0][1]
                self.bbox = self.collection.extent.spatial.bboxes[0]
                self.logger.info(f"Loaded existing collection {self.start_date} - {self.end_date}")
        else:
            self.collection = pystac.Collection(id=self.config.get("stac_collection_id", str(uuid.uuid4())),
                                                href=self.collection_filename,
                                                extent=None,
                                                description=self.config.get("stac_collection_description", ""),
                                                stac_extensions=[
                                                    "https://stac-extensions.github.io/cf/v0.2.0/schema.json"],
                                                catalog_type=pystac.CatalogType.SELF_CONTAINED)

        if generate_thumbnail_assets and "thumbnail" in self.config:
            tcfg = self.config["thumbnail"]
            self.thumbnail_generator = Thumbnail(
                variable=tcfg["variable"],
                cmap=tcfg["cmap"],
                vmin=tcfg["vmin"],
                vmax=tcfg["vmax"],
                x_coord=tcfg["x-coordinate"],
                y_coord=tcfg["y-coordinate"],
                plot_width=tcfg["width"]
            )
        else:
            self.thumbnail_generator = None

    def run(self):
        os.makedirs(self.base_folder, exist_ok=True)

        for input_pattern in self.input_paths:
            for fpath in glob.glob(input_pattern,recursive=True):
                self.process_item(fpath)

        if self.collection_path:
            self.finalise_collection()

    def finalise_collection(self):
        spatial_extent = pystac.SpatialExtent([self.bbox])
        temporal_extent = pystac.TemporalExtent([self.start_date, self.end_date]) if self.climatology_interval is None else pystac.TemporalExtent(list(self.climatology_interval))
        extent = pystac.Extent(spatial_extent, temporal_extent)
        self.collection.extent = extent
        with open(self.collection_path, "w") as f:
            f.write(json.dumps(self.collection.to_dict(include_self_link=False), indent=4))

    def process_item(self, fpath):
        input_filename = os.path.split(fpath)[-1]

        self.logger.info(f"Processing item {fpath}")

        var_id = self.config["variable"]
        dset_id = self.config["dataset_id"]

        i = NCFileInspector(fpath, var_id, self.config)
        bbox = i.get_bbox()

        if self.bbox is None:
            self.bbox = bbox
        else:
            min_x = bbox[0]
            min_y = bbox[1]
            max_x = bbox[2]
            max_y = bbox[3]
            if min_x < self.bbox[0]:
                self.bbox[0] = min_x
            if min_y < self.bbox[1]:
                self.bbox[1] = min_y
            if max_x > self.bbox[2]:
                self.bbox[2] = max_x
            if max_y > self.bbox[3]:
                self.bbox[3] = max_y

        dt = i.get_datetime(0)

        item_subfolder = expand_dt_template(self.item_subfolder,dt)
        os.makedirs(os.path.join(self.base_folder, item_subfolder), exist_ok=True)
        item_subfolder_levels = len(item_subfolder.split("/"))
        kerchunk_filename = os.path.splitext(input_filename)[0] + "-kerchunk.json"
        kerchunk_filepath = os.path.join(self.base_folder, item_subfolder, kerchunk_filename)
        output_filename = os.path.splitext(input_filename)[0] + ".geojson"
        output_filepath = os.path.join(self.base_folder, item_subfolder, output_filename)
        if not self.overwrite_items:
            if os.path.exists(output_filepath):
                if not self.generate_kerchunk_assets or os.path.exists(kerchunk_filepath):
                    self.logger.info(f"Skipping item {fpath}, output already exists")
                    return

        if self.start_date is None or dt < self.start_date:
            self.start_date = dt
        if self.end_date is None or dt > self.end_date:
            self.end_date = dt

        item_id = str(uuid.uuid4())

        props = self.config.get("defaults", {}).get("item", {})

        props.update(i.get_properties())

        # Add dataset ID
        props[self.config["dset_id_name"]] = dset_id

        # Add templated properties
        for prop, tmpl in self.config["templated_properties"].items():
            props[prop] = tmpl.format(**vars())

        if self.climatology_interval is not None:
            props["day_of_year"] = dt.timetuple()[7]

        input_filename = os.path.split(fpath)[-1]

        output_filename = os.path.splitext(input_filename)[0] + ".geojson"

        date_arguments = {}
        if self.climatology_interval is None:
            date_arguments["datetime"] = dt
        else:
            date_arguments["datetime"] = dt
            date_arguments["start_datetime"] = self.climatology_interval[0]
            date_arguments["end_datetime"] = self.climatology_interval[1]

        item = pystac.Item(id=item_id,
                           href=output_filename,
                           collection=self.collection,
                           bbox = bbox,
                           properties=props,
                           geometry=get_geometry(bbox),
                           stac_extensions=["https://stac-extensions.github.io/cf/v0.2.0/schema.json"],
                           **date_arguments)


        item.clear_links()

        if self.collection_path:
            superfolder = os.path.join(*([".."]*item_subfolder_levels))
            clink = pystac.Link(rel="collection", target=os.path.join(superfolder,self.collection_filename), media_type="application/json")
            item.add_link(clink)

        netcdf_filename = os.path.split(fpath)[-1]
        asset_dict = get_netcdf_asset_dict(netcdf_filename, self.config, dt)
        netcdf_href = asset_dict["href"]

        if self.generate_kerchunk_assets:
            kerchunk_asset_dict = get_kerchunk_asset_dict(kerchunk_filename, self.config, dt)

            generate_kerchunk(fpath, netcdf_href, kerchunk_filepath)
            href = kerchunk_asset_dict["href"]
            del kerchunk_asset_dict["href"]
            if self.inline_kerchunk:
                with open(kerchunk_filepath,"rb") as f:
                    kerchunk_content = f.read()
                    href = "data:application/json;base64,"+base64.b64encode(kerchunk_content).decode()
            asset_key = "reference_file"
            kerchunk_asset = pystac.Asset(href=href,
                                 roles=["reference","data"],
                                 media_type="application/zstd",
                                 extra_fields=kerchunk_asset_dict)
            item.add_asset(asset_key, kerchunk_asset)

        if self.generate_netcdf_assets:
            asset_key = os.path.splitext(netcdf_filename)[0]
            del asset_dict["href"]
            asset = pystac.Asset(href=netcdf_href,
                                 roles=["data"],
                                 media_type="application/netcdf",
                                 extra_fields=asset_dict)
            item.add_asset(asset_key,asset)

        if self.thumbnail_generator:
            thumbnail_filename = os.path.splitext(input_filename)[0] + ".png"
            thumbnail_filepath = os.path.join(self.base_folder, item_subfolder, thumbnail_filename)
            asset_dict = get_thumbnail_asset_dict(thumbnail_filename, self.config, dt)
            href = asset_dict["href"]
            del asset_dict["href"]
            self.thumbnail_generator.generate(i.get_dataset(), thumbnail_filepath)
            asset = pystac.Asset(href=href,
                                 roles=["thumbnail"],
                                 media_type="image/png",
                                 extra_fields=asset_dict)
            item.add_asset("thumbnail", asset)

        with open(output_filepath,"w") as f:
            o = item.to_dict(include_self_link=False)
            f.write(json.dumps(o,indent=4))



