#!/usr/bin/env python

#-----------------------------------------------------------------------------#
#   neighborhoods.py                                                          #
#                                                                             #
#   Copyright (c) 2015, StyleSeat, Inc.                                       #
#   All rights reserved.                                                      #
#-----------------------------------------------------------------------------#

import glob
import inspect
import os

import fiona
import shapely.geometry

class Neighborhood(object):
    _ATTRS = ('state', 'county', 'city', 'name')

    def __init__(self, lon, lat, state=None):
        for attr in self._ATTRS:
            setattr(self, attr, '')
        data_dir = self._compute_data_dir()
        shapefile_paths = self._compute_shapefile_paths(data_dir, state=state)
        self._find_neighborhood(lon, lat, shapefile_paths)

    def __repr__(self):
        id = (getattr(self, attr) for attr in ('name', 'city', 'state'))
        id = ', '.join(id)
        return self.__class__.__name__ + "({})".format(id)

    def __str__(self):
        return self.name

    def _compute_data_dir(self):
        current_file = inspect.getfile(self.__class__)
        current_dir = os.path.dirname(current_file)
        data_dir = os.path.join(current_dir, 'data')
        return data_dir

    def _compute_shapefile_paths(self, data_dir, state=None):
        if not state:
            state = ''
        shapefile_pattern = os.path.join(data_dir, '*{}.shp'.format(state))
        shapefile_paths = glob.glob(shapefile_pattern)
        return shapefile_paths

    def _find_neighborhood(self, lon, lat, shapefile_paths):
        point = shapely.geometry.Point(lon, lat)
        for shapefile_path in shapefile_paths:
            with fiona.open(shapefile_path) as fiona_collection:
                for shapefile_record in fiona_collection:
                    shape = shapely.geometry.asShape(shapefile_record['geometry'])
                    if shape.contains(point):
                        for attr in self._ATTRS:
                            value = shapefile_record['properties'][attr.upper()]
                            setattr(self, attr, value)
                        return
