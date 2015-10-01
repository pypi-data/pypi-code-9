# Copyright (C) 2014
# Institut d'Astrophysique Spatiale
#
# Forked from the BoA project
#
# Copyright (C) 2002-2006
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
.. module:: ReaPoint
    :synopsis: contains the Rea Pointing reduction tools
"""
__version__ =  '$Revision: 2719 $'
__date__ =     '$Date: 2010-04-28 15:13:38 +0200 (mer. 28 avril 2010) $'

#----------------------------------------------------------------------------------
#----- Import ---------------------------------------------------------------------
#----------------------------------------------------------------------------------
from rea import ReaMapping
import numpy as np

import os, copy, string

from rea           import ReaConfig
from rea.Bogli     import Plot, Forms, BogliConfig
from rea.Utilities import fitBaseEllipticalGaussian, tolist_rea
from rea.Utilities import compressNan, fitGaussian, modelgaussbase
from rea.ReaError  import ReaError
from rea.fortran   import fUtilities, fMap, fStat

#----------------------------------------------------------------------------------
#----- Rea Pointing Class ----------------------------------------------------------
#----------------------------------------------------------------------------------
class Point(ReaMapping.Map):
    """.. class: Point
    :synopsis: An object of this class is responsible for the reduction of
    pointing scan(s)
    """


    def __init__(self):
        """Initialise an instance."""

        ReaMapping.Map.__init__(self)

        self.Maps = []
        self.__Result = []
        self._PointingResult = 0
        self._ArrayParamOffsets = {}

#--------------------------------------------------------------------------------
#----- public methods -----------------------------------------------------------
#--------------------------------------------------------------------------------

    def iterMap(self, chanList=[], phase=0, flag=0, sizeX=[], sizeY=[]):
        """reconstruct a map in (Az,El) coordinates combining receivers
        and using varying scale to zoom on signal

        Parameters
        ----------
        chanList : list of int
            channels to consider
        phase : int
            phase to plot
        flag  : int
            flag values to consider
        sizeX : float array
            limits in Az of the map
        sizeY : float array
            limits in El of the map
        """

        self.Maps = []  # reinitialise Maps attribute
        # start with one pixel per beam
        self.slowMap(chanList=chanList, phase=phase, flag=flag, sizeX=sizeX,\
                sizeY=sizeY, oversamp=1.)

        firstMap = self._Map__Results
        self.Maps.append(firstMap)

        # localize max. of signal
        dimX = firstMap.shape[0]
        dimY = firstMap.shape[1]

        # convert to list, to use index
        l = tolist_rea(np.ravel(firstMap))

        # remove NaN values, if any
        allNumbers = []
        for x in l:
            if str(x) != str(np.nan):
                allNumbers.append(x)

        maxi = max(allNumbers)
        mini = min(allNumbers)
        # remove the Nan in this list, otherwise index does not work
        for n in range(len(l)):
            if str(l[n]) == str(np.nan):
                l[n] = mini
        posMax = l.index(maxi)

        # convert to x,y
        maxX = int(posMax/dimY)
        maxY = posMax - dimY * maxX + 0.5
        maxX = maxX + 0.5
        # then to Az, El
        maxAz, maxEl = self.wcs2phy(maxX, maxY)
        # new limits for the second map
        newX1, newY1 = self.wcs2phy(maxX-3.5, maxY-3.5)
        newX2, newY2 = self.wcs2phy(maxX+3.5, maxY+3.5)
        Plot.plot([newX1, newX2, newX2, newX1, newX1],\
                  [newY1, newY1, newY2, newY2, newY1], style='l', overplot=1)
        self.MessHand.info(" after 1st iteration, offsets Az,El ="+str(maxAz)+","+str(maxEl))

        # second iteration:
        # compute a second map +/- 3 beams around max
        self.slowMap(chanList=chanList, phase=phase, flag=flag,\
                sizeX=[newX1, newX2], sizeY=[newY1, newY2], oversamp=3.)
        secondMap = self._Map__Results
        self.Maps.append(secondMap)
        # determine new maximum position
        dimX = secondMap.shape[0]
        dimY = secondMap.shape[1]
        # convert to list, to use index
        l = tolist_rea(np.ravel(secondMap))
        # remove NaN values, if any
        allNumbers = []
        for x in l:
            if str(x) != str(np.nan):
                allNumbers.append(x)
        maxi = max(allNumbers)
        mini = min(allNumbers)
        # remove the Nan in this list, otherwise index does not work
        for n in range(len(l)):
            if str(l[n]) == str(np.nan):
                l[n] = mini
        posMax = l.index(maxi)
        # convert to x,y
        maxX = int(posMax/dimY)
        maxY = posMax - dimY * maxX + 0.5
        maxX = maxX + 0.5
        # then to Az, El
        maxAz, maxEl = self.wcs2phy(maxX, maxY)
        # new limits for the third map
        newX1, newY1 = self.wcs2phy(maxX-3.5, maxY-3.5)
        newX2, newY2 = self.wcs2phy(maxX+3.5, maxY+3.5)
        Plot.plot([newX1, newX2, newX2, newX1, newX1],\
                  [newY1, newY1, newY2, newY2, newY1], style='l', overplot=1)
        self.MessHand.info(" after 2nd iteration, offsets Az,El ="+str(maxAz)+","+str(maxEl))

        # third iteration:
        # compute a second map +/- 3 pixels around max
        self.slowMap(chanList=chanList, phase=phase, flag=flag,\
                sizeX=[newX1, newX2], sizeY=[newY1, newY2], oversamp=5.)

        self.Maps.append(self._Map__Results)

    def solvePointing(self, chanList=[], gradient=False, circular=False, radius= -5, \
                      Xpos = 0., Ypos = 0., fixedPos = False, \
                      plot=False, display=True, caption='', style='idl4', aspect=True):
        """compute the offset on timelines

        Parameters
        ----------
        chanList : list of int
            list of channels to be used (default: all)
        gradient : bool
            shall we fit a gradient ? (default: no)
         circular : bool
            fit a cricular gaussian instead of an elliptical gaussian
        radius : float
            use only bolo inside this radius
            (negative means multiple of beam) (default 5 beams)
        Xpos, Ypos : float
            source position if using fixed position
        fixedPos : bool
            if set, don't fit position, but use Xpos, Ypos
        plot : bool
            do we plot the results? (default: no)
        display : bool
            display the result of the fit (default: yes)
        caption : str
            plot caption
        aspect : bool
            do we keep aspect ratio ?

        Notes
        -----

        the results is store in self.PoitingResult (i.e. all
        parameters as computed by mpfit routine).

        If mpfit failed, then self.PoitingResult is set to -1

        """

        # Retrieve the data..
        # The az/el off already contains the actual array offsets
        chanList = self.ReceiverArray.checkChanList(chanList)
        theData  = self.getChanListData('flux',  chanList, dataFlag=[], getFlaggedData=0)
        theWeig  = self.getChanListData('weight', chanList, dataFlag=[], getFlaggedData=0)
        offsets  = self.getChanListData('azeloff', chanList, dataFlag=[], getFlaggedData=0)

        fwhm = self.ReceiverArray.BeamSize

        # Transform that to a flat 1D array
        dataX = np.array(offsets)[:,:, 0].flatten()
        dataY = np.array(offsets)[:,:, 1].flatten()
        theData = np.array(theData).flatten()
        theWeig = np.array(theWeig).flatten()

        if radius < 0:
            radius = abs(radius)*fwhm

        if radius != 0:

            good_for_fit = np.less(np.sqrt((dataX-Xpos)**2+(dataY-Ypos)**2), radius)

            dataX   = np.compress(np.equal(good_for_fit, 1), dataX)
            dataY   = np.compress(np.equal(good_for_fit, 1), dataY)
            theData = np.compress(np.equal(good_for_fit, 1), theData)
            theWeig = np.compress(np.equal(good_for_fit, 1), theWeig)

            # fUtilities.compress crash for array > 2100000
            # dataX,n   = fUtilities.compress(dataX,good_for_fit,1)
            # dataX     = dataX[:n]
            # dataY,n   = fUtilities.compress(dataY,good_for_fit,1)
            # dataY     = dataY[:n]
            # theData,n = fUtilities.compress(theData,good_for_fit,1)
            # theData   = theData[:n]


        # now use the data to fit a 2D-Gaussian

        try:
            self._PointingResult = fitBaseEllipticalGaussian(theData, dataX, dataY,\
                                                            err = 1./np.sqrt(theWeig),\
                                                            fwhm=fwhm,\
                                                            gradient=gradient,\
                                                            circular=circular,\
                                                            Xpos=Xpos, Ypos=Ypos,\
                                                            fixedPos=fixedPos)
            self.showPointing(plot=plot, display=display,
                              caption=caption, aspect=aspect,
                              style=style)
        except ReaError as error:
            self.MessHand.warning('fit did not converge:' + error.msg)
            self._PointingResult = None
        except ValueError:
            self.MessHand.warning('fit was not possible')
            self._PointingResult = None

    def solvePointingOnMap(self, gradient=False, circular=False, radius=-10, \
                           Xpos = 0., Ypos = 0., fixedPos = False, \
                           plot=False, display=True, caption='', aspect=True, style='idl4'):
        """compute the offset on the data.Map object

        Parameters
        ----------
        gradient : bool
            shall we fit a gradient ? (default: no)
         circular : bool
            fit a cricular gaussian instead of an elliptical gaussian
        radius : float
            use only bolo inside this radius
            (negative means multiple of beam) (default 5 beams)
        Xpos, Ypos : float
            source position if using fixed position
        fixedPos : bool
            if set, don't fit position, but use Xpos, Ypos
        plot : bool
            do we plot the results? (default: no)
        display : bool
            display the result of the fit (default: yes)
        caption : str
            plot caption
        aspect : bool
            do we keep aspect ratio ?
        style : str
            the style used for the color

        Notes
        -----
        * The result of the fits is store in self.PointingResult,
        i.e. all parameters as computed by mpfit routine.

        * If mpfit failed, then self.PoitingResult is set to -1

        WARNING : No Smoothing should be applied to the map
        before using this function, or the fitted fwhm will be
        useless, use fine oversamp to make reasonable fit

        """

        if self.Map.Data == []:
            self.MessHand.error('No map computed yet')
            return

        # fit a 2D-Gaussian on the map
        try:
            self._PointingResult = self.Map.extractSource(gradient=gradient,
                                                         circular=circular,
                                                         radius=radius,
                                                         Xpos=Xpos, Ypos=Ypos,
                                                         fixedPos=fixedPos)
            self.showPointing(plot=plot, display=display, caption=caption,
                              aspect=aspect, style=style)
        except ReaError as error:
            self.MessHand.warning('fit did not converge:' + error.msg)
            self._PointingResult = None


    def showPointing(self, plot=True, display=True, noMap=False, caption='',
                     aspect=True, style='idl4', limitsZ=[], noerase=False):
        """display results of last solvePointing (in text, and on the map if plot=1)

        Parameters
        ----------
        plot : bool
            display the results on a map
        display : bool
            display the result on screen
        noMap : bool
            do not display the map
        caption : str
            caption of the plot
        aspect : bool
            do we keep aspect ratio ?
        style : str
            the style used for the color
        limitsZ : float array
            limits in amplitude for the map
        noerase : bool
            do we keep the plot ?
        """

        if not(self._PointingResult):
            self.MessHand.error('No pointing results to be displayed')
            return

        PointingResult = self._PointingResult

        if display:
            # Display out the result

            # Dictionnary to make links between keys in the pointing result
            # variable and the displayed name
            pointingDict = {'gauss_x_offset': 'Delta Az ["]',\
                            'gauss_x_fwhm'  : 'FWHM_1   ["]',\
                            'gauss_y_offset': 'Delta El ["]',\
                            'gauss_y_fwhm'  : 'FWHM_2   ["]',\
                            'gauss_tilt'    : 'Tilt   [deg]',
                            'gauss_peak'    : 'Peak flux   '}

            if self.Map.WCS['CTYPE1'].find('RA') >= 0 and self.Map.WCS['CTYPE2'].find('DEC') >= 0:
                pointingDict['gauss_x_offset'] = 'RA     [deg]'
                pointingDict['gauss_y_offset'] = 'Dec    [deg]'
                # if map is equatorial, convert FWHM to arcsec for display
                PointingResult['gauss_x_fwhm']['value'] *= 3600.
                PointingResult['gauss_y_fwhm']['value'] *= 3600.
            if self.Map.WCS['CTYPE1'].find('GLON') >= 0 and self.Map.WCS['CTYPE2'].find('GLAT') >= 0:
                pointingDict['gauss_x_offset'] = 'GLon   [deg]'
                pointingDict['gauss_y_offset'] = 'GLat   [deg]'
                # if map is in Galactic, convert FWHM to arcsec for display
                PointingResult['gauss_x_fwhm']['value'] *= 3600.
                PointingResult['gauss_y_fwhm']['value'] *= 3600.

            # Select what will be displayed from the PointingResult
            toBeOutput = ['gauss_peak',\
                          'gauss_x_offset', 'gauss_y_offset',\
                          'gauss_x_fwhm', 'gauss_y_fwhm', 'gauss_tilt']

            outStr = ""
            for item in toBeOutput:
                outStr += pointingDict[item] + " = " + \
                         str(PointingResult[item]['value'])+'\n'
            self.MessHand.info(outStr)
            if self.Map.WCS['CTYPE1'].find('RA') >= 0 and self.Map.WCS['CTYPE2'].find('DEC') >= 0:
                # convert FWHM back to deg to compute the ellipsis
                PointingResult['gauss_x_fwhm']['value'] *= 1./3600.
                PointingResult['gauss_y_fwhm']['value'] *= 1./3600.
            if self.Map.WCS['CTYPE1'].find('GLON') >= 0 and self.Map.WCS['CTYPE2'].find('GLAT') >= 0:
                PointingResult['gauss_x_fwhm']['value'] *= 1./3600.
                PointingResult['gauss_y_fwhm']['value'] *= 1./3600.

        if plot:
            # extract parameters of the ellipsis to plot
            xoff = PointingResult['gauss_x_offset']['value']
            yoff = PointingResult['gauss_y_offset']['value']
            xfwhm = PointingResult['gauss_x_fwhm']['value']
            yfwhm = PointingResult['gauss_y_fwhm']['value']
            tilt = PointingResult['gauss_tilt']['value']*np.pi/180.

            if not self.Map:
                self.doMap(style=style)
            else:
                if not noMap:
                    self.showMap(aspect=aspect, style=style, limitsZ=limitsZ,
                                 noerase=noerase, caption=caption)
            # Overlay the pointing result
            Forms.ellipse(xoff, yoff, xfwhm, yfwhm, tilt)


    def arrayParameters(self, chanList='all', gradient=0, circular=0, radius=0, plot=False, onMap=False):
        """determine the array parameters from the data

        Parameters
        ----------
        chanList : list of int
            the channel list to be used (default: current list)
        gradient : bool
            remove a background gradient in the data (default: no)
        circular : bool
            fit a cricular gaussian instead of an elliptical gaussian
        radius : float
            limit the fit to a certain range
        plot : bool
            do we plot the result ?
        onMap : bool
            do we fit maps ? (False, would make the fit on timelines)

        Notes
        -----

        * The results of the fits are stored as an associative array in self._ArrayParamOffsets,
        ie. all parameters as computed by mpfit for all channels

        * If mpfit failed then the corresponding value is set to -1


        """

        chanList = self.ReceiverArray.checkChanList(chanList)

        fwhm = self.ReceiverArray.BeamSize

        arrayParamOffsets = self._ArrayParamOffsets

        # Loop through all the channels
        for chan in chanList:
            self.MessHand.info('Fitting channel %i...'%chan)

            if plot:
                if radius:
                    sizeX = [-1.*radius, 1.*radius]
                    sizeY = sizeX
                else:
                    sizeX = []
                    sizeY = []

                self.doMap([chan], oversamp=5,\
                           sizeX=sizeX, sizeY=sizeY, \
                           aspect=1, noPlot=1, showRms=0)

            # By construction the source should be at 0,0
            if not onMap:
                self.solvePointing([chan], gradient=gradient, circular=circular, radius=radius,\
                                       plot=plot, display=False)
            else:
                self.doMap([chan], oversamp=5, noPlot=1)
                self.solvePointingOnMap(gradient=gradient, circular=circular, radius=radius,\
                                            plot=plot, display=False)


            if plot:
                if self._PointingResult:
                    diffOffX = self._PointingResult['gauss_x_offset']['value']
                    diffOffY = self._PointingResult['gauss_y_offset']['value']
                else:
                    diffOffX = 0
                    diffOffY = 0

                Plot.xyout(diffOffX, diffOffY, 'Channel '+str(chan))
                Plot.nextpage()


            if self._PointingResult:
                self.MessHand.longinfo('Offsets to RCP (%5.1f,%5.1f)"; ' % \
                                       (self._PointingResult['gauss_x_offset']['value'],\
                                        self._PointingResult['gauss_y_offset']['value']) + \
                                       'retrieved FHWM %4.1f"x%4.1f" (%5.2f)' %\
                                        (self._PointingResult['gauss_x_fwhm']['value'],\
                                         self._PointingResult['gauss_y_fwhm']['value'],\
                                         self._PointingResult['gauss_tilt']['value']))

            arrayParamOffsets[chan] = self._PointingResult

        # Normalizing gains by keeping only the good channels, change
        # fixed value to value propto beam size

        self.MessHand.longinfo('Normalizing the gains')
        fluxes = []
        for chan in arrayParamOffsets.keys():
            if arrayParamOffsets[chan] and \
                    arrayParamOffsets[chan]['gauss_x_offset']['value'] < 10 and \
                    arrayParamOffsets[chan]['gauss_y_offset']['value'] < 10 and \
                    arrayParamOffsets[chan]['gauss_x_fwhm']['value'] < 25 and \
                    arrayParamOffsets[chan]['gauss_y_fwhm']['value'] < 25:
                fluxes.append(arrayParamOffsets[chan]['gauss_peak']['value'])

        fluxes     = np.array(fluxes)
        medianFlux = fStat.f_median(fluxes)

        for chan in arrayParamOffsets.keys():
            if arrayParamOffsets[chan]:
                arrayParamOffsets[chan]['gain'] = arrayParamOffsets[chan]['gauss_peak']['value']/medianFlux

        self._ArrayParamOffsets = arrayParamOffsets
        self.MessHand.longinfo('You can now use the ReaPointing.updateArrayParameters method')


    def updateArrayParameters(self):
        """Update the Parameters Offsets with the computed values

        Notes
        -----
        leave the reference chan position unchanged
        """

        arrayParamOffsets = self._ArrayParamOffsets
        offsets = copy.copy(self.ReceiverArray.Offsets)
        refChan = self.ReceiverArray.RefChannel
        gains   = self.ReceiverArray.Gain
        fwhm    = self.ReceiverArray.FWHM
        tilt    = self.ReceiverArray.Tilt

        if fwhm.size == 0:
            nc = self.ReceiverArray.NChannels
            tilt = np.zeros(nc, np.float32)
            fwhm = np.zeros((2, nc), np.float32)

        # find the reference offset
        if refChan in arrayParamOffsets.keys():
            refOffset = np.array([arrayParamOffsets[refChan]['gauss_x_offset']['value'],\
                               arrayParamOffsets[refChan]['gauss_y_offset']['value']])
        else:
            self.MessHand.warning('Reference Offsets not found in fit')
            refOffset = np.array([0, 0])

        for chan in arrayParamOffsets.keys():
            chanIndex = self.ReceiverArray.getChanIndex(chan)
            if not chanIndex in [-1] and arrayParamOffsets[chan]:
                thisOffset = np.array([arrayParamOffsets[chan]['gauss_x_offset']['value'],\
                                    arrayParamOffsets[chan]['gauss_y_offset']['value']])

                offsets[:, chanIndex] = ( offsets[:, chanIndex] - \
                                             np.array([(thisOffset-refOffset)]).transpose().astype(np.float32))

                gains[chanIndex] = arrayParamOffsets[chan]['gain']
                fwhm[:, chanIndex] = np.array([[arrayParamOffsets[chan]['gauss_x_fwhm']['value'], \
                                                arrayParamOffsets[chan]['gauss_y_fwhm']['value']]]).transpose().astype(np.float32)
                tilt[chanIndex]   = arrayParamOffsets[chan]['gauss_tilt']['value']
            else:
                self.MessHand.warning('Channel %s not valid or no good fit'%str(chan))

        self.ReceiverArray.Offsets = offsets
        self.ReceiverArray.Gain    = gains
        self.ReceiverArray.FWHM    = fwhm
        self.ReceiverArray.Tilt    = tilt

    #---------------------------------------------------------------------------------
    def reduce(self, datasetName='', obstoProc=[], febe='', baseband=1,
               radius=-2., update=False, tau=0.):
        """Process a Pointing scan - this method is called by the apexCalibrator

        Parameters
        ----------
        datasetName : str
            path to the dataset to be reduced
        obstoProc : list of int
            list of subscans to consider (default: all)
        febe : str
            frontend-backend to consider
        baseband : int
            which baseband do we reduce ?
        radius : float
            radius to be used for fitting (def: 2xbeam)
        update : bool
            continue previous scan? (def: no)
        tau : float
            zenithal opacity to apply
        """
        if len(obstoProc) == 1:
            if isinstance(obstoProc[0], type([])): # e.g. obstoProc == [range(4,8)]
                self.read(inFile=datasetName, subscans=obstoProc[0],
                          febe=febe, readAzEl0=1, baseband=baseband)
            else:
                # cannot work subscan by subscan
                self.read(inFile=datasetName, subscans=range(1, obstoProc[0]+1),
                          febe=febe, readAzEl0=1, baseband=baseband)
        else:
            self.read(inFile=datasetName, subscans=obstoProc,
                      febe=febe, readAzEl0=1, baseband=baseband)

        # If chopped data, then compute phase diff
        if self.ScanParam.WobUsed:
            self.ScanParam.computeOnOff()
            self._phaseDiff()

        if string.upper(self.ScanParam.Object) != "JUPITER" and \
               string.upper(self.ScanParam.Object) != "MARS" and \
               string.upper(self.ScanParam.Object) != "SATURN":
            self.flagFractionRms(ratio=10)
        self.medianBaseline()
        self.flatfield()

        # TODO: This is WRONG
        # Conversion to Jy - ToDo: not so clean!
        if string.find(self.ReceiverArray.FeBe, 'LABOCA') >= 0:
            be = self.ReceiverArray.BEGain
            self.Data *= np.array(be/270. * 6.3E6, np.float)
        elif string.find(self.ReceiverArray.FeBe, 'BOLOSZ') >= 0:
            self.Data *= np.array(0.135, np.float)
        else:
            self.MessHand.warning("Unknown instrument - data not calibrated")

        if tau:
            self.correctOpacity(tau)

        Plot.panels(2, 2)
        Plot.nextpage()  # start a new page
        # First plot = signal before skynoise removal
        four = self.ReceiverArray.fourpixels()
        self.signal(four, noerase=1, caption=self.ScanParam.caption()+' - Raw signal')

        # Now clean up the signal
        beam = self.ReceiverArray.BeamSize
        if string.upper(self.ScanParam.Object) == "JUPITER":
            self.flagPosition(radius=3.*beam, flag=8)
            self.flagFractionRms(ratio=10)
        else:
            self.flagPosition(radius=2.*beam, flag=8)
            self.flagFractionRms(ratio=5)
        self.medianNoiseRemoval(chanRef=-1, factor=0.95, nbloop=5)
        # Repeat median noise splitting channels in 4 groups
        # (corresponds to amplifier boxes for LABOCA)
        nb_all = self.ReceiverArray.NChannels
        if nb_all > 12:  # at least 3 bolo per group
            self.medianNoiseRemoval(range(int(nb_all/4)+1),
                                    chanRef=-1, factor=0.98, nbloop=2)
            self.medianNoiseRemoval(range(int(nb_all/4)+1, 2*int(nb_all/4)+1),
                                    chanRef=-1, factor=0.98, nbloop=2)
            self.medianNoiseRemoval(range(2*int(nb_all/4)+1, 3*int(nb_all/4)+1),
                                    chanRef=-1, factor=0.98, nbloop=2)
            self.medianNoiseRemoval(range(3*int(nb_all/4)+1, nb_all+1),
                                    chanRef=-1, factor=0.98, nbloop=2)
        self.polynomialBaseline(order=1, subscan=0)
        if string.upper(self.ScanParam.Object) == "JUPITER":
            self.flagFractionRms(ratio=10)
        else:
            self.flagFractionRms(ratio=5)

        self.despike(below=-3, above=5)
        self.computeWeight()
        self.unflag(flag=8)
        Plot.nextpage()
        four = self.ReceiverArray.fourpixels()
        self.signal(four, noerase=1, caption='Skynoise subtracted')

        # Now compute the map and solve for pointing
        self.doMap(oversamp=3., noPlot=1,
                   sizeX=[-10.*beam, 10.*beam], sizeY=[-10.*beam, 10.*beam])
        self.Map.computeRms()
        self.solvePointingOnMap(radius=radius, plot=0, display=0)
        Plot.nextpage()
        # compute good Z limits
        pixels = np.ravel(self.Map.Data)
        pixels, nb = compressNan([pixels])
        minmax = fStat.minmax(pixels)
        minZ = max([minmax[0], -3.*self.Map.RmsBeam])
        if self._PointingResult :
            peak = self._PointingResult['gauss_peak']['value']
            if peak > 3.*self.Map.RmsBeam:
                maxZ = peak
            else:
                maxZ = minmax[1]
        else:
            maxZ = minmax[1]
        if self._PointingResult :
            self.showPointing(noerase=1, limitsZ=[minZ, maxZ], caption=' ')
            offX = self._PointingResult['gauss_x_offset']['value']
            offY = self._PointingResult['gauss_y_offset']['value']
            fwX  = self._PointingResult['gauss_x_fwhm']['value']
            fwY  = self._PointingResult['gauss_y_fwhm']['value']
            Plot.xyout(0, 8.5*beam, str("peak = %6.1f Jy/beam"%(peak)), size=2.)
            Plot.xyout(0, -8.*beam, str("FWHM = %4.1f x %4.1f"%(fwX, fwY)), size=2.)
            Plot.xyout(0, -9.5*beam, str("x=%5.1f ; y=%5.1f"%(offX, offY)), size=2.)
        else:
            # when pointing failed, display only the map
            self.Map.display(noerase=1, limitsZ=[minZ, maxZ], caption=' ')
            Plot.xyout(0, -9.5*beam, "no fit", size=2.5)
        Plot.nextpage()

        # Finally show the RMS of all bolos, and compute median NEFD
        # but flag the source first
        if self._PointingResult != -1:
            if peak > 3.*self.Map.RmsBeam:
                self.flagPosition(Az = offX, El = offY, radius = max([fwX, fwY]))
        self.plotBoloRms(noerase=1)
        rms = self.getChanListData('rms')
        medrms = fStat.f_median(rms)
        sampl = fStat.f_median(1./self.ScanParam.get('deltat'))
        nefd = medrms / np.sqrt(sampl)
        Plot.xyout(0, 1.05*max(self.ReceiverArray.Offsets[1,:]),
                   str("NEFD = %5.1f mJy/sqrt(Hz)"%(nefd*1.E3)), size=1.5)
        Plot.panels(1, 1)

    #---------------------------------------------------------------------------------
    def reduceCross(self,datasetName='',obstoProc=[],febe='',baseband=1,update=False):
        """Process a Pointing scan observed with cross-OTF

        Parameters
        ----------
        datasetName : str
            path to the dataset to be reduced
        obstoProc : list of int
            list of subscans to consider (default: all)
        febe : str
            frontend-backend to consider
        baseband : int
            which baseband do we reduce ?
        update : bool
            continue previous scan? (def: no)
        """
        if len(obstoProc) == 1:
            if isinstance(obstoProc[0], type([])): # e.g. obstoProc == [range(4,8)]
                self.read(inFile=datasetName, subscans=obstoProc[0],
                          febe=febe, readAzEl0=1, baseband=baseband)
            else:
                # cannot work subscan by subscan
                self.read(inFile=datasetName, subscans=range(1, obstoProc[0]+1),
                          febe=febe, readAzEl0=1, baseband=baseband)
        else:
            self.read(inFile=datasetName, subscans=obstoProc,
                      febe=febe, readAzEl0=1, baseband=baseband)

        # First, subtract zero order baseline and average noise
        self.medianBaseline(subscan=0)

        # Plot signal before subtracting correlated noise
        Plot.panels(2, 2)
        Plot.nextpage()  # start a new page
        four = self.ReceiverArray.fourpixels()
        self.signal(four, noerase=1, caption=self.ScanParam.caption()+' - Raw signal')

        # If chopped data, then compute phase diff
        if self.ScanParam.WobUsed:
            self.ScanParam.computeOnOff()
            self._phaseDiff()

        self.medianBaseline(subscan=0)
        ref = self.ReceiverArray.RefChannel
        self.averageNoiseRemoval(chanRef=ref)

        self.despike(below=-5)  # flag negative, if any
        Plot.nextpage()  # start a new page
        self.signal(four, noerase=1, caption='Phase diffed, average noise subtracted')

        # We will store Az and El offsets based on subscans
        offAz, fluxAz = np.array([], np.float), np.array([], np.float)
        offEl, fluxEl = np.array([], np.float), np.array([], np.float)
        for i in range(len(self.ScanParam.SubscanNum)):
            subNum = self.ScanParam.SubscanNum[i]
            tmpAz = self.getChanData('azoff', ref, subscans=[subNum])
            tmpEl = self.getChanData('eloff', ref, subscans=[subNum])
            tmpFlux = self.getChanData('flux', ref, subscans=[subNum])
            # Update Az or El data, depending on SCANDIR
            if string.find(self.ScanParam.ScanDir[i], 'LON') > -1:
                self.MessHand.info("Subscan %i in Az direction"%(subNum))
                offAz = np.concatenate((offAz, tmpAz))
                fluxAz = np.concatenate((fluxAz, tmpFlux))
            elif string.find(self.ScanParam.ScanDir[i], 'LAT') > -1:
                self.MessHand.info("Subscan %i in El direction"%(subNum))
                offEl = np.concatenate((offEl, tmpEl))
                fluxEl = np.concatenate((fluxEl, tmpFlux))
            else:
                self.MessHand.warning("Subscan %i in undefined direction, skipping..."%(subNum))

        fwhm2sigma = 1./(2*np.sqrt(2*np.log(2)))

        if len(offAz):
            err = ones(offAz.shape)
            Plot.nextpage()
            Plot.pointSize(5)
            Plot.plot(offAz, fluxAz, noerase=1, style='l', width=1,
                      labelX='Az offset [arcsec]', labelY='Flux [arb. u.]')
            Plot.plot(offAz, fluxAz, overplot=1, style='p')
            m = fitGaussian(offAz, fluxAz, err, const=1)
            if m.status >= 0:
                resAz = m.params[1]
                ampAz = m.params[0]
                widAz = m.params[2] / fwhm2sigma
                xx = min(offAz) + arange(101)*(max(offAz)-min(offAz))/100.
                yy = modelgaussbase(m.params, xx)
                Plot.plot(xx, yy, overplot=1, ci=2, style='l', width=3)
                Plot.plot([resAz, resAz], [0, m.params[0]], overplot=1, style='l', width=5, ci=3)
                Plot.xyout(resAz, 0., "%5.1f"%(resAz), size=2.5)
                y0 = min(fluxAz) + 0.9*(max(fluxAz)-min(fluxAz))
                Plot.xyout(xx[5], y0, "Az", size=4)
            else:
                resAz, ampAz, widAz = -999, 0, 0
        else:
            resAz, ampAz, widAz = -999, 0, 0

        if len(offEl):
            err = ones(offEl.shape)
            Plot.nextpage()
            Plot.pointSize(5)
            Plot.plot(offEl, fluxEl, noerase=1, style='l', width=1,
                      labelX='El offset [arcsec]', labelY='Flux [arb. u.]')
            Plot.plot(offEl, fluxEl, overplot=1, style='p')
            m = fitGaussian(offEl, fluxEl, err, const=1)
            if m.status >= 0:
                resEl = m.params[1]
                ampEl = m.params[0]
                widEl = m.params[2] / fwhm2sigma
                xx = min(offEl) + arange(101)*(max(offEl)-min(offEl))/100.
                yy = modelgaussbase(m.params, xx)
                Plot.plot(xx, yy, overplot=1, ci=2, style='l', width=3)
                Plot.plot([resEl, resEl], [0, m.params[0]], overplot=1, style='l', width=5, ci=3)
                Plot.xyout(resEl, 0., "%5.1f"%(resEl), size=2.5)
                y0 = min(fluxEl) + 0.9*(max(fluxEl)-min(fluxEl))
                Plot.xyout(xx[95], y0, "El", size=4)
            else:
                resEl, ampEl, widEl = -999, 0, 0
        else:
            resEl, ampEl, widEl = -999, 0, 0

        Plot.panels(1, 1)

        # Store results in self.PointingResult
        result = {'gauss_x_offset':resAz,'gauss_y_offset':resEl,
                  'width_x':widAz,'width_y':widEl,
                  'ampl_x':ampAz,'ampl_y':ampEl}
        self.PointingResult = result


    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    def writeModelData(self, filename='LABOCA-ABBA.dat'):
        """generate one line to be written in the .dat file used for
        determining pointing model.

        Parameters
        ----------
        filename : str
            the filename to update

        Notes
        -----
        LABOCA Specific : This will work only if data have been read
        in with readAzEl0 = 1 and after the pointing has been reduced

        """

        param = self.ScanParam
        # we need to find the 1st timestamp that is not flagged
        i0 = 0
        while param.FlagHandler.isSetOnIndex(i0):
            i0 += 1
        sourceAz = param.AntAz0 - param.AzOff[i0]
        sourceEl = param.AntEl0 - param.ElOff[i0]
        encodAz  = param.EncAz0 - param.AzOff[i0]
        encodEl  = param.EncEl0 - param.ElOff[i0]
        PCA      = param.PDeltaCA
        PIE      = param.PDeltaIE
        FCA      = param.FDeltaCA
        FIE      = param.FDeltaIE
        scan     = param.ScanNum
        cCA      = self._PointingResult ['gauss_x_offset']['value'] / 3600.
        cIE      = self._PointingResult ['gauss_y_offset']['value'] / 3600.
        datLine = '%.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %i\n' % \
                  (sourceAz, sourceEl, encodAz, encodEl,
                   cCA, cIE, PCA, PIE, FCA, FIE, scan)
        output = file(filename, 'a')
        output.write(datLine)
        output.close
