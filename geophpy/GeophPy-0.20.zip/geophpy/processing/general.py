# -*- coding: utf-8 -*-
'''
    geophpy.processing.general
    --------------------------

    DataSet Object general processing routines.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
### USER DEFINED PARAMETERS ##########################################

# list of correlation methods available for wumappy interface
festoon_correlation_list = ['Pearson', 'Spearman', 'Kendall']

# list of destriping methods available for wumappy interface
destriping_list = ['add', 'mult']

# list of regional trend methods available for wumappy interface
regtrendmethod_list = ['rel', 'abs']

# list of regional trend components available for wumappy interface
regtrendcomp_list = ['loc', 'reg']

######################################################################



import numpy as np
import scipy.ndimage as ndimage
from scipy.stats import spearmanr, kendalltau
from geophpy.misc.utils import *
from geophpy.operation.general import *



def peakfilt(dataset, setmin=None, setmax=None, setmed=False, setnan=False, valfilt=False):
   '''
   cf. dataset.py

   '''
###ORIGINAL CODE having some flaws:
###- min and max are builtin functions (reserved words)
###- should be able to work on values as well as on zimage
###- should be able to replace by nan or median instead of threshold
###- is iterative (for ...) ; should be global (where ...)
   #for i in range(dataset.info.lines_nb) :
   #   if ((min != None) and (dataset.data.values[i][2] < min)):
   #      dataset.data.values[i][2] = min
   #   elif ((max != None) and (dataset.data.values[i][2] > max)):
   #      dataset.data.values[i][2] = max
###
   if (valfilt):
      val = dataset.data.values[:,2]
   else:
      val = dataset.data.z_image

   if (setmin != None):
      idx = np.where(val < setmin)
      if (setnan):
         val[idx] = np.nan
      elif (setmed):
         val[idx] = np.nan # compute median here ...TBD...
      else:
         val[idx] = setmin

   if (setmax != None):
      idx = np.where(val > setmax)
      if (setnan):
         val[idx] = np.nan
      elif (setmed):
         val[idx] = np.nan # compute median here ...TBD...
      else:
         val[idx] = setmax



def medianfilt(dataset, nx=3, ny=3, percent=0, gap=0, valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # ...TBD... should use original wumap algorithm
      pass
   else:
      zimg = dataset.data.z_image
      if (percent == 0) & (gap == 0):
         zimg[:,:] = ndimage.median_filter(zimg, size=(nx, ny))
      else:
         # ...TBD... should use here also original wumap algorithm
         pass



def getfestooncorrelationlist():
   """
   cf. dataset.py

   """
   return festoon_correlation_list



def festoonfilt(dataset, method='Pearson', shift=0, valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = correlcols(zimg.shape[1])

      # Compute the profiles correlation map ######################
      if (shift == 0):
         cor1, pva1 = correlmap(dataset, method)
         shift      = correlshift(cor1, pva1)

      # Apply the same shift to each profile #########################
      for i in cols:
         zimg[:,i] = np.roll(zimg[:,i],shift)

   return shift



def correlcols(nx):
   return range(1,nx-1,2) # ...TBD... à revoir ?



def correlmap(dataset, method):
         """
         cf. dataset.py

         """
         zimg = dataset.data.z_image
         cols = correlcols(zimg.shape[1])
         ny   = zimg.shape[0]
         jmax = 2*ny-1
         cor1 = np.zeros(shape=(jmax,len(cols))) / 0.
         pva1 = cor1.copy()
         ii   = 0

         if (method == 'Pearson'):
            # Use Pearson correlation ################################
            for i in cols:
               z1   = (zimg[:,i-1] + zimg[:,i+1]) / 2. # ...TBD... nanmean ?
               z1   = (z1 - np.nanmean(z1)) / np.nanstd(z1)
               zi   = zimg[:,i] * 1.
               zi   = (zi - np.nanmean(zi)) / np.nanstd(zi)
               idx  = np.isfinite(z1) & np.isfinite(zi)
               jlen = 2*len(idx.nonzero()[0])-1
               if (jlen > 0):
                  jmin  = (jmax - jlen) // 2
                  cor1[jmin:jmin+jlen,ii] = np.correlate(z1[idx],zi[idx],mode='full') / idx.sum()
                  pva1[jmin:jmin+jlen,ii] = 1
               ii += 1
         else:
            # Use Spearman or Kendall correlation ####################
            for i in cols:
               z1 = (zimg[:,i-1] + zimg[:,i+1]) / 2. # ...TBD... nanmean ?
               for j in range(-ny+1,ny):
                  zi = np.roll(zimg[:,i],j)
                  if (j < 0):
                     zi[ny+j:ny] = np.nan
                  else:
                     zi[0:j] = np.nan
                  idx = np.isfinite(z1) & np.isfinite(zi)
                  if (method == 'Spearman'):
                     # Use Spearman correlation ######################
                     cors, pval = spearmanr(z1[idx],zi[idx])
                  elif (method == 'Kendall'):
                     # Use Kendall correlation #######################
                     # ...TBD... something goes wrong here ? what ? why ?
                     #cors, pval = kendalltau(z1[idx],zi[idx])
                     pass
                  else:
                     # Undefined correlation method ##################
                     # ...TBD... raise an error here !
                     pass
               if (len(z1[idx]) > 1):
                  cor1[j+ny-1,ii] = cors
                  pva1[j+ny-1,ii] = pval
               ii+=1

         return cor1, pva1



def correlshift(cor1, pva1, apod=None, output=None):
         """
         cf. dataset.py

         """
         ny = (cor1.shape[0] + 1) // 2

         # Define correlation curve apodisation threshold ############
         if (apod == None):
            apod = 0.1 # percent of the max correl coef

         # Make a mask for nans and apodisation ######################
         corl  = np.isfinite(cor1).sum(axis=1).astype(float)
         idx   = np.where(corl < max(corl) * apod)
         corl[idx] = np.nan

         pval  = np.isfinite(pva1).sum(axis=1).astype(float)
         idx   = np.where(pval < max(pval) * apod)
         pval[idx] = np.nan

         # Fold the correlation map ##################################
         cor2  = np.nansum(cor1,axis=1) / corl
         pva2  = np.nansum(pva1,axis=1) / pval
         corm  = cor2 / pva2

         # Deduce the best 'shift' value from the max correl coef ####
         idx   = (corm == np.nanmax(corm)).nonzero()
         # ...TBD... en fait ici fitter une gaussienne et trouver son max
         shift = idx[0][0]-ny+1

         if (output != None):
            output[:] = corm[:]

         return shift



def getdestripinglist():
   """
   cf. dataset.py

   """
   return destriping_list



def destripecon(dataset, Nprof=0, setmin=None, setmax=None, method="add", valfilt=False):
   '''
   cf. dataset.py

   '''
   dstmp = dataset.copy()
   dstmp.peakfilt(setmin=setmin, setmax=setmax, setnan=True, valfilt=valfilt)

   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = range(zimg.shape[1])

      # Compute the mean for each profile ############################
      Z    = dstmp.data.z_image
      ZMOY = np.nanmean(Z,axis=0,keepdims=True)

      # Compute the mean of reference ################################
      if (Nprof == 0):
         MOYR = np.nanmean(Z)
      else:
         MOYR = np.zeros(ZMOY.shape)
         kp2  = Nprof // 2
         for jc in cols:
            jc1 = max(0,jc-kp2)
            jc2 = min(zimg.shape[1]-1,jc+kp2)
            MOYR[0,jc] = np.nanmean(Z[:,jc1:jc2])

      # Rescale the profiles #########################################
      if (method == "add"):
         zimg += MOYR
         zimg -= ZMOY
      elif (method == "mult"):
         zimg *= MOYR
         zimg /= ZMOY
      else:
         # Undefined destriping method ###############################
         # ...TBD... raise an error here !
         pass



def destripecub(dataset, Nprof=0, setmin=None, setmax=None, Ndeg=3, valfilt=False):
   '''
   cf. dataset.py

   '''
   dstmp = dataset.copy()
   dstmp.peakfilt(setmin=setmin, setmax=setmax, setnan=True, valfilt=valfilt)

   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = range(zimg.shape[1])
      y = zimage_ycoord(dataset)

      # Compute the polynomial coefs for each profile ################
      Z    = dstmp.data.z_image
      ZPOL = np.polyfit(y[:,0],Z,Ndeg)

      # Compute the polynomial reference #############################
      if (Nprof == 0):
         POLR = np.nanmean(ZPOL, axis=1, keepdims=True)
      else:
         POLR = np.zeros(ZPOL.shape)
         kp2  = Nprof // 2
         for jc in cols:
            jc1 = max(0,jc-kp2)
            jc2 = min(zimg.shape[1]-1,jc+kp2)
            POLR[:,jc] = np.nanmean(ZPOL[:,jc1:jc2], axis=1, keepdims=True)[:,0]

      # Rescale the profiles #########################################
      for d in range(Ndeg):
         zimg -= np.array([ZPOL[d+1]])*y**(d+1)
      if (Nprof != 1):
         zimg -= ZPOL[0]
         for d in range(Ndeg+1):
            zimg += np.array([POLR[d]])*y**d



def getregtrendmethodlist():
   """
   cf. dataset.py

   """
   return regtrendmethod_list



def getregtrendcomplist():
   """
   cf. dataset.py

   """
   return regtrendcomp_list



def regtrend(dataset, nx=3, ny=3, method="rel", component="loc", valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = range(zimg.shape[1])
      ligs = range(zimg.shape[0])
      nx2  = nx//2
      ny2  = ny//2
      znew = zimg * 0.

      # Compute the mean of all data #################################
      zmoy = np.nanmean(zimg)

      # Compute the mean in each window ##############################
      for jl in ligs:
         jl1 = max(0, jl - nx2)            # ...TBD... -1 ?
         jl2 = min(max(ligs), jl + nx2)    # ...TBD... -1 ?
         for jc in cols:
            jc1 = max(0, jc - ny2)         # ...TBD... -1 ?
            jc2 = min(max(cols), jc + ny2) # ...TBD... -1 ?
            zloc = np.nanmean(zimg[jl1:jl2,jc1:jc2])
            if (component == "loc"):
               if (method == "rel"):
                  znew[jl,jc] = zimg[jl,jc] * zmoy / zloc
               elif (method == "abs"):
                  znew[jl,jc] = zimg[jl,jc] - zloc
               else:
                  # Undefined method #################################
                  # ...TBD... raise an error here !
                  pass
            elif (component == "reg"):
               znew[jl,jc] = zloc
            else:
               # Undefined component #################################
               # ...TBD... raise an error here !
               pass

      # Write result to input dataset ################################
      zimg[:,:] = znew



def wallisfilt(dataset, nx=3, ny=3, setmean=None, setstdev=None, setgain=None, limit=None, edgefactor=None, valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = range(zimg.shape[1])
      # ...TBD...



def ploughfilt(dataset, nx=3, ny=3, apod=0, angle=None, cutoff=None, valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image

      if (apod > 0):
         apodisation2d(zimg, apod)

      cols = range(zimg.shape[1])
      # ...TBD...
