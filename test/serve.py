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

from http.server import SimpleHTTPRequestHandler, HTTPServer
import os.path
import argparse
import re

webroot = os.path.split(__file__)[0]

class CORSRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=webroot, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",default="localhost")
    parser.add_argument("--port",type=int, default=9002)
    args = parser.parse_args()
    server = HTTPServer((args.host,args.port),CORSRequestHandler)
    print("Paste the following URLs into the radiant earth STAC browser (https://radiantearth.github.io/stac-browser/#/):")
    for root,dirs,files  in os.walk(os.path.join(webroot,"stac-generated")):
        for file in files:
            if file.endswith(".geojson"):
                filepath = os.path.join(root,file)
                relpath = os.path.relpath(filepath,webroot)
                print("\thttp://%s:%d/%s"%(args.host,args.port,relpath))
    server.serve_forever()
