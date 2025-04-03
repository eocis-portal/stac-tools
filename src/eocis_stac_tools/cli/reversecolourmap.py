import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_path")
parser.add_argument("output_path")

args = parser.parse_args()

with open(args.input_path) as f:
    cmap = json.loads(f.read())

cmap.reverse()

with open(args.output_path,"w") as f:
    f.write(json.dumps(cmap))