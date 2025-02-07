

import argparse
import glob
import json

from mako.template import Template

def apply_update(attr,value,o):
    attr_parts = attr.split(".")
    if len(attr_parts) > 1:
        for part in attr_parts[:-1]:
            if isinstance(o,list):
                o = o[int(part)]
            else:
                o = o[part]
        attr = attr_parts[-1]
    if isinstance(o, list):
        o[int(attr)] = value
    else:
        o[attr] = value
    return value

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--paths", nargs="+", help="specify files to modify", required=True)
    parser.add_argument("--attr", nargs=2, action="append", help="specify attribute, value pairs", required=True)

    args = parser.parse_args()

    paths = []
    for path in args.paths:
        paths += glob.glob(path)

    for path in paths:
        print(f"processing {path}")
        with open(path) as f:
            o = json.loads(f.read())

        for (attr_name,attr_value) in args.attr:
            template = Template(attr_value)
            new_value = template.render(**o)
            print(attr_name,new_value)
            apply_update(attr_name,new_value,o)

        with open(path,"w") as of:
            of.write(json.dumps(o, indent=4))

if __name__ == '__main__':
    main()