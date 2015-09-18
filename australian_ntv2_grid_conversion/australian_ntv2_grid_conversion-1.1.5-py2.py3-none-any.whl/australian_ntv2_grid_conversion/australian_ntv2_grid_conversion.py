# Copyright 2015, Phil Howarth (phil@plaintech.net.au)
#
# This file is part of Australian NTv2 Grid Conversion.
#
# Australian NTv2 Grid Conversion is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Australian NTv2 Grid Conversion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Australian NTv2 Grid Conversion.  If not, see <http://www.gnu.org/licenses/>.

import struct
import redfearn
import argparse
import os
import sys
import math
import csv


class DictReaderInsensitive(csv.DictReader, object):
    # This class overrides the csv.fieldnames property.
    # All fieldnames are without white space and in lower case
    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(DictReaderInsensitive, self).fieldnames]

    def __next__(self):
        # get the result from the original __next__, but store it in DictInsensitive
        d_insensitive = DictInsensitive()
        d_original = super(DictReaderInsensitive, self).__next__()
        # store all pairs from the old dict in the new, custom one
        for key, value in d_original.items():
            d_insensitive[key] = value
        return d_insensitive


class DictInsensitive(dict):
    # This class overrides the __getitem__ method to automatically strip() and lower() the input key
    def __getitem__(self, key):
        return dict.__getitem__(self, key.strip().lower())


# class to allow multi-line help comments in argparse
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)


class Ntv2:

    def __init__(self):
        # size of record in NtV2 files
        self.record_size_bytes = 16
        # redfearn coordinate systems are defined differently to ntv2 coordinate systems
        self.redfearn_from_system = None
        self.redfearn_to_system = None
        # set the string to print in csv files if trying to convert a point outside the grid file
        self.invalid_data_string = '***'
        # location of data files
        try:
            self.data_files_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        except NameError:  # We are the main py2exe script, not a module
            self.data_files_folder = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), 'data'))
        self.agd66_file = os.path.join(self.data_files_folder, 'A66 National (13.09.01).gsb')
        self.agd84_file = os.path.join(self.data_files_folder, 'National 84 (02.07.01).gsb')
        # this parameter can be set by a user to manually define a grid file to use
        self.ntv2_file = None

    def set_ntv2_file(self, ntv2_file):
        self.ntv2_file = ntv2_file

    def _transform(self, from_system, to_system, lat, lon):
        # skip on out if no transformation is required (this happens sometimes if maybe we just want to convert from latlon to grid)
        if from_system == to_system:
            return {
                'latitude': lat,
                'longitude': lon,
                'lat_trans_acc': 0,
                'lon_trans_acc': 0
            }

        # find the ntv2 grid file
        ntv2_file = None
        if self.ntv2_file:
            ntv2_file = self.ntv2_file
        if from_system == 'agd84' and to_system == 'gda94':
            if not ntv2_file:
                ntv2_file = self.agd84_file
            f_or_r = 'f'
        elif from_system == 'gda94' and to_system == 'agd84':
            if not ntv2_file:
                ntv2_file = self.agd84_file
            f_or_r = 'r'
        elif from_system == 'agd66' and to_system == 'gda94':
            if not ntv2_file:
                ntv2_file = self.agd66_file
            f_or_r = 'f'
        elif from_system == 'gda94' and to_system == 'agd66':
            if not ntv2_file:
                ntv2_file = self.agd66_file
            f_or_r = 'r'
        else:
            print("Invalid transform requested")
            sys.exit(1)

        # Check for input ntv2 file
        if not ntv2_file or not os.access(ntv2_file, os.R_OK):
            print('Cannot access the ntv2 grid file at {}'.format(ntv2_file))
            print('Please specify a valid ntv2 file with the -ntv2_file flag')
            sys.exit(1)

        # convert lat and lon to seconds
        lat = self.convert_decimal_degrees_to_seconds(lat)
        lon = self.convert_decimal_degrees_to_seconds(lon)
        # longitude values within the Australian Ntv2 files are Positive West and so need to be multiplied by -1
        # This is reversed on the way out so that coordinates are normal
        if lon > 0:
            lon = -lon
        # Read the entire file as a single byte string
        with open(ntv2_file, 'rb') as f:
            # perform the transformation
            if f_or_r == 'f':
                converted_values = self._forward_bilinear_transformation(f, lat, lon)
            elif f_or_r == 'r':
                converted_values = self._reverse_bilinear_transformation(f, lat, lon)
            else:
                raise ValueError("Can't decide between forward and reverse")
        return converted_values

    def _forward_bilinear_transformation(self, f, lat, lon):
        # read the file and subgrid headers
        headers = self._read_headers(f)
        major_f = headers['FILE_HEADER']['MAJOR_F']
        # determine which subgrid should be used
        subgrid = self._get_subgrid_to_use(headers, lat, lon)
        # Compute subgrid parameters
        # number_of_rows = 1 + int((subgrid['N_LAT'] - subgrid['S_LAT']) / subgrid['LAT_INC'])
        number_of_columns = 1 + int((subgrid['W_LONG'] - subgrid['E_LONG']) / subgrid['LONG_INC'])
        # Calculate row and column of grid node A
        i = 1 + int((lat - subgrid['S_LAT']) / subgrid['LAT_INC'])
        j = 1 + int((lon - subgrid['E_LONG']) / subgrid['LONG_INC'])
        # Calculate grid node numbers (sequentially) of 4 nearest nodes
        node_a = number_of_columns * (i - 1) + j
        grid_node_locations = {
            'A': node_a,
            'B': node_a + 1,
            'C': node_a + number_of_columns,
            'D': node_a + number_of_columns + 1
        }
        # get values from 4 nearest nodes
        node_values = {}
        for node in grid_node_locations:
            node_location = (grid_node_locations[node] - 1) * self.record_size_bytes + subgrid['data_offset']
            node_values[node] = self._read_node_values(f, node_location)
        # compute coordinates of node A:
        lat_a = subgrid['S_LAT'] + (i - 1) * subgrid['LAT_INC']
        lon_a = subgrid['E_LONG'] + (j - 1) * subgrid['LONG_INC']
        # Compute interpolation scale factors
        x = (lon - lon_a) / subgrid['LONG_INC']
        y = (lat - lat_a) / subgrid['LAT_INC']

        interpolated_values = {}
        for key in node_values['A']:
            # Compute latitude interpolation parameters
            a0 = node_values['A'][key]
            a1 = node_values['B'][key] - node_values['A'][key]
            a2 = node_values['C'][key] - node_values['A'][key]
            a3 = node_values['A'][key] + node_values['D'][key] - node_values['B'][key] - node_values['C'][key]
            # interpolate values
            interpolated_values[key] = a0 + a1*x + a2*y + a3*x*y

        # Add interpolated shift to coordinates to compute GDA94 coordinates
        lat_gda94 = self.convert_seconds_to_decimal_degrees(lat + interpolated_values['lat_shift'])
        lon_gda94 = self.convert_seconds_to_decimal_degrees(lon + interpolated_values['lon_shift'])
        # Convert accuracy figures to m
        # if any on the accuracy node values are equal to -1 then the accuracy cannot be calculated
        acc_values = [node_values['A']['lat_acc'], node_values['B']['lat_acc'], node_values['C']['lat_acc'], node_values['D']['lat_acc'],
                      node_values['A']['lon_acc'], node_values['B']['lon_acc'], node_values['C']['lon_acc'], node_values['D']['lon_acc']]
        if -1.0 in acc_values:
            lat_trans_acc = '***'
            lon_trans_acc = '***'
        else:
            lat_trans_acc = interpolated_values['lat_acc'] * math.pi * major_f / (3600 * 180)
            lon_trans_acc = math.cos(math.radians(lat_gda94)) * interpolated_values['lon_acc'] * math.pi * major_f / (3600 * 180)

        # print('{}, {}'.format(lat, lon))
        # print(subgrid)
        # print(number_of_columns)
        # print('{}, {}'.format(i, j))
        # print(grid_node_locations)
        # print('{}, {}'.format(x, y))
        # print(node_values)
        # print(interpolated_values)
        # print(major_f)
        # print(acc_values)
        # print(lat_trans_acc)
        # print(lon_trans_acc)

        return {
            'latitude': lat_gda94,
            'longitude': -lon_gda94,  # longitude values within the Australian Ntv2 files are Positive West and so need to be multiplied by -1
            'lat_trans_acc': lat_trans_acc,
            'lon_trans_acc': lon_trans_acc
        }

    def _reverse_bilinear_transformation(self, f, lat, lon):
        # read the file and subgrid headers
        headers = self._read_headers(f)
        major_f = headers['FILE_HEADER']['MAJOR_F']

        # Set initial estimate of AGD84 coordinates to the GDA94 coordinates of the point
        lat_est = lat
        lon_est = lon
        # Iterate next steps 4 times
        for i in range(1, 5):
            # Set coordinates of Point P to current estimate of AGD coordinates
            lat_p = lat_est
            lon_p = lon_est
            # determine which subgrid should be used
            subgrid = self._get_subgrid_to_use(headers, lat_p, lon_p)
            # Compute subgrid parameters
            # number_of_rows = 1 + int((subgrid['N_LAT'] - subgrid['S_LAT']) / subgrid['LAT_INC'])
            number_of_columns = 1 + int((subgrid['W_LONG'] - subgrid['E_LONG']) / subgrid['LONG_INC'])
            # Determine grid nodes to interpolate from
            # Calculate row and column of grid node A
            i = 1 + int((lat_p - subgrid['S_LAT']) / subgrid['LAT_INC'])
            j = 1 + int((lon_p - subgrid['E_LONG']) / subgrid['LONG_INC'])
            # Calculate grid node numbers (sequentially) of 4 nearest nodes
            node_a = number_of_columns * (i - 1) + j
            grid_node_locations = {
                'A': node_a,
                'B': node_a + 1,
                'C': node_a + number_of_columns,
                'D': node_a + number_of_columns + 1
            }
            # get values from 4 nearest nodes
            node_values = {}
            for node in grid_node_locations:
                node_location = (grid_node_locations[node] - 1) * self.record_size_bytes + subgrid['data_offset']
                node_values[node] = self._read_node_values(f, node_location)
            # compute coordinates of node A:
            lat_a = subgrid['S_LAT'] + (i - 1) * subgrid['LAT_INC']
            lon_a = subgrid['E_LONG'] + (j - 1) * subgrid['LONG_INC']
            # Compute interpolation scale factors
            x = (lon_p - lon_a) / subgrid['LONG_INC']
            y = (lat_p - lat_a) / subgrid['LAT_INC']
            # Compute latitude interpolation parameters
            interpolated_values = {}
            for key in node_values['A']:
                a0 = node_values['A'][key]
                a1 = node_values['B'][key] - node_values['A'][key]
                a2 = node_values['C'][key] - node_values['A'][key]
                a3 = node_values['A'][key] + node_values['D'][key] - node_values['B'][key] - node_values['C'][key]
                # interpolate values
                interpolated_values[key] = a0 + a1*x + a2*y + a3*x*y
            # Subtract interpolated shift to compute estimate of AGD coordinates
            lat_est = lat - interpolated_values['lat_shift']
            lon_est = lon - interpolated_values['lon_shift']

        # Convert accuracy figures to m
        # if any on the accuracy node values are equal to -1 then the accuracy cannot be calculated
        acc_values = [node_values['A']['lat_acc'], node_values['B']['lat_acc'], node_values['C']['lat_acc'], node_values['D']['lat_acc'],
                      node_values['A']['lon_acc'], node_values['B']['lon_acc'], node_values['C']['lon_acc'], node_values['D']['lon_acc']]
        if -1.0 in acc_values:
            lat_trans_acc = '***'
            lon_trans_acc = '***'
        else:
            lat_trans_acc = interpolated_values['lat_acc'] * math.pi * major_f / (3600 * 180)
            lon_trans_acc = (math.cos(math.radians(self.convert_seconds_to_decimal_degrees(lat))) * interpolated_values['lon_acc'] * math.pi * major_f / (3600 * 180))

        # print('{}, {}'.format(lat_p, lon_p))
        # print(subgrid)
        # print(number_of_columns)
        # print('{}, {}'.format(i, j))
        # print(grid_node_locations)
        # print('{}, {}'.format(x, y))
        # print(node_values)
        # print(interpolated_values)
        # print(major_f)
        # print(acc_values)
        # print(lat_trans_acc)
        # print(lon_trans_acc)

        return {
            'latitude': self.convert_seconds_to_decimal_degrees(lat_est),
            'longitude': -self.convert_seconds_to_decimal_degrees(lon_est),  # longitude values within the Australian Ntv2 files are Positive West and so need to be multiplied by -1
            'lat_trans_acc': lat_trans_acc,
            'lon_trans_acc': lon_trans_acc
        }

    @staticmethod
    def _get_subgrid_to_use(headers, lat, lon):
        subgrid_name = 'NONE'
        subgrid_to_use = {}
        child_subgrids_present = True
        loop_counter_1 = 0
        loop_counter_2 = 0
        while child_subgrids_present:
            subgrid_count = 0
            loop_counter_1 += 1

            for subgrid in headers['SUB_GRID_HEADERS']:
                loop_counter_2 += 1
                if loop_counter_2 > 50:
                    break
                if subgrid['PARENT'] == subgrid_name:
                    # print('----------------------------------------------------------------------------------------')
                    # print(subgrid)
                    # print('{} < {} < {} and {} < {} < {}'.format(subgrid['S_LAT'], lat, subgrid['N_LAT'], subgrid['E_LONG'], lon, subgrid['W_LONG']))
                    if subgrid['S_LAT'] < lat < subgrid['N_LAT'] and subgrid['E_LONG'] < lon < subgrid['W_LONG']:
                        subgrid_count += 1
                        subgrid_name = subgrid['SUB_NAME']
                        subgrid_to_use = subgrid
                        break
                    # print(subgrid_name)
                    # print(subgrid_to_use)
                    # print(subgrid_count)

            if loop_counter_1 > 50:
                break

            if subgrid_count <= 0:
                child_subgrids_present = False

            if subgrid_name == 'NONE':
                raise ValueError('The supplied coordinates are outside the range covered by this grid file')

        return subgrid_to_use

    def _read_headers(self, f):
        # ensure we are at the start of the file
        f.seek(0)
        # read file overview
        file_header = self._read_file_overview_header(f)

        sub_grid_headers = []
        for i in range(0, file_header['NUM_FILE']):
            # read sub grid header
            sub_grid_headers.append(self._read_subgrid_header(f))
            # skip over data values (use 1 to seek relative to current position)
            f.seek(sub_grid_headers[i]['GS_COUNT'] * self.record_size_bytes, 1)

        return {
            'FILE_HEADER': file_header,
            'SUB_GRID_HEADERS': sub_grid_headers
        }

    def _read_file_overview_header(self, f):
        # Read the file overview header
        num_orec = struct.unpack('<8sii', f.read(self.record_size_bytes))  # number of records in overview header
        num_srec = struct.unpack('<8sii', f.read(self.record_size_bytes))  # number of records in subgrid header
        num_file = struct.unpack('<8sii', f.read(self.record_size_bytes))  # number of subgrids
        gs_type = struct.unpack('<8s8s', f.read(self.record_size_bytes))   # shift type (SECONDS)
        version = struct.unpack('<8s8s', f.read(self.record_size_bytes))   # distortion model
        system_f = struct.unpack('<8s8s', f.read(self.record_size_bytes))  # "From" ellipsoid name
        system_t = struct.unpack('<8s8s', f.read(self.record_size_bytes))  # "To" ellipsoid name
        major_f = struct.unpack('<8sd', f.read(self.record_size_bytes))    # "From" semi major axis
        minor_f = struct.unpack('<8sd', f.read(self.record_size_bytes))    # "From" semi minor axis
        major_t = struct.unpack('<8sd', f.read(self.record_size_bytes))    # "To" semi major axis
        minor_t = struct.unpack('<8sd', f.read(self.record_size_bytes))    # "To" semi minor axis

        return {
            'NUM_OREC': num_orec[1],
            'NUM_SREC': num_srec[1],
            'NUM_FILE': num_file[1],
            'GS_TYPE': gs_type[1].decode('utf-8').strip(),
            'VERSION': version[1].decode('utf-8').strip(),
            'SYSTEM_F': system_f[1].decode('utf-8').strip(),
            'SYSTEM_T': system_t[1].decode('utf-8').strip(),
            'MAJOR_F': major_f[1],
            'MINOR_F': minor_f[1],
            'MAJOR_T': major_t[1],
            'MINOR_T': minor_t[1]
        }

    def _read_subgrid_header(self, f):
        sub_name = struct.unpack('8s8s', f.read(self.record_size_bytes))   # sub grid name
        parent = struct.unpack('8s8s', f.read(self.record_size_bytes))     # parent sub grid name
        created = struct.unpack('8s8s', f.read(self.record_size_bytes))    # date
        updated = struct.unpack('<8s8s', f.read(self.record_size_bytes))   # date
        s_lat = struct.unpack('<8sd', f.read(self.record_size_bytes))      # lower latitude
        n_lat = struct.unpack('<8sd', f.read(self.record_size_bytes))      # upper latitude
        e_long = struct.unpack('<8sd', f.read(self.record_size_bytes))     # lower longitude
        w_long = struct.unpack('<8sd', f.read(self.record_size_bytes))     # upper longitude
        lat_inc = struct.unpack('<8sd', f.read(self.record_size_bytes))    # latitude interval
        long_inc = struct.unpack('<8sd', f.read(self.record_size_bytes))   # longitude interval
        gs_count = struct.unpack('<8sii', f.read(self.record_size_bytes))  # grid node count

        return {
            'SUB_NAME': sub_name[1].decode('utf-8').strip(),
            'PARENT': parent[1].decode('utf-8').strip(),
            'CREATED': created[1].decode('utf-8').strip(),
            'UPDATED': updated[1].decode('utf-8').strip(),
            'S_LAT': s_lat[1],
            'N_LAT': n_lat[1],
            'E_LONG': e_long[1],
            'W_LONG': w_long[1],
            'LAT_INC': lat_inc[1],
            'LONG_INC': long_inc[1],
            'GS_COUNT': gs_count[1],
            'data_offset': f.tell()  # add value for the offset to the start of this subgrid's values for easier access later
        }

    def _read_node_values(self, f, offset=0):
        if offset != 0:
            f.seek(offset)
        values = struct.unpack('<ffff', f.read(self.record_size_bytes))
        return {
            'lat_shift': values[0],
            'lon_shift': values[1],
            'lat_acc': values[2],
            'lon_acc': values[3]
        }

    @staticmethod
    def convert_decimal_degrees_to_seconds(dd):
        return dd * 3600

    @staticmethod
    def convert_seconds_to_decimal_degrees(s):
        return s / 3600

    def set_redfearn_systems(self, from_system, to_system):
        self.redfearn_from_system = self.get_redfearn_system(from_system)
        self.redfearn_to_system = self.get_redfearn_system(to_system)

    @staticmethod
    def get_redfearn_system(ntv2_coordinate_system):
        if ntv2_coordinate_system == 'gda94':
            return 'GDA'
        elif ntv2_coordinate_system == 'agd66' or ntv2_coordinate_system == 'agd84':
            return 'AGD'
        else:
            raise ValueError('Unknown coordinate system')

    def grid_to_grid(self, easting, northing, zone, from_system, to_system):
        self.set_redfearn_systems(from_system, to_system)
        from_latlon = redfearn.grid2latlon(easting, northing, zone, self.redfearn_from_system)
        latlon_pt = self._transform(from_system, to_system, from_latlon['latitude'], from_latlon['longitude'])
        grid_pt = redfearn.latlon2grid(latlon_pt['latitude'], latlon_pt['longitude'], self.redfearn_to_system)
        return {'easting': grid_pt['easting'],
                'northing': grid_pt['northing'],
                'zone': grid_pt['zone'],
                'lat_trans_acc': latlon_pt['lat_trans_acc'],
                'lon_trans_acc': latlon_pt['lon_trans_acc']}

    def grid_to_latlon(self, easting, northing, zone, from_system, to_system):
        self.set_redfearn_systems(from_system, to_system)
        from_latlon = redfearn.grid2latlon(easting, northing, zone, self.redfearn_from_system)
        latlon_pt = self._transform(from_system, to_system, from_latlon['latitude'], from_latlon['longitude'])
        return {'latitude': latlon_pt['latitude'],
                'longitude': latlon_pt['longitude'],
                'lat_trans_acc': latlon_pt['lat_trans_acc'],
                'lon_trans_acc': latlon_pt['lon_trans_acc']}

    def latlon_to_grid(self, latitude, longitude, from_system, to_system):
        self.set_redfearn_systems(from_system, to_system)
        latlon_pt = self._transform(from_system, to_system, latitude, longitude)
        grid_pt = redfearn.latlon2grid(latlon_pt['latitude'], latlon_pt['longitude'], self.redfearn_to_system)
        return {'easting': grid_pt['easting'],
                'northing': grid_pt['northing'],
                'zone': grid_pt['zone'],
                'lat_trans_acc': latlon_pt['lat_trans_acc'],
                'lon_trans_acc': latlon_pt['lon_trans_acc']}

    def latlon_to_latlon(self, latitude, longitude, from_system, to_system):
        latlon_pt = self._transform(from_system, to_system, latitude, longitude)
        return {'latitude': latlon_pt['latitude'],
                'longitude': latlon_pt['longitude'],
                'lat_trans_acc': latlon_pt['lat_trans_acc'],
                'lon_trans_acc': latlon_pt['lon_trans_acc']}

    @staticmethod
    def print_point(point, output_format, suppress_accuracy=False):
        if output_format == 'grid':
            print('{:40}:{:15.3f}'.format('Easting', point['easting']))
            print('{:40}:{:15.3f}'.format('Northing', point['northing']))
            print('{:40}:{:15}'.format('Zone', point['zone']))
        if output_format == 'latlon':
            print('{:40}:{:15.9f}'.format('Latitude', point['latitude']))
            print('{:40}:{:15.9f}'.format('Northing', point['longitude']))
        if not suppress_accuracy:
            print('{:40}:{:15.4f}'.format('Latitude transformation accuracy (m)', point['lat_trans_acc']))
            print('{:40}:{:15.4f}'.format('Longitude transformation accuracy (m)', point['lon_trans_acc']))

    def convert_csv_file(self, from_system, to_system, input_file_path, output_file_path=None, output_format='', suppress_accuracy=False):
        if sys.version_info[0] == 2:  # Not named on 2.6
            access = 'wb'
            kwargs = {}
        else:
            access = 'wt'
            kwargs = {'newline':''}

        if output_file_path is None:
            output_file_path = '{}_{}{}'.format(os.path.splitext(input_file_path)[0], to_system, os.path.splitext(input_file_path)[1])
        data = []
        data_type = 'unknown'
        read_pt = {}
        point_ids_present = False
        i_f = 0
        row_number = 1
        try:
            with open(input_file_path) as csv_file:
                reader = DictReaderInsensitive(csv_file)
                for row in reader:
                    if i_f == 0:
                        if 'latitude' in row and 'longitude' in row:
                            data_type = 'latlon'
                        elif 'easting' in row and 'northing' in row and 'zone' in row:
                            data_type = 'grid'
                        else:
                            print("Can't read data file, please check that it is in the correct format")
                            sys.exit(1)
                        if 'id' in row:
                            point_ids_present = True
                        i_f = 1

                    try:
                        if data_type == 'latlon':
                            read_pt = {'latitude': float(row['latitude']),
                                       'longitude': float(row['longitude'])}
                        elif data_type == 'grid':
                            read_pt = {'easting': float(row['easting']),
                                       'northing': float(row['northing']),
                                       'zone': int(row['zone'])}
                        else:
                            print('Invalid data_type')
                            sys.exit(1)

                        if point_ids_present:
                            read_pt['id'] = str(row['id']).strip()

                        data.append(read_pt)
                    except ValueError:
                        print('Invalid data on line {}'.format(row_number))

                    row_number += 1
        except IOError as e:
            print(os.strerror(e.errno))
            print("Could not find the input file: {}".format(input_file_path))
            sys.exit(1)

        try:
            with open(output_file_path, access, **kwargs) as output_file:
                fieldnames = []
                if point_ids_present:
                    fieldnames.append('id')
                if output_format == '' or output_format != 'grid' or output_format != 'latlon':
                    output_format = data_type
                if output_format == 'latlon':
                    fieldnames.extend(['latitude', 'longitude'])
                if output_format == 'grid':
                    fieldnames.extend(['easting', 'northing', 'zone'])
                if not suppress_accuracy:
                    fieldnames.extend(['latitude transformation accuracy (m)', 'longitude transformation accuracy (m)'])
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                for pt in data:
                    try:
                        if data_type == 'grid':
                            if output_format == 'latlon':
                                new_pt = self.grid_to_latlon(pt['easting'], pt['northing'], pt['zone'], from_system, to_system)
                            else:
                                output_format = 'grid'
                                new_pt = self.grid_to_grid(pt['easting'], pt['northing'], pt['zone'], from_system, to_system)
                        elif data_type == 'latlon':
                            if output_format == 'grid':
                                new_pt = self.latlon_to_grid(pt['latitude'], pt['longitude'], from_system, to_system)
                            else:
                                output_format = 'latlon'
                                new_pt = self.latlon_to_latlon(pt['latitude'], pt['longitude'], from_system, to_system)
                        else:
                            print('Invalid data_type')
                            sys.exit(1)
                    except ValueError:
                        # Could not convert data pt
                        new_pt = {'easting': self.invalid_data_string, 'northing': self.invalid_data_string, 'zone': self.invalid_data_string, 'latitude': self.invalid_data_string,
                                  'longitude': self.invalid_data_string, 'lat_trans_acc': self.invalid_data_string, 'lon_trans_acc': self.invalid_data_string}

                    if output_format == 'grid':
                        write_pt = {'easting': new_pt['easting'],
                                    'northing': new_pt['northing'],
                                    'zone': int(new_pt['zone'])}
                    if output_format == 'latlon':
                        write_pt = {'latitude': new_pt['latitude'],
                                    'longitude': new_pt['longitude']}
                    if not suppress_accuracy:
                        write_pt['latitude transformation accuracy (m)'] = new_pt['lat_trans_acc']
                        write_pt['longitude transformation accuracy (m)'] = new_pt['lon_trans_acc']
                    if point_ids_present:
                        write_pt['id'] = pt['id']
                    writer.writerow(write_pt)

        except IOError as e:
            print(os.strerror(e.errno))
            print("Could not create the output file: {}".format(output_file_path))
            sys.exit(1)

        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert between Australian grid coordinate systems (AGD66, AGD84 & GDA94)', formatter_class=SmartFormatter)
    # Required inputs
    parser.add_argument('input_format', type=str, choices=('grid', 'latlon', 'file'),
                        help="R|The type of conversion required where\n"
                             "grid   = Grid coordinate - Must provide Easting, Northing and Zone\n"
                             "latlon = Latitude and Longitude\n"
                             "file   = Convert all coordinates in input file")
    parser.add_argument('from_system', type=str, choices=('agd66', 'agd84', 'gda94'), help='The coordinate system you wish to convert FROM')
    parser.add_argument('to_system', type=str, choices=('agd66', 'agd84', 'gda94'), help='The coordinate system you wish to convert TO')
    # Optional inputs
    parser.add_argument('-latitude', '-a',  type=float, help='Latitude in decimal degrees format e.g. -37.8136')
    parser.add_argument('-longitude', '-o', type=float, help='Longitude in decimal degrees format e.g. 144.9631')
    parser.add_argument('-easting', '-e',  type=float, help='Easting in decimal format e.g. 320704.446')
    parser.add_argument('-northing', '-n', type=float, help='Northing in decimal format e.g. 5812911.7')
    parser.add_argument('-zone', '-z', type=int, help='Zone (integer)')
    parser.add_argument('-input_file', '-f', type=str, help='Full path to input file')
    parser.add_argument('-output_file', '-g', type=str, help='Full path to output file')
    parser.add_argument('-output_format', '-p', type=str, default=None, choices=('grid', 'latlon'), help='Defaults to the same as the input format')
    parser.add_argument('--suppress_accuracy', action='store_true', default=False, help='Conversion accuracies are not printed')
    # Data file inputs
    parser.add_argument('-ntv2_file', type=str, help='Full path to ntv2 data file to use (instead of defaults)')

    # Add all arguments to the local namespace
    args = parser.parse_args()

    # get new Ntv2 instance
    ntv2 = Ntv2()

    # Check for input ntv2 file
    if args.ntv2_file is not None:
        if not os.access(args.ntv2_file, os.R_OK):
            parser.error('Cannot read supplied ntv2 file')
        else:
            ntv2.set_ntv2_file(args.ntv2_file)

    if args.from_system == args.to_system and not args.output_format:
        # what are we doing?
        parser.error("Don't need to do anything to convert from {} to {}".format(args.from_system, args.to_system))
    elif args.input_format == 'grid':
        if not args.easting or not args.northing or not args.zone:
            parser.error('Easting, Northing and Zone must all be supplied to be able to convert grid coordinates')
    elif args.input_format == 'latlon':
        if not args.latitude or not args.longitude:
            parser.error('Latitude and longitude must be supplied to be able to convert latlon coordinates')
    elif args.input_format == 'file':
        if not (args.input_file and os.access(args.input_file, os.R_OK)):
            parser.error("Can't read the file: {}".format(args.input_file))
        if not args.output_file:
            args.output_file = None

    if args.input_format == 'grid':
        if args.output_format == 'latlon':
            converted_pt = ntv2.grid_to_latlon(args.easting, args.northing, args.zone, args.from_system, args.to_system)
        else:
            args.output_format = 'grid'
            converted_pt = ntv2.grid_to_grid(args.easting, args.northing, args.zone, args.from_system, args.to_system)
        ntv2.print_point(converted_pt, args.output_format, args.suppress_accuracy)
        sys.exit(0)

    elif args.input_format == 'latlon':
        if args.output_format == 'grid':
            converted_pt = ntv2.latlon_to_grid(args.latitude, args.longitude, args.from_system, args.to_system)
        else:
            args.output_format = 'latlon'
            converted_pt = ntv2.latlon_to_latlon(args.latitude, args.longitude, args.from_system, args.to_system)
        ntv2.print_point(converted_pt, args.output_format, args.suppress_accuracy)
        sys.exit(0)

    elif args.input_format == 'file':
        if ntv2.convert_csv_file(args.from_system, args.to_system, args.input_file, output_file_path=args.output_file, output_format=args.output_format, suppress_accuracy=args.suppress_accuracy):
            sys.exit(0)
        else:
            print('Could not convert file {}'.format(args.input_file))
            sys.exit(1)
