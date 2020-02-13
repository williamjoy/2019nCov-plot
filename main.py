import csv
import numpy as np

from datetime import datetime
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import Divider, Size
from mpl_toolkits.axes_grid1.mpl_axes import Axes

import matplotlib.font_manager as mfm
import argparse
import re

import matplotlib
matplotlib.rcParams['figure.figsize'] = (15.0, 10.0)
FONT_FILE = '/System/Library/Fonts/STHeiti Light.ttc'
prop = mfm.FontProperties(fname=FONT_FILE)
#prop.set_size('small')

TIME_ZERO = datetime.fromisoformat('2020-01-24')
FILE_NAME = "./hubei.csv"
FILE_NAME = "./DXYArea.csv"
_, ax = plt.subplots()

parser = argparse.ArgumentParser(description='Plot 2019nCov Confirmed cases')
parser.add_argument('--province', help='province name')
parser.add_argument('--save-file', help='file name to save')
parser.add_argument('--exclude', help='exclude data, regular expression')
args = parser.parse_args()
black_list_re = re.compile(args.exclude) if args.exclude else None

plt.xlabel(f'day from {TIME_ZERO}', fontproperties=prop)

ax.set(xlim=(0, (datetime.now().replace(hour=0, minute=0) -
                 TIME_ZERO).total_seconds()/3600/24 + 2))
with open(FILE_NAME, newline='',  encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    if args.province:
        value_key = 'city_confirmedCount'
        name_key = 'cityName'
        data = list(filter(lambda x:  x.get(
            'provinceName', "").startswith(args.province), reader))
    else:
        value_key = 'province_confirmedCount'
        name_key = 'provinceName'
        data = reader

    data_by_geo = {}
    for row in data:
        geo_location = row.get(name_key, "None")
        if black_list_re and black_list_re.findall(geo_location):
            continue
        value = int(row.get(value_key, 0))
        updateTime = datetime.fromisoformat(row.get('updateTime'))
        day_diff = (updateTime.replace(hour=0, minute=0, second=0,
                                       microsecond=0) - TIME_ZERO).total_seconds()/3600/24

        data_by_geo.setdefault(geo_location, {})

        # truncate to day
        if data_by_geo.get(geo_location).get(day_diff, 0) < value:
            data_by_geo[geo_location][day_diff] = value

    for geo_location, points in data_by_geo.items():
        if not points:
            continue
        print(geo_location, max(points.values()))
        plt.scatter(points.keys(),
                    points.values(),
                    label=f'{geo_location}: {max(points.values())}',
                    marker='o')
ax.legend(loc='upper left', prop=prop)
ax.grid(True)
#plt.figure(figsize=(1920,1080))
if args.save_file:
    plt.savefig(f'{args.save_file}.svg', format='svg')
else:
    plt.show()
