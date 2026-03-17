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
import os
import hashlib
import json
import uuid
import glob
import logging
import base64
import copy
import pystac
import pandas

from mako.template import Template

import xarray as xr
from kerchunk.hdf import SingleHdf5ToZarr
from .thumbnail import Thumbnail
from .static_thumbnail import StaticThumbnail
from .cog_generation import generate_cog

def expand_dt_template(s, dt):
    return s.format(**{
        "year": dt.year,
        "month": dt.month,
        "day": dt.day
    })

def floats(seq):
    return [float(x) for x in seq]

def fmt_date(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S%Z").replace("UTC","Z")

class CustomDateExtractor:

    def __init__(self, code_path):
        self.locals = {}
        self.globals = {}
        with open(code_path) as f:
            exec(f.read(), globals(), globals())


    def extract(self, filepath, ds):
        return globals()["date_extract"](filepath, ds)

class DatasetWrapper:

    def __init__(self, fpath, var_id):
        self.fpath = fpath
        self.ds = xr.open_dataset(fpath)
        self.var_id = var_id
        self.var = self.ds[var_id]

    def get_spatial_extent(self, axis, values):
        values.append(self.ds[axis].min().item())
        values.append(self.ds[axis].max().item())

    def get_datetime(self, index=0):
        try:
            return pandas.Timestamp(self.ds.time.values[index]).to_pydatetime().replace(tzinfo=None)
        except:
            filename = os.path.split(self.fpath)[-1]
            try:
                return datetime.datetime.strptime(filename[0:8],"%Y%m%d").replace(tzinfo=None)
            except:
                return datetime.datetime.strptime(filename[0:6],"%Y%m").replace(tzinfo=None, day=15)

    def get_datetime_interval(self, index=0):
        if "time_bnds" in self.ds:
            start_dt = (pandas.Timestamp(self.ds.time_bnds.values[index,0]).to_pydatetime().replace(
                tzinfo=None))
            end_dt = pandas.Timestamp(self.ds.time_bnds.values[index,1]).to_pydatetime().replace(
                tzinfo=None)
            return (start_dt, end_dt)
        return (None, None)


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

    def get_dataset(self):
        return self.ds

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

def get_netcdf_asset_dict(fpath, config, dt, dataset_attrs):
    template = Template(config['netcdf_url'])
    href = template.render(**dataset_attrs)
    href = f"{expand_dt_template(href, dt)}{fpath}"
    d = {
        "href": href
    }
    d.update(config["defaults"]["netcdf_asset"])
    return d

def get_kerchunk_asset_dict(fpath, config, dt, dataset_attrs):
    template = Template(config['kerchunk_url'])
    href = template.render(**dataset_attrs)
    href = f"{expand_dt_template(href, dt)}{fpath}"
    d = {
        "href": href,
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

def get_cog_asset_dict(fpath, config, dt):
    d = {
        "href": f"{expand_dt_template(config['cog_url'], dt)}{fpath}",
    }
    if "cog_asset" in config["defaults"]:
        d.update(config["defaults"]["cog_asset"])
    return d

def generate_kerchunk(filepath, url, outpath):
    with open(filepath, "rb") as f:
        h5chunks = SingleHdf5ToZarr(f, url, inline_threshold=300)
        with open(outpath, "wb") as of:
            of.write(json.dumps(h5chunks.translate(), indent=4).encode())


class Netcdf2Stac:

    def __init__(self, base_folder, auxilary_base_folder, input_paths, config_paths,
                 collection_filename="collection.json",
                 parent_collection_path = None,
                 item_subfolder="items",
                 generate_kerchunk_assets=True, inline_kerchunk=False, generate_netcdf_assets=True,
                 generate_collection_thumbnail_asset=False,
                 generate_item_thumbnail_assets=False,
                 overwrite_items=False,
                 generate_cog=[],
                 cog_nodata_values={},
                 cog_dtypes={},
                 cog_crs=None):
        self.base_folder = base_folder
        self.auxilary_base_folder = auxilary_base_folder
        self.input_paths = input_paths
        self.collection_filename = collection_filename
        self.parent_collection_path = parent_collection_path

        if self.collection_filename:
            self.collection_path = os.path.join(self.base_folder,self.collection_filename)
        else:
            self.collection_path = ""

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

        self.generate_collection_thumbnail_asset = generate_collection_thumbnail_asset
        self.generate_item_thumbnail_assets = generate_item_thumbnail_assets
        self.overwrite_items = overwrite_items

        self.generate_cog = generate_cog
        self.cog_nodata_values = cog_nodata_values
        self.cog_dtypes = cog_dtypes
        self.cog_crs = cog_crs

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
        self.custom_date_extractor = None
        date_extractor_path = None
        for config_path in self.config_paths:
            config_dir = os.path.dirname(config_path)
            with open(config_path) as f:
                config = json.load(f)
                self.config = merge(self.config, config)
                if "date_extractor_path" in config:
                    date_extractor_path = os.path.join(config_dir,config["date_extractor_path"])

        if "license" not in self.config:
            raise Exception("The configuration must include a top level key 'license'")

        if date_extractor_path is not None:
            self.custom_date_extractor = CustomDateExtractor(date_extractor_path)

        if self.collection_path is not None and os.path.exists(self.collection_path):
            # read start/end dates from the existing collection
            with open(self.collection_path) as f:
                o = json.loads(f.read())
                old_collection = pystac.Collection.from_dict(o)
                self.start_date = old_collection.extent.temporal.intervals[0][0].replace(tzinfo=None)
                self.end_date = old_collection.extent.temporal.intervals[0][1].replace(tzinfo=None)
                self.bbox = old_collection.extent.spatial.bboxes[0]
                self.logger.info(f"Loaded existing collection {self.start_date} - {self.end_date}")

        if self.parent_collection_path is not None:
            with open(self.parent_collection_path) as f:
                o = json.loads(f.read())
                self.parent_collection = pystac.Collection.from_dict(o)
        else:
            self.parent_collection = None

        extra_fields = {}
        for (key,value) in self.config.get("defaults",{}).get("all",{}).items():
            extra_fields[key] = copy.deepcopy(value)
        for (key,value) in self.config.get("defaults",{}).get("collection",{}).items():
            extra_fields[key] = copy.deepcopy(value)
        providers = []
        for p in self.config.get("providers",[]):
            providers.append(pystac.Provider(**p))

        collection_id = self.config["stac_collection_id"]
        self.collection = pystac.Collection(id=collection_id,
                                            href=f"https://stac.ceda.ac.uk/collections/{collection_id}",
                                            extent=None,
                                            extra_fields=extra_fields,
                                            license=self.config["license"],
                                            keywords=self.config.get("keywords",None),
                                            title=self.config.get("title", ""),
                                            description=self.config.get("description", ""),
                                            stac_extensions=self.config.get("stac-extensions",[]),
                                            catalog_type=pystac.CatalogType.SELF_CONTAINED,
                                            providers=providers)
        if self.parent_collection:
            self.collection.add_link(pystac.Link(pystac.RelType.PARENT,
                                                 target=f"/collections/{self.parent_collection.id}",
                                                 media_type=pystac.MediaType.JSON,
                                                 title=self.parent_collection.title))
            child_link_found = False
            for link in self.parent_collection.links:
                if isinstance(link.target,str) and link.target == f"/collections/{collection_id}":
                    child_link_found = True
            if not child_link_found:
                self.parent_collection.add_link(pystac.Link(pystac.RelType.CHILD,
                                     target=f"/collections/{collection_id}",
                                     media_type=pystac.MediaType.JSON,
                                     title=self.collection.title))
                with open(self.parent_collection_path, "w") as f:
                    f.write(json.dumps(self.parent_collection.to_dict(include_self_link=False), indent=4))

        if "thumbnail" in self.config:
            tcfg = self.config["thumbnail"]
            if "image_path" in tcfg:
                # resolve the background image path relative to the configuration files
                for config_path in self.config_paths:
                    image_path = os.path.join(os.path.split(config_path)[0],tcfg["image_path"])
                    if os.path.exists(image_path):
                        self.thumbnail_generator = StaticThumbnail(image_path)
                        break
            else:
                background_image_path = None
                if "background_image_path" in tcfg:
                    # resolve the background image path relative to the configuration files
                    for config_path in self.config_paths:
                        background_image_path = os.path.join(os.path.split(config_path)[0],
                                                             tcfg["background_image_path"])
                        if os.path.exists(background_image_path):
                            break
                self.thumbnail_generator = Thumbnail(
                    variable=tcfg["variable"],
                    cmap=tcfg["cmap"],
                    vmin=tcfg["vmin"],
                    vmax=tcfg["vmax"],
                    x_coord=tcfg["x-coordinate"],
                    y_coord=tcfg["y-coordinate"],
                    plot_width=tcfg["width"],
                    background_image_path=background_image_path,
                    selector=tcfg.get("selector",{})
                )
        else:
            self.thumbnail_generator = None

    def run(self):
        os.makedirs(self.base_folder, exist_ok=True)
        os.makedirs(self.auxilary_base_folder, exist_ok=True)

        all_paths = []
        for input_pattern in self.input_paths:
            all_paths += glob.glob(input_pattern,recursive=True)

        if len(all_paths) == 0:
            print("No input files found")
            return

        thumbnail_asset = None
        for idx in range(len(all_paths)):
            if idx == len(all_paths)-1 and self.generate_collection_thumbnail_asset:
                thumbnail_asset = self.process_item(all_paths[idx], return_thumbnail_asset=True)
            else:
                self.process_item(all_paths[idx], return_thumbnail_asset=self.generate_item_thumbnail_assets)

        if self.collection_path:
            self.finalise_collection(thumbnail_asset)

    def finalise_collection(self, thumbnail_asset=None):
        if thumbnail_asset is not None:
            self.collection.add_asset("thumbnail",thumbnail_asset)
        spatial_extent = pystac.SpatialExtent([self.bbox])
        temporal_extent = pystac.TemporalExtent([self.start_date, self.end_date])
        extent = pystac.Extent(spatial_extent, temporal_extent)
        self.collection.extent = extent
        extra_time = self.collection.extra_fields.get("cube:dimensions",{}).get("time",None)
        if extra_time:
            extra_time["extent"] = [fmt_date(self.start_date), fmt_date(self.end_date)]
        if self.collection_path is not None:
            with open(self.collection_path, "w") as f:
                f.write(json.dumps(self.collection.to_dict(include_self_link=False), indent=4))

    def process_item(self, fpath, return_thumbnail_asset=False):
        input_filename = os.path.split(fpath)[-1]

        self.logger.info(f"Processing item {fpath}")

        var_id = self.config["variable"]

        try:
            i = DatasetWrapper(fpath, var_id)
        except Exception as ex:
            self.logger.exception(f"Reading {fpath}")
            return False

        if "bbox" in self.config:
            bbox = self.config["bbox"]
        else:
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

        if self.custom_date_extractor is not None:
            interval_start_dt, dt, interval_end_dt = self.custom_date_extractor.extract(fpath,i.get_dataset())
        else:
            if "timestamp" in self.config:
                dt = datetime.datetime.fromisoformat(self.config["timestamp"])
                print(dt)
            else:
                dt = i.get_datetime(0)


            interval_start_dt, interval_end_dt = i.get_datetime_interval()
            print(interval_start_dt, interval_end_dt)

        item_subfolder = expand_dt_template(self.item_subfolder,dt)
        os.makedirs(os.path.join(self.base_folder, item_subfolder), exist_ok=True)
        os.makedirs(os.path.join(self.auxilary_base_folder, item_subfolder), exist_ok=True)
        item_subfolder_levels = len(item_subfolder.split("/"))
        kerchunk_filename = os.path.splitext(input_filename)[0] + "-kerchunk.json"
        kerchunk_filepath = os.path.join(self.auxilary_base_folder, item_subfolder, kerchunk_filename)
        output_filename = os.path.splitext(input_filename)[0] + ".geojson"
        output_filepath = os.path.join(self.base_folder, item_subfolder, output_filename)
        if not self.overwrite_items:
            if os.path.exists(output_filepath):
                if not self.generate_kerchunk_assets or os.path.exists(kerchunk_filepath):
                    self.logger.info(f"Skipping item {fpath}, output already exists")
                    return

        # establish a unique ID for this item
        item_id = str(uuid.uuid4())

        # if the item already exists, re-use its id
        if os.path.exists(output_filepath):
            with open(output_filepath) as f:
                o = json.loads(f.read())
                item_id = o["id"]

        if self.start_date is None or dt < self.start_date:
            self.start_date = dt
        if interval_start_dt is not None and interval_start_dt < self.start_date:
            self.start_date = interval_start_dt

        if self.end_date is None or dt > self.end_date:
            self.end_date = dt
        if interval_end_dt is not None and interval_end_dt > self.end_date:
            self.end_date = interval_end_dt

        props = {}
        for (key, value) in self.config.get("defaults", {}).get("all", {}).items():
            props[key] = copy.deepcopy(value)
        for (key, value) in self.config.get("defaults", {}).get("item", {}).items():
            props[key] = copy.deepcopy(value)

        extra_time = props.get("cube:dimensions", {}).get("time", None)
        if extra_time:
            extra_time["values"] = [fmt_date(dt)]

        x_extent = props.get("cube:dimensions", {}).get("x", {}).get("extent",None)
        y_extent = props.get("cube:dimensions", {}).get("y", {}).get("extent", None)

        if x_extent == []:
            i.get_spatial_extent("x", x_extent)
        if y_extent == []:
            i.get_spatial_extent("y", y_extent)


        props["license"] = self.config["license"]

        for (source_key, dest_key) in self.config.get("global_attr_map",{}).items():
            if source_key in i.get_dataset().attrs:
                props[dest_key] = i.get_dataset().attrs[source_key]

        # Add dataset ID, title, description
        dset_id = self.config.get("dataset_id", "")
        if dset_id:
            props["dataset_id"] = dset_id

        title = self.config.get("title", "")
        if title:
            props["title"] = title

        description = self.config.get("description", "")
        if description:
            props["description"] = description

        # Add templated properties
        if "templated_properties" in self.config:
            for prop, tmpl in self.config["templated_properties"].items():
                try:
                    prop_comps = prop.split(":")
                    prop = prop_comps[0]
                    directive = prop_comps[1] if len(prop_comps) > 1 else None
                    template = Template(tmpl)
                    template_properties = copy.deepcopy(i.get_dataset().attrs)
                    template_properties["year"] = f"{dt.year:04d}"
                    template_properties["month"] = f"{dt.month:02d}"
                    template_properties["day"] = f"{dt.day:02d}"
                    if interval_start_dt is not None:
                        template_properties["start_year"] = f"{interval_start_dt.year:04d}"
                        template_properties["start_month"] = f"{interval_start_dt.month:02d}"
                        template_properties["start_day"] = f"{interval_start_dt.day:02d}"
                    if interval_end_dt is not None:
                        template_properties["end_year"] = f"{interval_end_dt.year:04d}"
                        template_properties["end_month"] = f"{interval_end_dt.month:02d}"
                        template_properties["end_day"] = f"{interval_end_dt.day:02d}"

                    v = template.render(**template_properties)
                    if directive == "comma_separated_list":
                        v = list(map(lambda s: s.strip(),v.split(",")))
                    props[prop] = v
                except Exception as ex:
                    print(f"warning, unable to resolve template {prop} {tmpl}: {ex}")

        input_filename = os.path.split(fpath)[-1]

        output_filename = os.path.splitext(input_filename)[0] + ".geojson"

        date_arguments = {}
        date_arguments["datetime"] = dt

        if interval_start_dt is not None and interval_end_dt is not None:
            date_arguments["start_datetime"] = interval_start_dt
            date_arguments["end_datetime"] = interval_end_dt

        item = pystac.Item(id=item_id,
                           href=output_filename,
                           collection=self.collection,
                           bbox = bbox,
                           properties=props,
                           geometry=get_geometry(bbox),
                           stac_extensions=self.config.get("stac-extensions",[]),
                           **date_arguments)

        item.clear_links()

        if self.collection_path:
            superfolder = os.path.join(*([".."]*item_subfolder_levels))
            clink = pystac.Link(rel="collection", target=os.path.join(superfolder,self.collection_filename), media_type="application/json")
            item.add_link(clink)

        netcdf_filename = os.path.split(fpath)[-1]
        asset_dict = get_netcdf_asset_dict(netcdf_filename, self.config, dt, i.get_dataset().attrs)
        netcdf_href = asset_dict["href"]

        if self.generate_kerchunk_assets:
            kerchunk_asset_dict = get_kerchunk_asset_dict(kerchunk_filename, self.config, dt, i.get_dataset().attrs)

            if self.overwrite_items or not os.path.exists(kerchunk_filepath):
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

        if self.generate_cog:
            for variable in self.generate_cog:
                tif_filename = os.path.splitext(input_filename)[0] + "_" + variable + ".tif"
                asset_dict = get_cog_asset_dict(tif_filename, self.config, dt)
                cog_href = asset_dict["href"]
                del asset_dict["href"]
                tif_filepath = os.path.join(self.auxilary_base_folder, item_subfolder, tif_filename)
                generate_cog(i.get_dataset(), variable, tif_filepath,
                             dtype=self.cog_dtypes.get(variable),
                             nodata_value=self.cog_nodata_values.get(variable),
                             crs = self.cog_crs)
                asset_key = f"data_{variable}"
                asset = pystac.Asset(href=cog_href,
                                     roles=["data"],
                                     media_type="image/tiff; application=geotiff",
                                     extra_fields=asset_dict)
                item.add_asset(asset_key, asset)
        thumbnail_asset = None

        if return_thumbnail_asset and self.thumbnail_generator is not None:
            thumbnail_filename = os.path.splitext(input_filename)[0] + ".png"
            thumbnail_filepath = os.path.join(self.auxilary_base_folder, item_subfolder, thumbnail_filename)
            asset_dict = get_thumbnail_asset_dict(thumbnail_filename, self.config, dt)
            href = asset_dict["href"]
            del asset_dict["href"]
            self.thumbnail_generator.generate(i.get_dataset(), thumbnail_filepath)
            thumbnail_asset = pystac.Asset(href=href,
                                 roles=["thumbnail"],
                                 media_type="image/png",
                                 extra_fields=asset_dict)
            # add the thumbnail asset to the item as well
            item.add_asset("thumbnail", thumbnail_asset)

        if self.overwrite_items or not os.path.exists(output_filepath):
            with open(output_filepath,"w") as f:
                o = item.to_dict(include_self_link=False)
                f.write(json.dumps(o,indent=4))

        if return_thumbnail_asset:
            return thumbnail_asset



