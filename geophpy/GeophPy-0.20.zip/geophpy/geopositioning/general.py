# -*- coding: utf-8 -*-
'''
   geophpy.geopositioning.general
   ------------------------------

   DataSet Object general geopositioning routines.

   :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
   :license: GNU GPL v3.

'''

import numpy as np
from scipy.interpolate import griddata
from geophpy.geoposset import *



def setgeoref(dataset, refsystem, points_list, utm_zoneletter=None, utm_zonenumber=None):
   '''
   cf. dataset.py

   '''
   if (len(points_list) >= 4):
      if (refsystem == 'WGS84'):
         easting_array = []
         northing_array = []
         for point in points_list:        # building of the easting and northing arrays
            easting_value, northing_value, utm_zonenumber, utm_zoneletter = wgs84_to_utm(point[2], point[1])
            easting_array.append(easting_value)
            northing_array.append(northing_value)
      else:                               # if refsystem == 'UTM'
         easting_array = points_list.T[1]
         northing_array = points_list.T[2]
      
      x_array = points_list.T[3]
      y_array = points_list.T[4]
   
      nx   = np.around((dataset.info.x_max-dataset.info.x_min)/dataset.info.x_gridding_delta) + 1
      ny   = np.around((dataset.info.y_max - dataset.info.y_min)/dataset.info.y_gridding_delta) + 1

      # Build the (xi, yi) regular vector coordinates ###################
      xi = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
      yi = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)

      # Build the (X, Y) regular grid coordinates #######################
      X, Y = np.meshgrid(xi, yi)

      # Interpolate the easting image #######################################
      easting = griddata((x_array, y_array), easting_array, (X, Y), method='linear')
      # Interpolate the northing image #######################################
      northing = griddata((x_array, y_array), northing_array, (X, Y), method='linear')


      if (np.isnan(easting).any() or np.isnan(northing).any()):   # if a nan occured in built arrays
         error = -2     # dataset zone greater than points list zone
      else:             # no error
         error = 0      
         dataset.data.easting_image = easting
         dataset.data.northing_image = northing
         dataset.georef.active = True
         dataset.georef.refsystem = refsystem
         dataset.georef.points_list = points_list
         dataset.georef.utm_zoneletter = utm_zoneletter
         dataset.georef.utm_zonenumber = utm_zonenumber
   else:
      error = -1        # not enough points
      
   return error