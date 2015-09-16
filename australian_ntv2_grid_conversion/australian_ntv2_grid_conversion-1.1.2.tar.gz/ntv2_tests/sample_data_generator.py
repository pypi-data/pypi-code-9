# Path hack.
import sys

import os

sys.path.insert(0, os.path.abspath('..'))
import random
import australian_ntv2_grid_conversion as angv

random_csv = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random.csv'
agd66_csv = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random_AGD66.csv'
agd84_csv = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random_AGD84.csv'
agd66_csv_gday = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random_AGD66_gday_input.csv'
agd84_csv_gday = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random_AGD84_gday_input.csv'
agd66_csv_gdait = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random_AGD66_gdait_input.csv'
agd84_csv_gdait = 'D:/sync_folder/plaintech_share/Projects/australian_ntv2_grid_conversion/ntv2_tests/GDAit_and_GDAy_conversions/random_AGD84_gdait_input.csv'

min_lat = -48.15
max_lat = -8.55
min_lon = 104
max_lon = 164
number_of_points = 10000

random_data = []
agd66_data = []
agd84_data = []

ntv2 = angv.Ntv2()

for i in range(0, number_of_points, 1):
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        random_data.append({'lat': lat, 'lon': lon})

for j in range(0, number_of_points, 1):
    valid_agd66_point = False
    while valid_agd66_point is False:
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        try:
            ntv2.latlon_to_latlon(lat, lon, 'agd66', 'gda94')
        except ValueError:
            continue
        else:
            agd66_data.append({'lat': lat, 'lon': lon})
            valid_agd66_point = True

for k in range(0, number_of_points, 1):
    valid_agd84_point = False
    while valid_agd84_point is False:
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        try:
            ntv2.latlon_to_latlon(lat, lon, 'agd84', 'gda94')
        except ValueError:
            continue
        else:
            agd84_data.append({'lat': lat, 'lon': lon})
            valid_agd84_point = True

with open(random_csv, 'w') as output_file:
    output_file.write('latitude, longitude\n')
    for i in random_data:
        output_file.write('{}, {}\n'.format(i['lat'], i['lon']))

with open(agd66_csv, 'w') as output_file:
    output_file.write('latitude, longitude\n')
    for i in agd66_data:
        output_file.write('{}, {}\n'.format(i['lat'], i['lon']))

with open(agd84_csv, 'w') as output_file:
    output_file.write('latitude, longitude\n')
    for i in agd84_data:
        output_file.write('{}, {}\n'.format(i['lat'], i['lon']))

c = 0
with open(agd66_csv_gday, 'w') as output_file:
    for i in agd66_data:
        output_file.write('p{},{},{},,,,DecDeg\n'.format(c, i['lat'], i['lon']))
        c += 1

c = 0
with open(agd84_csv_gday, 'w') as output_file:
    for i in agd84_data:
        output_file.write('p{},{},{},,,,DecDeg\n'.format(c, i['lat'], i['lon']))
        c += 1

c = 0
with open(agd66_csv_gdait, 'w') as output_file:
    output_file.write('POINT,Latitude,Longitude,Height,Zo,Dat,Description\n\n')
    for i in agd66_data:
        output_file.write('p{},{},{},,,,DecDeg\n'.format(c, i['lat'], i['lon']))
        c += 1

c = 0
with open(agd84_csv_gdait, 'w') as output_file:
    output_file.write('POINT,Latitude,Longitude,Height,Zo,Dat,Description\n\n')
    for i in agd84_data:
        output_file.write('p{},{},{},,,,DecDeg\n'.format(c, i['lat'], i['lon']))
        c += 1
