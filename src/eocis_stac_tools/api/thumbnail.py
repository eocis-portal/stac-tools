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

import os
import json

import datashader as dsh
import datashader.transfer_functions as tf
from datashader import reductions as rd


class Thumbnail:

    def __init__(self, variable, cmap, vmin, vmax, x_coord, y_coord, plot_width):
        self.variable = variable

        self.vmin = vmin
        self.vmax = vmax
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.plot_width = plot_width

        self.cmap_colours = []

        cmap_path = os.path.join(os.path.split(__file__)[0], "cmaps", cmap + ".json")

        with open(cmap_path) as f:
            o = json.loads(f.read())
            for rgb in o:
                r = int(255 * rgb[0])
                g = int(255 * rgb[1])
                b = int(255 * rgb[2])
                self.cmap_colours.append(f"#{r:02X}{g:02X}{b:02X}")


    def generate(self, dataset, output_path):
        da = dataset[self.variable]

        da = da.squeeze()

        if len(da.shape) != 2:
            raise Exception(f"too many dimensions to plot {da.dims}")

        h = da.shape[0]
        w = da.shape[1]

        plot_height = int(self.plot_width * (h / w))
        cvs = dsh.Canvas(plot_width=self.plot_width, plot_height=plot_height,
                         x_range=(float(da[self.x_coord].min()), float(da[self.x_coord].max())),
                         y_range=(float(da[self.y_coord].min()), float(da[self.y_coord].max())))

        agg = cvs.raster(da.squeeze(), agg=rd.first, interpolate='linear')

        shaded = tf.shade(agg, cmap=self.cmap_colours,
                          how="linear",
                          span=(self.vmin, self.vmax))

        p = shaded.to_pil()
        with open(output_path, "wb") as f:
            p.save(f, format="PNG")


