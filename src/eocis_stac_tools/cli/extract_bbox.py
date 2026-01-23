
import pyproj
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--x-min', type=float, default=-613350)
parser.add_argument('--x-max', type=float, default=911550)
parser.add_argument('--y-min', type=float, default=-289850)
parser.add_argument('--y-max', type=float, default=1323250)
parser.add_argument('--crs', type=int, default=27700)
parser.add_argument('--sample', type=int, default=10000) # sample every 10k

args = parser.parse_args()

transformer = pyproj.transformer.Transformer.from_crs(args.crs,4326,always_xy=True)

latlons = []
x = args.x_min
while x < args.x_max + args.sample:
    if x > args.x_max:
        x = args.x_max

    y = args.y_min
    while y < args.y_max + args.sample:
        if y > args.y_max:
            y = args.y_max

        latlons.append(transformer.transform(x,y))
        y += args.sample
    x += args.sample

lons = [lon for (lon,lat) in latlons]
lats = [lat for (lon,lat) in latlons]

print(f"lat: {min(lats)} - {max(lats)}, lon: {min(lons)} - {max(lons)}")

