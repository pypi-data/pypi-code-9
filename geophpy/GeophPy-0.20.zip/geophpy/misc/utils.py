# -*- coding: utf-8 -*-
'''
   geophpy.misc.utils
   ------------------

   :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
   :license: GNU GPL v3.

'''
from __future__ import unicode_literals
import numpy as np



# ...TBD... following function seems not to be used !!!
def array1D_getdeltamedian(array):
   '''
   To get the median of the deltas from a 1D-array

   Parameters:

   :array: 1D-array to treat

   Returns:

   :deltamedian:

   '''
   #deltamedian = None
   #deltalist = []
   #for i in range(0,len(array)-1):
   #   if (array[i] != np.nan):
   #      prev = array[i]
   #      break
   #for val in array[i+1:]:
   #   if ((val != np.nan) and (val != prev)):
   #      deltalist.append(val - prev)
   #      prev = val
   #deltamedian = np.median(np.array(deltalist))
   #return deltamedian
   return np.median(np.diff(array))



# ...TBD... following function seems not to be used !!!
def array1D_extractdistelementslist(array):
   '''
   To extract distinct elements of a 1D-array

   Parameters:

   :array: 1D-array to treat

   Returns:

   :distlist: list of distinct values from the array

   '''
   #distlist = []
   #for val in array:
   #   if (val != np.nan):
   #      found = False
   #      for dist in distlist:
   #         if (val == dist):
   #            found = True
   #            break
   #      if (found == False):
   #         distlist.append(val)
   #return np.array(distlist)
   return np.unique(array)



def profile_completewithnan(x, y_array, nan_array, ydeltamin, factor=10, ymin=None, ymax=None):
    ''' Completes profile x with 'nan' values
    Parameters :

    :x: x value
    :y_array: 1D array to test gaps, [1,2,4,2,6,7,3,8,11,9,15,12,...]
    :nan_array: 2D array to complete with 'nan' values, [[x1, y1, 'nan'], [x2, y2, 'nan'], ...]
    :ydeltamin: delta min to test before two consecutives points, to complete with 'nan' values
    :factor: factor to take in account to test gap
    :ymin: min y position in the profile.
    :ymax: max y position in the profile.

    Returns:
        nan_array completed
    '''

    if (ymin == None):
        yprev = y_array[0]
        indexfirst = 1
    else:
        yprev = ymin
        indexfirst = 0

    for y in y_array[indexfirst:]:
        ydelta = y - yprev
        if (ydelta > (factor*2*ydeltamin)):
            # complete with 'nan' values
            for i in range(1,int(np.around(ydelta/ydeltamin))):
                nan_array.append([x, yprev+i*ydeltamin/2, np.nan])
                nan_array.append([x, y-i*ydeltamin/2, np.nan])
        yprev = y

    if (ymax != None):
        # treats the last potential gap
        ydelta = ymax - yprev
        if (ydelta > (factor*2*ydeltamin)):
            # complete with 'nan' values
            for i in range(1,int(np.around(ydelta/ydeltamin))):
                nan_array.append([x, yprev+i*ydeltamin/2, np.nan])
                nan_array.append([x, ymax-i*ydeltamin/2, np.nan])

    return nan_array



# ...TBD... following function seems not to be used !!!
def array2D_extractyprofile(x, x_array, y_array):
   '''
   To extract the y profile at x coordinate

   Parameters:

   :x: x value at which to extract the y profile

   :x_array: 1D-array containing x values associated to each y value

   :y_array: 1D-array containing y profiles

   Note: x_array and y_array must have the same dimension, but do not need to be sorted

   Returns:

   :profile: unique y values encountered at x coordinate, in ascending order

   '''
   #profile = []
   #for i in range(0, len(x_array)-1):
   #   if (x_array[i] == x):
   #      profile.append(y_array[i])
   #return np.array(profile)
   return np.unique(y_array[np.where(x_array == x)])



def getdecimalsnb(value):
   '''
   To get the number of decimals from a float value

   Parameters:

   :value: float number to treat

   Returns:

   :decimalsnb: decimal precision of the value

   '''
   decimalsnb = 0
### use abs(value) in order to :
###- avoid referencing value
###- get the correct answer when value is negative
   test = abs(value)
   while ((test - int(test)) > 0.):
      decimalsnb += 1
      test *= 10
   return decimalsnb



def zimage_xcoord(dataset):
   '''
   To get the X coordinates array of a Z_image
   '''
   return np.array([np.linspace(dataset.info.x_min,dataset.info.x_max,dataset.data.z_image.shape[1])])



def zimage_ycoord(dataset):
   '''
   To get the Y coordinates array of a Z_image
   '''
   return np.array([np.linspace(dataset.info.y_min,dataset.info.y_max,dataset.data.z_image.shape[0])]).T
