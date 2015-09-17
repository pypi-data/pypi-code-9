# -*- coding: utf-8 -*-
'''
    geophpy.processing.magnetism
    ----------------------------

    DataSet Object general magnetism processing routines.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import numpy as np
from scipy.linalg import lu_solve, lu_factor
from geophpy.operation.general import *

def logtransform(dataset, multfactor=5):
   '''
   To transform the data in logarihtmics values

   Parameters :

   :dataset: DataSet Object to do the treatment
   
   :multfactor: multiplying factor

   '''

   val = dataset.data.z_image

   # Calculation of lines and columns numbers
   ny = len(val)
   nx = len(val[0])
   
   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if (val[iy][ix] != np.nan) :                          # if valid value
            val[iy][ix] = val[iy][ix] * multfactor             # multiplying

   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((val[iy][ix] != np.nan) and (val[iy][ix] < -1)):
            val[iy][ix] = -np.log10(-val[iy][ix])

   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((val[iy][ix] != np.nan) and (val[iy][ix] > 1)):
            val[iy][ix] = np.log10(val[iy][ix])

   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((val[iy][ix] != np.nan) and (val[iy][ix] > -1) and (val[iy][ix] < 1)) :
            val[iy][ix] = np.nan

   dataset.data.z_image = val



def polereduction(dataset, apod=0, inclineangle = 65, alphaangle = 0):
   '''
   To reduce at the magnetic pôle from a DataSet Object.

   Parameters:

   :dataset: DataSet Object to do the treatment
   
   :apod: apodisation factor (%), to reduce bord effects

   :inclinangle: incline angle of the magnetic field

   :alphaangle: angle of magnetic field and y axe

   '''

   val = dataset.data.z_image
   
   # Calculation of lines and columns numbers
   ny = len(val)
   nx = len(val[0])
   # Calculation of total values number
   nt = nx * ny

   nan_indexes = np.isnan(val)                                 # searches the 'nan' indexes in the initial array
   if(np.isnan(val).any()):                                    # if at least 1 'nan' is detected in the array,
      
      x = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
      y = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)
      _fillnanvalues(x, y, val.T)                              # fills the 'nan' values by interpolated values

   if (apod > 0):
      apodisation2d(val, apod)

   # Meaning calculation
   mean = val.mean()

   # complex conversion, val[][] -> cval[][]
   cval = np.array(val, dtype=complex)

   # fast fourier series calculation
   cvalfft = np.fft.fft2(cval)

   # filter application
   # deg->rad angle conversions
   rinc = (inclineangle*np.pi)/180 # inclination in radians
   ralpha = (alphaangle*np.pi)/180  # alpha angle in radians

   cosu = np.absolute(np.cos(rinc) * np.cos(ralpha))
   cosv = np.absolute(np.cos(rinc) * np.sin(ralpha))
   cosz = np.sin(rinc)

   deltax = dataset.info.x_gridding_delta
   deltay = dataset.info.y_gridding_delta
   
   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            cz = np.sqrt(np.square(cu) + np.square(cv))
            cred = complex(cz*cosz, cu*cosu + cv*cosv)
            cvalfft[iy][ix] = ((cvalfft[iy][ix] * np.square(cz))/np.square(cred))

   # FFT inversion
   icvalfft = np.fft.ifft2(cvalfft)
   val = icvalfft.real + mean                                  # real part added to mean calculation

   val[nan_indexes] = np.nan                                   # set the initial 'nan' values, as in the initial array

   dataset.data.z_image = val                                  # to get the 'z_image' array in (x,y) format.



def continuation(dataset, prosptech, apod, downsensoraltitude, upsensoraltitude, continuationflag, continuationvalue):
   '''
   Continuation of the magnetic field

   Parameters :

   :dataset: DataSet Object to do the treatment
   
   :prosptech: Prospection technical

   :apod: apodisation factor (%), to reduce bord effects

   :downsensoraltitude: Altitude of the down magnetic sensor

   :upsensoraltitude: Altitude of the up magnetic sensor

   :continuationflag: Continuation flag, False if not continuation

   :continuationvalue: Continuation altitude, greater than 0 if upper earth ground, lower than 0 else
   
   '''

   val = dataset.data.z_image

   # Calculation of lines and columns numbers
   ny = len(val)
   nx = len(val[0])
   # Calculation of total values number
   nt = nx * ny

   nan_indexes = np.isnan(val)                                 # searches the 'nan' indexes in the initial array
   if(np.isnan(val).any()):                                    # if at least 1 'nan' is detected in the array,
      
      x = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
      y = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)
      _fillnanvalues(x, y, val.T)                                # fills the 'nan' values by interpolated values

   if (apod > 0):
      apodisation2d(val, apod)

   dz = downsensoraltitude - upsensoraltitude     
   zp = - continuationvalue + downsensoraltitude

   # complex conversion, val[][] -> cval[][]
   cval = np.array(val, dtype=complex)

   # fast fourier series calculation
   cvalfft = np.fft.fft2(cval)

   deltax = dataset.info.x_gridding_delta
   deltay = dataset.info.y_gridding_delta

   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            cz = np.sqrt(np.square(cu) + np.square(cv)) * (2. * np.pi)
            if (continuationflag == True):
               ce = np.exp(zp * cz)
               cvalfft[iy][ix] = (cvalfft[iy][ix] * complex(ce, 0.))
            if (prosptech == prosptechlist[1]):                # if prospection technic is magnetic field gradient
               cdz = 1. - np.exp(dz * cz)
               cvalfft[iy][ix] = (cvalfft[iy][ix] / complex(cdz, 0.))

   # FFT inversion
   icvalfft = np.fft.ifft2(cvalfft)
   val = icvalfft.real

   val[nan_indexes] = np.nan                                   # set the initial 'nan' values, as in the initial array

   dataset.data.z_image = val                                  # to get the 'z_image' array in (x,y) format.


def eulerdeconvolution(dataset, xmin, xmax, ymin, ymax, apod=0, nflag=False, nvalue=0):
   '''
   cf. dataset   
   '''

   val = dataset.data.z_image

   # Calculation of lines and columns numbers
   ny = len(val)
   nx = len(val[0])
   # Calculation of total values number
   nt = nx * ny

   x = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
   y = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)

   nan_indexes = np.isnan(val)                                 # searches the 'nan' indexes in the initial array
   if(np.isnan(val).any()):                                    # if at least 1 'nan' is detected in the array,     
      _fillnanvalues(x, y, val.T)                                # fills the 'nan' values by interpolated values

   if (apod > 0):
      apodisation2d(val, apod)

   # complex conversion, val[][] -> cval[][]
   cval = np.array(val, dtype=complex)
   val = cval.real

   deltax = dataset.info.x_gridding_delta
   deltay = dataset.info.y_gridding_delta

   # fast fourier series calculation
   cvalfft = np.fft.fft2(cval)
   cvalfftdx = np.array(np.zeros((ny,nx)), dtype=complex)
   cvalfftdy = np.array(np.zeros((ny,nx)), dtype=complex)
   cvalfftdz = np.array(np.zeros((ny,nx)), dtype=complex)

   # derivations calculation
   for iy in range(ny):                                        # for each column
      for ix in range(nx):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            cz = np.sqrt(np.square(cu) + np.square(cv))
            # x derivation 
            cvalfftdx[iy][ix] = cvalfft[iy][ix]*complex(0., cu*np.pi*2.)
            # y derivation 
            cvalfftdy[iy][ix] = cvalfft[iy][ix]*complex(0., cv*np.pi*2.)
            # z derivation 
            cvalfftdz[iy][ix] = cvalfft[iy][ix]*cz*np.pi*2.
         else:
            cvalfftdx[0][0] = complex(0., 0.)
            cvalfftdy[0][0] = complex(0., 0.)
            cvalfftdz[0][0] = complex(0., 0.)

   # FFT inversion
   valdx = (np.fft.ifft2(cvalfftdx)).real
   valdy = (np.fft.ifft2(cvalfftdy)).real
   valdz = (np.fft.ifft2(cvalfftdz)).real

   ixmin, xnearestmin = _searchnearest(x, xmin)
   ixmax, xnearestmax = _searchnearest(x, xmax)
   
   iymin, ynearestmin = _searchnearest(y, ymin)
   iymax, ynearestmax = _searchnearest(y, ymax)

   if ((nflag == 0) or (nvalue==0)):   # automatic calculation structural index
                                       # 4 unknowns equation to solve
      b = np.zeros(4)
      A = np.zeros((4,4))
      for l in range(iymin, iymax+1):
         for c in range(ixmin, ixmax+1):
            coef = x[c] * valdx[l][c] + y[l] * valdy[l][c]
            b[0] += coef * val[l][c]
            b[1] += coef * valdx[l][c]
            b[2] += coef * valdy[l][c]
            b[3] += coef * valdz[l][c]

            A[0][0] += np.square(val[l][c])
            A[0][1] += val[l][c] * valdx[l][c]
            A[0][2] += val[l][c] * valdy[l][c]
            A[0][3] += val[l][c] * valdz[l][c]
            A[1][1] += np.square(valdx[l][c])
            A[1][2] += valdx[l][c] * valdy[l][c]
            A[1][3] += valdx[l][c] * valdz[l][c]
            A[2][2] += np.square(valdy[l][c])
            A[2][3] += valdy[l][c] * valdz[l][c]
            A[3][3] += np.square(valdz[l][c])

      # symmetry
      A[1][0] = A[0][1]
      A[2][0] = A[0][2]
      A[3][0] = A[0][3]
      A[2][1] = A[1][2]
      A[3][1] = A[1][3]
      A[3][2] = A[2][3]

      x = _gaussresolution(A, b)
      nvalue = -x[0]
      xpt = x[1]
      ypt = x[2]
      depth = x[3]
      
   else :                              # fixed structural index
                                       # 3 unknowns equation to solve
      b = np.zeros(3)
      A = np.zeros((3,3))
      for l in range(iymin, iymax+1):
         for c in range(ixmin, ixmax+1):
            coef = nvalue * val[l][c] + x[c] * valdx[l][c] + y[l] * valdy[l][c]
            b[0] += coef * valdx[l][c]
            b[1] += coef * valdy[l][c]
            b[2] += coef * valdz[l][c]

            A[0][0] += np.square(valdx[l][c])
            A[0][1] += valdx[l][c] * valdy[l][c]
            A[0][2] += valdx[l][c] * valdz[l][c]
            A[1][1] += np.square(valdy[l][c])
            A[1][2] += valdy[l][c] * valdz[l][c]
            A[2][2] += np.square(valdz[l][c])

      # symmetry
      A[1][0] = A[0][1]
      A[2][0] = A[0][2]
      A[2][1] = A[1][2]

      x = _gaussresolution(A, b)
      xpt = x[0]
      ypt = x[1]
      depth = x[2]
      

   
   return nvalue, xpt, ypt, depth, xnearestmin, ynearestmin, xnearestmax, ynearestmax



def _searchnearest(array, val):
   '''
   Search the nearset value of val, in the array

   Parameters :

   :array:  1D array ordered to find the nearest value of val

   :val: value to find

   Returns :

   :index: index in the array of the nearest value found

   :valnearest: value of the nearest value found
   
   '''
   n = len(array)
   for i in range(n):
      gap = abs(val-array[i])
      if ((i==0) or (gap<mingap)):
         mingap = gap
         index = i
   return index, array[index]            
      


def _gaussresolution(A,b):
   '''
   Solving Ax=b equation with gauss pivot and LU factorisation
   '''
   
   n=len(A)
   # gauss pivot calculation
   for i1 in range(n-1):
      # find the partial pivot
      l=i1      
      xam = np.absolute(A[i1][i1])
      for j in range(i1+1,n):
         x = np.absolute(A[j][i1])
         if (x>xam):
            xam = x
            l=j

      # set pivot at its place, swapping pivot and current lines
      if (l>i1):
         aux = b[l]
         b[l] = b[i1]
         b[i1] = aux
         for j in range(n):
            aux = A[l][j]
            A[l][j] = A[i1][j]
            A[i1][j] = aux

   # solves Ax=b using LU factorisation
   x = lu_solve(lu_factor(A), b)

   return x



def analyticsignal(dataset, apod=0):
   '''
   cf. dataset
   '''
   
   val = dataset.data.z_image

   # Calculation of lines and columns numbers
   ny = len(val)
   nx = len(val[0])
   # Calculation of total values number
   nt = nx * ny

   nan_indexes = np.isnan(val)                                 # searches the 'nan' indexes in the initial array
   if(np.isnan(val).any()):                                    # if at least 1 'nan' is detected in the array,
      
      x = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
      y = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)
      _fillnanvalues(x, y, val.T)                              # fills the 'nan' values by interpolated values

   if (apod > 0):
      apodisation2d(val, apod)

   # complex conversion, val[][] -> cval[][]
   cval = np.array(val, dtype=complex)

   deltax = dataset.info.x_gridding_delta
   deltay = dataset.info.y_gridding_delta

   # fast fourier series calculation
   cvalfft = np.fft.fft2(cval)
   cvalfftdx = np.fft.fft2(cval)
   cvalfftdy = np.fft.fft2(cval)
   cvalfftdz = np.fft.fft2(cval)

   # dx derivations calculation
   cvalfftdx[0][0] = complex(0., 0.)
   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            # x derivation 
            cvalfftdx[iy][ix] = cvalfft[iy][ix]*complex(0., cu*np.pi*2)
         
   # FFT inversion
   icvalfft = np.fft.ifft2(cvalfftdx)
   val = np.square(icvalfft.real)

   # dy derivations calculation
   cvalfftdy[0][0] = complex(0., 0.)
   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            # y derivation 
            cvalfftdy[iy][ix] = cvalfft[iy][ix]*complex(0., cv*np.pi*2)
         
   # FFT inversion
   icvalfft = np.fft.ifft2(cvalfftdy)
   val = val + np.square(icvalfft.real)

   # dz derivations calculation
   cvalfftdz[0][0] = complex(0., 0.)
   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            cz = np.sqrt(np.square(cu) + np.square(cv))
            # z derivation 
            cvalfftdz[iy][ix] = cvalfft[iy][ix]*cz*np.pi*2
         
   # FFT inversion
   icvalfft = np.fft.ifft2(cvalfftdz)
   val = np.sqrt(val + np.square(icvalfft.real))

   val[nan_indexes] = np.nan                                   # set the initial 'nan' values, as in the initial array

   dataset.data.z_image = val                                  # to get the 'z_image' array in (x,y) format.



def gradmagfieldconversion(dataset, prosptechused, prosptechsim, apod=0, downsensoraltused = 0.3, upsensoraltused = 1.0, downsensoraltsim = 0.3, upsensoraltsim = 1.0, inclineangle = 65, alphaangle = 0):
   '''
   cf. dataset
   '''
   
   case, sense = _definecaseandsense(prosptechused, prosptechsim)

   if ((case != None) and (sense != None)):

      val = dataset.data.z_image

      # Calculation of lines and columns numbers
      ny = len(val)
      nx = len(val[0])
      # Calculation of total values number
      nt = nx * ny

      nan_indexes = np.isnan(val)                                 # searches the 'nan' indexes in the initial array
      if(np.isnan(val).any()):                                    # if at least 1 'nan' is detected in the array,
      
         x = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
         y = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)
         _fillnanvalues(x, y, val.T)                              # fills the 'nan' values by interpolated values

      if (apod > 0):
         apodisation2d(val, apod)

      # complex conversion, val[][] -> cval[][]
      cval = np.array(val, dtype=complex)

      deltax = dataset.info.x_gridding_delta
      deltay = dataset.info.y_gridding_delta

      # fast fourier series calculation
      cvalfft = np.fft.fft2(cval)

      if (case >= 2):
         # deg->rad angle conversions
         rinc = (inclineangle*np.pi)/180 # inclination in radians
         ralpha = (alphaangle*np.pi)/180  # alpha angle in radians
         cosu = np.absolute(np.cos(rinc) * np.cos(ralpha))
         cosv = np.absolute(np.cos(rinc) * np.sin(ralpha))
         cosz = np.sin(rinc)

      for ix in range(nx):                                        # for each column
         for iy in range(ny):                                     # for each line
            if ((ix != 0) or (iy != 0)):                          # if not first point of array
               cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
               cz = np.sqrt(np.square(cu) + np.square(cv))

               if (case == 1):
                  c1 = (downsensoraltsim - downsensoraltused)*2.*np.pi*cz
                  c2 = (upsensoraltsim - downsensoraltsim)*2.*np.pi*cz
                  c = np.exp(-c1) - np.exp(-c2)
               elif (case == 2):
                  c1 = (downsensoraltsim - downsensoraltused)*2.*np.pi*cz
                  c2 = (upsensoraltsim - downsensoraltsim)*2.*np.pi*cz
                  cred = complex(cz*cosz, cu*cosu + cv*cosv)
                  c = ((np.exp(-c1) - np.exp(-c2))*cz)/cred
               else :                  # case = 3
                  cred = complex(cz*cosz, cu*cosu + cv*cosv)
                  c = cz/cred
                  
               if (sense == 0):
                  coef = c
               else:
                  coef = 1./c

               cvalfft[iy][ix] = cvalfft[iy][ix] * coef
               
      # FFT inversion
      icvalfft = np.fft.ifft2(cvalfft)
      val = icvalfft.real

      val[nan_indexes] = np.nan                                   # set the initial 'nan' values, as in the initial array
   
      dataset.data.z_image = val                                  # to get the 'z_image' array in (x,y) format.
                  


def _definecaseandsense( prosptechused, prosptechsim):
   '''
   define case and sense of conversion
   case 1 = "Magnetic field" <-> "Magnetic field gradient"
   case 2 = "Magnetic field" <-> "Vertical component gradient"
   case 3 = "Magnetic field gradient" <-> "Vertical component gradient"
   '''

   case = None
   sense = None
   if ((prosptechused == prosptechlist[0]) and (prosptechsim == prosptechlist[1])) :
      case = 1
      sense = 0
   elif ((prosptechused == prosptechlist[0]) and (prosptechsim == prosptechlist[2])) :
      case = 2
      sense = 0
   elif ((prosptechused == prosptechlist[1]) and (prosptechsim == prosptechlist[0])) :
      case = 1
      sense = 1
   elif ((prosptechused == prosptechlist[1]) and (prosptechsim == prosptechlist[2])) :
      case = 3
      sense = 0
   elif ((prosptechused == prosptechlist[2]) and (prosptechsim == prosptechlist[0])) :
      case = 2
      sense = 1
   elif ((prosptechused == prosptechlist[2]) and (prosptechsim == prosptechlist[1])) :
      case = 3
      sense = 1

   return case, sense


def susceptibility(dataset, prosptech, apod=0, downsensoraltitude = 0.3, upsensoraltitude = 1.0, calculationdepth=.0, stratumthickness=1.0, inclineangle = 65, alphaangle = 0):
   '''
   cf. dataset
   '''
   val = dataset.data.z_image
   
   # Calculation of lines and columns numbers
   ny = len(val)
   nx = len(val[0])
   # Calculation of total values number
   nt = nx * ny

   nan_indexes = np.isnan(val)                                 # searches the 'nan' indexes in the initial array
   if(np.isnan(val).any()):                                    # if at least 1 'nan' is detected in the array,
      
      x = np.linspace(dataset.info.x_min, dataset.info.x_max, nx, endpoint=True)
      y = np.linspace(dataset.info.y_min, dataset.info.y_max, ny, endpoint=True)
      _fillnanvalues(x, y, val.T)                                # fills the 'nan' values by interpolated values

   if (apod > 0):
      apodisation2d(val, apod)

   # complex conversion, val[][] -> cval[][]
   coef = 1./(400.*np.pi)
   cval = np.array(val*coef, dtype=complex)

   # fast fourier series calculation
   cvalfft = np.fft.fft2(cval)

   # filter application
   # deg->rad angle conversions
   rinc = (inclineangle*np.pi)/180 # inclination in radians
   ralpha = (alphaangle*np.pi)/180  # alpha angle in radians

   cosu = np.absolute(np.cos(rinc) * np.cos(ralpha))
   cosv = np.absolute(np.cos(rinc) * np.sin(ralpha))
   cosz = np.sin(rinc)

   dz = downsensoraltitude - upsensoraltitude
   zp = calculationdepth + downsensoraltitude
   
   deltax = dataset.info.x_gridding_delta
   deltay = dataset.info.y_gridding_delta

   if (inclineangle == 0):
      teta = np.pi/2
   elif (inclineangle == 90) :    # pi/2
      teta = np.pi
   else :
      teta = np.pi + np.arctan(-2/np.tan(rinc))

   # Field Module, medium field along I inclination calcultation if bipolar field
   FM = 14.722 * (4*(np.square(np.cos(teta)) + np.square(np.sin(teta))))

   cvalfft[0][0] = 0.
   for ix in range(nx):                                        # for each column
      for iy in range(ny):                                     # for each line
         if ((ix != 0) or (iy != 0)):                          # if not first point of array
            cu, cv = _freq(ix, iy, deltax, deltay, nx, ny)     # complex u and v calculation
            # continuation
            cz = np.sqrt(np.square(cu) + np.square(cv))
            cvalfft[iy][ix] = cvalfft[iy][ix] * complex(np.exp(2*np.pi*cz*zp), 0.)
            # pole reduction with potential calculation(and not with field as standard pole reduction)
            cred = complex(cz*cosz, cu*cosu + cv*cosv)
            cvalfft[iy][ix] = (cvalfft[iy][ix] * complex(cz,0))/(2*np.pi*np.square(cred))

            if (prosptech == prosptechlist[1]):                         # if prospection technic is magnetic field gradient
               cvalfft[iy][ix] = cvalfft[iy][ix] / (1-np.exp(dz*cz))         

   # FFT inversion
   icvalfft = np.fft.ifft2(cvalfft)

   # Equivalent stratum thickness
   val = (icvalfft.real*2*100000)/(FM*stratumthickness)         # 100000 because susceptibiliy in 10^-5 SI

   val[nan_indexes] = np.nan                                   # set the initial 'nan' values, as in the initial array

   dataset.data.z_image = val                                  # to get the 'z_image' array in (x,y) format.



prosptechlist = ["Magnetic field", "Magnetic field gradient", "Vertical component gradient"]

def getprosptechlist():
   '''
   Get list of prospection technicals availables

   Returns : list of prospection technicals
   
   '''

   return prosptechlist
   


def _freq(ix, iy, deltax, deltay, nc, nl):
   '''
   Calculation of spatials frequencies u and v
   '''
   nyd = 1 + nl/2
   nxd = 1 + nc/2

   if (iy < nyd):
      cv = (float(iy))/((nl-1)*deltay)
   else:
      cv = float(iy-nl)/((nl-1)*deltay)

   if (ix < nxd):
      cu = (float(ix))/((nc-1)*deltax)
   else:
      cu = float(ix-nc)/((nc-1)*deltax)

   return cu, cv


def _fillnanvalues(xi, yi, val):
   '''
   Fills the 'nan' values by interpolated values using simple spline interpolation method !
   '''
   for profile in val:                                         # for each profile,
      if (np.isnan(profile).any()):                            # if one 'nan' at least in the profile, does the completion
         nan_indexes = np.isnan(profile)
         data_indexes = np.logical_not(nan_indexes)
         valid_data = profile[data_indexes]
         interpolated = np.interp(nan_indexes.nonzero()[0], data_indexes.nonzero()[0], valid_data)   
         profile[nan_indexes] = interpolated

