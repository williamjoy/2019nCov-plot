import csv
import random
import numpy as np

from datetime import datetime
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import Divider, Size
from mpl_toolkits.axes_grid1.mpl_axes import Axes

import matplotlib.font_manager as mfm
import argparse
import re

import matplotlib

random.seed(6878748400691668451)
MARKERS = ['.', 'o', 'v', '^', '<', '>', 's', 'p',
          '*', 'h', 'H', '+', 'D', 'd', 'P', 'X']
LINESTYLES = ['-', '--', '-.', ':']

matplotlib.rcParams['figure.figsize'] = (20.0, 12.0)
FONT_FILE = '/System/Library/Fonts/STHeiti Light.ttc'
prop = mfm.FontProperties(fname=FONT_FILE)
# prop.set_size('small')

FILE_NAME = "./canada.csv"
_, ax = plt.subplots()
ax.yaxis.tick_right()
parser = argparse.ArgumentParser(description='Plot 2019nCov Confirmed cases')
parser.add_argument('--value-column', help='project on column name, default: numconf', default='numconf')
parser.add_argument('--save-file', help='file name to save')
parser.add_argument('--blacklist', help='blacklist data, regular expression')
parser.add_argument('--whitelist', help='whitelist data, regular expression')
parser.add_argument('--title', help='graph title', default='Confirmed Cases')
args = parser.parse_args()
print (args)
blacklist_re = re.compile(args.blacklist) if args.blacklist else None
whitelist_re = re.compile(args.whitelist) if args.whitelist else None

plt.xlabel(f'Date', fontproperties=prop)

with open(FILE_NAME, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    value_key = args.value_column
    name_key = 'prname'
    title = 'Canada'
    data = reader

    plt.ylabel(f'{args.title}', fontproperties=prop)
    data_by_geo = {}
    for row in data:
        geo_location = row.get(name_key, "None")
        if blacklist_re and blacklist_re.findall(geo_location):
            continue
        if whitelist_re and  not whitelist_re.findall(geo_location):
            print(geo_location, whitelist_re)
            continue
        try:
            value = int(row.get(value_key, 0))
        except ValueError as e:
            continue
        updateTime = datetime.strptime(row.get('date'), '%d-%m-%Y')
        if updateTime > datetime.strptime('01-03-2020', '%d-%m-%Y'):
            data_by_geo.setdefault(geo_location, {})
            data_by_geo[geo_location][updateTime] = value

    for geo_location, points in data_by_geo.items():
        if not points:
            continue
        marker = random.choice(MARKERS)
        print(marker, geo_location, max(points.values()))
        plt.plot_date(list(points.keys()),
                      list(points.values()),
                      marker=marker,
                      linestyle=random.choice(LINESTYLES),
                      label=f'{geo_location}: {max(points.values())}')
ax.legend(loc='upper left', prop=prop)
ax.grid(True)
plt.title(args.title)
plt.gcf().autofmt_xdate()
if args.save_file:
    plt.savefig(f'{args.save_file}.svg', format='svg',)
else:
    plt.show()
