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
MAKERS = ['.', ',', 'o', 'v', '^', '<', '>', 's', 'p',
          '*', 'h', 'H', '+', 'D', 'd', '|', '_', 'P', 'X']
LINESTYLES = ['-', '--', '-.', ':']

matplotlib.rcParams['figure.figsize'] = (20.0, 12.0)
FONT_FILE = '/System/Library/Fonts/STHeiti Light.ttc'
prop = mfm.FontProperties(fname=FONT_FILE)
# prop.set_size('small')

FILE_NAME = "./hubei.csv"
FILE_NAME = "./DXYArea.csv"
_, ax = plt.subplots()
ax.yaxis.tick_right()
parser = argparse.ArgumentParser(description='Plot 2019nCov Confirmed cases')
parser.add_argument('--province', help='province name')
parser.add_argument('--save-file', help='file name to save')
parser.add_argument('--exclude', help='exclude data, regular expression')
args = parser.parse_args()
black_list_re = re.compile(args.exclude) if args.exclude else None

plt.xlabel(f'Date', fontproperties=prop)

with open(FILE_NAME, newline='',  encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    if args.province:
        title = args.province
        value_key = 'city_confirmedCount'
        name_key = 'cityName'
        data = list(filter(lambda x:  x.get(
            'provinceName', "").startswith(args.province), reader))
    else:
        title = '全国'
        value_key = 'province_confirmedCount'
        name_key = 'provinceName'
        data = reader

    plt.ylabel(f'{title} confirmed cases', fontproperties=prop)
    data_by_geo = {}
    for row in data:
        geo_location = row.get(name_key, "None")
        if black_list_re and black_list_re.findall(geo_location):
            continue
        value = int(row.get(value_key, 0))
        updateTime = datetime.fromisoformat(row.get('updateTime'))

        data_by_geo.setdefault(geo_location, {})
        data_by_geo[geo_location][updateTime] = value

    for geo_location, points in data_by_geo.items():
        if not points:
            continue
        print(geo_location, max(points.values()))
        plt.plot_date(list(points.keys()),
                      list(points.values()),
                      marker=random.choice(MAKERS),
                      linestyle=random.choice(LINESTYLES),
                      label=f'{geo_location}: {max(points.values())}')
ax.legend(loc='upper left', prop=prop)
ax.grid(True)
plt.title('confirmed cases')
plt.gcf().autofmt_xdate()
if args.save_file:
    plt.savefig(f'{args.save_file}.svg', format='svg',)
else:
    plt.show()
