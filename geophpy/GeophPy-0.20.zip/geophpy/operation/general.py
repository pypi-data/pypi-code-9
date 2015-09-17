# -*- coding: utf-8 -*-
'''
   geophpy.operation.general
   -------------------------

   DataSet Object general operations routines.

   :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
   :license: GNU GPL v3.

'''
### USER DEFINED PARAMETERS ##########################################

# list of "griddata" interpolation methods available for wumappy interface
gridding_interpolation_list = ['none', 'nearest', 'linear', 'cubic']

######################################################################



import numpy as np
from scipy.interpolate import griddata, RectBivariateSpline
from copy import deepcopy
from geophpy.misc.utils import *



def copy(dataset):
   '''
   cf. dataset.py

   '''
###ORIGINAL CODE having some flaws:
###- newdataset was a parameter instead of a "return"
###- values were correctly handled but the code was sequential
###- zimage was duplicated as a tuple instead of an np.array
###- fields and info were not duplicated but "referenced"
###- georef was missing ...
   #newdataset.data.values = []
   #for l in range(len(dataset.data.values)):
      ## for each line adds a value in the column
      #newdataset.data.values.append(dataset.data.values[l])
   #newdataset.data.values = np.array(newdataset.data.values)
   #newdataset.data.z_image = []
   #for l in range(len(dataset.data.z_image)):
      #newdataset.data.z_image.append(dataset.data.z_image[l])
   #newdataset.data.fields = dataset.data.fields
   #newdataset.info = dataset.info
###SECOND CODE somewhat better:
   ## initialisation of the duplicate DataSet Object
   #newdataset = DataSet._new()
   ## duplication of the raw values
   #newdataset.data.values = dataset.data.values.copy()
   ## duplication of the zimage
   #newdataset.data.z_image = dataset.data.z_image.copy()
   ## duplication of the fieldnames
   #newdataset.data.fields = dataset.data.fields.copy()
   ## duplication of the dataset meta data
   #newdataset.info = deepcopy(dataset.info)
   ## duplication of the georeferencing meta data
   #newdataset.georef.active = (dataset.georef.active & True)
   #newdataset.georef.points_list = dataset.georef.points_list.copy()
   #return newdataset
###THIRD CODE straightforward:
   return deepcopy(dataset)



def getgriddinginterpolationlist():
   """
   cf. dataset.py

   """
   return gridding_interpolation_list



def interpolate(dataset, interpolation="none", x_delta=None, y_delta=None, x_decimal_maxnb=2, y_decimal_maxnb=2, x_frame_factor=0., y_frame_factor=0.):
   '''
   cf. dataset.py

   '''
   T = dataset.data.values.T
   x_array = T[0]
   y_array = T[1]
   z_array = T[2]

   # Get distinct x values ###########################################
   x_list = np.unique(x_array)

   # Get the median delta between two distinct x values ##############
   if (x_delta == None):
      if (x_decimal_maxnb == None):
         # Undefined x rounding precision ############################
         # ...TBD... raise an error here !
         pass
      x_delta = np.median(np.around(np.diff(x_list), x_decimal_maxnb))
      # ...TBD... why not take the min diff value instead of the median ?
      #x_delta = np.nanmin(np.around(np.diff(x_list), x_decimal_maxnb))
   else:
      x_decimal_maxnb = getdecimalsnb(x_delta)

   # Determinate min and max x coordinates and number of x pixels ####
   xmin = x_array.min()
   xmax = x_array.max()
   xmin = (1.+x_frame_factor)*xmin - x_frame_factor*xmax
   xmax = (1.+x_frame_factor)*xmax - x_frame_factor*xmin
   xmin = round(xmin, x_decimal_maxnb)
   xmax = round(xmax, x_decimal_maxnb)
   # Don't forget the "+1" (éternel pb poteaux et intervalles !) #####
   nx   = np.around((xmax-xmin)/x_delta) + 1

   # Get the median delta between two distinct y values ##############
   if (y_delta == None):
      if (y_decimal_maxnb == None):
         # Undefined y rounding precision ############################
         # ...TBD... raise an error here !
         pass
      # Get median value for each profile ############################
      deltamedianlist = []
      for x in x_list:
         # Extract the y profile at x coordinate #####################
         profile = np.unique(y_array[np.where(x_array == x)])
         # Append the median of this y profile #######################
         deltamedianlist.append(np.median(np.around(np.diff(profile), y_decimal_maxnb)))
         # ...TBD... why not take the min diff value instead of the median ?
         #deltamedianlist.append(np.nanmin(np.around(np.diff(profile), y_decimal_maxnb)))
      # Get median value of all median values ########################
      y_delta = np.median(np.array(deltamedianlist))
      # ...TBD... why not take the min diff value instead of the median ?
      #y_delta = np.nanmin(np.array(deltamedianlist))
   else:
      y_decimal_maxnb = getdecimalsnb(y_delta)

   # Determinate min and max y coordinates and number of y pixels ####
   ymin = y_array.min()
   ymax = y_array.max()
   ymin = (1.+y_frame_factor)*ymin - y_frame_factor*ymax
   ymax = (1.+y_frame_factor)*ymax - y_frame_factor*ymin
   ymin = round(ymin, y_decimal_maxnb)
   ymax = round(ymax, y_decimal_maxnb)
   # Don't forget the "+1" (éternel pb poteaux et intervalles !) #####
   ny   = np.around((ymax - ymin)/y_delta) + 1

   # Build the (xi, yi) regular vector coordinates ###################
   xi = np.linspace(xmin, xmax, nx, endpoint=True)
   yi = np.linspace(ymin, ymax, ny, endpoint=True)

   # Build the (X, Y) regular grid coordinates #######################
   X, Y = np.meshgrid(xi, yi)

   # Build the Zimage regularly gridded matrix #######################
   if (interpolation == "none"):
      ## just project data into the grid
      ## if several data points fall into the same pixel, they are averaged
      ## don't forget to "peakfilt" the rawvalues beforehand to avoid averaging bad data points
      Z = X * 0.
      P = Z.copy()
      for x,y,z in dataset.data.values:
         indx = np.where(xi+x_delta/2. > x)
         indy = np.where(yi+y_delta/2. > y)
         Z[indy[0][0],indx[0][0]] += z
         P[indy[0][0],indx[0][0]] += 1
      Z = Z/P
   elif (interpolation in getgriddinginterpolationlist()) :
      ## perform data interpolation onto the grid
      ## the interpolation algorithm will deal with overlapping data points
      ## nevertheless don't forget to "peakfilt" the rawvalues beforehand to avoid interpolation being too much influenced by bad data points
      '''
      # Fill holes in each profiles with "nan" #######################
      ## this is to avoid filling holes with interpolated values
      nan_array = []
      for x in x_list:
         profile = np.unique(y_array[np.where(x_array == x)])
         nan_array = profile_completewithnan(x, profile, nan_array, y_delta, factor=2, ymin=ymin, ymax=ymax)
      if (len(nan_array) != 0):
         completed_array = np.append(dataset.data.values, np.array(nan_array), axis=0)
         T = completed_array.T
         x_array = T[0]
         y_array = T[1]
         z_array = T[2]
      '''
      # Interpolate the Zimage #######################################
      Z = griddata((x_array, y_array), z_array, (X, Y), method=interpolation)
   else:
      # Undefined interpolation method ###############################
      # ...TBD... raise an error here !
      pass

   # Fill the DataSet Object #########################################
   dataset.data.z_image = Z
   dataset.info.x_min = xmin
   dataset.info.x_max = xmax
   dataset.info.y_min = ymin
   dataset.info.y_max = ymax
   dataset.info.z_min = np.nanmin(Z)
   dataset.info.z_max = np.nanmax(Z)
   dataset.info.x_gridding_delta = x_delta
   dataset.info.y_gridding_delta = y_delta
   dataset.info.gridding_interpolation = interpolation



#def apodisation2d(val, apodisation_factor):
   '''
   2D apodisation, to reduce side effects

   Parameters :

   :val: 2-Dimension array

   :apodisation_factor: apodisation factor in percent (0-25)

   '''
#   if (apodisation_factor > 0):
#      # apodisation in the x direction
#      for profile in val.T:
#         _apodisation1d(profile, apodisation_factor)

      # apodisation in the y direction
#      for profile in val:
#         _apodisation1d(profile, apodisation_factor)



#def _apodisation1d(array1D, apodisation_factor):
   '''
   1D apodisation, to reduce side effects

   Parameters :

   :array1D: 1-Dimension array

   :apodisation_factor: apodisation factor in percent (0-25)

   '''
#   na = len(array1D)                                  # n is the number of array elements
#   napod = int(np.around((na * apodisation_factor)/100))     # napod is the number of array elements to treat
#   if (napod <= 1):                                   # one element at least must be treated
#      napod = 1
#   pi2 = np.pi/2.
#   for n in range(napod):                             # for napod first data
#      array1D[n] = array1D[n]*np.cos((napod-n)*pi2/napod)

#   for n in range(na-napod, na):                      # for napod last data
#      array1D[n] = array1D[n]*np.cos((n+1-na+napod)*pi2/napod)



def apodisation2d(val, apodisation_factor):
   '''
   2D apodisation, to reduce side effects

   Parameters :

   :val: 2-Dimension array

   :apodisation_factor: apodisation factor in percent (0-25)

   Returns :
      - apodisation pixels number in x direction
      - apodisation pixels number in y direction
      - enlarged array after apodisation
   '''

   array2DTemp = []
   array2D = []
   
   if (apodisation_factor > 0):
      # apodisation in the x direction
      nx = len(val.T[0])                                       # n is the number of array elements
      napodx = int(np.around((nx * apodisation_factor)/100))   # napod is the number of array elements to treat
      if (napodx <= 1):                                        # one element at least must be treated
         napodx = 1
      for profile in val.T:
         array2DTemp.append(_apodisation1d(profile, napodx))
      array2DTemp = (np.array(array2DTemp)).T

      # apodisation in the y direction
      ny = len(array2DTemp[0])                                 # n is the number of array elements
      napody = int(np.around((ny * apodisation_factor)/100))   # napod is the number of array elements to treat
      if (napody <= 1):                                        # one element at least must be treated
         napody = 1
      for profile in array2DTemp:
         array2D.append(_apodisation1d(profile, napody))
   else:                                                       # apodisation factor = 0
      array2D = val

#   return napodx, napody, np.array(array2D)
   return np.array(array2D)



def _apodisation1d(array1D, napod):
   '''
   1D apodisation, to reduce side effects

   Parameters :

   :array1D: 1-Dimension array

   :napod: apodisation pixels number

   Returns : 1-Dimension array of len(array1D) + napod elements
   

   '''
   pi2 = np.pi/2.

   na = len(array1D)                                 # n is the number of array elements
   nresult = na + 2*napod
   array1Dresult = []
   for n in range(napod):
      array1Dresult.append(array1D[n]*np.cos((napod-n)*pi2/napod))
   for n in range(na):
      array1Dresult.append(array1D[n])
   for n in range(na-napod, na):                      # for napod last data
      array1Dresult.append(array1D[n]*np.cos((n+1-na+napod)*pi2/napod))

   return array1Dresult   



def apodisation2Dreverse(val, valwithapod, napodx, napody):
   '''
   To do the reverse apodisation
   '''
   na = len(val)
   nb = len(val[0])
   for n in range(na):
      for m in range(nb):
         val[n][m] = valwithapod[n+napody][m+napodx]


def sample(dataset):
   '''
   To rebuild the Values from a Z_image
   '''
   X = zimage_xcoord(dataset)
   Y = zimage_ycoord(dataset)
   Z = dataset.data.z_image
   xi = dataset.data.values[:,0]
   yi = dataset.data.values[:,1]
   zi = dataset.data.values[:,2]
   zCubSpl = RectBivariateSpline(Y, X, Z, kx=3, ky=3)   # why Y,X ?
   zj = zCubSpl.ev(xi, yi, dx=0, dy=0)
   zi *= 0.
   zi += zj
