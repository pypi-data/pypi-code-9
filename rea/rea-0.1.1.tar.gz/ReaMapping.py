# Copyright (C) 2014
# Institut d'Astrophysique Spatiale
#
# Forked from the BoA project
#
# Copyright (C) 2002-2007
# Max-Planck-Institut fuer Radioastronomie Bonn
# Argelander Institut fuer Astronomie
# Astronomisches Institut der Ruhr-Universitaet Bochum
#
# Produced for the LABOCA project
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Library General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Library General Public License for more
# details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#

"""
.. module:: ReaMapping
    :synopsis: contains the ReaMapping and Image classes
"""
__version__ =  '$Revision: 2724 $'
__date__ =     '$Date: 2010-06-01 18:06:15 +0200 (mar. 01 juin 2010) $'

#----------------------------------------------------------------------------------
#----- Import ---------------------------------------------------------------------
#----------------------------------------------------------------------------------

import numpy as np
import copy

import cPickle, string

from rea           import ReaDataAnalyser, ReaMessageHandler, ReaFits, ReaFlagHandler
from rea           import ReaConfig, ReaError, Utilities
from rea.Bogli     import Plot, MultiPlot
from rea.fortran   import fUtilities, fMap, fStat
from rea.Utilities import Timing, compressNan, tolist_rea, inPolygon, outPolygon
from rea.Utilities import modelBaseEllipticalGaussian, fitBaseEllipticalGaussian

from rea.Utilities import ProgressBar

import os.path

#----------------------------------------------------------------------------------
#----- Image Class ----------------------------------------------------------------
#----------------------------------------------------------------------------------

class Image:
    """..class: Image
    :synopsis: An object of this class describes an image and its axis
    """

    # TODO add method getPixel putPixel and/or getRegion setRegion
    def __init__(self):

        self.__MessHand = ReaMessageHandler.MessHand(self.__module__)

        self.Header = {
            'Object':   'Unknown',\
            'Telescope':  'None',\
            'FeBe':       'None',\
            'Tau':        0.0, \
            'Elevation':  0.0, \
            'JyPerCount': 1.0 \
            }

        self.Data     = []   # The bitmap map (2D arrays)
        self.Weight   = []   # The weights per pixel
        self.Coverage = []   # The coverage per pixel, i.e. weight=1

        self.RmsBeam  = 0.   # rms/beam in current unit
        self.BeamSize = 0.   # beam size, in same unit as WCS

        self.WCS = {
            # Number of Axis (2 for simple images)
            'NAXIS': 2,\
            \
            # time of observation
            'MJD-OBS': 'None',\
            # frame of reference
            'RADESYS': 'FK5',\
            # coordinate epoch
            'EQUINOX': 2000.0,\
            \
            # of pixel
            'NAXIS1': 0,\
            # Type
            'CTYPE1': 'X',\
            # pixel scale
            'CDELT1': 1.0,\
            # unit
            'CUNIT1': 'dummy',\
            # Pixel coordinate of reference point
            'CRPIX1': 0.0,\
            # celestial coordinate of reference point
            'CRVAL1': 0.0,\
            \
            'NAXIS2': 0,\
            'CTYPE2': 'Y',\
            'CDELT2': 1.0,\
            'CUNIT2': 'dummy',\
            'CRPIX2': 0.0,\
            'CRVAL2': 0.0,\
            \
            # linear transformation matrix
            'PC1_1': 1,\
            'PC1_2': 0,\
            'PC2_1': 0,\
            'PC2_2': 1}

    def __str__(self):
        """Defines a string, shown when the print instruction is used."""

        out = "Image of %s with %s on %s (%ix%i pixels)" %\
              (self.Header['Object'],\
               self.Header['FeBe'],\
               self.Header['Telescope'],\
               self.WCS['NAXIS1'], self.WCS['NAXIS2'])

        return out

    def wcs2pix(self, X, Y):
        """Convert from physical coordinates described by self.WCS
        to pixel coordinates

        Parameters
        ----------
        X,Y  : float
            the physical coordinates to convert from

        Returns
        -------
        i, j : float
            the pixel coordinates

        Notes
        -----
        We should switch to libwcs at some point
        """

        if self.WCS['CUNIT1'] == 'arcsec':
            cdeltUnit = 1./3600.
        else:
            cdeltUnit = 1.
        AXIS1 = np.array([self.WCS['NAXIS1'], self.WCS['CRPIX1'], self.WCS['CDELT1'],
                       self.WCS['CRVAL1'], cdeltUnit])
        AXIS2 = np.array([self.WCS['NAXIS2'], self.WCS['CRPIX2'], self.WCS['CDELT2'],
                       self.WCS['CRVAL2'], cdeltUnit])
        i, j = fMap.wcs2pix(X, Y, AXIS1, AXIS2)
        if not X.ndim and not Y.ndim:
            i = i[0]
            j = j[0]
        return i, j

    def wcs2phy(self, i, j):
        """Convert from pixel coordinates to physical (world) coordinates

        Parameters
        ----------
        i, j : float
            the pixel coordinates to convert from

        Returns
        -------
        X, Y : float
            the physical coordinates

        Notes
        -----
        We should switch to libwcs at some point
        """
        if self.WCS['CUNIT1'] == 'arcsec':
            cdeltUnit = 1./3600.
        else:
            cdeltUnit = 1.
        AXIS1 = np.array([self.WCS['NAXIS1'], self.WCS['CRPIX1'], self.WCS['CDELT1'],
                       self.WCS['CRVAL1'], cdeltUnit])
        AXIS2 = np.array([self.WCS['NAXIS2'], self.WCS['CRPIX2'], self.WCS['CDELT2'],
                       self.WCS['CRVAL2'], cdeltUnit])
        X, Y = fMap.wcs2phy(i, j, AXIS1, AXIS2)
        if not i.ndim and not j.ndim:
            X = X[0]
            Y = Y[0]
        return X, Y


    def computeWCS(self, pixelSize, sizeX=[], sizeY=[], minmax=[]):
        """fill main WCS keywords according to pixel size and map limits

        Parameters
        ----------
        pixelSize : int
            size of pixel in acrsecond
        sizeX : float
            map limits in azimuth, in arcsecond
        sizeY : float
            map limits in elevation, in arcsecond
        minmax : float array
            [minAzoff,maxAzoff,minEloff,maxEloff] in this order
        """

        # TODO add shift for 'CRPIX1/2' or 'CRVAL1/2' to be general and allow for
        # offset in  maps

        # determine coordinate limits and map size
        if sizeX == []:
            minAzoff = minmax[0]
            maxAzoff = minmax[1]
        else:
            minAzoff = sizeX[0]
            maxAzoff = sizeX[1]

        if sizeY == []:
            minEloff = minmax[2]
            maxEloff = minmax[3]
        else:
            minEloff = sizeY[0]
            maxEloff = sizeY[1]

        Xcenter = (minAzoff + maxAzoff)/2.
        Ycenter = (minEloff + maxEloff)/2.
        if self.WCS['CUNIT1'] == 'arcsec':
            cosY = np.cos(np.radians(Ycenter/3600.))
        else:
            cosY = np.cos(np.radians(Ycenter))

        dimX = int(np.ceil(abs(maxAzoff - minAzoff)/pixelSize*cosY + 1.))
        dimY = int(np.ceil(abs(maxEloff - minEloff)/pixelSize + 1.))

        # Size of the image
        self.WCS['NAXIS1'] = dimX
        self.WCS['NAXIS2'] = dimY

        # Size of pixels
        self.WCS['CDELT1'] = (maxAzoff - minAzoff)/abs(maxAzoff - minAzoff)*pixelSize
        self.WCS['CDELT2'] = (maxEloff - minEloff)/abs(maxEloff - minEloff)*pixelSize

        # put the reference in the center of the image ...
        self.WCS['CRPIX1'] = (dimX-1)/2.
        self.WCS['CRPIX2'] = (dimY-1)/2.

        # ... corresponding to the center of the map
        self.WCS['CRVAL1'] = Xcenter
        self.WCS['CRVAL2'] = Ycenter

    def physicalCoordinates(self):
        """return arrays with physical units corresponding to the map"""

        # TODO : Recheck that, wcs convention is 1 at the center of the pixel

        # We want to have the coordinates of the center of the pixel,
        # remember wcs2phy is O-indexed, so pixel coordinates goes
        # from 0 to 1, hence 0.5 is the middle of the pixel

        allAz = self.wcs2phy(np.arange(self.WCS['NAXIS1'])+0.5, np.repeat([0.5], self.WCS['NAXIS1']))[0]
        allEl = self.wcs2phy(np.repeat([0.5], self.WCS['NAXIS2']), np.arange(self.WCS['NAXIS2'])+0.5)[1]
        repeatAz = np.repeat(allAz, self.WCS['NAXIS2'])
        resultAz = np.reshape(repeatAz, (self.WCS['NAXIS1'], self.WCS['NAXIS2']))
        repeatEl = np.repeat(allEl, self.WCS['NAXIS1'])
        resultEl = np.transpose(np.reshape(repeatEl, (self.WCS['NAXIS2'], self.WCS['NAXIS1'])))

        return (resultAz, resultEl)


    def display(self, weight=False, coverage=False, \
                style='idl4', caption='', \
                wedge=False, aspect=True, overplot=False,
                doContour=False, levels=[], labelContour=0,\
                limitsX = [], limitsY = [], limitsZ = [], \
                showRms=False, rmsKappa=3.5, \
                noerase=False, snmap=False, cell=15, sparse=8):
        """show the reconstructed maps in (Az,El)

        Parameters
        ----------
        weigth, coverage : bool
            plot the rms or weight map instead of signal map
        style : 'str'
            the style used for the color (default idl4)
        caption : str
            the caption of the plot (default '')
        limitsX, limitsY, limitsZ : float array
            the limits in X/Y/intensity
        wedge : bool
            draw a wedge ? (default : yes)
        aspect : bool
            keep the aspect ratio (default : yes)
        overplot : bool
            should we overplot this image (default : no)
        doContour : bool
            draw contour instead of map (default : no)
        levels : float array
            the levels of the contours (default : intensity progression)
        labelContour : bool
            label the contour (default : no)
        showRms : bool
            compute and display rms/beam? (def: no)
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        noerase : bool
            do not clear the window? (def: false)
        snmap : bool
            display a signal-to-noise map in arb. units (def: no)
        cell, sparse : int
            see ReaMapping.Image.computeSNMap
        """

        if snmap:
            toPlot = self.computeSNMap(cell=cell, sparse=sparse)
        else:
            toPlot = self.Data

        WCS = self.WCS

        if weight:
            toPlot = self.Weight
        if coverage:
            toPlot = self.Coverage

        labelX = ''
        if WCS['CTYPE1'][0:4] == 'OLON':
            labelX = "\gD Az"
        elif WCS['CTYPE1'][0:4] == 'RA--':
            labelX = "\ga"
            if WCS['EQUINOX'] == 2000.0:
                labelX += ' (J2000)'
            if WCS['EQUINOX'] == 1950.0:
                labelX += ' (B1950)'
        elif WCS['CTYPE1'][0:4] == 'GLON':
            labelX = "Gal. long."
        else:
            labelX = WCS['CTYPE1']
        if WCS['CUNIT1']:
            labelX += " ["+WCS['CUNIT1']+"]"

        labelY = ''
        if WCS['CTYPE2'][0:4] == 'OLAT':
            labelY = "\gD El"
        elif WCS['CTYPE2'][0:4] == 'DEC-':
            labelY = "\gd"
            if WCS['EQUINOX'] == 2000.0:
                labelY += ' (J2000)'
            if WCS['EQUINOX'] == 1950.0:
                labelY += ' (B1950)'
        elif WCS['CTYPE2'][0:4] == 'GLAT':
            labelY = "Gal. lat."
        else:
            labelY = WCS['CTYPE2']
        if WCS['CUNIT2']:
            labelY += " ["+WCS['CUNIT2']+"]"

        Plot.draw(toPlot, wedge=wedge, WCS=WCS,\
                  labelX=labelX, labelY=labelY, caption=caption, \
                  limitsX = limitsX, limitsY = limitsY, limitsZ = limitsZ,\
                  nan=1, style=style, aspect=aspect, overplot=overplot,\
                  doContour=doContour, levels = levels, labelContour=labelContour,
                  noerase=noerase)

        if showRms:
            # compute rms/beam
            Xrange, Yrange = [], []
            if limitsX:
                x1, y1 = self.wcs2pix(limitsX[0], WCS['CRVAL2'])
                x2, y2 = self.wcs2pix(limitsX[1], WCS['CRVAL2'])
                Xrange = [int(x1)+1, int(x2)]
            if limitsY:
                x1, y1 = self.wcs2pix(WCS['CRVAL1'], limitsY[0])
                x2, y2 = self.wcs2pix(WCS['CRVAL1'], limitsY[1])
                Yrange = [int(y1), int(y2)+1]

            self.computeRms(rmsKappa=rmsKappa,
                            limitsX=Xrange, limitsY=Yrange)

    def smoothBy(self, fwhm, norm='peak'):
        """Smooth the image with a 2D Gaussian of given FWHM.
             Smoothing is peak-normalised, therefore conserves Jy/beam
             as unit.

        Parameters
        ----------
        fwhm : float
            the FWHM of the smoothing gaussian
        norm : {'peak', 'int'}
            normalize to peak ('peak') or integrated ('int') flux.
        """

        # Compute a kernel of the same pixelSize as the image
        pixsize = abs(self.WCS['CDELT2'])
        smoothingKernel = Kernel(pixsize, fwhm)
        self.smoothWith(smoothingKernel)
        # Normalisation of the data plane: pixel unit is flux/beam
        # so, update to the new beam size
        if (norm == 'peak'):
            newbeam = np.sqrt(self.BeamSize*self.BeamSize + fwhm**2)
        else:
            newbeam = self.BeamSize

        self.Data   *= np.array((newbeam**2) / (self.BeamSize**2), np.float)
        self.Weight *= np.array((newbeam**2) / (self.BeamSize**2), np.float)
        self.BeamSize = newbeam

    def smoothWith(self, kernel):
        """smooth the image with the given kernel

        Parameters
        ----------
        kernel : ReaMapping.Image
            the kernel
        """

        if abs(self.WCS['CDELT1']) == abs(kernel.WCS['CDELT1']) and \
               abs(self.WCS['CDELT2']) == abs(kernel.WCS['CDELT2']):
            self.Data     = fMap.ksmooth(self.Data,     kernel.Data)
            self.Weight   = fMap.ksmooth(self.Weight,   kernel.Data)
            self.Coverage = fMap.ksmooth(self.Coverage, kernel.Data)


    def blankRegion(self, ccord, radius, outside=False):
        """selects a circular region on the map and blanks
             the region, or everything outside the region

        Parameters
        ----------
        ccord : float array
            x,y world coordinates of center
        radius : float
            radius of the region to blank
        outside : bool
            blank outside region
        """

        dat = np.array(self.Data)

        # convert radius to number of pixels in x and y directions
        npixx = abs(radius/self.WCS['CDELT1'])
        npixy = abs(radius/self.WCS['CDELT2'])

        # convert central coordinates to pixel coordinates
        (cpixx, cpixy) = self.wcs2pix(ccord[0], ccord[1])

        xcoord = copy.deepcopy(dat)
        ycoord = copy.deepcopy(dat)

        for i in range(self.WCS['NAXIS1']):
            for j in range(self.WCS['NAXIS2']):
                xcoord[i, j] = i+1
                ycoord[i, j] = j+1

        pixdist = np.sqrt(((xcoord-cpixx)**2)/(npixx**2) +\
                     ((ycoord-cpixy)**2)/(npixy**2))
        mask = where(pixdist < 1., 1, 0)

        print cpixx, cpixy, npixx, npixy

        if outside:
            mask = where(mask == 0, 1, 0)

        self.blankOnMask(mask)
        return shape(np.compress(np.ravel(mask), np.ravel(mask)))[0]


    def blankOnMask(self, mask):
        """cut the map according to an input mask

        Parameters
        ----------
        mask : 2D float array
            input mask

        Returns
        -------
        int
            number of flagged pixels
        """

        dat = copy.deepcopy(np.array(self.Data))
        weight = copy.deepcopy(np.array(self.Weight))
        cover = copy.deepcopy(np.array(self.Coverage))

        putmask(dat, mask, np.nan)
        putmask(weight, mask, 0.)
        putmask(cover, mask, 0)

        self.Data = dat#.tolist()
        self.Weight = weight#.tolist()
        self.Coverage = cover#.tolist()

        nset = shape(np.compress(np.ravel(mask), np.ravel(mask)))[0]
        return nset

    def blank(self, below=np.nan, above=np.nan):
        """cut the map below and/or above a threshold

        Parameters
        ----------
        below : float
            cut below this value
        above : float
            cut above this value

        Returns
        -------
        int
            number of flagged pixels
        """

        mapdata = copy.deepcopy(np.array(self.Data))

        mask = where(bitwise_or((mapdata < below), (mapdata > above)), 1, 0)

        nset = self.blankOnMask(mask)
        return nset

    def blankSigma(self, below=np.nan, above=np.nan, snmap=1, cell=15, sparse=8):
        """cut the map below and/or above a number of sigmas of the s/n map (default) or the map

        Parameters
        ----------
        below : float
            cut below this value
        above : float
            cut above this value
        snmap : bool
            True to use ReaMapping.Image.computeSNMap, False for global rms
        cell, spare : int
            see ReaMapping.Image.computeSNMap

        Returns
        -------
        int
            number of flagged pixels
        """

        if snmap:
            mapdata = self.computeSNMap(cell=cell, sparse=sparse)
        else:
            mapdata = copy.deepcopy(np.array(self.Data))

        good_data = compressNan(mapdata)[0]

        if snmap:
            mask = where(bitwise_or((mapdata < below), (mapdata > above)), 1, 0)
        else:
            mean = fStat.f_mean(good_data)
            rms = fStat.f_rms(good_data, mean)
            mask = where(bitwise_or((mapdata < below*rms), (mapdata > above*rms)), 1, 0)

        nset = self.blankOnMask(mask)
        return nset

    def sigmaClip(self, above=5, below=-5):
        """despike (sigma clip) a map

        Parameters
        ----------
        below : float
            cut below the rms times this value
        above : float
            cut above the rms times this value

        Returns
        -------
        int
            number of flagged pixels
        """

        good_data = compressNan(self.Data)[0]
        mean = fStat.f_mean(good_data)
        rms = fStat.f_rms(good_data, mean)

        nset = self.blank(below=below*rms, above=above*rms)
        self._Image__MessHand.info('flagging %s pixels in map' % nset)

        return nset

    def iterativeSigmaClip(self, above=5, below=-5, maxIter=10):
        """despike (sigma clip) a map iteratively

        Parameters
        ----------
        below : float
            cut below the rms times this value
        above : float
            cut above the rms times this value
        maxIter : int
            maximum number of iterations

        Returns
        -------
        int
            number of flagged pixels
        """

        despiked = 1
        i = 0

        # Run loop
        while ((despiked > 0) and (i < maxIter)):
            i += 1
            despiked = self.sigmaClip(above=above, below=below)
    #----------------------------------------------------------------------------
    def setValuesOnMask(self, mask, value):
        """reassign values to the map according to an input mask

        Parameters
        ----------
        mask : 2D int array
            input mask
        value : float
            the value to be used for reassignment

        Returns
        -------
        int
            number of reassigned pixels
        """

        dat = copy.deepcopy(np.array(self.Data))
        weight = copy.deepcopy(np.array(self.Weight))
        cover = copy.deepcopy(np.array(self.Coverage))

        putmask(dat, mask, value)
        putmask(weight, mask, 0.)
        putmask(cover, mask, 0)

        self.Data = dat#.tolist()
        self.Weight = weight#.tolist()
        self.Coverage = cover#.tolist()

        nset = shape(np.compress(np.ravel(mask), np.ravel(mask)))[0]
        return nset

    #----------------------------------------------------------------------------
    def setValues(self, below=np.nan, above=np.nan, value=np.nan):
        """cut the map below and/or above a threshold

        Parameters
        ----------
        below : float
            cut below this value
        above : float
            cut above this value
        value : float
            value to set

        Returns
        -------
        int
            number of set pixels
        """

        mapdata = copy.deepcopy(np.array(self.Data))

        mask = where(bitwise_or((mapdata < below), (mapdata > above)), 1, 0)

        nset = self.setValuesOnMask(mask, value)

        return nset
    #----------------------------------------------------------------------------

    def getPixel(self, nbPix=3):
        """allow user to get pixel values using mouse

        Parameters
        ----------
        nbPix : int
            size of area to compute average (default 3x3)
        """

        self.__MessHand.info("Click left to get one pixel, mid to get average over " +\
                           str(nbPix*nbPix)+", right to exit (on Data array only)")

        data = self.Data
        WCS  = self.WCS

        x, y = 0, 0
        char = ''
        while(char != 'X'):
            if (char == 'D'):
                # average over [x1,x2] x [y1,y2]
                offset = (nbPix-1)/2.
                if offset <= i < WCS['NAXIS1']-offset and \
                       offset <= j < WCS['NAXIS2']-offset:
                    x1 = int(i-offset)
                    x2 = int(i+offset+1)
                    y1 = int(j-offset)
                    y2 = int(j+offset+1)

                    listVal = self.Data[x1:x2, y1:y2]
                    listVal = np.ravel(listVal)

                    listVal, nNan = compressNan([listVal])
                    if len(listVal) > 0:
                        val = sum(listVal)/float(len(listVal))
                        self.__MessHand.info("[%ix%i]-%i: (%6.2f,%6.2f) = %6.2f" \
                                             % (nbPix, nbPix, len(listVal), x, y, val))
                else:
                    self.__MessHand.warning("some pixel(s) are outside the plot")
            elif (char == 'A'):
                # Print a single pixel
                if 0 <= i < WCS['NAXIS1'] and 0 <= j < WCS['NAXIS2']:
                    val = self.Data[i, j]
                    self.__MessHand.info("("+str("%7.3f" % x)+","+str("%7.3f" % y)+") = "+str(val))
                else:
                    self.__MessHand.warning("pixel outside the plot")

            x, y, char = Plot.getpix(x, y)
            i, j = self.wcs2pix(x, y)
            i = int(i)
            j = int(j)

    #--------------------------------------------------------------------------------
    def zoom(self, mouse=1, style='idl4', wedge=True,\
                limitsZ=[], aspect=False, limitsX=[], limitsY=[], caption=None,\
                doContour=False, levels=[], showRms=True, rmsKappa=3.5):
        """allow the user to select a region in the map to zoom in

        Parameters
        ----------
        mouse : bool
            use the mouse? (default: yes)
        style : 'str'
            the style used for the color (default idl4)
        wedge : bool
            draw a wedge ? (default : yes)
        caption : str
            the caption of the plot (default '')
        limitsX, limitsY, limitsZ : float array
            the limits in X/Y/intensity
        aspect : bool
            keep the aspect ratio (default : yes)
         doContour : bool
            draw contour instead of map (default : no)
        levels : float array
            the levels of the contours (default : intensity progression)
        showRms : bool
            compute and display rms/beam? (def: no)
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        """

        if not self.Data:
            self.__MessHand.error('No map computed yet')
            return

        if not mouse:
            if not limitsX or not limitsY:
                self.MessHand.error('X/Y limits must be given if not using the mouse')
                return
            else:
                limX = limitsX
                limY = limitsY
        else:
            self.__MessHand.info('Use the mouse cursor to select 2 opposite corners')
            WCS  = self.WCS
            x, y = 0, 0
            char = ''
            while char == '':
                x, y, char = Plot.getpix(x, y)
                i, j = self.wcs2pix(x, y)
                if not(0 <= i < WCS['NAXIS1'] and 0 <= j < WCS['NAXIS2']):
                    self.__MessHand.warning("pixel outside the plot")
                    char = ''
            x1, y1 = x, y
            self.__MessHand.longinfo("Corner1: ("+str("%8.4f" % x)+","+str("%8.4f" % y)+")")
            char = ''
            while char == '':
                x, y, char = Plot.getpix(x, y)
                i, j = self.wcs2pix(x, y)
                if not(0 <= i < WCS['NAXIS1'] and 0 <= j < WCS['NAXIS2']):
                    self.__MessHand.warning("pixel outside the plot")
                    char = ''
            x2, y2 = x, y
            self.__MessHand.longinfo("Corner2: ("+str("%8.4f" % x)+","+str("%8.4f" % y)+")")

            # sort limits
            if self.WCS['CTYPE1'][:4] == "OLON":
                # for HO map, X axis goes increasing
                limX = [min([x1, x2]), max([x1, x2])]
            else:
                limX = [max([x1, x2]), min([x1, x2])]
            limY = [min([y1, y2]), max([y1, y2])]
        if not caption:
            caption = 'Zoom'
        self.__MessHand.info('limitsX=['+str("%8.4f" % max(limX))+',' + \
                             str("%8.4f" % min(limX)+'],') + \
                             'limitsY=['+str("%8.4f" % min(limY))+',' + \
                             str("%8.4f" % max(limY)+'] '))
        self.display(style=style,
                     limitsX=limX, limitsY=limY, limitsZ=limitsZ,
                     aspect=aspect, caption=caption, wedge=wedge,
                     doContour=doContour, levels=levels,
                     showRms=showRms, rmsKappa=rmsKappa)


    #--------------------------------------------------------------------------------
    def extractSource(self, gradient=False, circular=False, radius=-10, \
                      Xpos = 0., Ypos = 0., fixedPos = False, incl=0., fixIncl=False):
        """fit a 2D Gaussian on  a map

        Parameters
        ----------
        gradient : bool
            remove a gradient ?
        circular : bool
            fit a circular gaussian ?
        radius : float
            fit within a radius aperture,
            negative values are in fwhm unit
        Xpos, Ypos : float
            position of the circular aperture
        fixedPos : bool
            do we fix source position ?
        incl : float
            elliptical gaussian angle
        fixIncl : bool
            do we fix the angle ?

        Returns
        -------
        parinfo
           the full fit result
        """

        if self.Data == []:
            self.__MessHand.error('No map computed yet')
            return

        fwhm = self.BeamSize  # that's in the map coordinates unit
        # If map in EQ system, use central position as starting point
        if self.WCS['CTYPE1'].find('RA') >= 0 or self.WCS['CTYPE2'].find('DEC') >= 0:
            if not Xpos:  # but only if not provided by the user
                Xref = self.WCS['CRVAL1']
            else:
                Xref = Xpos
            if not Ypos:
                Yref = self.WCS['CRVAL2']
            else:
                Yref = Ypos
        else:
            Xref, Yref = Xpos, Ypos

        mapArray          = self.Data
        weightArray       = self.Weight
        azArray, elArray  = self.physicalCoordinates()

        # put everything into 1D easier for radius compression
        mapArray    = np.ravel(mapArray)
        weightArray = np.ravel(weightArray)
        azArray     = np.ravel(azArray)
        elArray     = np.ravel(elArray)

         # Remove 0 weights
        goodData    = np.nonzero(weightArray > 0)
        mapArray    = np.take(mapArray, goodData)
        weightArray = np.take(weightArray, goodData)
        azArray     = np.take(azArray, goodData)
        elArray     = np.take(elArray, goodData)

        if radius < 0:
            radius = abs(radius)*fwhm

        # Select data to a certain radius from the given X/Y pos
        if radius != 0:
            good_for_fit = np.less(np.sqrt((azArray-Xref)**2+(elArray-Yref)**2), radius)
            azArray, n   = fUtilities.compress(azArray, good_for_fit, 1)
            azArray     = azArray[:n]
            elArray, n   = fUtilities.compress(elArray, good_for_fit, 1)
            elArray     = elArray[:n]
            mapArray, n = fUtilities.compress(mapArray, good_for_fit, 1)
            mapArray   = mapArray[:n]
            weightArray, n = fUtilities.compress(weightArray, good_for_fit, 1)
            weightArray   = weightArray[:n]

        # now use the data to fit a 2D-Gaussian
        try:
            pointingResult = fitBaseEllipticalGaussian(mapArray, azArray, elArray,\
                                                       err = 1/np.sqrt(weightArray),\
                                                       fwhm=fwhm,\
                                                       gradient=gradient,\
                                                       circular=circular,\
                                                       Xpos=Xpos, Ypos=Ypos,\
                                                       fixedPos=fixedPos,\
                                                       incl=incl,\
                                                       fixIncl=fixIncl)
        except ReaError as error:
            self.__MessHand.warning('fit did not converge:')
            self.__MessHand.warning(error.msg)
            pointingResult = -1

        # TODO: is it the best thing to return the result?
        return pointingResult


    #--------------------------------------------------------------------------
    #
    # methods to compute rms/beam
    #--------------------------------------------------------------------------
    def rmsDistribution(self, cell=3):
        """compute the distribution of rms in the map

        Parameters
        ----------
        cell : int
            size of cells on which rms are computed (default: 3x3)

        Returns
        -------
        list
            rms values in cell
        """

        data = self.Data
        rmsdistr = copy.deepcopy(self.Data)
        WCS  = self.WCS

        allRms = []
        for x in range(WCS['NAXIS1']-cell):
            for y in range(WCS['NAXIS2']-cell):
                listVal = self.Data[x:x+cell, y:y+cell]
                listVal = np.ravel(listVal)

                listVal, nNan = compressNan([listVal])
                if len(listVal) > 0:
                    mean = fStat.f_mean(listVal)
                    val = fStat.f_rms(listVal, mean)
                    allRms.append(val)

        return allRms

    def rmsMap(self, cell=15, sparse=8):
        """compute the distribution of rms in the map

        Parameters
        ----------
        cell : int
            size of cells on which rms are computed (default: 15x15)
        sparse : int
            compute rms only on pixels separated by this number
                            (to save time) (default: 8)

        Returns
        -------
        2D float array
            the rmsMap
        """

        data = self.Data
        rmsdistr = copy.deepcopy(self.Data)*0.0+float('nan')
        WCS  = self.WCS

        off1 = int(cell/2.)

        maxx = int(WCS['NAXIS1'])
        maxy = int(WCS['NAXIS2'])

        # find x values to compute rms
        xval = [off1+1]
        done = 0
        while (done == 0):
            newx = xval[shape(xval)[0]-1]+sparse
            if (newx < maxx-off1-1):
                xval.extend([newx])
            else:
                done = 1
        # same for y
        yval = [off1+1]
        done = 0
        while (done == 0):
            newy = yval[shape(yval)[0]-1]+sparse
            if (newy < maxy-off1-1):
                yval.extend([newy])
            else:
                done = 1
        off2 = cell-off1

        for x in range(off1, WCS['NAXIS1']-off2):
            for y in range(off1, WCS['NAXIS2']-off2):

                listVal = self.Data[x-off1:x+off1, y-off1:y+off1]
                listVal = np.ravel(listVal)

                listVal, nNan = compressNan([listVal])
                if len(listVal) > 0:
                    mean = fStat.f_mean(listVal)
                    val = fStat.f_rms(listVal, mean)
                    rmsdistr[x, y] = val

        return rmsdistr

    def computeSNMap(self, cell=15, sparse=8):
        """compute a signal-to-noise map from the current map data and weights

        Parameters
        ----------
        cell : int
            size of cells on which rms are computed (default: 10x10)
        sparse : int
            compute rms only on pixels separated by this number (to save time) (default: 5)
        """

        # we assume that the local rms in the map is exactly 1./sqrt(weight) times some constant.
        # to determine the constant, we have to first find the local rms in the map
        # if there is a strong source, one should cut it out first.

        dat = copy.deepcopy(np.array(self.Data))
        weight = copy.deepcopy(np.array(self.Weight))

        # compute rms map
        rmsmap = np.ravel(self.rmsMap(cell=cell, sparse=sparse))

        # compute unscaled rms map from weights
        rmsunsc = 1./np.sqrt(np.ravel(weight))

        # find where both of these maps are ok
        mask1 = where(bitwise_and((rmsmap > -10000000.), (rmsunsc > -10000000.)), 1, 0)

        mask2 = where(bitwise_and((rmsmap != 0), (rmsunsc != 0)), 1, 0)
        mask = mask1*mask2

        rmsmap = np.compress(mask, rmsmap)
        rmsunsc = np.compress(mask, rmsunsc)

        # the coefficient should be...
        coeffs = rmsmap/rmsunsc

        # take the median
        coeff = fStat.f_median(coeffs)
        self._Image__MessHand.info('computed rms = %f * (1./sqrt(weight))'%coeff)

        # TBD: remove outliers??

        # return the s/n map
        self.snmap = dat/((1./np.sqrt((weight)))*coeff)

    def meanDistribution(self, cell=3, limitsX=[], limitsY=[]):
        """compute and plot the distribution of means in the map

        Parameters
        ----------
        cell : int
            size of cells on which mean values are computed (default: 3x3)
        limitsX, limitsY: float array
            optionally define a sub-region (pixel coord)

        Returns
        -------
        float array
            the mean distribution
        """

        WCS  = self.WCS

        # Number of beams in the map
        nbX = WCS['NAXIS1']-cell
        nbY = WCS['NAXIS2']-cell

        # if sub-region asked, check that coord are within the map
        if limitsX:
            if limitsX[0] < 0:
                limitsX[0] = 0
            if limitsX[1] > nbX:
                limitsX[1] = nbX
        if limitsY:
            if limitsY[0] < 0:
                limitsY[0] = 0
            if limitsY[1] > nbY:
                limitsY[1] = nbY

        theData = copy.copy(self.Data)
        if limitsX:
            theData = theData[limitsX[0]:limitsX[1],:]
            nbX = limitsX[1]-limitsX[0]
        if limitsY:
            theData = theData[:, limitsY[0]:limitsY[1]]
            nbY = limitsY[1]-limitsY[0]

        allMean, nbOk = fStat.meandistribution(theData, nbX, nbY, nbX*nbY, cell)
        allMean = allMean[:nbOk]

        return allMean

    def computeRmsBeam(self,cell=3,rmsKappa=3.5,limitsX=[],limitsY=[]):
        """compute rms/beam in a map (smoothed at beam resolution)

        Parameters
        ----------
        cell : float
            size of one beam in pixel
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        limitsX, limitsY : float array
            optionally define a sub-region (pixel coord)
        """
        # Distribution of flux/beam
        m = self.meanDistribution(cell=cell, limitsX=limitsX, limitsY=limitsY)
        # Remove the NaNs at this stage
        mm, nNan = compressNan([m])
        # clip data at more than k-sigma (e.g. a source)
        m2, nbOk = fStat.clipping(mm, rmsKappa)
        m2 = m2[:nbOk]
        self.RmsBeam = fStat.f_stat(m2)[1]
        self.__MessHand.info("r.m.s. / beam = %f"%(self.RmsBeam))

    def computeRms(self,rmsKappa=3.5,limitsX=[],limitsY=[]):
        """compute rms/beam in a map (dispersion between pixels)

        Parameters
        ----------
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        limitsX, limitsY: float array
            optionally define a sub-region (pixel coord)
        """
        if limitsX or limitsY:
            if not limitsX:
                localData = self.Data[:, limitsY[0]:limitsY[1]]
            elif not limitsY:
                localData = self.Data[limitsX[0]:limitsX[1],:]
            else:
                localData = self.Data[limitsX[0]:limitsX[1],
                                      limitsY[0]:limitsY[1]]
        else:
            localData = self.Data
        # Distribution of pixel values
        pixels = np.ravel(localData)
        # Remove the NaNs at this stage
        pixels, nb = compressNan([pixels])
        # clip data at more than k-sigma (e.g. a source)
        m2, nbOk = fStat.clipping(pixels, rmsKappa)
        m2 = m2[:nbOk]
        self.RmsBeam = fStat.f_stat(m2)[3]  # median deviation
        self.__MessHand.info("map r.m.s. = %f"%(self.RmsBeam))

    def submap(self,limitsX=[],limitsY=[]):
        """this function returns a map covering a sub-region of the
             initial map

        Parameters
        ----------
        limitsX, limitsY: float array
            the limits in world coordinates

        Returns
        -------
        ReaMapping.Image
            an object of class Image is returned
        """

        localMap = copy.deepcopy(self)
        if limitsX or limitsY:
            if not limitsX:
                # only limitsY given
                x1, x2 = 0, self.WCS['NAXIS1']
                i, y1 = self.wcs2pix(self.WCS['CRVAL1'], min(limitsY))
                i, y2 = self.wcs2pix(self.WCS['CRVAL1'], max(limitsY))
            elif not limitsY:
                # only limitsX given
                y1, y2 = 0, self.WCS['NAXIS2']
                x1, j = self.wcs2pix(max(limitsX), self.WCS['CRVAL2'])
                x2, j = self.wcs2pix(min(limitsX), self.WCS['CRVAL2'])
            else:
                # both limits given by user
                x1, y1 = self.wcs2pix(max(limitsX), min(limitsY))
                x2, y2 = self.wcs2pix(min(limitsX), max(limitsY))

            # make sure that the limits don't go outside the existing data
            x1 = max([0, int(x1)])
            x2 = min([self.WCS['NAXIS1'], int(x2)+1])
            y1 = max([0, int(y1)])
            y2 = min([self.WCS['NAXIS2'], int(y2)+1])
            localMap.Data     = self.Data[x1:x2, y1:y2]
            localMap.Weight   = self.Weight[x1:x2, y1:y2]
            localMap.Coverage = self.Coverage[x1:x2, y1:y2]
            # update WCS info - need to compute the actual limits
            limX1, limY1 = self.wcs2phy(x1, y1)
            limX2, limY2 = self.wcs2phy(x2, y2)
            minmaxXY = [limX1, limX2, limY1, limY2]
            pixSize = abs(self.WCS['CDELT1'])
            localMap.computeWCS(pixSize, minmax=minmaxXY)

        return localMap

    def writeFits(self,outfile='reaMap.fits',
                  overwrite=False,limitsX=[],limitsY=[],intensityUnit="Jy/beam",
                  writeFlux=True,writeWeight=True,writeCoverage=True,
                  writeRms=False,rmsfile=''):
        """store the current map (2D array with WCS info) to a FITS file

        Parameters
        ----------
        outfile : str
            output file name (default reaMap.fits)
        overwrite : bool
            overwrite existing file ?
        limitsX, limitsY : float array
            optional map limits (in world coordinates)
        intensityUnit : str
            optional unit of the intensity (default: "Jy/beam")
        writeFlux, writeWeight, writeCoverage, writeRms : bool
            should these planes be included in the output file?
        rmsfile : str
            extension used to write a separate file for rmsMap, if any
        """

        filename = os.path.join(ReaConfig.outDir, outfile)

        if os.path.exists(filename):
            if not overwrite:
                self.__MessHand.error('File %s exists' % filename)
                return

        try:
            dataset = ReaFits.createDataset("!" + filename)
        except Exception as data:
            self.__MessHand.error('Could not open file %s: %s' % (outfile, data))
            return

        if limitsX or limitsY:
            localMap = self.submap(limitsX=limitsX, limitsY=limitsY)
        else:
            localMap = self

        try:
            if writeFlux:
                localMap.__writeImage(dataset, "Intensity", intensityUnit=intensityUnit)
            if writeWeight:
                localMap.__writeImage(dataset, "Weight")
            if writeCoverage:
                localMap.__writeImage(dataset, "Coverage")
            dataset.close()

        except Exception as data:
            self.__MessHand.error('Could not write data to file %s: %s' % (outfile, data))
            return

        if writeRms:
            localMap.Data = np.array(1., np.float)/np.sqrt(localMap.Weight)
            if not rmsfile:
                rmsfile = outfile[:-5]+'-rms.fits'
            dataset = ReaFits.createDataset("!" + rmsfile)
            localMap.__writeImage(dataset, "RMS", intensityUnit=intensityUnit)
            dataset.close()

        localMap = 0  # free memory
        dataset = 0

    def __writeImage(self, dataset, extname, intensityUnit=""):
        if extname == "Intensity":
            data = self.Data
        elif extname == "Weight":
            data = self.Weight
        elif extname == "Coverage":
            data = self.Coverage
        elif extname == "RMS":
            data = self.Data
        else:
            self.__MessHand.error("Don't know how to write image '%s'" % extname)

        if not data.any():
            self.__MessHand.info("No data to write image %s" % extname)
            return

        WCS = self.WCS

        try:
            dataImage = dataset.createImage(data)
            if not dataImage:
                self.__MessHand.error("Error while creating image '%s'" % extname)
                return

            dataImage.createKeywordDate()
            dataImage.createKeyword("CREATOR", "Rea",
                                    comment="REceiver Array Analysis Project")
            dataImage.createKeyword("EXTNAME", extname,
                                    comment="Type of data contained in this image")

            dataImage.createKeyword("MJD-OBS", WCS["MJD-OBS"],
                                    comment="time of observation")
            dataImage.createKeyword("RADESYS", WCS["RADESYS"],
                                    comment="frame of reference")
            dataImage.createKeyword("EQUINOX", WCS["EQUINOX"],
                                    comment="coordinate epoch")

            dataImage.createKeyword("CTYPE1", WCS["CTYPE1"],
                                    comment="Type of coordinate 1")
            dataImage.createKeyword("CRPIX1", WCS["CRPIX1"],
                                    comment="Reference pixel of coordinate 1")
            dataImage.createKeyword("CDELT1", WCS["CDELT1"],
                                    comment="Increment per pixel of coordinate 1")
            dataImage.createKeyword("CRVAL1", WCS["CRVAL1"],
                                    comment="Value of coordinate 1 at reference point")
            dataImage.createKeyword("CUNIT1", WCS["CUNIT1"],
                                    comment="Unit of coordinate 1")

            dataImage.createKeyword("CTYPE2", WCS["CTYPE2"],
                                    comment="Type of coordinate 2")
            dataImage.createKeyword("CRPIX2", WCS["CRPIX2"],
                                    comment="Reference pixel of coordinate 2")
            dataImage.createKeyword("CDELT2", WCS["CDELT2"],
                                    comment="Increment per pixel of coordinate 2")
            dataImage.createKeyword("CRVAL2", WCS["CRVAL2"],
                                    comment="Value of coordinate 2 at reference point")
            dataImage.createKeyword("CUNIT2", WCS["CUNIT2"],
                                    comment="Unit of coordinate 2")

            dataImage.createKeyword("PC1_1", WCS["PC1_1"],
                                    comment="Linear transformation matrix")
            dataImage.createKeyword("PC1_2", WCS["PC1_2"],
                                    comment="Linear transformation matrix")
            dataImage.createKeyword("PC2_1", WCS["PC2_1"],
                                    comment="Linear transformation matrix")
            dataImage.createKeyword("PC2_2", WCS["PC2_2"],
                                    comment="Linear transformation matrix")

            dataImage.createKeyword("OBJECT", self.Header["Object"],
                                    comment="Object observed")
            dataImage.createKeyword("TELESCOP", self.Header["Telescope"],
                                    comment="Telescope name")
            dataImage.createKeyword("FEBE", self.Header["FeBe"],
                                    comment="Frontend-backend combination")

            # BUNIT: this assumes that calibration was done!
            if extname == "Intensity":
                dataImage.createKeyword("BUNIT", intensityUnit,
                                        comment="Physical unit of image")
                dataImage.createKeyword("TAU", self.Header["Tau"],
                                        comment="Opacity Correction")
                dataImage.createKeyword("EL", self.Header["Elevation"],
                                        comment="Median Elevation")
                dataImage.createKeyword("COUNT2JY", self.Header["JyPerCount"],
                                        comment="Calibration factor")
            dataImage.createKeyword("BMAJ", self.BeamSize,
                                    comment="Beam major axis")
            dataImage.createKeyword("BMIN", self.BeamSize,
                                    comment="Beam minor axis")
            dataImage.createKeyword("BPA", 0.,
                                    comment="Beam position angle")

            dataImage.writeImage()

            self.__MessHand.debug("Image '%s' written. Size: %s"
                                  % (extname, str(dataImage.getShape())))

            data = 0  # free memory
            dataImage = 0

        except Exception as msg:
            self.__MessHand.error("Error while writing image '%s'" % extname)
            self.__MessHand.error("Exception: '%s'" % msg)
            return

    # -------------------------------------------------------------------
    def dumpMap(self,outfile='ReaMap.sav'):
        """save an Image instance to a file

        Parameters
        ----------
        outfile : str
            name of the output file
        """

        filename = os.path.join(ReaConfig.outDir, outfile)
        try:
            f = file(filename, 'w')
        except:
            self.__MessHand.error(" permission denied, please change filename/out directory")
            return
        cPickle.dump(self, f, 2)
        f.close()
        self.__MessHand.debug("Image written to %s"%outfile)


#----------------------------------------------------------------------------------
#----- Kernel Class ---------------------------------------------------------------
#----------------------------------------------------------------------------------
class Kernel(Image):
    """.. class : Kernel
    :synopsis: define a kernel
    """

    def __init__(self, pixelSize, beamSize):
        """Initialise an instance of a Kernel class

        Parameters
        ----------
        pixelSize : float
            the physical size of a pixel
        beamSize : float
            the beam FWHM in the same unit
        """

        Image.__init__(self)

        self.computeWCS(pixelSize,\
                        minmax = np.array([-1, 1, -1, 1], np.float32)*beamSize*3.)

        # For smoothing, we NEED an odd number of pixels
        # if that's not the case, then generate a slightly larger kernel
        nbX = self.WCS['NAXIS1']
        if not nbX%2:
            self.computeWCS(pixelSize,\
                            minmax = np.array([-1, 1, -1, 1], np.float32)*beamSize*3. +
                            np.array([-1, 1, -1, 1], np.float32)*pixelSize/2.)

        kernel_azimuth, kernel_elevation = self.physicalCoordinates()

        # kernel_parameters = np.array([0.,0.,0.,beamSize**2*16*pi*log(2.),
        kernel_parameters = np.array([0., 0., 0., 1.,
                                   0., 0., beamSize, beamSize, 0.])
        tmpData = modelBaseEllipticalGaussian(kernel_parameters,\
                                              [kernel_azimuth, kernel_elevation])
        self.Data = tmpData.astype(np.float32)


#----------------------------------------------------------------------------------
#----- Rea Mapping Class ----------------------------------------------------------
#----------------------------------------------------------------------------------
class Map(ReaDataAnalyser.DataAna):
    """..class : Map
    :synopsis: An object of this class is responsible for the restoration of
    mapping data of single or multiple files.
    """

    def __init__(self):
        """Initialise an instance."""
        ReaDataAnalyser.DataAna.__init__(self)

        self.__Results = []
        self.Map = Image()


#--------------------------------------------------------------------------------
#----- map methods --------------------------------------------------------------
#--------------------------------------------------------------------------------

    def showMap(self,style='idl4',wedge=True,\
                limitsZ=[],aspect=True,limitsX=[],limitsY=[],caption=None,\
                doContour=False,levels=[],showRms=False,rmsKappa=3.5,noerase=False):
        """show the reconstructed map in (Az,El) or (Ra,Dec)

        Parameters
        ----------
        style : str
            the colormap
        wedge : bool
            display the wedge (default yes)
        aspect : bool
            keep aspect ratio (default yes)
        limitsZ : float array
            range to display in color
        limitsX : float array
            range to display in X
        limitsY : float array
            range to display in Y
        caption : str
            caption of the map
        doContour : bool
            do we plot contour map ?
        levels : float array
            levels for the contour plot
        showRms : bool
            do we plot rms instead of map ?
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        noerase : bool
            shall we keep the display ?
        """

        if self.Map.Data == []:
            self.MessHand.error('No map computed yet')
            return
        if not caption:
            caption = self.ScanParam.caption()

        self.Map.display(style=style,
                         limitsX=limitsX, limitsY=limitsY, limitsZ=limitsZ,
                         aspect=aspect, caption=caption, wedge=wedge,
                         doContour=doContour, levels=levels,
                         showRms=showRms, rmsKappa=rmsKappa,
                         noerase=noerase)

    #--------------------------------------------------------------------------------

    def displayMap(self, weight=0, coverage=0, style='idl4', caption='', wedge=1, \
                aspect=1, overplot=0, doContour=0, levels=[], labelContour=0,\
                limitsX = [], limitsY = [], limitsZ = [], \
                showRms=0, rmsKappa=3.5):

        if self.Map.Data == []:
            self.MessHand.error('No map computed yet')
            return

        self.Map.display(weight=weight, coverage=coverage, style=style, \
                         caption=caption, wedge=wedge, aspect=aspect, \
                         overplot=overplot, doContour=doContour, levels=levels, \
                         labelContour=labelContour, \
                         limitsX = limitsX, limitsY = limitsY, limitsZ = limitsZ, \
                         showRms=showRms, rmsKappa=rmsKappa )

    #--------------------------------------------------------------------------------

    def smoothMap(self, fwhm):
        """smooth the image with a 2D gaussian of given FWHM

        Parameters
        ----------
        fwhm : float
            the FWHM of the smoothing gaussian
        """

        if self.Map.Data == []:
            self.MessHand.error('No map computed yet')
            return

        self.Map.smoothBy(fwhm)

    #--------------------------------------------------------------------------------

    def getPixelFromMap(self,nbPix=3):
        """allow user to get pixel values using mouse

        Parameters
        ----------
        nbPix : int
            size of area to compute average (default 3x3)
        """

        if self.Map.Data == []:
            self.MessHand.error('No map computed yet')
            return

        self.Map.getPixel(nbPix)

    #--------------------------------------------------------------------------------

    def computeRmsFromMap(self,rmsKappa=3.5,limitsX=[],limitsY=[]):
        """compute rms/beam in a map (dispersion between pixels)

        Parameters
        ----------
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        limitsX, limitsY: float array
            optionally define a sub-region (pixel coord)
        """

        if self.Map.Data == []:
            self.MessHand.error('No map computed yet')
            return

        self.Map.computeRms(rmsKappa, limitsX, limitsY)

#--------------------------------------------------------------------------------
#----- public methods -----------------------------------------------------------
#--------------------------------------------------------------------------------


    def doMap(self,chanList=[], \
              channelFlag=[], plotFlaggedChannels=False, \
              dataFlag=[], plotFlaggedData=False, \
              oversamp=3.0, system='HO',\
              sizeX=[],sizeY=[],limitsZ=[],style='idl4',wedge=True,smooth=False,noPlot=False,\
              caption=None,aspect=True,showRms=True,rmsKappa=2.,derotate=False,neighbour=False):
        """reconstruct a map in (Az,El) coordinates combining receivers

        Parameters
        ----------
        chanList : list of int
            channels to consider
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : boo;
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                                          flag   | plotFlagged | Plot..
                                          'None' |  0          | all data
                                          []     |  0          | unflagged data (default)
                                          []     |  1          | data with at least one flag set
                                          1      |  0          | data with flag 1 not set
                                          1      |  1          | data with flag 1 set
                                          [1,2]  |  0          | data with neither flag 1 nor flag 2 set
                                          [1,2]  |  1          | data with either flag 1 or flag 2 set
        oversamp : float
            oversampling factor (beam fwhm / pixel size). Default=2.
        system : {'HO', 'EQ', 'GAL'}
            coordinate system used for the map :
             * 'HO' for Az,El *offsets*
             * 'EQ' for RA, Dec absolute coord.
             * 'GAL' for Galactic system
        sizeX : float array
            limits in Az of the map
        sizeY : float array
            limits in El of the map
        noNan : bool
            remove NaN in self.Results?
        style : str
            color table to use in image
        smooth : bool
            do we smooth with beam? (default: no)
        noPlot : bool
            do not plot the map? (default: no, i.e. yes we plot)
        wedge : bool
            do we plot a wedge ?
        caption : bool
            plot caption
        aspect : bool
            keep aspect ratio? (default: yes)
        showRms : bool
            compute and print rms/beam? (default: yes)
        rmsKappa : float
            kappa in kappa-sigma clipping used to compute rms
        derotate : float
            derotate Nasmyth array by Elevation
        neighbour : bool
            do we divide signal into 4 neighbouring pixels? (def: no)
        """

        # check channel list; will return all non-flagged channels if chanList = []
        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)

        if not(len(chanList)):
            self.MessHand.error("no valid channels")
            return
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        myTiming = Timing()
        myTiming.setTime()

        rotAngles = np.zeros(self.ScanParam.NInt, np.float)
        if "NASMYTH" in self.ReceiverArray.DewCabin:
            rotAngles += -self.ScanParam.El

        # Select offsets according to system, 'HO' or 'EQ'
        system = string.upper(system)
        if system == 'HO':
            XYOffsets = np.transpose(self.ScanParam.get('AzimuthElevationOffset', flag='None'))
            XOffsets = self.ScanParam.get('AzimuthOffset')
            YOffsets = self.ScanParam.get('ElevationOffset')

        elif system == 'EQ':
            XYOffsets = np.array([self.ScanParam.get('RA', flag='None'), \
                                   self.ScanParam.get('Dec', flag='None')])
            XOffsets = self.ScanParam.get('RA')
            YOffsets = self.ScanParam.get('Dec')

            rotAngles += np.array(self.ScanParam.ParAngle)

        elif (system == 'GAL'):
            if not len(self.ScanParam.GLon):
                self.ScanParam.computeGal()
            XYOffsets = np.array([self.ScanParam.get('Glon', flag='None'), \
                                   self.ScanParam.get('Glat', flag='None')])
            XOffsets = self.ScanParam.get('Glon')
            YOffsets = self.ScanParam.get('Glat')

            if not len(self.ScanParam.GalAngle):
                self.ScanParam.computeGalAngle()

            rotAngles += np.array(self.ScanParam.ParAngle) + np.array(self.ScanParam.GalAngle)


        data        = self.Data
        dataWeights = self.DataWeights

        OffsetsUsed = self.ReceiverArray.Offsets

        # Retrieve the beam and compute pixel size
        fwhm = self.ReceiverArray.BeamSize
        pixelSize = fwhm / oversamp

        if (system == 'EQ') or (system == 'GAL'):
            # then unit is Degree
            pixelSize = pixelSize/3600.
            fwhm = fwhm/3600.

            # TODO : Use the proper routine... ScanParam.getChanSep()
            chanListAzEl = np.array(self.ReceiverArray.UsedChannels)-1
            OffsetsAzEl = np.take(self.ReceiverArray.Offsets, chanListAzEl, axis=1)
            refChOffsets = self.ReceiverArray.Offsets[:, self.ReceiverArray.RefChannel-1]

            # even if system is 'EQ', the following needs to be done in order
            # to allow computation of the extrema of the map
            # TODO: This if fundamentally wrong, the projection is bullshit here...
            OffsetsUsed = OffsetsUsed / 3600.
            Yrange = fStat.minmax(YOffsets)
            OffsetsUsed[0,:] /= np.array(np.cos(np.radians((Yrange[0]+Yrange[1])/2.)), np.float)

        # compute roughly the extrema of the map (taking into account the ScanParam
        # flags but not the ReceiverArray Flags nor the Data Flags
        minmaxXY = np.concatenate(\
                (fStat.minmax(XOffsets)+np.array([-1, 1])*2*pixelSize + \
                 fStat.minmax(np.take(OffsetsUsed[0,:], chanListIndexes)), \
                 fStat.minmax(YOffsets)+np.array([-1, 1])*2*pixelSize + \
                 fStat.minmax(np.take(OffsetsUsed[1,:], chanListIndexes)) ) \
                )
        if (system == 'EQ') or (system == 'GAL'):
            # swap X min and max (East to the left)
            minmaxXY[0], minmaxXY[1] = minmaxXY[1], minmaxXY[0]

        # Create the resulting image
        Map = self.Map
        Map.__init__()

        Map.Header['Object']     = self.ScanParam.Object
        Map.Header['Telescope']  = self.ReceiverArray.Telescope.Name
        Map.Header['FeBe']       = self.ReceiverArray.FeBe
        Map.Header['JyPerCount'] = self.ReceiverArray.JyPerCount
        Map.Header['Tau']        = self.ScanParam.Tau
        Map.Header['Elevation']  = fStat.f_median(self.ScanParam.get('El'))

        Map.BeamSize = fwhm

        if system == 'HO':
            Map.WCS['CTYPE1']   = 'OLON--SFL'
            Map.WCS['CTYPE2']   = 'OLAT--SFL'
            Map.WCS['CUNIT1']   = 'arcsec'
            Map.WCS['CUNIT2']   = 'arcsec'
            cdeltUnit           = 1./3600.
        elif (system == 'EQ'):
            Map.WCS['CTYPE1']   = 'RA---SFL'
            Map.WCS['CTYPE2']   = 'DEC--SFL'
            Map.WCS['CUNIT1']   = 'deg'
            Map.WCS['CUNIT2']   = 'deg'
            cdeltUnit           = 1.
        elif (system == 'GAL'):
            Map.WCS['CTYPE1']   = 'GLON-GLS'
            Map.WCS['CTYPE2']   = 'GLAT-GLS'
            Map.WCS['CUNIT1']   = 'deg'
            Map.WCS['CUNIT2']   = 'deg'
            cdeltUnit           = 1.
        Map.WCS['MJD-OBS']  = self.ScanParam.DateObs

        # update main WCS keywords
        Map.computeWCS(pixelSize, sizeX, sizeY, minmaxXY)
        AXIS1 = np.array([Map.WCS['NAXIS1'], Map.WCS['CRPIX1'], Map.WCS['CDELT1'],
                       Map.WCS['CRVAL1'], cdeltUnit])
        AXIS2 = np.array([Map.WCS['NAXIS2'], Map.WCS['CRPIX2'], Map.WCS['CDELT2'],
                       Map.WCS['CRVAL2'], cdeltUnit])

        self.MessHand.longinfo("Building a map with dimensions (x,y) = " +\
                           str(int(AXIS1[0]))+','+str(int(AXIS2[0])))

        if Map.WCS['NAXIS1']*Map.WCS['NAXIS2']*32*3/8/1e6 > 600:
            if ReaConfig.online:
                self.MessHand.error('Such maps would require more than 600Mb of memory, aborting...')
                return
            elif not self.MessHand.yesno('do you really want to do such a big map (>600Mb) ?'):
                return

        mapData     = np.zeros((int(AXIS1[0]), int(AXIS2[0])), np.float32)
        mapWeight   = np.zeros((int(AXIS1[0]), int(AXIS2[0])), np.float32)
        mapCoverage = np.zeros((int(AXIS1[0]), int(AXIS2[0])), np.float32)

        dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
        if dataFlag == None:
            self.MessHand.error("no valid flags")
            return

        if dataFlag in ['', 'None']:
            dataFlagMask = np.ones(shape=self.FlagHandler.getFlags().shape, \
                                dtype=self.FlagHandler.getFlags().dtype.char)
        else:
            if plotFlaggedData:
                dataFlagMask = self.FlagHandler.isSetMask(dataFlag)
            else:
                dataFlagMask = self.FlagHandler.isUnsetMask(dataFlag)

        if system == 'HO':
            mapData, mapWeight, mapCoverage = fMap.horizontalprojection(chanListIndexes, data, \
                                                                        dataWeights, \
                                                                        dataFlagMask, 1, \
                                                                        XYOffsets, OffsetsUsed,
                                                                        rotAngles,
                                                                        AXIS1, AXIS2,
                                                                        mapData, mapWeight, mapCoverage)
        if system == 'EQ' or system == 'GAL':
            mapData, mapWeight, mapCoverage = fMap.equatorialprojection(chanListIndexes, data, \
                                                                        dataWeights, \
                                                                        dataFlagMask, 1, \
                                                                        XYOffsets, OffsetsAzEl,
                                                                        rotAngles,
                                                                        refChOffsets,
                                                                        AXIS1, AXIS2, neighbour,
                                                                        mapData, mapWeight, mapCoverage)

        Map.Data     = mapData
        Map.Weight   = mapWeight
        Map.Coverage = mapCoverage

        self.Map = Map

        # Smoothing after normalisation
        if smooth:
            kernel_to_smooth = Kernel(pixelSize, fwhm)
            self.Map.smoothWith(kernel_to_smooth)

        if not noPlot:
            self.showMap(wedge=wedge, style=style, aspect=aspect,
                         limitsZ=limitsZ, caption=caption,
                         showRms=showRms, rmsKappa=rmsKappa)

        self.MessHand.debug(" map done in " + str(myTiming))


    #--------------------------------------------------------------------------------
    def flagSource(self,chanList=[],threshold=1.,flag=8,model=None,derotate=False):
        """Flag the data according to a model map

        Parameters
        ----------
        chanList : list of int
            the list of channels to work with
        threshold : float
            the pixel value in input map above which is considered as source
        flag : int
            the value of flag to set (def: 8)
        model : ReaMapping.Image
            the input model map (with WCS)
            (None means use current data.Map)
        derotate : bool
            rotate array by El?
        """
        if not model:
            model = self.Map

        if not model.Data:
            self.MessHand.error("no map computed yet, and no model provided")
            return

        chanList = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if string.find(model.WCS['CTYPE1'], 'GLON') > -1:
            if not len(self.ScanParam.GalAngle):
                if not len(self.ScanParam.GLon):
                    self.ScanParam.computeGal()
                self.ScanParam.computeGalAngle()
            rotAngles = np.array(self.ScanParam.ParAngle) + np.array(self.ScanParam.GalAngle)
            XYOffsets = np.array([self.ScanParam.get('Glon', flag='None'), \
                               self.ScanParam.get('Glat', flag='None')])
        else:
            if (derotate):
                rotAngles = np.array(self.ScanParam.ParAngle)+(90-np.array(self.ScanParam.get('El', flag='None')))
            else:
                rotAngles = np.array(self.ScanParam.ParAngle)
            XYOffsets = np.array([self.ScanParam.get('RA', flag='None'), \
                               self.ScanParam.get('Dec', flag='None')])
         # TODO : Use the proper routine... ScanParam.getChanSep()
        chanListAzEl = np.array(self.ReceiverArray.UsedChannels)-1
        OffsetsAzEl = np.array((np.take(self.ReceiverArray.Offsets[0,:], chanListAzEl), \
                           np.take(self.ReceiverArray.Offsets[1,:], chanListAzEl)))
        refChOffsets = self.ReceiverArray.Offsets[:, self.ReceiverArray.RefChannel-1]
        AXIS1 = np.array([model.WCS['NAXIS1'], model.WCS['CRPIX1'],
                       model.WCS['CDELT1'], model.WCS['CRVAL1'], 1.])
        AXIS2 = np.array([model.WCS['NAXIS2'], model.WCS['CRPIX2'],
                       model.WCS['CDELT2'], model.WCS['CRVAL2'], 1.])

        # to avoid Segmentation faults with large arrays, one has to allocate the
        # resulting array of flags on the python side
        newflags = np.zeros(shape(self.Data), np.float)
        result = fMap.flagsource(chanListIndexes, self.Data, model.Data,
                                 threshold, flag, XYOffsets, OffsetsAzEl,
                                 rotAngles, refChOffsets, AXIS1, AXIS2, newflags)

        mask = Utilities.as_column_major_storage(result.astype(np.int8))
        # self.FlagHandler.setOnMask(mask, flag)
        # here also, to avoid seg. fault, call the fortran routine
        # channel by channel
        for index in chanListIndexes:
            self.FlagHandler.setOnMask(mask[:, index], flag, dim=1, index=index)


    #--------------------------------------------------------------------------------

    def flagSourceOld(self,chanList=[],threshold=1.,flag=8,model=None):
        """Flag the data according to a model map

        Parameters
        ----------
        chanList : list of int
            the list of channels to work with
        threshold : float
            the pixel value in input map above which is considered as source
        flag : int
            the value of flag to set (def: 8)
        model : ReaMapping.Image
            the input model map (with WCS)
            (None means use current data.Map)
        """

        if not model:
            model = self.Map

        if not model.Data:
            self.MessHand.error("no map computed yet, and no model provided")
            return

        chanList = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        XYOffsets = np.array([self.ScanParam.get('RA', flag='None'), \
                           self.ScanParam.get('Dec', flag='None')])
         # TODO : Use the proper routine... ScanParam.getChanSep()
        rotAngles = np.array(self.ScanParam.ParAngle)
        chanListAzEl = np.array(self.ReceiverArray.UsedChannels)-1
        OffsetsAzEl = np.array((np.take(self.ReceiverArray.Offsets[0,:], chanListAzEl), \
                           np.take(self.ReceiverArray.Offsets[1,:], chanListAzEl)))
        refChOffsets = self.ReceiverArray.Offsets[:, self.ReceiverArray.RefChannel-1]
        AXIS1 = np.array([model.WCS['NAXIS1'], model.WCS['CRPIX1'],
                       model.WCS['CDELT1'], model.WCS['CRVAL1'], 1.])
        AXIS2 = np.array([model.WCS['NAXIS2'], model.WCS['CRPIX2'],
                       model.WCS['CDELT2'], model.WCS['CRVAL2'], 1.])

        result = fMap.flagsourceold(chanListIndexes, self.Data, model.Data,
                                 threshold, flag,
                                 XYOffsets, OffsetsAzEl, rotAngles, refChOffsets,
                                 AXIS1, AXIS2)

        mask = result.astype('B')
        self.FlagHandler.setOnMask(mask, flag)

    #--------------------------------------------------------------------------------

    def addSource(self,model,chanList=[],factor=1.):
        """add data to time stream according to a model map

        Parameters
        ----------
        chanList : list of int
            the list of channels to work with
        factor : float
            multiply by this factor (default 1)
        model : ReaMapping.Image
            the input model map (with WCS)
            (default: use current data.Map)
        """

        if not model:
            model = self.Map

        if not model.Data:
            self.MessHand.error("no map computed yet, and no model provided")
            return

        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if string.find(model.WCS['CTYPE1'], 'GLON') > -1:
            if not len(self.ScanParam.GalAngle):
                if not len(self.ScanParam.GLon):
                    self.ScanParam.computeGal()
                self.ScanParam.computeGalAngle()
            rotAngles = np.array(self.ScanParam.ParAngle) + np.array(self.ScanParam.GalAngle)
            XYOffsets = np.array([self.ScanParam.get('Glon', flag='None'), \
                               self.ScanParam.get('Glat', flag='None')])
        else:
            rotAngles = np.array(self.ScanParam.ParAngle)
            XYOffsets = np.array([self.ScanParam.get('RA', flag='None'), \
                               self.ScanParam.get('Dec', flag='None')])

        chanListAzEl = np.array(self.ReceiverArray.UsedChannels)-1
        OffsetsAzEl = np.array((np.take(self.ReceiverArray.Offsets[0,:], chanListAzEl), \
                           np.take(self.ReceiverArray.Offsets[1,:], chanListAzEl)))
        refChOffsets = self.ReceiverArray.Offsets[:, self.ReceiverArray.RefChannel-1]
        AXIS1 = np.array([model.WCS['NAXIS1'], model.WCS['CRPIX1'],
                       model.WCS['CDELT1'], model.WCS['CRVAL1'], 1.])
        AXIS2 = np.array([model.WCS['NAXIS2'], model.WCS['CRPIX2'],
                       model.WCS['CDELT2'], model.WCS['CRVAL2'], 1.])

        # get the new data + factor x model array
        tmp = fMap.addsource(chanListIndexes, self.Data, model.Data, \
                             XYOffsets, OffsetsAzEl, rotAngles, refChOffsets, \
                             AXIS1, AXIS2, factor)
        # replace self.Data with updated one
        self.Data = copy.copy(tmp)
        self._DataAna__resetStatistics()
        tmp = 0  # free memory
    #--------------------------------------------------------------------------------

    def zoom(self,mouse=1,style='idl4',wedge=True,\
                limitsZ=[],aspect=True,limitsX=[],limitsY=[],caption=None,\
                doContour=False,levels=[],showRms=True,rmsKappa=3.5):
        """allow the user to select a region in the map to zoom in

        Parameters
        ----------
        mouse : bool
            use the mouse? (default: yes)
       style : str
            the colormap
        wedge : bool
            display the wedge (default yes)
        aspect : bool
            keep aspect ratio (default yes)
        limitsZ : float array
            range to display in color
        limitsX : float array
            range to display in X
        limitsY : float array
            range to display in Y
        caption : str
            caption of the map
        doContour : bool
            do we plot contour map ?
        levels : float array
            levels for the contour plot
        showRms : bool
            do we plot rms instead of map ?
        rmsKappa : float
            for kappa-sigma clipping before computing rms
        """

        if not caption:
            caption = self.ScanParam.caption()

        self.Map.zoom(mouse=mouse, style=style,
                      limitsX=limitsX, limitsY=limitsY, limitsZ=limitsZ,
                      aspect=aspect, caption=caption, wedge=wedge,
                      doContour=doContour, levels=levels,
                      showRms=showRms, rmsKappa=rmsKappa)

    #--------------------------------------------------------------------------------
    def beamMap(self,chanList=[], \
                channelFlag=[], plotFlaggedChannels=0, \
                dataFlag=[], plotFlaggedData=0, \
                oversamp=2.0,sizeX=[],sizeY=[],\
                style='idl4'):
        """build a beam map in (Az,El) coordinates

        Parameters
        ----------
        chanList : list of int
            channels to consider
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                                          flag   | plotFlagged | Plot..
                                          'None' |  0          | all data
                                          []     |  0          | unflagged data (default)
                                          []     |  1          | data with at least one flag set
                                          1      |  0          | data with flag 1 not set
                                          1      |  1          | data with flag 1 set
                                          [1,2]  |  0          | data with neither flag 1 nor flag 2 set
                                          [1,2]  |  1          | data with either flag 1 or flag 2 set
        oversamp : float
            oversampling factor (beam fwhm / pixel size). Default=2.
        sizeX : float array
            limits in Az of the map
        sizeY : float array
            limits in El of the map

        Notes
        -----
        Deprecated

        """

        # do exactly as a normal map, but don't add channel offsets
        self.doMap(chanList=chanList, \
                   channelFlag=channelFlag, plotFlaggedChannels=plotFlaggedChannels, \
                   dataFlag=dataFlag, plotFlaggedData=plotFlaggedData, \
                   oversamp=oversamp,\
                   beammap=1, sizeX=sizeX, sizeY=sizeY, style=style)


    #----------------------------------------------------------------------------
    def chanMap(self,chanList=[], \
                channelFlag=[], plotFlaggedChannels=False, \
                dataFlag=[], plotFlaggedData=False, \
                derotate=False, \
                oversamp=1.,sizeX=[],sizeY=[],\
                style='idl4',limitsZ=[],center=False,showRms=False,rmsKappa=3.5):
        """Compute and plot channel maps in HO offset coordinates

        Parameters
        ----------
        chanList : list of int
            channels to consider
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                                          flag   | plotFlagged | Plot..
                                          'None' |  0          | all data
                                          []     |  0          | unflagged data (default)
                                          []     |  1          | data with at least one flag set
                                          1      |  0          | data with flag 1 not set
                                          1      |  1          | data with flag 1 set
                                          [1,2]  |  0          | data with neither flag 1 nor flag 2 set
                                          [1,2]  |  1          | data with either flag 1 or flag 2 set
        oversamp : float
            oversampling factor (beam fwhm / pixel size). Default=2.
        sizeX : float array
            limits in Az of the map
        sizeY : float array
            limits in El of the map
        style : str
            color table to use in images
        derotate : bool
            derotate from Elevation (i.e. plot in Nasmyth)
        center : bool
           shift each map by the receiver offsets ?
           Thereby it shifts the source to the center of each channel map.
        showRms : bool
            compute and print rms/beam? (default: no)
        rmsKappa : float
            kappa in kappa-sigma clipping used to compute rms
        """

        # Check the list of input channels
        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)

        if not(len(chanList)):
            self.MessHand.error("no valid channel")
            return

        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        data        = self.Data
        dataWeights = self.DataWeights
        AzElOffsets = self.ScanParam.get('AzimuthElevationOffset', flag='None')

        OffsetsUsed = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))
        # OffsetsUsed     = np.array([np.zeros(self.ReceiverArray.NUsedChannels,Float32),\
        #                         np.zeros(self.ReceiverArray.NUsedChannels,Float32)],Float32)

        if center:
            OffsetsUsed = OffsetsUsed*0

        # Retrieve the beam
        fwhm = self.ReceiverArray.BeamSize

        # Compute the pixel size and ...
        pixelSize = fwhm / oversamp

        # compute roughly the extrema of the map (taking into account
        # the ScanParam flags but not the ReceiverArray Flags or the
        # Data Flags

        AzOffsets = self.ScanParam.get('AzimuthOffset')
        ElOffsets = self.ScanParam.get('ElevationOffset')
        rotAngles = np.zeros(self.ScanParam.NInt, np.float)

        minmaxAzEl = np.concatenate(\
                (fStat.minmax(AzOffsets)+np.array([-1, 1])*2*pixelSize - \
                 fStat.minmax(np.take(OffsetsUsed[0,:], chanListIndexes))[::-1], \
                 fStat.minmax(ElOffsets)+np.array([-1, 1])*2*pixelSize - \
                 fStat.minmax(np.take(OffsetsUsed[1,:], chanListIndexes))[::-1] ) \
                )

        # Create a master image
        Map = Image()

        Map.Header['Object']     = self.ScanParam.Object
        Map.Header['Telescope']  = self.ReceiverArray.Telescope.Name
        Map.Header['FeBe']       = self.ReceiverArray.FeBe
        Map.Header['JyPerCount'] = self.ReceiverArray.JyPerCount

        Map.WCS['CTYPE1']   = 'OLON--SFL'
        Map.WCS['CTYPE2']   = 'OLAT--SFL'
        Map.WCS['CUNIT1']   = 'arcsec'
        Map.WCS['CUNIT2']   = 'arcsec'
        Map.WCS['MJD-OBS']  = self.ScanParam.DateObs

        # update main WCS keywords
        Map.computeWCS(pixelSize, sizeX, sizeY, minmaxAzEl)
        cdeltUnit = 1./3600.  # CDELTi are in arcsec
        AXIS1 = np.array([Map.WCS['NAXIS1'], Map.WCS['CRPIX1'], Map.WCS['CDELT1'],
                       Map.WCS['CRVAL1'], cdeltUnit])
        AXIS2 = np.array([Map.WCS['NAXIS2'], Map.WCS['CRPIX2'], Map.WCS['CDELT2'],
                       Map.WCS['CRVAL2'], cdeltUnit])

        self.MessHand.info("Building maps with dimensions (x,y) = "+str(int(AXIS1[0]))+','+str(int(AXIS2[0])))

        # Initialise a list of maps
        allMaps = []

        ChanRef = self.ReceiverArray.RefChannel

        rotAngles = np.zeros(self.ScanParam.NInt, np.float)
        if "NASMYTH" in self.ReceiverArray.DewCabin:
            rotAngles += -self.ScanParam.El

        # Now start a loop on channels, to build each map
        for chan in range(len(chanList)):
            mapData     = np.zeros((int(AXIS1[0]), int(AXIS2[0])), np.float32)
            mapWeight   = np.zeros((int(AXIS1[0]), int(AXIS2[0])), np.float32)
            mapCoverage = np.zeros((int(AXIS1[0]), int(AXIS2[0])), np.float32)

            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

            if dataFlag in ['', 'None']:
                dataFlagMask = np.ones(shape=self.FlagHandler.getFlags().shape, \
                                    dtype=self.FlagHandler.getFlags().dtype.char)
            else:
                if plotFlaggedData:
                    dataFlagMask = self.FlagHandler.isSetMask(dataFlag)
                else:
                    dataFlagMask = self.FlagHandler.isUnsetMask(dataFlag)

            mapData, mapWeight, mapCoverage = fMap.horizontalprojection(chanListIndexes[chan], data, \
                                                                        dataWeights, \
                                                                        dataFlagMask, 1, \
                                                                        AzElOffsets, OffsetsUsed,
                                                                        rotAngles,
                                                                        AXIS1, AXIS2,
                                                                        mapData, mapWeight, mapCoverage)
            # Storing of the map
            allMaps.append(copy.copy(mapData))

        # Store all maps in Results attribute
        self.__Results = allMaps

        labelX = "\gD Az ['']"
        labelY = "\gD El ['']"

        MultiPlot.draw(chanList, allMaps, WCS=Map.WCS,\
                       wedge=1, labelX=labelX, labelY=labelY,\
                       caption=self.ScanParam.caption(), style=style,\
                       limitsZ=limitsZ, nan=1)
        if showRms:
            cell = oversamp
            nbX = int(AXIS1[0]) - cell
            nbY = int(AXIS2[0]) - cell
            for chan in range(len(chanList)):
                oneMap = allMaps[chan]
                # Distribution of flux/beam
                m, nbOk = fStat.meandistribution(oneMap, nbX, nbY, nbX*nbY, cell)
                m = m[:nbOk]
                # clip data at more than 2-sigma (e.g. a source)
                m2, nbOk = fStat.clipping(m, rmsKappa)
                m2 = m2[:nbOk]
                oneRms = fStat.f_stat(m2)[1]
                self.MessHand.info("Channel %i : r.m.s. / beam = %f"%(chanList[chan], oneRms))

        if derotate:
            self.ReceiverArray.rotateArray(-(90-ElAverage))

    #----------------------------------------------------------------------------
    def flipOffsets(self,system='eq'):
        """change sign of telescope offsets w.r.t. reference position

        Parameters
        ----------
        system : str
            'eq' or 'ho', to flip RA/Dec offsets or Az/El

        Notes
        -----
        See TimelineData.ScanParam.flipOffsets
        """
        self.ScanParam.flipOffsets(system=system)

    #----------------------------------------------------------------------------
    def plotBoloRms(self,smoothFactor=1.5,style='idl4',limitsX=[],limitsY=[],limitsZ=[],
                    caption='',noerase=False):
        """plot the array with color scale showing rms

        Parameters
        ----------
        smoothFactor : float
            the map is smooted by this factor x beam
        style : str
            color table to use in images
        limitsX, limitsY, limitsZ : float array
            range to display in X, Y and Z
        caption : str
            plot caption
        noerase : bool
            do we erase the plot ?
        """

        chanList = self.ReceiverArray.checkChanList([])
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if not self._DataAna__statisticsDone:
            self._DataAna__statistics()

        bolo = self.ReceiverArray
        rms = self.getChanListData('rms', chanList)

        # Create a Map object to produce the plot
        mapRms = Map()
        mapRms.ReceiverArray = bolo
        nbInt  = 13
        nbBolo = bolo.NChannels
        mapRms.ScanParam.NInt = nbInt
        mapRms.ScanParam.NObs = 1
        b = bolo.BeamSize * 2. / 3600.
        mapRms.ScanParam.AzOff = np.array([0., 0., 0., 0., 0., -b, -b/2., b/2., b, b/2., -b/2., -b/2., b/2.], np.float)
        mapRms.ScanParam.ElOff = np.array([0., -b, -b/2., b/2., b, 0., 0., 0., 0., b/2., b/2., -b/2., -b/2.], np.float)
        mapRms.Data        = np.ones((nbInt, nbBolo), np.float)
        mapRms.DataWeights = np.ones((nbInt, nbBolo), np.float)
        mapRms.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros((nbInt, nbBolo), np.int8))
        mapRms.ScanParam.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros(nbInt, np.int32))
        for i in range(len(chanList)):
            mapRms.Data[:, chanList[i]-1] *= np.array(rms[i], np.float)

        mapRms.doMap(oversamp=1, noPlot=1, showRms=0)
        mapRms.Map.smoothBy(smoothFactor*bolo.BeamSize)
        # if no limitsZ input, try to compute a good one
        if limitsZ == []:
            med = fStat.f_median(rms)
            sigma = fStat.f_rms(rms, med)
            z1 = max(min(rms), med-sigma)
            z2 = max(max(rms), med+sigma)
            limitsZ = [z1, z2]
        if not caption:
            caption = bolo.FeBe + ' - channel rms'
        mapRms.Map.display(style=style, limitsX=limitsX, limitsY=limitsY,
                           limitsZ=limitsZ, caption=caption, noerase=noerase)
        bolo.plotArray(overplot=1, num=1)

    #--------------------------------------------------------------------------------
    def reduce(self,datasetName='',obstoProc=[],update=0,febe='',tau=0.):
        """Process a map scan - this method is called by the apexCalibrator

        Parameters
        ----------
        datasetName : str
            path to the dataset to be reduced
        obstoProc : list of int
            list of subscans to consider (default: all)
        update : bool
            do we update the data ReMapping object ?
        febe : str
            the Frontend-Backend name
        tau : float
            the zenith opacity

        Notes
        -----
        update is not used here...
        This is the most basic pipeline
        """

        if len(obstoProc) == 1:
            if isinstance(obstoProc[0], type([])): # e.g. obstoProc == [range(4,8)]
                self.read(inFile=datasetName, subscans=obstoProc[0], febe=febe)
            else:
                # cannot work subscan by subscan
                self.read(inFile=datasetName, subscans=range(1, obstoProc[0]+1), febe=febe)
        else:
            self.read(inFile=datasetName, subscans=obstoProc, febe=febe)

        # Automatic flagging of dead channels
        self.flagFractionRms(ratio=5.)   # flag at median(rms)/5 and median*5

        # TODO: Not how it should be !!
        # Conversion to Jy - ToDo: not so clean!
        if string.find(self.ReceiverArray.FeBe, 'LABOCA') >= 0:
            be = self.ReceiverArray.BEGain
            self.Data *= np.array(be/270. * 6.3E6, np.float)
        elif string.find(self.ReceiverArray.FeBe, 'BOLOSZ') >= 0:
            self.Data *= np.array(0.135, np.float)
        else:
            self.MessHand.warning("Unknow instrument - data not calibrated")

        if tau:
            self.correctOpacity(tau)

        # Remove correlated noise
        self.zeroStart()
        self.medianNoiseRemoval(chanRef=-1, factor=0.99, nbloop=2)
        self.medianNoiseRemoval(chanRef=-2, factor=0.99, nbloop=1)
        # Another order 1 baseline
        self.polynomialBaseline(order=1, subscan=0)
        # despiking
        self.despike(below=-3, above=10)

        # compute weight - hopefully, no too strong source!
        self.computeWeight()
        self.doMap(oversamp=2, system='EQ', noPlot=1)
        self.Map.computeRms()

        # compute good limitsZ
        pixels = np.ravel(self.Map.Data)
        pixels, nb = compressNan([pixels])
        minmax = fStat.minmax(pixels)
        minZ = max([minmax[0], -3.*self.Map.RmsBeam])

        # clip max according to weights
        maxW = fStat.minmax(np.ravel(self.Map.Weight))[1]
        minW = np.sqrt(maxW)
        if minW > maxW:
            # happens if maxW < 1.
            minW = maxW/5.
        ok = where(greater(self.Map.Weight, minW), 1, 0)
        goodmap = np.take(np.ravel(self.Map.Data), np.nonzero(np.ravel(ok)))
        goodmap, nb = compressNan([goodmap])
        maxZ = max([max(goodmap), 5.*self.Map.RmsBeam])
        self.Map.display(limitsZ=[minZ, maxZ], aspect=0, caption=self.ScanParam.caption())

        # compute rms in good weighted part, after sigma-clipping
        m2, nbOk = fStat.clipping(goodmap, 3.)
        m2 = m2[:nbOk]
        rms = fStat.f_stat(m2)[3]  # median deviation
        x0, y0 = self.Map.wcs2phy(self.Map.WCS['NAXIS1']/2., 1)
        Plot.xyout(x0, y0, str("map r.m.s. = %6.1f mJy/beam"%(1.E3*rms)), size=2)

#--------------------------------------------------------------------------------
def mapSum2(mapList):
    """
    Function (NOT a method) to co-add Image objects.
    Map data, weights and coverage planes are co-added.
    Returns a new Image object, with same WCS and data size.

    WARNING: this function assumes that all Image objects correspond
             to the same region of the sky (same size, same center)

    # Example of use:
    scans   = [some list of scan numbers]
    mapList = []  # initialise empty list
    ra1,ra2,de1,de2 = ...  # define limits to be used for all maps
    for s in scans:
        read(str(s))
        <processing of each scan>
        mapping(system='EQ',sizeX=[ra1,ra2],sizeY=[de1,de2])
        mapList.append(data.Map)
    ms = mapSum(mapList)  # co-added Image object
    ms.display()          # can be displayed
    ms.zoom()             # zoom function can be used
    ms.writeFits("output.fits")
    """

    result = copy.deepcopy(mapList[0])

    result.Data[:,:]     = 0.0
    result.Weight[:,:]   = 0.0
    result.Coverage[:,:] = 0.0

    progressBar = ProgressBar(minValue=0, maxValue=len(mapList))
    i = 0
    for iMap in mapList:

        progressBar(i)
        i = i+i

        try:
            # TODO: Do not use fixed number, test max(iMap.Data)
            mask_bad = where( (iMap.Data <= 10000000000000.), 0, 1)
            np.putmask(iMap.Data, mask_bad, 0.0)
            np.putmask(iMap.Weight, mask_bad, 0.0)

            result.Weight   += iMap.Weight
            result.Coverage += iMap.Coverage
            result.Data     += iMap.Data*iMap.Weight
        except:
            print 'map could not be added'

    result.Data = result.Data/result.Weight

    mask_bad = where((result.Weight == 0.0), 1, 0)
    np.putmask(result.Data, mask_bad, float('nan'))

    return result


#--------------------------------------------------------------------------------
def mapSum(mapList):
    """
    Function (NOT a method) to co-add Image objects.
    Map data, weights and coverage planes are co-added.
    Returns a new Image object, with same WCS and data size.

    WARNING: this function assumes that all Image objects correspond
             to the same region of the sky (same size, same center)

    # Example of use:
    scans   = [some list of scan numbers]
    mapList = []  # initialise empty list
    ra1,ra2,de1,de2 = ...  # define limits to be used for all maps
    for s in scans:
        read(str(s))
        <processing of each scan>
        mapping(system='EQ',sizeX=[ra1,ra2],sizeY=[de1,de2])
        mapList.append(data.Map)
    ms = mapSum(mapList)  # co-added Image object
    ms.display()          # can be displayed
    ms.zoom()             # zoom function can be used
    ms.writeFits("output.fits")
    """

    result = copy.deepcopy(mapList[0])

    nX = result.WCS['NAXIS1']
    nY = result.WCS['NAXIS2']

    progressBar = ProgressBar(minValue=0, maxValue=nX)
    for i in range(nX):
        progressBar(i)
        for j in range(nY):
            Pij = 0.
            Wij = 0.
            Cij = 0.
            for iMap in mapList:
                if str(iMap.Data[i, j]) != str(float('nan')):
                    Pij += iMap.Weight[i, j] * iMap.Data[i, j]
                    Wij += iMap.Weight[i, j]
                    Cij += iMap.Coverage[i, j]
            if Wij:
                result.Data[i, j] = Pij/Wij
                result.Weight[i, j] = Wij
                result.Coverage[i, j] = Cij
    print ""
    return result

#--------------------------------------------------------------------------------
def mapsumfast(mapList):
    """
    Function (NOT a method) to co-add Image objects.
    Map data, weights and coverage planes are co-added.
    Returns a new Image object, with same WCS and data size.

    WARNING: this function assumes that all Image objects correspond
             to the same region of the sky (same size, same center)

    # Example of use:
    scans   = [some list of scan numbers]
    mapList = []  # initialise empty list
    ra1,ra2,de1,de2 = ...  # define limits to be used for all maps
    for s in scans:
        read(str(s))
        <processing of each scan>
        mapping(system='EQ',sizeX=[ra1,ra2],sizeY=[de1,de2])
        mapList.append(data.Map)
    ms = mapSum(mapList)  # co-added Image object
    ms.display()          # can be displayed
    ms.zoom()             # zoom function can be used
    ms.writeFits("output.fits")
    """
    result = copy.deepcopy(mapList[0])
    if len(mapList) == 1:
        return result
    for i in range(len(mapList)-1):
        secondmap = mapList[i+1]
        newmap, newcoverage, newweight = fMap.mapsum(result.Data, result.Weight, result.Coverage,
                                                secondmap.Data, secondmap.Weight, secondmap.Coverage)
        result.Data = newmap
        result.Weight = newweight
        result.Coverage = newcoverage

    return result

#--------------------------------------------------------------------------------

def setValuesPolygon(map, poly=np.zeros((1, 2)), inout='IN', value=0.):
    """
    DES: function to replace map data inside/outside a polygon with a given value
    INP: (float array) poly : vertices of polygon
         (str)        inout : inside/outside the polygon, one of 'IN' or 'OUT'
         (float)      value : replace with this value
    OUT: (object)       map : new image object with same wcs and data size
    """
    # check polygon
    if poly.shape[1] != 2:
        self.MessHand.error("no valid polygon: wrong dimension")
        return
    if poly.shape[0] <= 2:
        self.MessHand.error("no valid polygon: not enough vertices")
        return

    # check inout
    inout = string.upper(inout)
    if inout not in ['IN', 'OUT']:
        self.MessHand.error("Inside or outside the polygon?")
        return

    result = copy.deepcopy(map)

    if inout == 'IN':
        for i in range(result.WCS['NAXIS1']):
            for j in range(result.WCS['NAXIS2']):
                x, y = result.wcs2phy(i, j)
                if inPolygon(x, y, poly):
                    result.Data[i, j] = value
    elif inout == 'OUT':
        for i in range(result.WCS['NAXIS1']):
            for j in range(result.WCS['NAXIS2']):
                x, y = result.wcs2phy(i, j)
                if outPolygon(x, y, poly):
                    result.Data[i, j] = value
    return result
