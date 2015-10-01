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
.. module: ReaDataAnalyser.py
   :synopsis: contains Rea channel analyser class
"""

__version__ =  '$Revision: 2718 $'
__date__ =     '$Date: 2010-04-21 18:53:14 +0200 (mer. 21 avril 2010) $'


# TODO Gain should be removed here

#----------------------------------------------------------------------------------
#----- Import ---------------------------------------------------------------------
#----------------------------------------------------------------------------------
import time, os, copy
import numpy as np

from rea.Bogli     import Plot, MultiPlot, Forms, DeviceHandler, BogliConfig
from rea.fortran   import fStat, fSNF, fUtilities, fFlag, fBaseline, fMap, fWavelets
from rea.Utilities import Timing, Cr2p, Cp2r, principalComponentAnalysis
from rea.Utilities import compressNan, tolist_rea, inPolygon, outPolygon
from rea.Utilities import as_column_major_storage

from rea import ReaDataEntity, ReaFlagHandler, ReaConfig


#----------------------------------------------------------------------------------
#----- FFT related function  ------------------------------------------------------
#----------------------------------------------------------------------------------
def applyWindow(inData, window=4, undo=False):
    """Utility to apply a window function to a chunk of data

    Parameters
    ----------
    inData : float array
        the data to apply the function to
    window : int
        the type window function to apply
              1 - Barlett; 2 - Welch ; 3 - Hanning ; 4 - Hamming (default);
              5 - Blackman; 6 - flat-top
    undo : bool
        if set, un-apply the window function

    Returns
    -------
    float array
        the resulting array (same size as input)
    """

    meanY = fStat.f_mean(inData)
    N = len(inData)

    # w = np.arange(N, typecode=np.float32)/(N-1)*N
    w = np.arange(N, dtype=np.float32)

    if window == 1:    # Barlett (0 ended)
        w = 1.0 - abs((w-N*1/2)/(N*1/2))
    elif window == 2:  # Welch (0 ended)
        w = 1.0 - ((w-N*1/2)/(N*1/2))**2
    elif window == 3:  # Hanning (0 ended)
        alpha = 0.5
        w = alpha - (1-alpha)*np.cos(2*np.pi*w/N)
    elif window == 4:  # Hamming
        alpha = 0.53836
        w = alpha - (1-alpha)*np.cos(2*np.pi*w/N)
    elif window == 5:  # Blackman
        w = 0.42-0.5*np.cos(2*np.pi*w/N)-0.008*np.cos(4*np.pi*w/N)
    elif window == 6:  # flat-top
        w = 1.0 - 1.933*np.cos(2*np.pi*w/N) + 1.286*np.cos(4*np.pi*w/N) - \
            0.388*np.cos(6*np.pi*w/N) + 0.0322*np.cos(8*np.pi*w/N)
    else:
        return

    # Compute the amplitude correction factor
    # corr = fStat.f_mean(w)
    corr = np.sqrt(np.sum(w**2)/N)

    if undo:
        if w[0] == 0 or w[-1] == 0 :
            result = 0.*inData
            # exclude 1st and last elements to avoid division by zero
            # result[1:-1] = (inData[1:-1]-meanY)/w[1:-1]*corr + meanY
            result[1:-1] = inData[1:-1] / w[1:-1] * corr
        else:
            # result = (inData-meanY)/w*corr+meanY
            result = inData / w * corr
    else:
        # result = (inData-meanY)*w/corr+meanY
        result = inData * w / corr

    return result

#----------------------------------------------------------------------------------
#----- FilterFFT class ------------------------------------------------------------
#----------------------------------------------------------------------------------
class FilterFFT:
    """..class:: FilterFFT
    :synopsis: To easily do FFT filtering

    Notes
    -----
    make the assumption that the input signal is real, so do not
         care about negative frequencies...
    """

    # from rea.Bogli import Plot

    def __init__(self, X, Y):

        # Starting values
        self.X         = np.array(X)
        self.Y         = np.array(Y)

        # Flag on the timing precision
        self.Timing    = 0
        self.SamplFreq = 0
        self.__checkTiming()
        self.Timing    = 1

        # ALl the computation will be done on the following data
        self.OutX = np.array(X)
        self.OutY = np.array(Y)

        # the number of point used for the FFT
        self.N         = 0

        # Result of the FFT
        self.Freq      = 0.0
        self.Amplitude = 0.0
        self.Phase     = 0.0
        self.Power     = 0.0

        # This will contain the datagram when computed
        self.DataGram  = None

    # -----------------------------------------------------------------------------
    def __checkTiming(self):
        """check if time sampling is precise enough to allow FFTs"""

        X = self.X
        Y = self.Y

        dX = X[1:]-X[:-1]
        nu = 1./dX
        # use median value (should be most frequent one)
        med = fStat.f_median(nu)
        # compute rms relative to this median
        # diff = nu - med
        # mean = fStat.f_mean(diff)
        rms  = fStat.f_rms(nu, med)

        # Sampling frequency and error
        f  = med
        df = rms

        # store the sampling Frequency
        self.SamplFreq = f

        # relative error "should" be below 0.1 per cent
        self.Timing = df/f*100 < 0.1


    # -----------------------------------------------------------------------------
    def __interpolate(self, step=0):
        """linear interpolation of the data to get a regulary gridded dataset

        Parameters
        ----------
        step : float
            force the step (default : median)
        """

        X = self.X
        Y = self.Y
        nData = len(X)

        if not step:
            step = 1./self.SamplFreq

        # let OutX be a little longer than X so that there is
        # no more a 'last point problem' when doing an invFFT

        outX = np.arange(X[0], X[-1]+step, step)
        outY = np.interp(outX, X, Y)

        self.OutX  = outX
        self.OutY  = outY

        self.Timing = 1

    # -----------------------------------------------------------------------------
    def __uninterpolate(self):
        """Rebin the data to the initial grid"""

        X         = self.X
        outX      = self.OutX
        outY      = self.OutY
        # self.OutY = (np.interp(outY,outX,X)).astype(np.float32)
        self.Y    = (np.interp(X, outX, outY)).astype(np.float32)

    # -----------------------------------------------------------------------------
    def doFFT(self, interpolate=False, windowing=4, windowSize=0, Xstart=0, Xend=0):
        """perform all the necessary steps to do a forward FFT

        Parameters
        ----------
        interpolate : bool
            force an interpolation to be done (default no : check of timing quality better than 0.1 %)
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        windowSize  : int
            length of chunks to compute FFT on and to average
                                (default: 0 = compute on the entire data serie)
        Xstart, Xend : int
            optional indices for using only part of the data
        """

        if not self.Timing or interpolate:
            self.__interpolate()

        if windowSize:
            fullSize = len(self.OutY)
            # Check that we have enough data points
            if fullSize >= windowSize:
                startPoint = 0
                endPoint   = windowSize
                nbChunk = 0
                while(endPoint <= fullSize):
                    self.doFFT(interpolate=interpolate, windowing=windowing, windowSize=0,\
                               Xstart = startPoint, Xend = endPoint)
                    if startPoint == 0:
                        chunkAmp = self.Amplitude
                        chunkPha = self.Phase
                    else:
                        chunkAmp = chunkAmp + self.Amplitude
                        chunkPha = chunkPha + self.Phase
                    startPoint += windowSize/2
                    endPoint    = startPoint + windowSize
                    nbChunk    += 1

                # Average the results by chunk
                self.Amplitude = chunkAmp / float(nbChunk)
                self.Phase     = chunkPha / float(nbChunk)
                # self.Freq already contains the correct Freq array
            else:
                self.doFFT(interpolate=interpolate, windowing=windowing, windowSize=0,\
                           Xstart = Xstart, Xend = Xend)

        else:
            self.__forwardFFT(windowing=windowing, Xstart = Xstart, Xend = Xend)

    # -----------------------------------------------------------------------------
    def invFFT(self, windowing=4):
        """perform all the necessary steps to do a backward FFT

        Parameters
        ----------
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        """

        self.__backwardFFT()
        if windowing:
            self.OutY = applyWindow(self.OutY, window=windowing, undo=1)
        # self.__uninterpolate()
        self.Y = self.OutY[:len(self.X)]

    # -----------------------------------------------------------------------------
    def doDataGram(self, interpolate=False, n=1024, windowing=4):
        """Compute the Datagram of the data

        Parameters
        ----------
        interpolate : bool
            force an interpolation to be done (default no : check of timing quality better then  0.1 %)
        n : int
            Number of points for the ffts
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        """

        if not self.Timing or interpolate:
            self.__interpolate()
        self.__computeDataGram(n=n, windowing=windowing)

    # -----------------------------------------------------------------------------
    def __computeDataGram(self, n=1024, windowing=4):
        """Compute the Datagram of the data

        Parameters
        ----------
        n : int
            number of points for the ffts
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)        """

        # Define the highest power of 2 containing the data
        nData = len(self.OutX)
        # higher power of 2 closer to n to perform the ffts
        N = 2**(int(np.ceil(np.log(n)/np.log(2))))

        # Number of frequency values
        midPoint = int(N/2+1)
        DataGram = np.zeros((nData-n, midPoint), np.float32)

        for index in xrange(0, nData-n):
            self.__forwardFFT(optimize=1, windowing=windowing, Xstart=index, Xend=index+n)
            DataGram[index,:] = (np.sqrt(self.Power)).astype(np.float32)

        self.DataGram = DataGram

    # -----------------------------------------------------------------------------
    def __forwardFFT(self,optimize=True, windowing=4, Xstart=0, Xend=0):
        """perform the FFT

        Parameters
        ----------
        optimize : bool
            False will use the full data set
            True will zero-pad the data till next power of 2 (default)
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        Xstart, Xend : int
            optional indices for using only part of the data
        """

        if Xend:
            X = self.OutX[Xstart:Xend]
            Y = self.OutY[Xstart:Xend]
        else:
            X = self.OutX[Xstart:]
            Y = self.OutY[Xstart:]

        if windowing:
            Y = applyWindow(Y, window=windowing)

        # Define the highest power of 2 containing the data
        nData = len(X)

        if optimize:
            N = 2**(int(np.ceil(np.log(nData)/np.log(2))))
        else:
            N = nData

        # Save the number of point used for the FFT
        self.N = N

        # Sampling frequency
        midPoint = int(N/2+1)
        samplFreq = self.SamplFreq
        freq = np.arange(midPoint, dtype=np.float32)*samplFreq/N

        # Do the FFT
        ff   = np.fft.rfft(Y, n=N)

        # In case we need to switch back to complex ffts...
        # Shift to have negative frequencies first
        # ff = concatenate([ff[midPoint:],ff[:midPoint]])
        # u = (np.arange(N,typecode='float')-(midPoint-2))*f/N

        amp, phase = Cr2p(ff)

        # Normalization of the amplitude
        self.Amplitude = amp * np.sqrt(2.) / float(nData)
        self.Phase     = phase
        self.Freq      = freq
        # PSD: sqrt(self.Power) will be rms/SQRT(Hz)
        self.Power     = self.Amplitude**2 / (samplFreq/N)  # Power density

    # -----------------------------------------------------------------------------
    # compute the inverse FFT
    def __backwardFFT(self):
        """perform the inverse FFT"""

        amp       = self.Amplitude
        phase     = self.Phase
        samplFreq = self.SamplFreq
        outX      = self.OutX
        N         = self.N

        # Remove the normalization of amplitude
        # amp     = amp / sqrt(2/samplFreq/N)
        amp     = amp / np.sqrt(2.) * np.float(len(self.X))

        ff = Cp2r(amp, phase)
        outY = np.fft.irfft(ff, n=N)
        self.OutY = outY[:len(outX)]

    # -----------------------------------------------------------------------------
    def plotFFT(self,plotPhase=False, \
               labelX='Frequency [Hz]', labelY='Amplitude (a.b.u/sqrt(Hz)', \
               limitsX=[],limitsY=[],logX=True, logY=True, overplot=False, ci=1, \
               returnSpectrum=False):
        """Plot the fft

        Parameters
        ----------
        plotPhase : bool
            plot phase instead of amplitude (default no)
        labelX, labelY  : str
            the X/Y label
        limitsX, limitsY : 2 float array
            the plot limits for X/Y
        logX, logY : bool
            do we plot the axis in log ?
        overplot : bool
            do we overplot ?
        ci : int
            color index
        returnSpectrum : bool
            return the values of freq. and amplitude?

        Returns
        -------
        tuple of 1d float array
           the freq and amplitude of the spectrum
        """

        X = self.Freq
        Y = self.Amplitude
        if plotPhase:
            Y = self.Phase
            labelY = 'Phase'
            logY = 0

        if logX:
            X = X[1:]
            Y = Y[1:]

        Plot.plot(X, Y, \
                  labelX=labelX, labelY=labelY, \
                  limitsX=limitsX, limitsY=limitsY, \
                  logX = logX, logY = logY, \
                  overplot=overplot, style='l', ci=ci)

        if returnSpectrum:
            return(X, Y)

    # -----------------------------------------------------------------------------
    def plotDataGram(self, interpolate=False, n=1024, windowing=4,limitsZ=[]):
        """Plot the Datagram of the Data

        Parameters
        ----------
        interpolate : bool
            force an interpolation to be done (default no : check of timing quality better then  0.1 %)
        n : int
            Number of points for the ffts
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        limitsZ : 2 float array
            limits in color range
        """

        if not self.DataGram:
            self.doDataGram(interpolate=interpolate, n=n, windowing=windowing)
        DataGram  = self.DataGram
        freq      = self.Freq
        X         = self.X

        Plot.draw(DataGram, style='idl4', sizeX=[X[0], X[-n]], sizeY=[min(freq), max(freq)], \
                  labelX="Time [s]", labelY="Frequency [Hz]", \
                  limitsZ=limitsZ, wedge=1, caption='sqrt(PSD) [rms/sqrt(Hz)]')


    # -----------------------------------------------------------------------------
    def blankAmplitude(self, below='?', above='?'):
        """blank the amplitude below and/or after a certain frequency

        Parameters
        ----------
        below : float
           blank below this frequency
        above : float
           blank above this frequency

        """

        frequency = self.Freq
        amplitude = self.Amplitude

        if above == '?':
            above = min(frequency)
        if below == '?':
            below = max(frequency)

        mask = np.nonzero(np.where(np.bitwise_and(frequency >= above, frequency <= below), 1, 0))

        if mask[0] > 0 and mask[-1] < len(amplitude)-1:
            value = (amplitude[mask[0]-1] + amplitude[mask[-1]+1]) / 2.
        else:
            value = min(amplitude)

        if len(mask) > 0:
            np.put(amplitude, mask, (value))

        self.Amplitude = amplitude

    # -----------------------------------------------------------------------------
    def taperAmplitude(self, above='?', N=2):
        """Butterworth taper the amplitude above a certain frequency

        Parameters
        ----------
        above : float
            frequency above which to taper
        N : int
            steepness parameter
        """

        frequency = self.Freq
        amplitude = self.Amplitude

        if above == '?':
            above = min(frequency)

        amplitude = amplitude / np.sqrt((1.+(frequency/above)**(2*N)))

        self.Amplitude = amplitude

    # -----------------------------------------------------------------------------
    def reduceAmplitude(self, center=50., width=1., factor=10., dB=False):
        """multiply the Fourrier spectrum with a gaussian filter function

        Parameters
        ----------
        center : float
            central frequency, in Hz
        width : float
            window FWHM
        factor : float
            attenuation factor
        dB : bool
            is factor expressed in dB? (default: no)
        """
        frequency = self.Freq
        amplitude = self.Amplitude

        # generate the filter function, sampled at 0.1 Hz
        c    = width / (2.*np.sqrt(np.log(2.)))  # convert FWHM
        gaus = exp(-1.*(frequency - center)**2 / c**2)
        filt = 1./(1.+(factor-1.)*gaus)
        # Plot.plot(frequency,self.Amplitude,logY=1)
        self.Amplitude = self.Amplitude * filt
        # Plot.plot(frequency,self.Amplitude,overplot=1,ci=2,style='l')
        # raw_input()

#----------------------------------------------------------------------------------
#----- Rea Channel Analyser -------------------------------------------------------
#----------------------------------------------------------------------------------

class DataAna(ReaDataEntity.TimelineData):
    """..class:: DataAna

    :synopsis: An object of this class is responsible for the flagging
        of individual channels. It provides methods to derive the rms of
        each channel and to automatically search for bad or noisy
        channels. Channels might be flagged according to a given input
        file. This object provides methods to derive the correlation
        matrix. Several methods can be used to remove skynoise

    """

    def __init__(self):
        """initialise an instance"""

        ReaDataEntity.TimelineData.__init__(self)

        # float and integer parameter attributes:
        self.__statisticsDone = False     # (logical) are statistics up-to-date?
        self.__corMatrixDone  = False     # (logical) is correlation Matrix up-to-date ?
        self.__pcaDone        = False     # (logical) is PCA up-to-date ?

        self.CorrelatedNoise    = np.array([], np.float32)   # The associated noise array
        self.CorMatrix   = np.array([], np.float32)          # Correlation Matrix
        self.FFCF_CN     = np.array([], np.float32)          # flat field correction factor (Correlated Noise)
        self.FFCF_Gain   = np.array([], np.float32)          # flat field correction factor (Gains)
        self.FF_Median   = np.array([], np.float32)          # median flat field

        self.__pca_eigenvalues = np.array([], np.float32)    # The remaining eigenvalues after PCA filtering
        self.__pca_eigenvectors = np.array([], np.float32)    # and corresponding eigenvectors

    def _coadd(self, other):
        ReaDataEntity.TimelineData._coadd(self, other)
        self.__resetStatistics()

    #--------------------------------------------------------------------------------
    #----- Reading: TimelineData.read + auto-flagging  --------------------------------
    #--------------------------------------------------------------------------------
    def read(self,inFile='',febe='',baseband=0,subscans=[],update=0,phase=0, \
             channelFlag=1, integrationFlag=9, \
             blanking=True, \
             readHe=False,readAzEl0=False,
             readT=False,readWind=False,readBias=False,
             readPWV=False):
        """fill a Rea data object from an MB-FITS file

        Parameters
        ----------
        inFile : str
            path to the dataset to be read
        febe : str
            FE-BE name to select
        baseband : int
            baseband to select
        subscans : list of int
            subscan numbers to read (default: all)
        update : bool
            if true, do not reset previous entity object
        phase : int
            phase to be stored (default: phase diff)
        blanking : bool
            automatic flagging of blanked data (default: yes)
        channelFlag : list of int
            flag for not connected feeds (default: 1 'NOT CONNECTED')
        integrationFlag : list of int
            flag for blanked integrations (default: 9 'BLANK DATA')
        readHe : bool
            do we need the He3 temparatures? (default: no)
        readAzEl0 : bool
            do we read monitor Az,El at start? (default: no)
        readT : bool
            do we read T_amb from monitor? (def: no)
        readWind : bool
            do we read wind speed, dir... (def: no)
        readPWV : bool
            do we read pwv? (def: no)
        readBias : bool
            do we need ASZCa bias settings? (def: no)

        Returns
        -------
        int
            status : 0 if reading ok, <> 0 if an error occured
             Possible error codes are:
                  -1 = file could not be openned
                  -2 = something wrong with FEBE
                  -3 = something wrong with basebands
                  -4 = something wrong with subscans
         """
        status = ReaDataEntity.TimelineData.read(self, inFile, febe, baseband, subscans, \
                                               update, phase, channelFlag, integrationFlag, \
                                               readHe, readAzEl0, readT, readWind, readBias, readPWV)

        if status:  # if reading failed
            return status

        self.__resetStatistics()

        return status

    #----------------------------------------------------------------------------
    def calibrateToJy(self):
        """Calibrate the data into Jy/beam unit as defined in the MBFits file  """
        countToJy         = self.ReceiverArray.JyPerCount
        self.Data        *= np.array((countToJy), np.float)
        self.DataWeights *= np.array((countToJy), np.float)

        self.__resetStatistics()

    #--------------------------------------------------------------------------------
    #----- flagging methods ---------------------------------------------------------
    #--------------------------------------------------------------------------------
    def flagRms(self,chanList=[],below=0,above=1e10,flag=2):
        """Flag channels with rms below 'below' or above 'above'

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        below : float
            flag channels with rms < 'below'
        above : float
            flag channels with rms > 'above'
        flag : int
            flag value to set (default: 2 'BAD SENSITIVITY')
        """

        self.MessHand.debug("flagRms start...")

        # recompute stat if needed
        if not self.__statisticsDone:
            self.__statistics()

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        # this should have returned a sublist of valid channels or all valid channels
        # if input chanList was empty
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanRms = np.array(self.getChanListData('rms', chanList))

        badChan = []
        badChan.extend(np.compress(np.where(chanRms < below, 1, 0), chanList))
        badChan.extend(np.compress(np.where(chanRms > above, 1, 0), chanList))

        if badChan:
            self.flagChannels(chanList=badChan, flag=flag)

        self.MessHand.debug("...flagRMS ends")

    #--------------------------------------------------------------------------------
    def flagFractionRms(self,chanList=[],ratio=10.,flag=2,plot=0,above=1,below=1):
        """flag according to rms, with limits depending on median rms

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        ratio : float
            channels with rms below median/ratio and above
            median*ratio will be flagged
        flag : int
            value of flag to set (default: 2 'BAD SENSITIVITY')
        plot : bool
            plot the results
        above : bool
            should we flag above median * ratio? (default yes)
        below : bool
            should we flag below median / ratio? (default yes)
        """

        self.MessHand.debug("flagFractionRms start...")

        # recompute stat if needed
        if not self.__statisticsDone:
            self.__statistics()

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanRms = np.array(self.getChanListData('rms', chanList))
        med = fStat.f_median(chanRms)

        if plot:
            self.plotRmsChan()
            Forms.shadeY(med*ratio, max(chanRms), ci=2)
            Forms.shadeY(min(chanRms), med/ratio, ci=2)

        if below:
            self.flagRms(chanList, below=med/ratio, flag=flag)
        if above:
            self.flagRms(chanList, above=med*ratio, flag=flag)

        self.MessHand.debug("...flagFractionRMS ends")

    #--------------------------------------------------------------------------------


    def flagAutoRms(self,chanList=[],threshold=3.,flag=2):
        """Automatic flagging of channels, based on their rms

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        threshold : float
            flag outliers channels w.r.t. threshold
        flag : int
            flag value to set  (default: 2 'BAD SENSITIVITY')

        Notes
        -----
        We flag all channels with rms above or below the median rms

        """

        self.MessHand.debug("flagRms start...")

        # recompute stat if needed
        if not self.__statisticsDone:
            self.__statistics()

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        # this should have returned a sublist of valid channels or all valid channels
        # if input chanList was empty
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanRms = np.array(self.getChanListData('rms', chanList))
        meanRms, sigmaRms, medianSDev, medianMDev = fStat.f_stat(chanRms)

        UsedChannels = self.ReceiverArray.UsedChannels

        badChan = []
        badChan.extend(np.compress(np.where(chanRms < medianSDev - threshold * sigmaRms, 1, 0), chanList))
        badChan.extend(np.compress(np.where(chanRms > medianSDev + threshold * sigmaRms, 1, 0), chanList))

        if badChan:
            self.flagChannels(chanList=badChan, flag=flag)

        self.MessHand.debug("...flagRMS ends")

#--------------------------------------------------------------------------------

    def flagChannels(self,chanList=[],flag=8):
        """assign flags to a list of channels

        Parameters
        ----------
        chanList : list of int
            list of channels to be flagged (default current list)
        flag : int
            flag values (default: 8 'TEMPORARY')
        """

        self.MessHand.debug("flagChannels start...")

        chanList = self.ReceiverArray.checkChanList(chanList)

        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # Flag in the ReceiverArray class and...
        nbFlag = self.ReceiverArray.flag(chanList, flag=flag)

        # ... report that on self.DataFlag
        chanIndexes = self.ReceiverArray.getChanIndex(chanList)
        for index in chanIndexes:
            if index != -1:
                if self.ReceiverArray.FlagHandler.isSetOnIndex(index):
                    self.FlagHandler.setAll(self.rflags['CHANNEL FLAGGED'], dim=1, index=index)

        self.MessHand.debug("...flagChannels ends")

    #--------------------------------------------------------------------------------
    def unflagChannels(self,chanList=[],flag=[]):
        """unflags a list of channels

        Parameters
        ----------
        chanList : list of int
            list of channels to be unflagged (default current list)
        flag : list of int
            flag values (default []: unset all flags)
        """

        self.MessHand.debug("unflagChannels start...")

        if isinstance(chanList, int):
            chanList = [chanList]

        if chanList == []:
            chanList = self.ReceiverArray.UsedChannels
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # Unflag in the ReceiverArray class and...
        nbFlag = self.ReceiverArray.unflag(chanList, flag=flag)

        # ... report that on self.DataFlag
        chanIndexes = self.ReceiverArray.getChanIndex(chanList)
        for index in chanIndexes:
            if index != -1:
                if self.ReceiverArray.FlagHandler.isUnsetOnIndex(index):
                    self.FlagHandler.unsetAll(self.rflags['CHANNEL FLAGGED'],
                                              dim=1, index=index)

        self.MessHand.debug("...unflagChannels ends")

    # ---------------------------------------------------------------------
    # TODO: This function should be called updateRCP and
    #       * call the proper ReceiverArray function depending on the RCP format
    #       * which should all give back the list of channel to flag
    #       * which we can apply to the local flagHandler like in flagChannels
    def flagRCP(self,rcpFile,flag=1):
        """flag channels not present in the given RCP file

        Parameters
        ----------
        rcpFile : str
            name of input RCP file
        flag : int
            value used to flag channels (def.: 1)
        """
        try:
            f = file(os.path.join(ReaConfig.rcpPath, rcpFile))
        except IOError:
            self.__MessHand.error("could not open file %s"%(rcpFile))
            return

        param = f.readlines()
        f.close()

        channels = []
        for i in xrange(len(param)):
            if param[i][0] not in ['!', '#', 'n']:    # skip comments
                tmp = string.split(param[i])
                num = string.atoi(tmp[0])
                channels.append(num)

        missing = []
        for i in xrange(self.ReceiverArray.NChannels):
            if i+1 not in channels:
                missing.append(i+1)

        if missing:
            self.flagChannels(chanList=missing, flag=flag)

    #--------------------------------------------------------------------------------

    def deglitch_old(self,chanList=[],window=10,above=5,flag=1,maxIter=10,minTimeSampInSubscan=100):
        """Flag yet unflagged data where glitches occur

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        window : int
            compute sliding rms in this window
        above : float
            flag data where the sliding rms > 'above'*rms
        flag : int
            flag values (default: 1 'SPIKE')
        maxIter : int
            number of iteration to perform
        minTimeSampInSubscan : int
           flag subscan with sample # lower than

        Notes
        -----
        IT IS HIGHLY RECOMMENDED TO REMOVE SKYNOISE BEFORE DEGLITCHING.

        """


        chanList = self.ReceiverArray.checkChanList(chanList)
        chanListIndices = self.ReceiverArray.getChanIndex(chanList)
        setFlags = np.take(self.FlagHandler.getFlags(), chanListIndices, axis=1)
        setFlags = np.take(setFlags, range(setFlags.shape[0]-window), axis=0)

        slideRms0 = self.slidingRms(nbInteg=window, channel=[], getFlagged=0, flag='None')

        # set flags on slideRms0
        mask = np.where(setFlags > 0, np.nan, 1)
        slideRms0 = slideRms0*mask

        meanRms = slideRms0[:, 0]*0.0

        for ts in xrange(len(slideRms0[:, 0])):
            timeSlice = slideRms0[ts,:]
            timeSlice, nnan = compressNan([timeSlice])
            meanRms[ts] = fStat.f_mean(timeSlice)

        addBefore = int(window/2.)
        addAfter = window-addBefore
        slideRms = (np.array(range(addBefore))*0.0+meanRms[0]).tolist()
        slideRms.extend(meanRms[:].tolist())
        slideRms.extend((np.array(range(addAfter))*0.0+meanRms[meanRms.shape[0]-1]).tolist())

        slideRms = np.array(slideRms)

        done = 0
        counter = 0
        totalflags = np.array(range(slideRms.shape[0]))*0

        while(done == 0):
            if (counter >= maxIter):
                break
            median = fStat.f_median(slideRms)
            offsets = np.array(slideRms)-median
            pos_mask = np.where(offsets > 0, 1, 0)
            offsets = np.compress(pos_mask, offsets)
            std_dev = fStat.f_mean(offsets)
            hiVal = median+above*std_dev
            mask = np.where(np.array(slideRms) >= hiVal, 1, 0)
            if (not(1 in mask)):
                done = 1
            else:
                counter += 1
            np.putmask(totalflags, mask, 1)
            np.putmask(slideRms, mask, np.nan)

        n_flagged = len(np.nonzero(totalflags))

        if n_flagged > 0:

            totalflags = np.convolve(totalflags, (np.array(range(window*2))*0+1).tolist(), mode=1)
            mask = np.where(totalflags > 0, 1, 0)

            subscan_start = [0]
            subscan_end = []
            oldFlagSet = mask[0]
            for i in xrange(len(mask)):
                if (oldFlagSet != mask[i]):
                    oldFlagSet = mask[i]
                    subscan_end.extend([i-1])
                    subscan_start.extend([i])

            subscan_end.extend([len(mask)-1])
            subscan_len = np.array(subscan_end)-np.array(subscan_start)

            for i in xrange(len(subscan_len)):
                if ((subscan_len[i] < minTimeSampInSubscan)):
                    mask[subscan_start[i]:subscan_end[i]+1] = 1

            # put the flags on the ScanParam flag array
            self.ScanParam.FlagHandler.setOnMask(mask, iFlags=flag)
            # put the flags on the main flag array
            for chan in chanListIndices:
                self.FlagHandler.setOnMask(mask, self.rflags['INTEGRATION FLAGGED'], \
                                           dim=1, index=chan)

            nflagged = np.compress(mask, mask).shape[0]
            self.MessHand.info("%5i timestamps flagged with flag %s" % (nflagged, str(flag)))

            self.__resetStatistics()

        return n_flagged


    #--------------------------------------------------------------------------------

    def deglitch2(self,chanList='all',above=10,flag=1,maxIter=10,minTimeSampInSubscan=200):
        """

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        window : int
            compute sliding rms in this window
        above : float
            flag data where the sliding rms > 'above'*rms
        flag : int
            flag values (default: 1 'SPIKE')
        maxIter : int
            number of iteration to perform
        minTimeSampInSubscan : int
           flag subscan with sample # lower than

        Notes
        -----
        # EXPERIMENTAL BUT FAST
        """

        # check chan list
        chanList = self.ReceiverArray.checkChanList([])
        chanListIndices = self.ReceiverArray.getChanIndex(chanList)

        # get flux
        flux = np.array(self.getChanListData('flux', chanList=chanList,\
                                          dataFlag='None'))

        # get flags, select those corresponding to chanList
        timeFlags = self.ScanParam.FlagHandler.getFlags()
        dataFlags = self.FlagHandler.getFlags()
        dataFlags = np.take(dataFlags, chanListIndices, 1)

        absflux = abs(flux)
        meanabs = np.sum(absflux, 0)/(float(len(chanListIndices)))
        med = fStat.f_median(meanabs)
        meanabs = meanabs-med

        done = 0
        counter = 0
        totalflags = np.array(range(flux.shape[1]))*0
        while(done == 0):
            if (counter >= maxIter):
                break
            m = fStat.f_median(meanabs)
            # compute the MEDIAN deviation!
            s = fStat.f_median(abs(meanabs))

            mask = np.where((meanabs > m+above*s), 1, 0)

            if (not(1 in mask)):
                done = 1
            else:
                counter += 1
                np.putmask(totalflags, mask, 1)
                np.putmask(meanabs, mask, m)

        n_flagged = len(np.nonzero(totalflags))

        nflagged = 0
        if n_flagged > 0:

            totalflags = np.convolve(totalflags, (np.array(range(20))*0+1).tolist(), mode=1)
            mask = np.where(totalflags > 0, 1, 0)

            subscan_start = [0]
            subscan_end = []
            oldFlagSet = mask[0]
            for i in xrange(len(mask)):
                if (oldFlagSet != mask[i]):
                    oldFlagSet = mask[i]
                    subscan_end.extend([i-1])
                    subscan_start.extend([i])

            subscan_end.extend([len(mask)-1])
            subscan_len = np.array(subscan_end)-np.array(subscan_start)

            for i in xrange(len(subscan_len)):
                if ((subscan_len[i] < minTimeSampInSubscan)):
                    mask[subscan_start[i]:subscan_end[i]+1] = 1

            # put the flags on the ScanParam flag array
            self.ScanParam.FlagHandler.setOnMask(mask, iFlags=flag)
            # put the flags on the main flag array
            for chan in chanListIndices:
                self.FlagHandler.setOnMask(mask, self.rflags['INTEGRATION FLAGGED'], \
                                           dim=1, index=chan)

            nflagged = np.compress(mask, mask).shape[0]
            self.MessHand.info("%5i timestamps flagged with flag %s" % (nflagged, str(flag)))
            self.MessHand.info("deglitch: %4i iterations" % (counter))

            self.__resetStatistics()

        return nflagged


    #--------------------------------------------------------------------------------


    def deglitch(self,chanList='all',above=5,flag=1,maxIter=10,window=20,minTimeSampInSubscan=200,plot=0):
        """Flag yet unflagged data where glitches occur. Iterative method.

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        window : int
            compute sliding rms in this window
        above : float
            flag data where the sliding rms > 'above'*rms
        flag : int
            flag values (default: 1 'SPIKE')
        maxIter : int
            number of iteration to perform
        minTimeSampInSubscan : int
           flag subscan with sample # lower than
        """

        # get ALL data
        chanList = self.ReceiverArray.checkChanList(chanList)
        chanListIndices = self.ReceiverArray.getChanIndex(chanList)

        flux = np.array(self.getChanListData('flux', chanList=chanList,\
                                          dataFlag='None'))

        # normalise by channel rms
        rms = self.getChanListData('rms', chanList=chanList)

        for i in xrange(len(chanList)):
            flux[i,:] = (flux[i,:]/rms[i]).astype(flux.dtype.char)

        # get time series flags
        timeFlags = self.ScanParam.FlagHandler.getFlags()
        dataFlags = self.FlagHandler.getFlags()
        dataFlags = np.take(dataFlags, chanListIndices, 1)
        # initialize array of standard deviations
        sdev = np.array(range(flux.shape[1])).astype(np.float)
        sdev[:] = 0.#float('NaN')
        for i in xrange(len(sdev)):
            if (timeFlags[i] == 0):
                fluxmask = np.where(dataFlags[i,:] == 0, 1, 0)
                fl = flux[:, i]
                fl = np.compress(fluxmask, fl)
                if (fl.shape[0] > 3):
                    mean = fStat.f_mean(fl)
                    sdev[i] = fStat.f_rms(fl, mean)

        done = 0
        counter = 0
        totalflags = np.array(range(sdev.shape[0]))*0

        while(done == 0):
            if (counter >= maxIter):
                break
            mask = np.where(sdev > 0., 1, 0)
            sdev_good = np.compress(mask, sdev)
            sdev_mean = fStat.f_mean(sdev_good)
            sdev_rms = fStat.f_rms(sdev_good, sdev_mean)
            sdev_median = fStat.f_median(sdev_good)
            hiVal = sdev_mean+above*sdev_rms
            mask = np.where(sdev >= hiVal, 1, 0)
            if (not(1 in mask)):
                done = 1
            else:
                counter += 1
                np.putmask(totalflags, mask, 1)
                np.putmask(sdev, mask, 0.)

        n_flagged = len(np.nonzero(totalflags))
        nflagged = 0

        if n_flagged > 0:

            totalflags = np.convolve(totalflags, (np.array(range(window))*0+1).tolist(), mode=1)
            mask = np.where(totalflags > 0, 1, 0)

            subscan_start = [0]
            subscan_end = []
            oldFlagSet = mask[0]
            for i in xrange(len(mask)):
                if (oldFlagSet != mask[i]):
                    oldFlagSet = mask[i]
                    subscan_end.extend([i-1])
                    subscan_start.extend([i])

            subscan_end.extend([len(mask)-1])
            subscan_len = np.array(subscan_end)-np.array(subscan_start)

            for i in xrange(len(subscan_len)):
                if ((subscan_len[i] < minTimeSampInSubscan)):
                    mask[subscan_start[i]:subscan_end[i]+1] = 1

            # put the flags on the ScanParam flag array
            self.ScanParam.FlagHandler.setOnMask(mask, iFlags=flag)
            # put the flags on the main flag array
            for chan in chanListIndices:
                self.FlagHandler.setOnMask(mask, self.rflags['INTEGRATION FLAGGED'], \
                                           dim=1, index=chan)

            nflagged = np.compress(mask, mask).shape[0]
            self.MessHand.info("%5i timestamps flagged with flag %s" % (nflagged, str(flag)))
            self.MessHand.info("deglitch: %4i iterations" % (counter))

            self.__resetStatistics()

        return nflagged

    #--------------------------------------------------------------------------------


    def glwDetect(self,chanList=[],scale=5,nsigma=5,window=25,plotCh='?',collapse=1,updateFlags=0):
        """detects glitchy time intervals using wavelets

        Parameters
        ----------
        chanList : list of int
            list of channels to consider [def. all]
        scale : int
            wavelet scale considered [def. 5]
        nsigma : int
            [def. 5]
        window : int
            window size for flag smoothing [def. 25]
        plotCh : int
            if set plot the result for channel plotCh
        collapse : bool
            whether to collapse channel flags together [def. 1]
        updateFlags : bool
            whether to update the data flags accordingly [def. 0]

        Returns
        -------
        float array
            Mask of channels to be flagged
        """

        self.MessHand.debug('glwDetect start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return 0

        nchan = len(chanList)

        # Create time step flags
        chFlags = np.zeros([self.ScanParam.NInt, self.ReceiverArray.NChannels], np.int8)
        for ch in chanList:
            nFl = 0
            Flags = np.zeros(np.size(self.ScanParam.MJD))
            ts = np.array(self.Data[:, ch-1])
            wtrans = fWavelets.wavetransform1d(ts, scale+1)
            wmax = wtrans[:, scale-1]
            Mean, Med, SDev, MDev = fStat.arraystat(wmax, Flags)
            hiVal = Med+nsigma*MDev
            loVal = Med-nsigma*MDev
            Flags = np.where(np.bitwise_or(wmax >= hiVal, wmax <= loVal), 1, 0)
            while (nFl < np.sum(chFlags)):
                nFl = np.sum(chFlags)
                Mean, Med, SDev, MDev = fStat.arraystat(wmax, Flags)
                hiVal = Med+nsigma*MDev
                loVal = Med-nsigma*MDev
                Flags = np.where(np.bitwise_or(wmax >= hiVal, wmax <= loVal), 1, 0)
            chFlags[:, ch-1] = Flags.astype(type(chFlags))

        # Smooth (and eventually collapse) flags
        kernel  = np.zeros(window) + 1
        if collapse:
            chFlags = np.where(np.sum(np.transpose(chFlags)) < 0.2*float(nchan), 0, 1)
            chFlags = np.convolve(chFlags, kernel, mode=1)
        else:
            for ch in chanList:
                chFlags[:, ch-1] = np.convolve(chFlags[:, ch-1], kernel, mode=1)

        # Plot the channel chPlot with flagged time intervals
        if (plotCh != '?'):
            MJD = self.ScanParam.get(dataType='mjd', flag='None')
            if collapse:
                Flags = chFlags
            else:
                Flags = chFlags[:, plotCh-1]
            d = np.array(self.getChanData('flux', plotCh, flag='None'))
            Mean, Med, SDev, MDev = fStat.arraystat(d, Flags)
            pl = np.where(Flags < 0.5, d, 0)
            Plot.plot(MJD, d-Med, style='l', ls=1, labelX='MJD - MJD(0) [sec]', labelY='flux density [arb.u.]', limitsY=[min(pl-Med)*2., max(pl-Med)*2.])
            Plot.plot(MJD, pl-Med, style='l', overplot=1, ci=2)


        # Update flags
        if updateFlags:
            if collapse:
                chans = np.zeros(self.ReceiverArray.NChannels) + 1
                Flags = multiply.outer(chFlags, chans)
                self.FlagHandler.setOnMask(Flags, 1)
            else:
                self.FlagHandler.setOnMask(chFlags, 1)

        self.MessHand.debug('... glwDetect end')

        return chFlags

#--------------------------------------------------------------------------------

    def despike(self,chanList=[],below=-5,above=5,flag=1):
        """Flag yet unflagged data below 'below'*rms and above 'above'*rms.

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        below : float
            flag data with value < 'below'*rms
        above : float
            flag data with value > 'above'*rms
        flag : int
            flag values (default: 1 'SPIKE')
        """

        self.MessHand.debug('despike start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return 0

        # recompute stat if needed
        if not self.__statisticsDone:
            self.__statistics()

        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return

        # process the DataFlags array
        totalFlag = 0

        for chan in chanList:
            # remember that physical channel numbers do not correspond to
            # index of Data*, so...
            chanIndex = self.ReceiverArray.getChanIndex(chan)[0]

            # dataType (unflagged)
            dataTest = self.getChanData(dataType='flux', chan=chan, flag='Blank')

            # We want to flag all the data which do not have this
            # particular flag, so check what is left
            dataTest_noFlag = np.ravel(self.getChanData(dataType='flux', chan=chan, flag=flag))

            if len(dataTest_noFlag) > 0:
                rms  = self.getChanData('rms', chan=chan)
                mean = self.getChanData('median', chan=chan)

                # ...per subscan
                # to work on subscan, one need to wait for subscanIndex fixes
                # a loop on subscans will the been needed to flag properly

                # rms = self.getChanData('rms_s',chan=chan,flag=flag)
                # mean = self.getChanData('mean_s',chan=chan,flag=flag)

                hiVal = mean+above*rms
                loVal = mean+below*rms

                mask = np.where(np.bitwise_or(dataTest >= hiVal, dataTest <= loVal), 1, 0)

                if len(np.nonzero(mask)) > 0:
                    n0 = self.FlagHandler.nSet(flag, dim=1, index=chanIndex)
                    self.FlagHandler.setOnMask(mask, flag, dim=1, index=chanIndex)
                    n1 = self.FlagHandler.nSet(flag, dim=1, index=chanIndex)
                    totalFlag += (n1-n0)
                    if (n1-n0):
                        self.MessHand.debug("Channel %i"%chan +\
                                            " %5i timestamps flagged" % (n1-n0) + \
                                            " with flag %s" % str(flag))
                    else:
                        self.MessHand.debug("Channel %i "%chan +\
                                            " nothing to flag")


        if totalFlag > 0:
            self.MessHand.info("Despike : %5i samples flagged with flag %s" % (totalFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing flagged")

        self.MessHand.debug("... despike end")

        return totalFlag



    #--------------------------------------------------------------------------------

    def iterativeDespike(self,chanList=[],below=-5,above=5,flag=1,maxIter=100):
        """Iteratively flag yet unflagged data below 'below'*rms and above 'above'*rms.

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: current list)
        below : float
            flag data with value < 'below'*rms
        above : float
            flag data with value > 'above'*rms
        maxIter : int
            maximum number of iteration (default 100)
        flag : int
            flag values (default: 1 'SPIKE')
        """

        # Initialize loop variables
        despiked = 1
        i = 0

        # Run loop
        while ((despiked > 0) and (i < maxIter)):
            i += 1
            despiked = self.despike(chanList=chanList, below=below, above=above, flag=flag)
        if despiked > 0:
            self.MessHand.info("IterativeDespike summary : %5i samples flagged with flag %s" % (despiked, str(flag)))

    #--------------------------------------------------------------------------------

    def unflag(self,channel=[],flag=[]):
        """Unflag data

        Parameters
        ----------
        channel : list of int
            list of channel to flag (default: current list)
        flag : list of int
            unflag only this value (default []: all non-reserved flag values)

        """

        self.MessHand.debug('unflag start...')

        # check channel list, special one, since even flagged channel has
        # to be taken into account

        CurrChanList = self.ReceiverArray.CurrChanList
        UsedChannels = self.ReceiverArray.UsedChannels

        if channel in ['all', 'al', 'a']:
            channel = UsedChannels
        elif channel == []:
            channel = CurrChanList
        elif isinstance(channel, type(1)):
            channel = [channel]

        chanList = []
        for num in channel:
            if num in UsedChannels:
                chanList.append(num)

        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return

        totalUnFlag = 0
        for chan in chanList:

            chanIndex = self.ReceiverArray.getChanIndex(chan)[0]

            n0 = self.FlagHandler.nUnset(flag, dim=1, index=chanIndex)
            self.FlagHandler.unsetAll(flag, dim=1, index=chanIndex)
            n1 = self.FlagHandler.nUnset(flag, dim=1, index=chanIndex)
            totalUnFlag += (n1-n0)

        if totalUnFlag > 0:
            self.MessHand.info("%5i samples unflagged with flag %s" % (totalUnFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing unflagged")

        self.MessHand.debug('... unflag end')

    #----------------------------------------------------------------------------
    def flag(self,dataType='', channel='all', below='?', above='?', flag=8):
        """flag data based on dataType, general flagging routine, may be slow

        Parameters
        ----------
        dataType : str
            flag based on this dataType
            * See TimelineData.getChanData
        channel : list of int
            list of channel to flag (default: all)
        below : float
            flag dataType < below (default max; or 5*RMS)
        above : float
            flag dataType > above (default min; or -5*RMS)
        flag : int
            flag value (default 8 'TEMPORARY')

        Notes
        -----
        'below' and 'above' should be in unit of the flagged data,
        except for 'Lon' and 'Lat' where they should be in arcsec
        """

        self.MessHand.debug('flag start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if channel in ['all', 'al', 'a'] and \
               ( dataType in ['LST', 'lst'] or \
                 dataType in ['MJD', 'mjd'] or \
                 dataType in ['UT'] \
                 ):

            # this is a channel independant and ScanParam based flagging ...
            self.MessHand.warning("You should use the flagInTime method")
            self.flagInTime(dataType=dataType, below=below, above=above, flag=flag)
            return

        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return

        # process the DataFlags array
        totalFlag = 0
        for chan in chanList:
            self.MessHand.debug("flaging for chan: "+str(chan))

            # remember that physical channel numbers do not correspond to
            # index of Data*, so...
            chanIndex = self.ReceiverArray.getChanIndex(chan)[0]

            # dataType (unflagged)
            dataTest = self.getChanData(dataType=dataType, chan=chan, flag='None')

            # We want to flag all the data which do not have this
            # particular flag, so check what is left
            dataTest_noFlag = np.ravel(self.getChanData(dataType=dataType, chan=chan, flag=flag))

            if len(dataTest_noFlag) > 0:
                self.MessHand.debug(" found something to flag")

                hiVal = max(dataTest_noFlag)
                loVal = min(dataTest_noFlag)

                # default inputs
                if above != '?':
                    loVal = above
                if below != '?':
                    hiVal = below

                mask = np.where(np.bitwise_and(dataTest >= loVal, dataTest <= hiVal), 1, 0)

                if len(np.nonzero(mask)) > 0:
                    n0 = self.FlagHandler.nSet(flag, dim=1, index=chanIndex)
                    self.FlagHandler.setOnMask(mask, flag, dim=1, index=chanIndex)
                    n1 = self.FlagHandler.nSet(flag, dim=1, index=chanIndex)
                    totalFlag += (n1-n0)
                    if (n1-n0):
                        self.MessHand.debug("Channel %i"%chan +\
                                            " %5i timestamps flagged" % (n1-n0) +\
                                            " with flag %s" % str(flag))
                    else:
                        self.MessHand.debug("Channel %i "%chan +\
                                            " nothing to flag")

        if totalFlag > 0:
            self.MessHand.info("%5i samples flagged with flag %s" % (totalFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing flagged")

        self.MessHand.debug("... flag end")

    #--------------------------------------------------------------------------------
    def flagInTime(self,channel='all', dataType='MJD', below='?', above='?', flag=8):
        """Flag data in time interval

        Parameters
        ----------
        dataType : str
            dataType on what to flag
            * 'lst','mjd', 'ut'
            * 'speed', 'azspeed', 'elspeed'
            * 'accel', 'azacc', 'alacc'
        below : float
            flag data below this value (default end of the scan)
        above : float
            flag data above this value (default start of the scan)
        flag : int
            flag to be set (default: 8 'TEMPORARY')
        """

        self.MessHand.debug('flagInTime start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel, flag='None')
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # return Data index
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        dataType = dataType.lower()

        # check dataType
        if ( dataType not in ['lst', 'mjd', 'ut'] and
             dataType not in ['speed', 'azspeed', 'elspeed'] and
             dataType not in ['accel', 'azacc', 'elacc']):
            self.MessHand.error("use only this method to flag in time")
            return      # get the default values
        dataTest = self.ScanParam.get(dataType=dataType, flag='None')
        if above == '?':
            above = min(dataTest)
        if below == '?':
            below = max(dataTest)

        self.ScanParam.flag(dataType=dataType, below=below, above=above, flag=flag)
        # Report the flag on the ScanParam attribute
        mask = self.ScanParam.FlagHandler.isSetMask()
        if len(np.nonzero(mask)) > 0:
            for chan in chanListIndexes:
                self.FlagHandler.setOnMask(mask, \
                                           self.rflags['INTEGRATION FLAGGED'], \
                                           dim=1, index=chan)
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing flagged")

        self.MessHand.debug("... flagInTime end")

    #--------------------------------------------------------------------------------
    def unflagInTime(self,channel='all', dataType='LST', below='?', above='?', flag=[]):
        """Unflag data in time interval

        Parameters
        ----------
        dataType : {'lst','mjd', 'ut', 'speed', 'azspeed', 'elspeed', 'accel', 'azacc', 'alacc'}
            dataType on what to flag
        below : float
            flag data below this value (default end of the scan)
        above : float
            flag data above this value (default start of the scan)
        flag : list of int
            flag to be set (default []: all flag values)
        """
        self.MessHand.debug('unflagInTime start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel, flag='None')
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # return Data index
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        dataType = dataType.lower()

        # check dataType
        if ( dataType not in ['lst', 'mjd', 'ut'] and
             dataType not in ['speed', 'azspeed', 'elspeed'] and
             dataType not in ['accel', 'azacc', 'elacc']):
            self.MessHand.error("use only this method to flag in time")
            return

        # get the default values
        dataTest = self.ScanParam.get(dataType=dataType, flag='None')
        if above == '?':
            above = min(dataTest)
        if below == '?':
            below = max(dataTest)

        self.ScanParam.unflag(dataType=dataType, below=below, above=above, flag=flag)
        # Report the flag on the ScanParam attribute
        mask = self.ScanParam.FlagHandler.isUnsetMask()
        if len(np.nonzero(mask)) > 0:
            for chan in chanListIndexes:
                self.FlagHandler.unsetOnMask(mask, \
                                             self.rflags['INTEGRATION FLAGGED'], \
                                             dim=1, index=chan)

        self.MessHand.debug("... unflagInTime end")

    #--------------------------------------------------------------------------------
    def flagMJD(self, below='?', above='?', flag=8):
        """Flag data in time interval

        Parameters
        ----------
        below : float
              flag data below this value (default end of the scan)
        above : float
              flag data above this value (default start of the scan)
        flag : int
              flag to be set (default: 8 'TEMPORARY')
        """

        self.flagInTime(dataType='MJD', below=below, above=above, flag=flag)

    #--------------------------------------------------------------------------------
    def unflagMJD(self, below='?', above='?', flag=[]):
        """Unflag data in time interval

        Parameters
        ----------
        below : float
              flag data below this value (default end of the scan)
        above : float
              flag data above this value (default start of the scan)
        flag : int
              flag to be set (default []: all flag values)
        """

        self.unflagInTime(dataType='MJD', below=below, above=above, flag=flag)

    #--------------------------------------------------------------------------------
    def flagPolygon(self, channel='all', system='EQ', poly=np.zeros((1, 2)), inout='IN', flag=8):
        """flag a position in the sky within or outside a given polygon

        Parameters
        ----------
        channel : list of int
            list of channels to flag (default: 'all')
        system : {'EQ' or 'HO'}
            coord system, either 'HO' (Az,El *OFFSETS*) or 'EQ' (RA, Dec absolute coord.) default='EQ'
        poly : float array
            vertices of polygon. 2D array of [X,Y]
        inout : {'IN', 'OUT'}
            inside/outside the polygon
        flag : int
            flag to be set (default 8 'TEMPORARY')
        """

        self.MessHand.debug('flagPolygon start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        # check system
        system = string.upper(system)
        if system not in ['EQ', 'HO']:
            self.MessHand.error("no valid coordinate system: "+system)
            return

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

        # check flags
        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return

        OffsetsUsed = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))

        totalFlag = 0

        if system == 'EQ':
            RADec = np.array([self.ScanParam.get('RA', flag='None'), \
                           self.ScanParam.get('Dec', flag='None')])
            OffsetsUsed = OffsetsUsed/3600.

            for chan in chanListIndexes:
                dRA = RADec[0]+(-1.*np.cos(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[0, chan]\
                                +   np.sin(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[1, chan])\
                               / np.array(np.cos(np.radians(RADec[1])))
                dDec = RADec[1] + np.sin(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[0, chan]\
                               + np.cos(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[1, chan]
                mask = self.maskPolygon(dRA, dDec, poly, inout)
                if len(np.nonzero(mask)):
                    n0 = self.FlagHandler.nSet(flag, dim=1, index=chan)
                    self.FlagHandler.setOnMask(mask, flag, dim=1, index=chan)
                    n1 = self.FlagHandler.nSet(flag, dim=1, index=chan)
                    totalFlag += (n1-n0)

        elif system == 'HO':
            AzEl = np.array([self.ScanParam.get('AzimuthOffset', flag='None'), \
                          self.ScanParam.get('ElevationOffset', flag='None')])

            for chan in chanListIndexes:
                dAz = AzEl[0] + OffsetsUsed[0, chan]
                dEl = AzEl[1] + OffsetsUsed[1, chan]
                mask = self.maskPolygon(dAz, dEl, poly, inout)
                if len(np.nonzero(mask)):
                    n0 = self.FlagHandler.nSet(flag, dim=1, index=chan)
                    self.FlagHandler.setOnMask(mask, flag, dim=1, index=chan)
                    n1 = self.FlagHandler.nSet(flag, dim=1, index=chan)
                    totalFlag += (n1-n0)

        if totalFlag > 0:
            self.MessHand.info("%5i samples flagged with flag %s" % (totalFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing flagged")

        self.MessHand.debug("... flagPolygon end")

    #--------------------------------------------------------------------------------
    def unflagPolygon(self, channel='all', system='EQ', poly=np.zeros((1, 2)), inout='IN', flag=[]):
        """unflag a position in the sky within or outside a given polygon

        Parameters
        ----------
        channel : list of int
            list of channels to flag (default: 'all')
        system : {'EQ' or 'HO'}
            coord. system, either 'HO' (Az,El *OFFSETS*) or 'EQ' (RA, Dec absolute coord.), default='EQ'
        poly : float array
            vertices of polygon
        inout : {'IN', 'OUT'}
            inside/outside the polygon
        flag : list of int
            list of flag to be unset (default [] : all)
        """

        self.MessHand.debug('unflagPolygon start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        # check system
        system = string.upper(system)
        if system not in ['EQ', 'HO']:
            self.MessHand.error("no valid coordinate system: "+system)
            return

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

        # check flags
        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return

        OffsetsUsed = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))

        totalFlag = 0

        if system == 'EQ':
            RADec = np.array([self.ScanParam.get('RA', flag='None'), \
                           self.ScanParam.get('Dec', flag='None')])
            OffsetsUsed = OffsetsUsed/3600.

            for chan in chanListIndexes:
                dRA = RADec[0]+(-1.*np.cos(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[0, chan]\
                                +   np.sin(np.radiansself.ScanParam.ParAngle))*OffsetsUsed[1, chan]\
                               / np.array(np.cos(np.radians(RADec[1])))
                dDec = RADec[1] + np.sin(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[0, chan]\
                               + np.cos(np.radians(self.ScanParam.ParAngle))*OffsetsUsed[1, chan]
                mask = self.maskPolygon(dRA, dDec, poly, inout)
                if len(np.nonzero(mask)):
                    n0 = self.FlagHandler.nUnset(flag, dim=1, index=chan)
                    self.FlagHandler.unsetOnMask(mask, flag, dim=1, index=chan)
                    n1 = self.FlagHandler.nUnset(flag, dim=1, index=chan)
                    totalFlag += (n1-n0)

        elif system == 'HO':
            AzEl = np.array([self.ScanParam.get('AzimuthOffset', flag='None'), \
                          self.ScanParam.get('ElevationOffset', flag='None')])

            for chan in chanListIndexes:
                dAz = AzEl[0] + OffsetsUsed[0, chan]
                dEl = AzEl[1] + OffsetsUsed[1, chan]
                mask = self.maskPolygon(dAz, dEl, poly, inout)
                if len(np.nonzero(mask)):
                    n0 = self.FlagHandler.nUnset(flag, dim=1, index=chan)
                    self.FlagHandler.unsetOnMask(mask, flag, dim=1, index=chan)
                    n1 = self.FlagHandler.nUnset(flag, dim=1, index=chan)
                    totalFlag += (n1-n0)

        if totalFlag > 0:
            self.MessHand.info("%5i samples unflagged with flag %s" % (totalFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing unflagged")

        self.MessHand.debug("... unflagPolygon end")

    #--------------------------------------------------------------------------------
    def maskPolygon(self,x,y,poly,inout='IN'):
        """create an array of zeros and ones for a list of points being inside/outside
               a polygon

        Parameters
        ----------
        x, y : float array
            coordinates of points
        poly : float array
            coordinates of points
        inout : str
            inside/outside the polygon

        Returns
        -------
        float array
            array to be used for masking data points
        """
        mask = []
        if inout == 'IN':            # look for points inside the polygon
            for i in xrange(len(x)):
                mask.append(inPolygon(x[i], y[i], poly))
        elif inout == 'OUT':         # look for points outside the polygon
            for i in xrange(len(x)):
                mask.append(outPolygon(x[i], y[i], poly))
        else:                      # wrong or missing information
            self.MessHand.warning("Inside or outside the polygon?")
        mask = np.array(mask)
        return mask

    #--------------------------------------------------------------------------------
    def flagPosition(self, channel='all', Az = 0, El = 0, radius = 0, flag = 8,
                     offset=True, outer=False):
        """flag a position in the sky within a given radius

        Parameters
        ----------
        channel : list of int
            list of channel to flag (default: 'all')
        Az, El : float
            the horizontal reference position (arcsec for offsets, deg for absolute)
        radius : float
            aperture to flag in unit of the reference position
        flag : int
            flag to be set (default 8 'TEMPORARY')
        offset : bool
            flag on the offsets ? (False, flag on absolute values)
        outer : bool
            flag OUTSIDE the given radius ?
        """

        self.MessHand.debug('flagPosition start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return


        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if offset:
            AzEl            = np.array([self.ScanParam.get('AzimuthOffset', flag='None'), \
                                     self.ScanParam.get('ElevationOffset', flag='None')])
            OffsetsUsed     = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))
        else:
            AzEl            = np.array([self.ScanParam.get('Azimuth', flag='None'), \
                                     self.ScanParam.get('Elevation', flag='None')])
            OffsetsUsed     = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))/3600.


        if "NASMYTH" in self.ReceiverArray.DewCabin:
            cosNAS = self.ScanParam.cosNAS
            sinNAS = self.ScanParam.sinNAS


        # TODO : Too slow, do the rotation here....

        totalFlag = 0
        for chan in chanListIndexes:
            chanOffsets = np.array([OffsetsUsed[:, chan]]).transpose()
            if "NASMYTH" in self.ReceiverArray.DewCabin:
                NInt = np.size(cosNAS)
                chanOffsets = chanOffsets.repeat(NInt, axis=1)
                for index in np.arange(NInt):
                    chanOffsets[:, index] = np.dot(np.array([[cosNAS[index], -sinNAS[index]], [sinNAS[index], cosNAS[index]]]), chanOffsets[:, index])

            dAz = AzEl[0] + chanOffsets[0] - Az
            dEl = AzEl[1] + chanOffsets[1] - El

            if outer:
                mask = np.where((dAz**2 + dEl**2) > radius**2, 1, 0)
            else:
                mask = np.where((dAz**2 + dEl**2) <= radius**2, 1, 0)
            if len(np.nonzero(mask)):
                n0 = self.FlagHandler.nSet(flag, dim=1,       index=chan)
                self.FlagHandler.setOnMask(mask, flag, dim=1, index=chan)
                n1 = self.FlagHandler.nSet(flag, dim=1,       index=chan)
                totalFlag += (n1-n0)

        if totalFlag > 0:
            self.MessHand.info("%5i samples flagged with flag %s" % (totalFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing flagged")

        self.MessHand.debug("... flagPosition end")


    #--------------------------------------------------------------------------------
    def flagRadius(self, channel='all', radius = 0, flag = 8, outer=False):
        """flag time series (all channels) by reference offset in Az/El

        Parameters
        ----------
        channel : list of int
            list of channel to flag (default: 'all')
        radius : float
            aperture to flag in ARCSECONDS
        flag : int
            flag to be set (default 8 'TEMPORARY')
        outer : bool
            flag OUTSIDE the given radius? default: no
        """

        self.MessHand.debug('flagRadius start...')

        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanListIndices = self.ReceiverArray.getChanIndex(chanList)

        AzEl            = np.array([self.ScanParam.get('AzimuthOffset', flag='None'), \
                                 self.ScanParam.get('ElevationOffset', flag='None')])

        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return


        if outer:
            mask = np.where((AzEl[0,:]**2 + AzEl[1,:]**2) > radius**2, 1, 0)
        else:
            mask = np.where((AzEl[0,:]**2 + AzEl[1,:]**2) <= radius**2, 1, 0)
        if len(np.nonzero(mask)):

            self.ScanParam.FlagHandler.setOnMask(mask, iFlags=flag)

            for chan in chanListIndices:
                self.FlagHandler.setOnMask(mask, self.rflags['INTEGRATION FLAGGED'], \
                                           dim=1, index=chan)

            nflagged = np.compress(mask, mask).shape[0]
            self.MessHand.info("%5i timestamps flagged with flag %s" % (nflagged, str(flag)))
            self.__resetStatistics()

        else:
            self.MessHand.warning("Nothing flagged")

        self.MessHand.debug("... flagPosition end")

    #--------------------------------------------------------------------------------
    def unflagPosition(self, channel='all', Az = 0, El = 0, radius = 0, flag = [], offset=True):
        """unflag a position in the sky within a given radius

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        Az, El : float
            the horizontal reference position (arcsec for offsets, deg for absolute)
        radius : float
            aperture to unflag in unit of the reference position
        flag : list of int
            unflag to be set (default []: unflag all non-reserved flag values)
        offset : bool
            unflag on the offsets ? (False, flag on absolute values)
        """

        self.MessHand.debug('unflagPosition start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if offset:
            AzEl            = np.array([self.ScanParam.get('AzimuthOffset', flag='None'), \
                                     self.ScanParam.get('ElevationOffset', flag='None')])
            OffsetsUsed     = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))
        else:
            AzEl            = np.array([self.ScanParam.get('Azimuth', flag='None'), \
                                     self.ScanParam.get('ElevationOffset', flag='None')])
            OffsetsUsed     = np.array(self.ReceiverArray.getChanSep(self.ReceiverArray.UsedChannels))/3600.

        flag = self._removeReservedFlagValues(flag)
        if flag == None:
            self.MessHand.error("no valid flags")
            return

        totalFlag = 0
        for chan in chanListIndexes:
            dAz = AzEl[0] + OffsetsUsed[0, chan] - Az
            dEl = AzEl[1] + OffsetsUsed[1, chan] - El
            mask = np.where((dAz**2 + dEl**2) <= radius**2, 1, 0)
            if len(np.nonzero(mask)):
                n0 = self.FlagHandler.nUnset(flag, dim=1, index=chan)
                self.FlagHandler.unsetOnMask(mask, dim=1, index=chan)
                n1 = self.FlagHandler.nUnset(flag, dim=1, index=chan)
                totalFlag += (n1-n0)

        if totalFlag > 0:
            self.MessHand.info("%5i samples unflagged with flag %s" % (totalFlag, str(flag)))
            self.__resetStatistics()
        else:
            self.MessHand.warning("Nothing unflagged")

        self.MessHand.debug("... unflagPosition end")


    #--------------------------------------------------------------------------------
    def flagSubscan(self,subList,flag=7):
        """flag subscans

        Parameters
        ----------
        subList : list of int
            list of subscan numbers (or single number) to be flagged
        flag : int
            value of flags to set (default: 7 'SUBSCAN FLAGGED')
        """
        # If a single number given, convert to list
        if isinstance(subList, type(1)):
            subList = [subList]
        # check if subscan numbers exist
        for subNum in subList:
            if subNum not in self.ScanParam.SubscanNum:
                subList.remove(subNum)
        if len(subList) == 0:
            self.MessHand.warning("No valid subscan number given")
            return

        numberFlags = 0
        # Use MJD rather than LST: it's never -999!
        mjd = self.getChanData('mjd', flag='None')  # get all mjd values, including
                        # flagged datapoints (same convention in SubscanIndex)
        for subNum in subList:
            numIndex = self.ScanParam.SubscanNum.index(subNum)
            mjd1 = mjd[self.ScanParam.SubscanIndex[0, numIndex]]
            mjd2 = mjd[self.ScanParam.SubscanIndex[1, numIndex]-1]
            self.flagInTime('mjd', above=mjd1, below=mjd2, flag=flag)
            numberFlags += 1

        self.MessHand.info(str("%i subscans flagged with flag %s"%(numberFlags, str(flag))))

    #--------------------------------------------------------------------------------
    def unflagSubscan(self,subList,flag=[]):
        """unflag subscans

        Parameters
        ----------
        subList : list of int
            list of subscan numbers (or single number) to be unflagged
        flag : list of int
            value of flags to unset (default []: all flag values)
        """
        # If a single number given, convert to list
        if isinstance(subList, type(1)):
            subList = [subList]
        # check if subscan numbers exist
        for subNum in subList:
            if subNum not in self.ScanParam.SubscanNum:
                subList.remove(subNum)
        if len(subList) == 0:
            self.MessHand.warning("No valid subscan number given")
            return

        numberFlags = 0
        # Use MJD rather than LST: it's never -999!
        mjd = self.getChanData('mjd', flag='None')  # get all mjd values, including
                        # flagged datapoints (same convention in SubscanIndex)
        for subNum in subList:
            numIndex = self.ScanParam.SubscanNum.index(subNum)
            mjd1 = mjd[self.ScanParam.SubscanIndex[0, numIndex]]
            mjd2 = mjd[self.ScanParam.SubscanIndex[1, numIndex]-1]
            self.unflagInTime('mjd', above=mjd1, below=mjd2, flag=flag)
            numberFlags += 1

        self.MessHand.info(str("%i subscan unflagged with flag %s"%(numberFlags, str(flag))))


    #--------------------------------------------------------------------------------
    def flagLon(self, channel='all', below='?', above='?', flag=8):
        """Flag data in Longitude interval

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        subList : list of int
            list of subscan numbers (or single number) to be unflagged
        below : float
            flag data below this value
        above : above
            flag data above this value
        flag : int
            flag to be set (default 8 'TEMPORARY')
        """
        self.flag(dataType='azoff', channel=channel, below=below, above=above, flag=flag)

    #--------------------------------------------------------------------------------
    def unflagLon(self, channel='all', below='?', above='?', flag=[]):
        """Unflag data in Longitude interval

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        subList : list of int
            list of subscan numbers (or single number) to be unflagged
        below : float
            flag data below this value
        above : float
            flag data above this value
        flag : list of int
            flag to be unset (default []: all non-reserved flag values)
        """
        self.flag(dataType='azoff', channel=channel, below=below, above=above, flag=flag)

    #--------------------------------------------------------------------------------

    def flagTurnaround(self, flag=1):
        """flag subscans where azimuth offset changes sign

        Parameters
        ----------
        flag : flag
            flag to be set (default 1 'TURNAROUND')
        """
        try:
            sublist = []
            for i in xrange(self.ScanParam.SubscanPos.shape[0]):
                if (self.ScanParam.SubscanPos[i] != 0):
                    sublist.append(self.ScanParam.SubscanNum[i])

            self.flagSubscan(subList=sublist, flag=flag)
        except:
            self.MessHand.warning('No subscan information, nothing will be done')

    #--------------------------------------------------------------------------------

    def unflagTurnaround(self, flag=[]):
        """unflag subscans where azimuth offset changes sign

        Parameters
        ----------
        flag : list of int
            flag to be unset (default []: all flag values)
        """
        try:
            sublist = []
            for i in xrange(self.ScanParam.SubscanPos.shape[0]):
                if (self.ScanParam.SubscanPos[i] != 0):
                    sublist.append(self.ScanParam.SubscanNum[i])

            self.unflagSubscan(subList=sublist, flag=flag)
        except:
            self.MessHand.warning('No subscan information, nothing will be done')

    #--------------------------------------------------------------------------------
    def flagSparseSubscans(self,minLiveFrac=0.3):
        """flag whole subscans with few live time stamps

        Parameters
        ----------
        minLiveFrac : float
            minimum fraction of live time stamps
        """

        self.__statistics()
        subnum = self.ScanParam.SubscanNum
        subin = self.ScanParam.SubscanIndex
        sflags = []
        tflags = self.ScanParam.FlagHandler.getFlags()
        for s in xrange(len(subnum)):
            n_in_sub = subin[1, s]-subin[0, s]
            flags_in_sub = tflags[subin[0, s]:subin[1, s]]
            mask = np.where(flags_in_sub == 0, 1, 0)
            ok_in_sub = np.compress(mask, mask).shape[0]
            if (float(ok_in_sub) > 0):
                if (float(ok_in_sub)/float(n_in_sub) < minLiveFrac):
                    sflags.append(subnum[s])

        if sflags:
            self.flagSubscan(sflags)

            self.__resetStatistics()

        return sflags.shape[0]



    def flagSubscanByRms(self,above=2.,maxIter=20):
        """iteratively flag subscans with high rms. Subscan rms is
        determined as the mean of all channels.

        Parameters
        ----------
        above : float
            flag data with value > 'above'*rms
        maxIter : int
            maximum number of iterations
        """

        if not self.__statisticsDone:
            self.__statistics()

        subnum = self.ScanParam.SubscanNum
        subflags = subnum*0
        subrms = np.array(self.getChanListData('rms_s'))
        mean_subrms = subrms[0,:]*0.0
        for i in xrange(len(mean_subrms)):
            mean_subrms[i] = fStat.f_mean(subrms[:, i])
        computation_mask = np.where(mean_subrms > 0, 1, 0)
        done = 0
        counter = 0
        while (done == 0):
            if (counter > maxIter):
                done = 1
            rms_considered = np.compress(computation_mask, mean_subrms)
            meanRms = fStat.f_median(rms_considered)
            rmsRms = fStat.f_rms(rms_considered, meanRms)
            subflagmask = np.where(mean_subrms > meanRms+above*rmsRms, 1, 0)
            np.putmask(mean_subrms, subflagmask, -1)
            new_comp_mask = np.where(mean_subrms > 0, 1, 0)
            if (new_comp_mask.tolist() == computation_mask.tolist()):
                done = 1
            else:
                computation_mask = new_comp_mask
                counter += 1
        totmask = np.where(mean_subrms < 0, 1, 0)
        subflaglist = np.compress(totmask, subnum)
        totmask2 = np.where(mean_subrms > 0, 1, 0)

        if subflaglist:
            self.flagSubscan(subflaglist)
            self.__resetStatistics()

        nflagged = np.compress(totmask, totmask).shape[0]


        return nflagged

#---------------------------------------------------------------------


    def flagSpeed(self, channel='all', below='?', above='?', flag=3):
        """Flag data according to telescope speed

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        below : float
            flag data below this value
        above : float
            flag data above this value
        flag : int
            flag to be set (default 3 'ELEVATION VELOCITY THRESHOLD')
        """
        self.flagInTime(channel=channel, dataType='speed', below=below, above=above, flag=flag)

#---------------------------------------------------------------------

    def unflagSpeed(self, channel='all', below='?', above='?', flag=[]):
        """Unflag data according to telescope speed

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        below : float
            unflag data below this value
        above : float
            unflag data above this value
        flag : list of int
            flag to be unset (default []: all flag values)
        """
        self.unflagInTime(channel=channel, dataType='speed', below=below, above=above, flag=flag)

#---------------------------------------------------------------------
    def flagAccel(self, channel='all', below='?', above='?', flag=2):
        """Flag data according to telescope acceleration

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        below : float
            flag data below this value
        above : float
            flag data above this value
        flag : int
            flag to be set (default 2 'ACCELERATION THRESHOLD')
        """
        self.flagInTime(channel=channel, dataType='accel', below=below, above=above, flag=flag)

#---------------------------------------------------------------------
    def unflagAccel(self, channel='all', below='?', above='?', flag=[]):
        """Unflag data according to telescope acceleration

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        below : float
            unflag data below this value
        above : float
            unflag data above this value
        flag : flag
            flag to be unset (default []: all flag values)
        """
        self.unflagInTime(channel=channel, dataType='accel', below=below, above=above, flag=flag)


#---------------------------------------------------------------------
    def flagNan(self, channel='all', flag=9):
        """flag data with NaN values

        Parameters
        ----------
        channel : list of int
            list of channel to unflag (default: 'all')
        flag : int
            flag to be used (default 9 'BLANK DATA'
        """

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)
        nInt = self.ScanParam.NInt
        for c in chanListIndexes:
            mask = fUtilities.masknan(self.Data[:, c])
            if len(np.nonzero(mask)):
                self.FlagHandler.setOnMask(mask, flag, dim=1, index=c)

#---------------------------------------------------------------------
    def flagJumps(self, channel='all', ratio = 3., window=4):
        """flags jumps seen by all bolo defined as the deviation to the median value

        Parameters
        ----------
        channel : list of int
            list of channel to flagprocess (default: all)
        ratio : float
            ratio above which to flag
        window : int
            window used to smooth the data

        Notes
        -----
        Data has to be baselined and with gain applied
        """
        # Data has to be baselined
        chanList = self.ReceiverArray.checkChanList(channel)

        medianAbsSignal = self._DataAna__computeMedianAbsSignal(chanList)
        time            = self.ScanParam.get('mjd')

        # smooth them
        nTimeStamp              = len(time)
        nSmoothedTimeStamp      = int(nTimeStamp/window)
        smoothedMedianAbsSignal = np.zeros((nSmoothedTimeStamp), np.float)
        smoothedTime            = np.zeros((nSmoothedTimeStamp), np.float)

        for i in xrange(nSmoothedTimeStamp):
            smoothedMedianAbsSignal[i] = np.sum(medianAbsSignal[window*i:window*(i+1)])/window
            smoothedTime[i] = np.sum(time[window*i:window*(i+1)])/window

        threshold = fStat.f_mean(smoothedMedianAbsSignal)*ratio
        toFlag = []
        i = 0

        start = -1
        while i < nSmoothedTimeStamp-1:
            while smoothedMedianAbsSignal[i] < threshold and i < nSmoothedTimeStamp-1:
                i += 1
            if i < nSmoothedTimeStamp-1:
                # start of a jump to flag
                start = max([0, i-1])
                while smoothedMedianAbsSignal[i] >= threshold and i < nSmoothedTimeStamp-1:
                    i += 1
                # here it goes back below theshold
                end = min([i+1, nSmoothedTimeStamp-1])
                if start >= 0:
                    toFlag.append([smoothedTime[start], smoothedTime[end]])

        self.MessHand.longinfo("found %i jumps"%(len(toFlag)))
        if toFlag:
            # if anything found
            for gap in toFlag:
                self.flagMJD(above=gap[0], below=gap[1], flag=4)


#---------------------------------------------------------------------
    # FFT filtering methods
#---------------------------------------------------------------------
    def blankFreq(self, channel='all', below='?', above='?'):
        """Permanently remove some frequency interval in the Fourrier spectrum
             of the signal. This is computed subscan by subscan.

        Parameters
        ----------
        channel : list of int
            list of channel to flagprocess (default: all)
        below : float
            filter data below this frequency [Hz]
        above : float
            filter data above this frequency [Hz]
        """
        self.MessHand.debug('blankFreq start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)

        # We use only MJD values for fft. They are the correct time stamps.
        mjd = self.getChanData('mjd', chanList, flag='None')
        nbSub = len(self.ScanParam.SubscanNum)   # number of subscans

        for chan in chanList:
            flux = self.getChanData('flux', chan, flag='None')
            num = self.ReceiverArray.getChanIndex(chan)[0]
            for i in xrange(nbSub):
                ind1 = self.ScanParam.SubscanIndex[0, i]
                ind2 = self.ScanParam.SubscanIndex[1, i]
                theTime = mjd[ind1:ind2]
                theFlux = flux[ind1:ind2]
                if not theFlux.flags.contiguous:
                    theFlux = theFlux.copy()
                # select only unflagged data - zeros for flagged ones
                maskOk = np.nonzero(self.FlagHandler.isUnsetMask(dim=1, index=num)[ind1:ind2])
                theFluxOk = np.zeros(theFlux.shape, np.float)
                np.put(theFluxOk, maskOk, np.take(theFlux, maskOk))

                oneFFT = FilterFFT(theTime, theFluxOk)
                oneFFT.doFFT()
                # Do the filtering
                oneFFT.blankAmplitude(above=above, below=below)
                oneFFT.invFFT()  # this also "unbins" the data

                np.put(theFlux, maskOk, np.take(oneFFT.Y, maskOk))  # flagged values unchanged
                # Now update flagged values with inverse FFT + previous value
                maskBad = np.nonzero(self.FlagHandler.isSetMask(dim=1, index=num)[ind1:ind2])
                oldVal = np.take(theFlux, maskBad)
                np.put(theFlux, maskBad, np.take(oneFFT.Y, maskBad)+oldVal)
                self.Data[ind1:ind2, num] = theFlux

        self.__resetStatistics()

#---------------------------------------------------------------------
    def reduceFreq(self, channel='all', center=50., width=1., factor=10.,optimize=1, window=4):
        """Permanently reduce some frequency interval in the Fourrier spectrum
             of the signal. This is computed subscan by subscan.

        Parameters
        ----------
        channel : list of int
            list of channel to process (default: all)
        center : float
            central frequency, in Hz
        width : float
            line FWHM
        factor : float
            attenuation factor
        """

        self.MessHand.debug('reduceFreq start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)

        # We use only MJD values for fft. They are the correct time stamps.
        mjd = self.getChanData('mjd', chanList, flag='None')
        nbSub = len(self.ScanParam.SubscanNum)   # number of subscans

        for chan in chanList:
            flux = self.getChanData('flux', chan, flag='None')
            num = self.ReceiverArray.getChanIndex(chan)[0]
            for i in xrange(nbSub):
                ind1 = self.ScanParam.SubscanIndex[0, i]
                ind2 = self.ScanParam.SubscanIndex[1, i]
                theTime = mjd[ind1:ind2]
                theFlux = flux[ind1:ind2]
                if not theFlux.flags.contiguous:
                    theFlux = theFlux.copy()
                # select only unflagged data - zeros for flagged ones
                maskOk = np.nonzero(self.FlagHandler.isUnsetMask(dim=1, index=num)[ind1:ind2])
                theFluxOk = np.zeros(theFlux.shape, np.float)
                np.put(theFluxOk, maskOk, np.take(theFlux, maskOk))

                oneFFT = FilterFFT(theTime, theFluxOk)
                oneFFT.doFFT(windowing=window)
                # Do the filtering
                oneFFT.reduceAmplitude(center=center, width=width, factor=factor)
                oneFFT.invFFT(windowing=window)
                np.put(theFlux, maskOk, np.take(oneFFT.Y, maskOk))  # flagged values unchanged
                # Now update flagged values with inverse FFT + previous value
                maskBad = np.nonzero(self.FlagHandler.isSetMask(dim=1, index=num)[ind1:ind2])
                oldVal = np.take(theFlux, maskBad)
                np.put(theFlux, maskBad, np.take(oneFFT.Y, maskBad)+oldVal)
                self.Data[ind1:ind2, num] = theFlux

        self.__resetStatistics()

#---------------------------------------------------------------------
    def taperFreq(self, channel='all', above='?', N=2, window=4):
        """Permanently taper off Fourier spectrum above given value
             of the signal

        Parameters
        ----------
        channel : list of int
            list of channel to flagprocess (default: all)
        above : float
            filter data above this value
        N : int
            Butterworth steepenes order
        """

        self.MessHand.debug('taperFreq start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)

        # We use only MJD values for fft. They are the correct time stamps.
        mjd   = self.getChanData('mjd', chanList, flag='None')
        nbSub = len(self.ScanParam.SubscanNum)   # number of subscans

        for chan in chanList:
            flux = self.getChanData('flux', chan, flag='None')
            num = self.ReceiverArray.getChanIndex(chan)[0]

            for i in xrange(nbSub):
                ind1 = self.ScanParam.SubscanIndex[0, i]
                ind2 = self.ScanParam.SubscanIndex[1, i]
                theTime = mjd[ind1:ind2]
                theFlux = flux[ind1:ind2]
                if not theFlux.flags.contiguous:
                    theFlux = theFlux.copy()

                # select only unflagged data - zeros for flagged ones
                maskOk = np.nonzero(self.FlagHandler.isUnsetMask(dim=1, index=num)[ind1:ind2])
                theFluxOk = np.zeros(theFlux.shape, np.float)
                np.put(theFluxOk, maskOk, np.take(theFlux, maskOk))

                oneFFT = FilterFFT(theTime, theFluxOk)
                oneFFT.doFFT(windowing=window)
                oneFFT.taperAmplitude(above=above, N=N)

                oneFFT.invFFT(windowing=window)
                np.put(theFlux, maskOk, np.take(oneFFT.Y, maskOk))  # flagged values unchanged
                # Now update flagged values with inverse FFT + previous value
                maskBad = np.nonzero(self.FlagHandler.isSetMask(dim=1, index=num)[ind1:ind2])
                oldVal = np.take(theFlux, maskBad)
                np.put(theFlux, maskBad, np.take(oneFFT.Y, maskBad)+oldVal)

                self.Data[ind1:ind2, num] = theFlux

        self.__resetStatistics()

#---------------------------------------------------------------------
    def flattenFreq(self, channel='all', below=0.1, hiref=1.,optimize=1, window=4):
        """flatten the 1/F part of the FFT using constant amplitude

        Parameters
        ----------
        channel : list of int
            list of channels to process (default: all)
        below : float
            filter data below this value
        hiref : float
            amplitudes at f < below will be replaced with
            the average value between below and hiref
        """
        self.MessHand.debug('flattenFreq start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)

        # We use only MJD values for fft. They are the correct time stamps.
        mjd = self.getChanData('mjd', chanList, flag='None')
        nbSub = len(self.ScanParam.SubscanNum)   # number of subscans

        for chan in chanList:
            flux = self.getChanData('flux', chan, flag='None')
            num = self.ReceiverArray.getChanIndex(chan)[0]

            for i in xrange(nbSub):
                ind1 = self.ScanParam.SubscanIndex[0, i]
                ind2 = self.ScanParam.SubscanIndex[1, i]
                theTime = mjd[ind1:ind2]
                theFlux = flux[ind1:ind2]
                if not theFlux.flags.contiguous:
                    theFlux = theFlux.copy()

                # select only unflagged data - zeros for flagged ones
                maskOk = np.nonzero(self.FlagHandler.isUnsetMask(dim=1, index=num)[ind1:ind2])
                theFluxOk = np.zeros(theFlux.shape, np.float)
                np.put(theFluxOk, maskOk, np.take(theFlux, maskOk))

                oneFFT = FilterFFT(theTime, theFluxOk)
                oneFFT.doFFT(windowing=window)
                # compute median value between below and hiref
                mask = np.nonzero(greater(oneFFT.Freq, below) and np.less(oneFFT.Freq, hiref))
                inside = np.take(oneFFT.Amplitude, mask)
                meanAmp = fStat.f_median(inside)
                # replace amplitudes at lower freq with this value
                mask = np.nonzero(np.less(oneFFT.Freq, below))
                for k in mask:
                    oneFFT.Amplitude[k] = meanAmp
                # inverse FFT
                oneFFT.invFFT(windowing=window)
                np.put(theFlux, maskOk, np.take(oneFFT.Y, maskOk))  # flagged values unchanged
                # Now update flagged values with inverse FFT + previous value
                maskTmp = self.FlagHandler.isSetMask(dim=1, index=num)[ind1:ind2]
                # ... but only if not NaN
                maskNan = fUtilities.masknan(self.Data[ind1:ind2, num])
                maskBad = np.nonzero(logical_and(maskTmp, logical_not(maskNan)))
                oldVal = np.take(theFlux, maskBad)
                np.put(theFlux, maskBad, np.take(oneFFT.Y, maskBad)+oldVal)

                self.Data[ind1:ind2, num] = theFlux   # store results in data

        self.__resetStatistics()

#---------------------------------------------------------------------
    #----- statistics methods -------------------------------------------------------
#---------------------------------------------------------------------

    def __resetStatistics(self):
        """to be called every time the data are altered: statistics and correlation matrix should be recomputed"""

        self.__statisticsDone = False
        self.__corMatrixDone  = False
        self.__pcaDone = False

        nUsedChannels = self.ReceiverArray.NUsedChannels
        nSub          = self.ScanParam.NObs
        nInt          = self.ScanParam.NInt

        dataShape = self.Data.shape
        nUsedChannels = dataShape[1]

        self.CorrelatedNoise = as_column_major_storage(np.zeros((nInt, nUsedChannels), np.float32))

        self.FFCF_CN         = np.ones((nUsedChannels, nUsedChannels), np.float32)
        self.CorMatrix       = np.ones((nUsedChannels, nUsedChannels), np.float32)

        self.FFCF_Gain       = np.ones(nUsedChannels, np.float32)
        self.FF_Median       = np.ones(nUsedChannels, np.float32)

        self.ChanRms         = np.ones(nUsedChannels, np.float32)
        self.ChanMean        = np.ones(nUsedChannels, np.float32)
        self.ChanMed         = np.ones(nUsedChannels, np.float32)

        self.ChanRms_s       = np.ones((nUsedChannels, nSub), np.float32)
        self.ChanMean_s      = np.ones((nUsedChannels, nSub), np.float32)
        self.ChanMed_s       = np.ones((nUsedChannels, nSub), np.float32)

    def __statistics(self):
        """computes mean, median, rms for all scans and subscans for all used channels """

        self.MessHand.debug('statistics start...')

        myTiming = Timing()

        if self._existData():

            myTiming.setTime()

            Mean, Med, SDev, MDev = fStat.arraystat(self.Data, self.FlagHandler.getFlags())
            self.ChanMean = Mean
            self.ChanMed  = Med
            self.ChanRms  = SDev

            Mean_s, Med_s, SDev_s, MDev_s = fStat.arraystat_s(self.Data, self.FlagHandler.getFlags(),\
                                                              self.ScanParam.SubscanIndex)
            self.ChanMean_s = Mean_s
            self.ChanMed_s  = Med_s
            self.ChanRms_s  = SDev_s

            # Mark Statistics as done
            self.__statisticsDone = True

            self.MessHand.debug(" statistics by scan in " + str(myTiming))

        self.MessHand.debug('... statistics end')


    def slidingRms(self, channel=[], nbInteg=10, flag=[], getFlagged=0):
        """compute rms in a sliding window

        Parameters
        ----------
        channel : list of int
            list of channel to flag (default: all; [] : current list)
        nbInteg : int
            number of elements on which one rms is computed (=window size)
        flag : list of int
            retrieve data flagged or unflagged accordingly
        getFlagged : bool
            flag revers to flagged/unflagged data
                                   flag   | getFlagged | Retrieve..
                                   'None' |  0         | all data
                                   []     |  0         | unflagged data (default)
                                   []     |  1         | data with at least one flag set
                                   1      |  0         | data with flag 1 not set
                                   1      |  1         | data with flag 1 set
                                   [1,2]  |  0         | data with neither flag 1 nor flag 2 set
                                   [1,2]  |  1         | data with either flag 1 or flag 2 set

        Returns
        float array
            the rms are returned
        """
        # check channel list
        chanList = self.ReceiverArray.checkChanList(channel)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        result = []
        for chan in chanList:
            # get data for this chan - that's a 1D array
            chanData = self.getChanData('flux', chan=chan, flag=flag, getFlagged=getFlagged)
            lenData = chanData.shape[0]
            # build a 2D array corresponding to the sliding window
            # there will be nb_data - window_size possible windows
            slidingData = np.zeros((nbInteg, lenData-nbInteg), np.float32)
            for i in xrange(lenData-nbInteg):
                slidingData[:, i] = chanData[i:i+nbInteg]
            # Now call arraystat on this 2D array, with all flags set to zero
            # (filtering already done in call to getChanData)
            Mean, Med, SDev, MDev = fStat.arraystat(slidingData, 0*slidingData)
            # store Rms in result
            result.append(SDev)

        # Return result as an array, with channels along 2nd dimension
        return np.transpose(np.array(result))



#---------------------------------------------------------------------
    # Correlated Noise methods
    #-----------------------------------------------------------------------
    def medianCorrelations(self,chanList=[],numCorr=0):
        """returns the  median correlation of each channel with all other channels

        Parameters
        ----------
        chanList : list of int
            the list of channels to consider
        numCorr : int
            if set to non-zero, takes the median correlation of the
            numCorr most correlated channels

        Returns
        -------
        float arr
            the median correlation
        """

        chanList = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if not chanList.any():
            self.MessHand.error('no valid channel')

        if not self.__corMatrixDone:
            self.computeWeights(chanList)

        matrix = np.take(np.take(self.CorMatrix, chanListIndexes, axis=0), chanListIndexes, axis=1)

        corrs = matrix[0,:]

        for rownum in xrange(len(matrix[:, 0])):
            row = matrix[rownum,:]
            mask = np.where(row < 1.0, 1, 0)
            row = np.compress(mask, row)
            if numCorr:
                maxCorrs = tolist_rea(np.take(row, np.argsort(row)[-(abs(numCorr)):]))
                corrs[rownum] = fStat.f_median(maxCorrs)
            else:
                corrs[rownum] = fStat.f_median(row)

        return corrs




    def plotCorMatrix(self,chanList=[], check = True, distance=False, weights=False, xLabel='Channels', style='idl4', limitsZ=[]):
        """plot the correlation matrix

        Parameters
        ----------
        chanList : list of int
            the list of channel to plot
        check : bool
            check the chanList first ?
        distance : bool
            sort the second dimension by distance ?
        weights : bool
            plot weights instead of correlation matrix ?
        xLabel : str
            the x label
        style : str
            the color table
        limitsZ : float array
            the intensity range
        """


        if not self.__corMatrixDone:
            self._DataAna__correlatedNoiseWeights()

        if check:
            chanList = self.ReceiverArray.checkChanList(chanList)

        if not chanList.any():
            self.MessHand.error('no channel to plot')

        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if not weights:
            matrix = np.take(np.take(self.CorMatrix, chanListIndexes, axis=0), chanListIndexes, axis=1)
            subCaption = ' correlation matrix'
            index = np.arange(chanListIndexes.shape[0])
            matrix[index, index] = np.nan
        else:
            matrix = np.take(np.take(self.Weight, chanListIndexes, axis=0), chanListIndexes, axis=1)
            subCaption = ' weight matrix'

        yLabel = xLabel

        if distance:
            yLabel = 'Distance to channel'

            nBolo = len(chanList)
            subChanSep = np.take(np.take(self.ReceiverArray.ChannelSep, chanListIndexes, axis=0), chanListIndexes, axis=1)

            for i in xrange(nBolo):
                indexArray = np.arange(nBolo)
                sortedIndex = np.take(indexArray, (np.argsort(subChanSep[i,:])))
                matrix[i,:] = np.take(matrix[i,:], (sortedIndex))


        Plot.draw(matrix, \
                  labelX=xLabel, labelY=yLabel, \
                  caption=self.ScanParam.caption()+subCaption, \
                  style=style, wedge=1,\
                  limitsZ=limitsZ, nan=1)


        #-----------------------------------------------------------------------
    def plotCorDist(self,chanList=[],average=1,upperlim=-1.,check=1,style='p',ci=1,overplot=0,limitsX=[],limitsY=[],pointsize=3.):
        """plot correlations (correlation matrix) as a function  of channel separation

        Parameters
        -----------
        chanList : list of int
            the list of channels to plot
        average : int
            number of data to average over (for easier viewing)
        upperlim : float
            return only distances in arcsec below this value
            (negative value means no limit, which is the default)
        check : bool
            check the chanList first ?
        plot : bool
            actually produce a plot?
        style : str
            'p' for point 'l' for line
        ci : int
            color index
        overplot : bool
            do we overplot ?
        limitsX, limitsY : float array
            limits in X and Y
        pointsize : float
            the size of the point
        """

        if check:
            chanList = self.ReceiverArray.checkChanList(chanList)

        if not chanList.any():
            self.MessHand.error('no channel to plot')

        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        self.__corMatrixDone = 0
        corMatrix = fSNF.cmatrix(self.Data, self.FlagHandler.getFlags(), chanListIndexes)
        self.CorMatrix        = corMatrix
        self.__corMatrixDone  = 1

        subChanSep = np.take(np.take(self.ReceiverArray.ChannelSep, chanListIndexes, axis=0), chanListIndexes, axis=1)
        nBolo = len(chanList)
        matrix = np.take(np.take(self.CorMatrix, chanListIndexes, axis=0), chanListIndexes, axis=1)
        for i in xrange(nBolo):
            indexArray = np.arange(nBolo)
            sortedIndex = np.take(indexArray, (np.argsort(subChanSep[i,:])))
            matrix[i,:] = np.take(matrix[i,:], (sortedIndex))
            subChanSep[i,:] = np.take(subChanSep[i,:], (sortedIndex))

        dataX = np.take(np.ravel(subChanSep), (np.argsort(np.ravel(subChanSep))))
        dataY = np.take(np.ravel(matrix), (np.argsort(np.ravel(subChanSep))))

        if (upperlim > 0):
            mask = np.where((dataX < upperlim), 1, 0)
            dataX = np.compress(mask, dataX)
            dataY = np.compress(mask, dataY)

        if (average > 1):
            average = int(average)
            newshape = len(dataX)/average
            dataX = np.sum(np.resize(dataX, (newshape, average)), 1)/float(average)
            dataY = np.sum(np.resize(dataY, (newshape, average)), 1)/float(average)


        BogliConfig.point['size'] = pointsize
        Plot.plot(dataX, dataY, overplot=overplot, ci=ci, style=style,\
                  limitsX=limitsX, limitsY=limitsY,\
                  labelX='Channel separation (arcsec)', labelY='correlation',\
                  caption=self.ScanParam.caption())
        BogliConfig.point['size'] = 0.01


    #-----------------------------------------------------------------------
    def __correlatedNoiseWeights(self, chanList=[], minCorr=0., a=0.95, b=2.0, core=10., beta=2.):
        """compute correlation and weight matrix of the used channels

        Parameters
        ----------
        chanList : list of int
            restrict the computation to certain channel (default : all used channel)
        minCorr : float
            minimum correlation coefficient (defaut:0, should be positiv)
        a : float
            parameter for weights, usually = 0.90-0.98
        b : float
            parameter for weights, usually = 1
        core : float
            core radius in arcmin for radial weighting (weight = 0.5)
        beta : float
            beta for beta profile for radial weighting

        Notes
        -----
        Weight is a non-linear rescaling of the correlation coefficient

                           weight_nm = ( CM_nm - a * min_m( CM_nm ) )**b

        an additionnal weighting factor is applied with channel separation

                           weight_nm  = weight_nm * 1.0 / ( 1 + ( dist_nm / core )**beta )

        """


        myTiming      = Timing()
        corMatrix     = self.CorMatrix
        nUsedChannels = self.ReceiverArray.NUsedChannels

        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)
        # channelFlags    = self.ReceiverArray.FlagHandler.getFlags()

        # Compute the Correlation Matrix first
        if not self.__corMatrixDone:
            corMatrix = fSNF.cmatrix(self.Data, self.FlagHandler.getFlags(), chanListIndexes)
            # Set the corMatrixDone
            self.CorMatrix        = corMatrix
            self.__corMatrixDone  = 1
            self.MessHand.debug("corMatrix computed in "+str(myTiming))

        myTiming.setTime()

        # Compute the Weights now
        boloWeight = np.zeros((nUsedChannels, nUsedChannels), np.float32)
        chanSep    = np.take(np.take(self.ReceiverArray.ChannelSep, self.ReceiverArray.UsedChannels-1, axis=0), self.ReceiverArray.UsedChannels-1, axis=1)

        boloWeight = fSNF.wmatrix(corMatrix, chanSep, chanListIndexes, minCorr, a, b, core, beta)

        # no need to normalize since in SNF this is done
        # Yes, master Yoda
        self.Weight = boloWeight

        self.MessHand.debug("weights computed in "+str(myTiming))

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    def writeFFCF(self,outFile='ffcf.txt'):
        """store current correlated noise flat field to a file

        Parameters
        ----------
        file : str
            complete name of output file
        """

        # filename = "ffcf_%s.txt"%(scanNum)

        try:
                # f = file(ReaConfig.rcpPath+outFile,'w') # how to addrsss rcppath?
            f = file(outFile, 'w')
        except IOError:
            self.MessHand.error("could not open file %s in write mode"%(outFile))
            return

        # Write header
        f.write("! FFCF_CN \n")
        # Write parameters for all channels
        for i in xrange(len(self.ReceiverArray.FlagHandler.getFlags())):
            f.write("%i %f %i \n" % \
                    (i+1, self.FFCF_CN[i, i], int(self.ReceiverArray.FlagHandler.getFlags()[i])))
        f.close()
    # ---------------------------------------------------------------------
    def readFFCF(self,inFile='ffcf.txt'):
        """read in a FFCF file

        Parameters
        ----------
        inFile : str
            complete name of file to read in
        """

        try:
            f = file(inFile)
        except IOError:
            self.MessHand.error("could not open file %s"%(inFile))
            return

        # read and process file
        param = f.readlines()
        f.close()
        ff, flag, chan = [], [], []   # local lists to store FFCF and flag

        for i in xrange(len(param)-1):	        # -1: skip last line
            if param[i][0] != '!':              # skip comments
                tmp = string.split(param[i])
                chan.append(string.atof(tmp[0]))
                ff.append(string.atof(tmp[1]))
                flag.append(string.atof(tmp[2]))

        for i in xrange(len(ff)):
            ic = int(chan[i])
            self.FFCF_CN[ic, ic] = ff[i]
            if (flag[i] != 0.):
                self.flagChannels(ic)

#-----------------------------------------------------------------------
    def __correlatedNoiseFFCF(self, chanList=[], skynoise=0, minSlope=0.1, maxSlope=10.0, plot=0, chanRef=-1):
        """compute correlation factor relative to given reference channel or skynoise

        Parameters
        ----------
        chanList : list of int
            list of channel to correlate (default current list)
        skynoise : bool
            correlate skynoise[channel] not signal[channel] to signal
        minSlope : float
            limit slope of least squares fit (default 0.1)
        maxSlope : float
            limit slope of least squares fit (default 10)
        plot : bool
            plot the correlation and the fit (default no)
        chanRef : int
            reference channel in case of plotting (default : first in chanList, must be in chanList!)
        """

        # This method is very robust and does not depend on the chanRef
        # TODO: it is possible to make it faster by needing a chanRef, i.e
        # just correlate to this one, however, the choice of the chanRef
        # can be problematic
        #
        # FB20070401 fixed fit plotting

        if not self._existData():
            self.MessHand.error(" (correlate) no data available! ")
            return

        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)


        if chanRef == -1:
            chanRef       = chanList[0]
            chanRefIndex  = chanListIndexes[0]
        else:
            chanRef = self.ReceiverArray.checkChanList(chanRef) [0]
            if not chanRef:
                self.MessHand.error("not a valid reference channel")
                return
            else:
                # chanRefIndex = list(chanList).index(chanRef)
                chanRefIndex = self.ReceiverArray.getChanIndex(chanRef)[0]

        if not chanRef in chanList:
            self.MessHand.error("reference channel must also be in chanList")
            return

        chanRefIndexList = np.nonzero( np.equal(chanListIndexes, chanRefIndex) )[0]

        dataFlags   = self.FlagHandler.getFlags()
        CorrelateTo = self.Data

        if skynoise:    # if correlation against skynoise
            CorrelateFrom = self.CorrelatedNoise
        else:     # if correlation against a channel
            CorrelateFrom = self.Data

        slopes, intercep, FFCF = fSNF.correlationfit(CorrelateFrom, CorrelateTo, dataFlags, chanListIndexes, \
                                                     np.array([minSlope, maxSlope]))

        self.FFCF_CN = FFCF   # make public              dimension: arraysize x arraysize
        self.Slopes = slopes  # safe for diagnostic only dimension: chanList  x chanList

        if plot:
            self.plotCorrel(chanRef=chanRef, chanList=chanList, skynoise=skynoise)
            dataX = [Plot.xAxis['limits']]*len(chanList)
            dataY = []

            # note that slopes and intercep have the size of chanList in this case
            for i in xrange(len(chanList)):
            # loop i=0,1,2,.... through nonflg chanList
                dataY.append( np.array(Plot.xAxis['limits']) * slopes[chanRefIndexList, i] + intercep[chanRefIndexList, i] )

            MultiPlot.plot(chanList, dataX, dataY, overplot=1, ci=2, style='l')

    #-----------------------------------------------------------------------
    def __computeCorrelatedNoise(self, chanList=[], clip = 4.0, fastnoise=0):
        """compute correlated noise must be run after
             CorrelatedNoiseWeights() and correlatedFFCF() with the same chanList

        Parameters
        ----------
        chanList : list of int
            list of channel to use (default: all; [] : current list)
        clip : float
            the limit where to use the data (+- clip*rms - default 5)
        fastnoise : bool
            only use the 7 most correlated channels
        """

        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        data            = self.Data
        dataFlags       = self.FlagHandler.getFlags()
        boloWeight      = self.Weight
        FFCF            = self.FFCF_CN
        nChan           = self.ReceiverArray.NUsedChannels
        nInt            = self.ScanParam.NInt    # number of integration points

        correlatedNoise = np.zeros((nInt, nChan), np.float32)

        correlatedNoise      = fSNF.correlatednoise(data, dataFlags, chanListIndexes, \
                                                    boloWeight, FFCF, clip)

        # Take only the 7 largest correlations for each channel (columns)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # print shape(correlatedNoise)
        if fastnoise:
            for i in xrange(np.size(correlatedNoise, 1)):
                corrNoiseColumn = correlatedNoise[:, i]
                corrNoiseSort = sort(corrNoiseColumn)
                # corrNoiseSort = corrNoiseSort.reverse()

                maskC = np.where(corrNoiseColumn >= corrNoiseSort[-7], 1, 0).astype(correlatedNoise.dtype.char)
                correlatedNoise[:, i] = maskC * correlatedNoise[:, i]

        self.CorrelatedNoise = correlatedNoise

    #-----------------------------------------------------------------------
    def removeCorrelatedNoise(self, chanList=[], threshold=1.e-3, iterMax=4, plot=0, \
                               coreRadius=30, beta=2., chanRef=None, fastnoise=0):
        """remove the correlated noise from the data.

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: all; [] : current list)
        threshold : float
            threshold value for the Flat Field Correction Factor (in %, default 1.e-3)
        iterMax : int
            maximum number of iteration
        plot : bool
            do be plot the result ?
        coreRadius : int
            core radius for weight taper beta profile
        chanRef : int
            reference channel to start with

        Notes
        -----
        NOTE: THIS METHOD IS EXPERIMENTAL AND MAY NOT WORK PROPERLY
        ON ALL INSTALLATIONS! If you are unsure, use medianNoiseRemoval or corrPCA for the removal of
        correlated noise.
        """

        if not self.__corMatrixDone:
            self._DataAna__correlatedNoiseWeights()

        if not chanRef:
            chanRef = self.ReceiverArray.RefChannel

        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)
        data            = self.Data
        chanRefIndex    = self.ReceiverArray.getChanIndex(chanRef)[0]
        chanRefIndexList = np.nonzero( np.equal(chanListIndexes, chanRefIndex) )[0]
        # print chanRefIndexList

        # First iteration to compute the FFCF
        if plot:
            DeviceHandler.selectDev(1)
        self._DataAna__correlatedNoiseFFCF(chanList=chanList, skynoise=0, plot=plot, chanRef=chanRef)
        if plot:
            if np.size(DeviceHandler.DevList) == 1:
                DeviceHandler.openDev()
            DeviceHandler.selectDev(2)
            BogliConfig.point['size'] = 3
            Plot.plot(self.Slopes[chanRefIndexList,:], labelY='slope', limitsY=[0, 2], ci=1, style='l')
            BogliConfig.point['size'] = 0.01
        ref = self.FFCF_CN
        self._DataAna__correlatedNoiseWeights(minCorr=0., a=0.95, b=2.0, core=coreRadius, beta=beta)
        self._DataAna__computeCorrelatedNoise(chanList=chanList, clip=5., fastnoise=fastnoise)

        # -------------------------------------------- Main loop to estimate the FFCF
        iterNum = 1
        while iterNum <= iterMax:
            self.MessHand.longinfo(" - iteration : %i"%(iterNum))

            if not plot:
                self._DataAna__correlatedNoiseFFCF(chanList=chanList, skynoise=1, plot=0)

            if plot:
                DeviceHandler.selectDev(1)
                self._DataAna__correlatedNoiseFFCF(chanList=chanList, skynoise=1, plot=1)
                # matrix = compress2d(self.FFCF_CN,chanListIndexes)
                # Plot.draw(matrix,wedge=1,limitsZ=[0,2],nan=0,style='idl4', \
                #          caption='Flat Field Correction Factor',labelY = 'good Channel index', \
                #          labelX = 'good Channel index')
                DeviceHandler.selectDev(2)
                BogliConfig.point['size'] = 3
                # ci = iterNum+1
                # plot slopes for first channel
                Plot.plot(self.Slopes[chanRefIndexList,:], labelY='slope', limitsY=[0, 2], overplot=0, style='l', ci=1)
                Plot.plot(diagonal(self.Slopes), overplot=1, style='l', ci=2)
                BogliConfig.point['size'] = 0.01

            change = fStat.f_mean(abs(np.ravel((ref-self.FFCF_CN)/ref)))
            self.MessHand.info(" FFCF relative change= %7.3f"%(change))
            if change < threshold:
                self.MessHand.info(" FFCF relative change limit reached: break")
                break
            else:
                ref     = self.FFCF_CN
                iterNum = iterNum+1

            self._DataAna__correlatedNoiseWeights(minCorr=0., a=0.95, b=2.0, core=coreRadius, beta=2.)
            self._DataAna__computeCorrelatedNoise(chanList=chanList, clip=5.)
        # ------------------------------------------------------------------------------
        if iterNum == iterMax:
            self.MessHand.info("maximum number of iteration reached")

        correlatedNoise = self.CorrelatedNoise
        FFCF            = self.FFCF_CN

        for iChan in chanListIndexes:    # diagonal FFCF are *Gains* thus multiply !!
            correlatedNoise[:, iChan] = (correlatedNoise[:, iChan]/FFCF[iChan, iChan]).astype(np.float32)

        if plot: # plotting correlated noise over signals
            print "... NEXT showing signal and skynoise ...PRESS <Enter>"
            raw_input()
            self.signal(skynoise=0)
            self.signal(skynoise=1, overplot=1, ci=2)

        self.MessHand.longinfo("subtracting CN from Data")

        for iChan in chanListIndexes:
            data[:, iChan] = (data[:, iChan]-correlatedNoise[:, iChan]).astype(np.float32)

        if plot:
            print "... NEXT showing residual signal ...PRESS <Enter>"
            raw_input()
            self.signal(skynoise=0)

        self.Data       = data
        self.__resetStatistics()

    def correlatedNoiseRemoval(self, chanList=[], threshold=1.e-3, iterMax=4, plot=0, \
                               coreRadius=30, beta=2., chanRef=17, fastnoise=0):
        """Deprecated : see removeCorrealatedNoise()"""
        self.MessHand.warning('Deprecated method, use ReaDataAnalyser.DataAna.removeCorrelatedNoise()')
        self.removeCorrelatedNoise(chanList=chanList, threshold=threshold, iterMax=iterMax, plot=plot, coreRadius=coreRadius, beta=beta, chanRef=chanRef, fastnoise=fastnoise)

    # -------------------------------------------------------------------
    # ---- correlated noise reduction by PCA ----------------------------
    # -------------------------------------------------------------------


    def removePrincipalComponent(self,chanList=[],order=1,subscan=False,minChanNum=0):
        """remove the correlated noise from the data
             by principal component analysis

        Parameters
        ----------
        chanList : list of int
            list of channel to flag
        order : int
            number of principal components to remove
        subscan : bool
            do the PCA subscan by subscan? default no
        minChanNum : int
            minimum number of valid channels to do PCA (default order+2)
        """

        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if not chanList.any() :
            self.MessHand.warning('PCA: no valid channels, nothing will be done')
            return

        if not minChanNum:
            minChanNum = order+2

        if (chanList.shape[0] <= minChanNum):
            self.MessHand.warning('PCA: not enough valid channels, nothing will be done')
            return

        # Retrieve only the requested channels
        Data = copy.copy(np.take(self.Data, chanListIndexes, axis=1))

        self.MessHand.info('Doing PCA of order '+str(order))

        if subscan:
            for i in xrange(len(self.ScanParam.SubscanNum)):
                self.MessHand.longinfo('   subscan '+str(self.ScanParam.SubscanNum[i]))
                # concatenate data of good channels
                first = self.ScanParam.SubscanIndex[0, i]
                last = self.ScanParam.SubscanIndex[1, i]
                pcadata, eigenvals, eigenvect = principalComponentAnalysis(Data[first:last,:], order)

                for j, iChanIndex in enumerate(chanListIndexes):
                    # self.CorrelatedNoise[:,iChanIndex] = self.Data[:,iChanIndex] - \
                    #     pcadata[:,j].astype(self.Data.dtype.char)
                    self.Data[first:last, iChanIndex] = pcadata[:, j]

        else:
            # concatenate data of good channels
            pcadata, eigenvals, eigenvect = principalComponentAnalysis(Data, order)
            self.__pca_eigenvalues = eigenvals
            self.__pca_eigenvectors = eigenvect

            for j, iChanIndex in enumerate(chanListIndexes):
                self.CorrelatedNoise[:, iChanIndex] = self.Data[:, iChanIndex] - pcadata[:, j]
                self.Data[:, iChanIndex] = pcadata[:, j].copy()

        self.Data.astype(Data.dtype)

        self.__pcaDone = True
        self.__resetStatistics()


    def corrPCA(self,chanList=[],order=1,subscan=0,minChanNum=0):
        """Deprecated : see removePrincipalComponent()"""
        self.MessHand.warning('Deprecated method, use ReaDataAnalyser.DataAna.removePrincipalComponent()')
        self.removePrincipalComponent(order=order, subscan=subscan, minChanNum=ChanNum)

    # -------------------------------------------------------------------
    # ---- baseline methods ---------------------------------------------
    # -------------------------------------------------------------------
    def polynomialBaseline(self,chanList=[],order=0, subscan=True, plot=False, subtract=True):
        """polynomial baseline removal on the Data.

        Parameters
        ----------
        chanList : list of int
            list of channel to flag (default: all; [] : current list)
        order : int
            polynomial order, >0
        subscan : bool
            compute baseline per subscan (default: yes)
        plot : bool
            plot the signal and the fitted polynomials (default: no)
        subtract : bool
            subtract the polynomial from the data (default: yes)
        """

        self.MessHand.debug('basePoly start...')

        # check polynomial order
        if order < 0:
            self.MessHand.error("polynomial order must be positive! ")
            return
        if order > 15:
            self.MessHand.warning("fitting is known to fail with high-order polynomial")

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        Data            = self.Data
        DataFlags       = self.FlagHandler.getFlags().copy()
        time            = self.ScanParam.get('MJD', flag='None')
        timeSub         = self.ScanParam.get('MJD', flag='None')

        # retrieve subscan index
        if subscan:
            subscanIndex = self.ScanParam.SubscanIndex
        else:
            subscanIndex = np.array([[0], [self.ScanParam.NInt]])

        if subscan and len(subscanIndex[0]) > 0:
            for i in xrange(1, len(subscanIndex[0])):
                timeSub[subscanIndex[0, i]:subscanIndex[1, i]] -= time[subscanIndex[0, i]]

        poly = fBaseline.arrayfitpoly_s(chanListIndexes, Data, DataFlags,
                                        timeSub, subscanIndex, order)

        # TODO FIX :
        # In the case of scan or single subscan fortran receive a 1d
        # array for iPoly instead of a [1,x] array.

        if plot:
            self.signal(chanList)
            dataX = []
            dataY = []

            for i in xrange(len(chanList)):
                iPoly = poly[i,:,:]
                iData = Data[:, chanListIndexes[i]]
                X, n = fUtilities.compress(time, DataFlags[:, chanListIndexes[i]], 0)
                dataX.append(X[:n])
                Y = fBaseline.evalchunkedpoly(timeSub, subscanIndex, iPoly)
                Y, n = fUtilities.compress(Y, DataFlags[:, chanListIndexes[i]], 0)
                dataY.append(Y[:n])

            MultiPlot.plot(chanList, dataX, dataY, overplot=1, ci=2, style='l')

        if subtract:
            if len(chanListIndexes) > 0:
                Data = fBaseline.subtractpoly(chanListIndexes, Data,
                                              timeSub, subscanIndex, poly)
                self.Data = Data
                self.__resetStatistics()
            else:
                self.MessHand.warning("Due to some bug (f2py?) subtraction is not possible on single channel")

        self.MessHand.debug('... basePoly end')

    # -----------------------------------------------------------------
    def medianBaseline(self,chanList=[],subscan=False,order=0):
        """baseline: Remove median value per channel and per subscan

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        subscan : bool
            compute baseline per subscan (default: yes)
        order : int
            polynomial order (default: 0)
        """

        self.MessHand.debug('medianBaseline start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if order > 1:
            self.MessHand.warning("order > 1 not implemented yet - subtracting order 1")
            order = 1

        if not self.__statisticsDone:
            self.__statistics()

        if subscan:
            nbSub    = len(self.ScanParam.SubscanNum)
            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                for sub in xrange(nbSub):
                    lo = self.ScanParam.SubscanIndex[0, sub]
                    hi = self.ScanParam.SubscanIndex[1, sub]
                    if order:
                        # compute median of delta_signal / delta_time
                        t = self.getChanData('mjd', chan,
                                             subscans=[self.ScanParam.SubscanNum[sub]])
                        tall = self.getChanData('mjd', chan,
                                                subscans=[self.ScanParam.SubscanNum[sub]],
                                                flag='None')
                        f = self.getChanData('flux', chan,
                                             subscans=[self.ScanParam.SubscanNum[sub]])

                        dt = t-t[0]
                        df = f-f[0]
                        med = fStat.f_median(df[1:]/dt[1:])
                        # compute product median * time
                        med_t = np.array(med, 'd')*tall
                        self.Data[lo:hi, chanNum] -= med_t.astype(np.float)
                    else:
                        # order 0
                        self.Data[lo:hi, chanNum] -= self.ChanMed_s[chanNum, sub]
        else:
            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                self.Data[:, chanNum] -= np.array(self.ChanMed[chanNum]).astype(np.float32)

        self.__resetStatistics()
        if order:
            # a first-order has been subtracted, need to subtract 0-order afterwards
            self.medianBaseline(order=0, subscan=subscan, chanList=chanList)

        self.MessHand.debug('... medianBaseline end')


    # -----------------------------------------------------------------
    def zeroStart(self,chanList=[],subscan = False):
        """make signal start at zero

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        subscan : bool
            compute zero per subscan? (default: no)
        """

        self.MessHand.debug('zeroStart start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if subscan:
            nbSub    = len(self.ScanParam.SubscanNum)
            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                for sub in xrange(nbSub):
                    # get only non-flagged data
                    subnum = self.ScanParam.SubscanNum[sub]
                    flux = self.getChanData('flux', chan, subscans=[subnum])
                    lo = self.ScanParam.SubscanIndex[0, sub]
                    hi = self.ScanParam.SubscanIndex[1, sub]
                    self.Data[lo:hi, chanNum] = self.Data[lo:hi, chanNum] - \
                                               np.array(flux[0], np.float)
        else:
            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                flux = self.getChanData('flux', chan)
                self.Data[:, chanNum] = self.Data[:, chanNum] - np.array(flux[0], np.float)

        self.__resetStatistics()
        self.MessHand.debug('... zeroStart end')

    # -----------------------------------------------------------------
    def zeroEnds(self,chanList=[],subscan=False):
        """make signal start AND end at zero, by subtracting an order-1 baseline

        Parameters
        ----------
        chanList listt of int
            list of channels to process (default: [] = current list)
        subscan : bool
            compute baseline per subscan? (default: no)
        """

        self.MessHand.debug('zeroEnds start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # get full time array (also on flagged timestamps)
        mjd = self.ScanParam.get('mjd', flag='None')

        if subscan:
            nbSub    = len(self.ScanParam.SubscanNum)
            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                for sub in xrange(nbSub):
                    lo = self.ScanParam.SubscanIndex[0, sub]
                    hi = self.ScanParam.SubscanIndex[1, sub]
                    tt = self.getChanData('mjd', chan,
                                          subscans=[self.ScanParam.SubscanNum[sub]])
                    ss = self.getChanData('flux', chan,
                                          subscans=[self.ScanParam.SubscanNum[sub]])
                    if len(tt) > 0.:
                        slope = (ss[-1]-ss[0]) / (tt[-1]-tt[0])
                        zero  = ss[0] - slope*tt[0]
                        base1 = slope * mjd[lo:hi] + zero
                        base1 = base1.astype(np.float)
                        self.Data[lo:hi, chanNum] = self.Data[lo:hi, chanNum] - base1
        else:
            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                tt = self.getChanData('mjd', chan)
                ss = self.getChanData('flux', chan)
                slope = (ss[-1]-ss[0]) / (tt[-1]-tt[0])
                zero  = ss[0] - slope*tt[0]
                base1 = slope * mjd + zero
                self.Data[:, chanNum] = self.Data[:, chanNum] - base1.astype(np.float)

        self.__resetStatistics()
        self.MessHand.debug('... zeroEnds end')

    # -----------------------------------------------------------------
    def medianFilter(self,chanList=[],window=20,subtract=1,plot=0,limitsX=[], limitsY=[]):
        """median filtering: remove median values computed over sliding window

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        window : int
            number of samples to compute median
        subtract : bool
            subtract from data? (default: yes)
        plot : bool
            plot the result? (default: no)
        limitsX, limitsY : float array
            limits to use in X/Y for the plot
        """

        self.MessHand.debug('medianFilter start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if plot:
            self.signal(chanList, limitsX=limitsX, limitsY=limitsY)

        median = []
        for chan in chanList:
            chanNum = self.ReceiverArray.getChanIndex(chan)[0]
            data = self.getChanData('flux', chan)
            nbSamp = len(data)
            median1Chan = []
            for i in xrange(nbSamp):
                if i < window/2:
                    median1Chan.append(fStat.f_median(data[:i+1]))
                elif i > nbSamp-window/2:
                    median1Chan.append(fStat.f_median(data[i:]))
                else:
                    median1Chan.append(fStat.f_median(data[i-window/2:i+window/2]))

            if subtract:
                # TODO: take care of flagged data!
                self.Data[:, chanNum] = self.Data[:, chanNum] - np.array(median1Chan).astype(np.float32)

            median.append(np.array(median1Chan).astype(np.float32))

        if plot:
            dataX = self.getChanListData('MJD', chanList)
            MultiPlot.plot(chanList, dataX, median, style='l', ci=2, overplot=1, \
                    labelX="MJD - MJD(0) [sec]", labelY="Flux density [arb.u.]")

        if subtract:
            self.__resetStatistics()
        self.MessHand.debug('... medianFilter end')

        return median

    # -----------------------------------------------------------------
    def __computeMeanSignal(self,chanList=[]):
        """compute mean value of the signals at each timestamp

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)

        Returns
        -------
        float array
            this function returns a 1D array containing the mean value
            of all non-flagged data at each timestamp
        """

        self.MessHand.debug('computeMeanSignal start...')
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # get all data, also flagged ones - flags will be handled in fortran
        fluxes = self.getChanListData('flux', chanList, channelFlag='None', dataFlag='None')
        flags  = self.getChanListData('flag', chanList, channelFlag='None', dataFlag='None')

        # Here the 1st dimension correspond to channels - that's what we want
        Mean = fStat.arraymean(fluxes, flags)

        # Now keep only values where timestamps are not flagged
        good = np.nonzero(self.ScanParam.FlagHandler.isUnsetMask())
        result = np.take(Mean, good)
        self.MessHand.debug('...computeMeanSignal end')
        return result

    # -----------------------------------------------------------------
    def __computeMedianSignal(self,chanList=[]):
        """compute median value of the signals at each timestamp

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)

        Returns
        -------
        float array
            this function returns a 1D array containing the median
            value of all non-flagged data at each timestamp
        """

        self.MessHand.debug('computeMedianSignal start...')
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # get all data, also flagged ones - flags will be handled in fortran
        fluxes = self.getChanListData('flux', chanList, channelFlag='None', dataFlag='None')
        flags  = self.getChanListData('flag', chanList, channelFlag='None', dataFlag='None')

        # Here the 1st dimension correspond to channels - that's what we want
        Med = fStat.arraymedian(fluxes, flags)

        # Now keep only values where timestamps are not flagged
        good = np.nonzero(self.ScanParam.FlagHandler.isUnsetMask())
        result = np.take(Med, good)
        self.MessHand.debug('...computeMedianSignal end')
        return result

    # -----------------------------------------------------------------
    def __computeMedianAbsSignal(self,chanList=[]):
        """compute median value of absolute values of signals at each timestamp

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)

        Returns
        -------
        float array
            this function returns a 1D array containing the median
            value of all non-flagged data at each timestamp
        """

        self.MessHand.debug('computeMedianAbsSignal start...')
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # get all data, also flagged ones - flags will be handled in fortran
        fluxes = self.getChanListData('flux', chanList, channelFlag='None', dataFlag='None')
        fluxes = absolute(fluxes)
        flags  = self.getChanListData('flag', chanList, channelFlag='None', dataFlag='None')

        # Here the 1st dimension correspond to channels - that's what we want
        Med = fStat.arraymedian(fluxes, flags)

        # Now keep only values where timestamps are not flagged
        good = np.nonzero(self.ScanParam.FlagHandler.isUnsetMask())
        result = np.take(Med, good)
        self.MessHand.debug('...computeMedianAbsSignal end')
        return result

    # -----------------------------------------------------------------
    def __computeMedianFlatField(self,chanList=[],chanRef=0):
        """compute flat field as median of signal ratio between channels

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        chanRef : int
            reference channel number
              * any channel number
              * 0 use Reference chan
              * -1 use mean signal as reference
              * -2 use median signal as reference
        """

        self.MessHand.debug('computeMedianFlatField start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if chanRef == 0:
            chanRef = self.ReceiverArray.RefChannel
        if chanRef > -1:
            chanRefIndex = self.ReceiverArray.getChanIndex(chanRef)[0]
            if chanRefIndex ==  -1:
                self.MessHand.error("chanRef: channel not used")
                return
            refFlags = self.FlagHandler.getFlags()[:, chanRefIndex].astype(np.int32)
        elif chanRef == -1:
            refFlags = self.ScanParam.FlagHandler.getFlags()
            refSignalFull = self._DataAna__computeMeanSignal(chanList)
                        # full non-flagged time stream
            goodFlagRef   = np.nonzero(self.ScanParam.FlagHandler.isUnsetMask())
                        # corresponding indices
        elif chanRef == -2:
            refFlags = self.ScanParam.FlagHandler.getFlags()
            refSignalFull = self._DataAna__computeMedianSignal(chanList)
            goodFlagRef   = np.nonzero(self.ScanParam.FlagHandler.isUnsetMask())

        for chan in chanList:
            num = self.ReceiverArray.getChanIndex(chan)[0]
            if chan == chanRef:
                self.FF_Median[num] = 1.
            else:
                # we consider only datapoints where both ref chan. and current
                # chan are not flagged
                chanFlags  = self.FlagHandler.getFlags()[:, num].astype(np.int8)
                chanSignal = self.getChanData('flux', chan, flag2 = refFlags)
                if chanRef > -1:
                    refSignal  = self.getChanData('flux', chanRef, flag2 = chanFlags)
                else:
                    chanFlags = np.take(chanFlags, goodFlagRef)
                    flagHandler = ReaFlagHandler.createFlagHandler(chanFlags)
                    good = np.nonzero(flagHandler.isUnsetMask())
                    refSignal = np.take(refSignalFull, good)

                if len(refSignal) == 0 or len(chanSignal) == 0:
                    # this happens if too much is flagged
                    self.MessHand.warning("Too much flags, could not determine FF for chan. %s"%(chan))
                    ratio = 1.
                else:
                    ratio = fStat.f_median(chanSignal / refSignal)
                self.FF_Median[num] = ratio

        self.MessHand.debug('... computeMedianFlatField end')

    # -----------------------------------------------------------------
    def __applyFlatField(self,chanList=[]):
        """divide signals by bolo gains to normalise them

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        """

        self.MessHand.debug('applyFlatField start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        for chan in chanList:
            num = self.ReceiverArray.getChanIndex(chan)[0]
            self.Data[:, num] = self.Data[:, num] / np.array((self.FFCF_Gain[num]), np.float32)

        self.__resetStatistics()
        self.MessHand.debug('... applyFlatField end')

    def flatfield(self,chanList=[],method='point'):
        """divide signals by bolo gains to normalise them

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        method : str
            choose which flat field to apply:
             * point [default] = use point source relative gains
             * median = use correlate noise relative gains
             * extend = use relative gains to extended emission
        """
        self.MessHand.debug('flatfield start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if method == 'point':
            self.FFCF_Gain = self.ReceiverArray.Gain
        elif method == 'median':
            self.FFCF_Gain = self.FF_Median
        elif method == 'extend':
            self.FFCF_Gain = self.ReceiverArray.ExtGain
        self.__applyFlatField(chanList=chanList)

    # -----------------------------------------------------------------
    def __computeMedianNoise(self,chanList=[]):
        """compute median noise, i.e. median of all bolos (normalised!) at
             each individual timestamp

        Parameters
        ----------
        chanList : list of int
            list of channels to process (default: [] = current list)
        """

        self.MessHand.debug('computeMedianNoise start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return
        alldata  = np.array(self.getChanListData('flux', chanList, channelFlag='None', dataFlag='None'), np.float32)
        allFlags = np.array(self.getChanListData('flag', chanList, channelFlag='None', dataFlag='None'))

        # Correct for median flat field
        for i in xrange(len(chanList)):
            num = self.ReceiverArray.getChanIndex(chanList[i])[0]
            alldata[i,:] = alldata[i,:] / np.array((self.FF_Median[num]), np.float32)

        # Number of integrations
        nInt = self.ScanParam.NInt
        skynoise = fStat.arraymedian(alldata, allFlags)
        skynoise = np.reshape(np.tile(skynoise, self.ReceiverArray.NUsedChannels), (self.ReceiverArray.NUsedChannels, nInt))
        self.Skynoise = as_column_major_storage(skynoise.transpose())

        self.MessHand.debug('... computeMedianNoise end')

    #-----------------------------------------------------------------------

    def medianNoiseLocal(self, chanList=[], chanRef=-2, computeFF=True,factor=1.,
                            numCorr=7, minDist=0., selByDist=False,outputChanList=False):

        """remove median noise from the data by using only the n most correlated channels w.r.t. each receiver

        Parameters
        ----------
        chanList : list of int
            list of channels (default: [] = current list)
        chanRef : int
            channel number or
             * -1 to compute relative gains w.r.t. mean signal
             * -2 to compute relative gains w.r.t. median signal (default)
        computeFF : bool
            compute skynoise FF (def.) or use existing FF_Median?
        factor : float
            fraction of skynoise to be subtracted (default: 100%)
        numCorr : int
            number of (most correlated) channels to use to compute the sky noise for each channel
        minDist : float
            minimum distance on sky, in ARCSEC, between channels to be considered (useful for extended emission)
        selByDist : boll
            set this to select the n closest channels (outside minDist) instead of the most correlated ones
        outputChanList : bool
            set this to obtain the list of most correlated channels in output
        """


        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return
        chanListIndices = self.ReceiverArray.getChanIndex(chanList)

        # compute the correlation matrix (stored in self.CorMatrix)
        self.computeWeights()

        # copy the data to have something to work on
        # (while data array itself is kept intact until the end)
        wdata = copy.deepcopy(self.Data)

        # loop over channles, remove noise from one channel at a time
        chanIndexList = []
        noiseChanList = []
        for chanIn in chanList:

            # get chan index
            chanIndex = self.ReceiverArray.getChanIndex(chanIn)[0]
            chanIndexList.append(chanIndex)

            # get channel separations
            chanSep = np.take(self.ReceiverArray.ChannelSep[:, chanIndex], chanListIndices)

            # determine correlations
            corr = np.take(self.CorMatrix[:, chanIndex], chanListIndices)

            if selByDist:
                mask = np.where((corr > -1.) and (corr <= 1.) and (chanSep > minDist), 1, 0)
                newList = np.compress(mask, chanList)
                newSep = np.compress(mask, chanSep)
                maxCorList = tolist_rea(np.take(newList, np.argsort(newSep)[:(abs(numCorr))]))
            else:
                mask = np.where((corr > -1.) and (corr <= 1.) and (chanSep > minDist), 1, 0)
                corr = np.compress(mask, corr)
                newList = np.compress(mask, chanList)
                # select
                maxCorList = tolist_rea(np.take(newList, np.argsort(corr)[-(abs(numCorr)):]))

            # make sure current channel is in list
            if not chanIn in maxCorList:
                maxCorList.append(chanIn)

            print str(chanIn)+' '+str(maxCorList)
            noiseChanList.append(maxCorList)

            # compute flatfield and median noise for new list
            if computeFF:
                self.__computeMedianFlatField(maxCorList, chanRef=chanRef)

            self.__computeMedianNoise(maxCorList)

            wdata[:, chanIndex] = self.Data[:, chanIndex] - self.Skynoise[:, chanIndex] * \
                                 np.array(self.FF_Median[chanIndex]*factor, np.float32)

        self.Data = copy.deepcopy(wdata)

        self.__resetStatistics()

        if outputChanList:
            noiseLocalOut = []
            noiseLocalOut.append(chanIndexList)
            noiseLocalOut.append(noiseChanList)
            return noiseLocalOut


    #-----------------------------------------------------------------------

    def medianNoiseFromList(self, cList, chanRef=-2, computeFF=1,factor=1.):
        """remove median noise from the data by using only the channels provided in input

        Parameters
        ----------
        cList : list of int
            list of channels as returned by medianNoiseLocal
        chanRef : int
            reference channel number (default: RefChannel;
              * -1 to compute relative gains w.r.t. mean signal
              * -2 to compute relative gains w.r.t. median signal
        computeFF : bool
            compute skynoise FF (def.) or use existing FF_Median?
        factor : float
            fraction of skynoise to be subtracted (default: 100%)
        """


        # check input channel list
        # Must consist of two sub-lists
        if (len(cList) != 2):
            self.MessHand.error("invalid channel list")
            return
        # First list contains the channel indices
        chanListIndices = cList[0]
        nChan = len(chanListIndices)
        # Second list contains the channels from which to estimate the noise
        noiseChanList = cList[1]
        if (len(noiseChanList) != nChan):
            self.MessHand.error("invalid channel list")
            return

        # copy the data to have something to work on
        # (while data array itself is kept intact until the end)
        wdata = copy.deepcopy(self.Data)

        # loop over channles, remove noise from one channel at a time
        for ind, maxCorList in enumerate(noiseChanList):

            # compute flatfield and median noise for new list
            if computeFF:
                self.__computeMedianFlatField(maxCorList, chanRef=chanRef)
            self.__computeMedianNoise(maxCorList)

            # Remove median noise
            wdata[:, chanListIndices[ind]] = self.Data[:, chanListIndices[ind]] - \
                          self.Skynoise[:, chanListIndices[ind]] * np.array(self.FF_Median[chanListIndices[ind]]*factor, np.float32)

        self.Data = copy.deepcopy(wdata)

        self.__resetStatistics()

    #-----------------------------------------------------------------------
    def removeMedianNoise(self, chanList=[], chanRef=-2, computeFF=True,
                           factor=1.,nbloop=1):
        """remove median noise from the data

        Parameters
        ----------
        chanList : list of int
            list of channels (default: [] = current list)
        chanRef : int
            reference channel number (default: RefChannel;
             * -1 to compute relative gains w.r.t. mean signal
             * -2 to compute relative gains w.r.t. median signal
        computeFF : bool
            compute skynoise FF (def.) or use existing FF_Median?
        factor : float
            fraction of skynoise to be subtracted (default: 100%)
        nbloop : int
            number of iterations (default: 1)
        """

        self.MessHand.debug('removeMedianNoise start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        for i in xrange(nbloop):
            if computeFF:
                self.__computeMedianFlatField(chanList, chanRef=chanRef)

            self.__computeMedianNoise(chanList)
            for chan in chanList:
                num = self.ReceiverArray.getChanIndex(chan)[0]
                self.Data[:, num] = self.Data[:, num] - self.Skynoise[:, num] * \
                                   np.array(self.FF_Median[num]*factor, np.float32)

        self.__resetStatistics()
        self.MessHand.debug('... removeMedianNoise end')

    def medianNoiseRemoval(self, chanList=[], chanRef=-2, computeFF=True,
                           factor=1.,nbloop=1):
        """Deprecated : see removeMedianNoise()"""
        self.MessHand.warning('Deprecated method, use ReaDataAnalyser.DataAna.removeMedianNoise()')
        self.removeMedianNoise(chanList=chanList, chanRef=chanRef,
                               computeFF=computeFF, factor=factor,
                               nbloop=nbloop)
    #-----------------------------------------------------------------------
    def averageNoiseRemoval(self, chanList=[], chanRef=0):
        """remove correlated noise computed as average value of all but
             the reference channel

        Parameters
        ----------
        chanList : list of int
            list of channels (default: [] = all valid channels)
        chanRef : int
            reference channel number, not used to compute the average noise
        """
        self.MessHand.debug('averageNoiseRemoval start...')

        # check channel list
        chanList = self.ReceiverArray.checkChanList(chanList)
        chanList = chanList.tolist()
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        tmpList = copy.copy(chanList)
        if chanRef:
            if not chanList.count(chanRef):
                self.MessHand.warning("Ref. channel not in Chanlist, average")
                self.MessHand.warning("noise not subtracted from ref. channel")
            else:
                tmpList.remove(chanRef)

        if tmpList:
            tmpData = self.getChanListData('flux', chanList=tmpList, dataFlag='None')
            tmpFlag = self.getChanListData('flag', chanList=tmpList, dataFlag='None')
            noise = fStat.arraymean(tmpData, tmpFlag)

            for chan in chanList:
                chanNum = self.ReceiverArray.getChanIndex(chan)[0]
                self.Data[:, chanNum] = self.Data[:, chanNum] - noise
        else:
            self.MessHand.warning("No channel available to compute noise")

    #-----------------------------------------------------------------------
    #-----------------------------------------------------------------------
    def correctOpacity(self,tau=0.):
        """correct for atmospheric opacity

        Parameters
        ----------
        tau : float
            the zenit opacity

        Notes
        -----
        the data are multiplied by the line of sigth tau as
            \propto exp(tau/sin(el))
        """
        self.MessHand.debug('correctOpacity start...')
        if not tau:
            self.MessHand.warning("No tau value provided - exiting")
            return

        # Save the value in the ScanParam Object for further retrieval
        self.ScanParam.Tau = tau


# use median value
#       el = self.ScanParam.get('el')
#       med_el = fStat.f_median(el)
#       tauLos = tau/np.sin(med_el * pi / 180.)
#       self.Data *= np.array(exp(tauLos),np.float)

# Use center of the array value
#       el = self.ScanParam.get('el',flag='None',getFlagged=0)
#       tauLos   = tau/np.sin(el*np.pi/180)
#       self.Data = (np.transpose(np.transpose(self.Data)*exp(tauLos))).astype(np.float32)

        # Use Channel elevation value

        data = self.Data

        chanList = self.ReceiverArray.checkChanList("all")
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        # return Data index
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        for index in xrange(len(chanList)):
            el = self.getChanData('el', chanList[index], flag='None')
            tauLos   = tau/np.sin(np.radians(el))
            data[:, chanListIndexes[index]] = (data[:, chanListIndexes[index]]*exp(tauLos)).astype(np.float32)

        self.Data = data

        self.__resetStatistics()
        self.MessHand.debug('... correctOpacity end')

#---------------------------------------------------------------------
    def addSourceModel(self,model,chanList='all',factor=1.):
        """add data according to a model map

        Parameters
        ----------
        model : ReaMapping.Image object
            the input model map (with WCS)
        chanList : list of int
            the list of channels to work with
        factor : float
            add model data multiplied with this factor

        """
        # check channel list
        self.MessHand.info('adding source model ...')
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        XYOffsets = np.array([self.ScanParam.get('RA', flag='None'), \
                           self.ScanParam.get('Dec', flag='None')])

        rotAngles = np.array(self.ScanParam.ParAngle)
        chanListAzEl = np.array(self.ReceiverArray.UsedChannels)-1

        # TODO : Use the proper routine... ScanParam.getChanSep()
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
        # self.Data = copy.copy(tmp)
        self.Data = tmp
        tmp = 0  # free memory
        self.MessHand.info('...done')

    #-----------------------------------------------------------------------
    # rebin: down sample the data by a factor 2
    #-----------------------------------------------------------------------
    def rebin(self):
        """Timeline average integrations 2 by 2"""

        NInt = self.ScanParam.NInt
        NCh  = self.Data.shape[1]

        newData = np.zeros((NInt/2, NCh), np.float32)
        newWeig = np.ones((NInt/2, NCh), np.float32)
        newFlag = np.zeros((NInt/2, NCh), np.int8)

        newBasLat = np.zeros((NInt/2), np.float32)
        newBasLon = np.zeros((NInt/2), np.float32)
        newAz     = np.zeros((NInt/2), np.float32)
        newEl     = np.zeros((NInt/2), np.float32)
        newAzOff  = np.zeros((NInt/2), np.float32)
        newElOff  = np.zeros((NInt/2), np.float32)
        newLatOff = np.zeros((NInt/2), np.float32)
        newLonOff = np.zeros((NInt/2), np.float32)
        newRot    = np.zeros((NInt/2), np.float32)
        newPar    = np.zeros((NInt/2), np.float32)
        newLST    = np.zeros((NInt/2), np.float32)
        newMJD    = np.zeros((NInt/2), np.float64)
        newRA     = np.zeros((NInt/2), np.float32)
        newDec    = np.zeros((NInt/2), np.float32)
        newRAOff  = np.zeros((NInt/2), np.float32)
        newDecOff = np.zeros((NInt/2), np.float32)
        newFlags  = np.zeros((NInt/2), np.int32)
        newFocX   = np.zeros((NInt/2), np.float32)
        newFocY   = np.zeros((NInt/2), np.float32)
        newFocZ   = np.zeros((NInt/2), np.float32)

        two = np.array((2.), np.float32)

        for i in xrange(NInt/2):
            newData[i,:] = (self.Data[2*i,:] + self.Data[2*i+1,:])/two
            newWeig[i,:] = (self.DataWeights[2*i,:] + self.DataWeights[2*i+1,:])/two
            # Flags: flag new datapoint if one of the two is flagged
            tmpFlag      = np.bitwise_or(self.FlagHandler.getFlags()[2*i,:], \
                                      self.FlagHandler.getFlags()[2*i+1,:])
            newFlag[i,:] = tmpFlag.astype(np.int8)

            # ScanParam attributes
            newFlags[i]  = np.bitwise_or(self.ScanParam.FlagHandler.getFlags()[2*i], \
                                      self.ScanParam.FlagHandler.getFlags()[2*i+1])
            newBasLat[i] = (self.ScanParam.BasLat[2*i] + self.ScanParam.BasLat[2*i+1])/2.
            newBasLon[i] = (self.ScanParam.BasLon[2*i] + self.ScanParam.BasLon[2*i+1])/2.
            newAz[i]     = (self.ScanParam.Az[2*i]     + self.ScanParam.Az[2*i+1])/2.
            newEl[i]     = (self.ScanParam.El[2*i]     + self.ScanParam.El[2*i+1])/2.
            newAzOff[i]  = (self.ScanParam.AzOff[2*i]  + self.ScanParam.AzOff[2*i+1])/2.
            newElOff[i]  = (self.ScanParam.ElOff[2*i]  + self.ScanParam.ElOff[2*i+1])/2.
            newLatOff[i] = (self.ScanParam.LatOff[2*i] + self.ScanParam.LatOff[2*i+1])/2.
            newLonOff[i] = (self.ScanParam.LonOff[2*i] + self.ScanParam.LonOff[2*i+1])/2.
            newRot[i]    = (self.ScanParam.Rot[2*i]    + self.ScanParam.Rot[2*i+1])/2.
            newPar[i]    = (self.ScanParam.ParAngle[2*i] + self.ScanParam.ParAngle[2*i+1])/2.
            newLST[i]    = (self.ScanParam.LST[2*i]    + self.ScanParam.LST[2*i+1])/2.
            newMJD[i]    = (self.ScanParam.MJD[2*i]    + self.ScanParam.MJD[2*i+1])/2.
            newRA[i]     = (self.ScanParam.RA[2*i]     + self.ScanParam.RA[2*i+1])/2.
            newDec[i]    = (self.ScanParam.Dec[2*i]    + self.ScanParam.Dec[2*i+1])/2.
            newRAOff[i]  = (self.ScanParam.RAOff[2*i]  + self.ScanParam.RAOff[2*i+1])/2.
            newDecOff[i] = (self.ScanParam.DecOff[2*i] + self.ScanParam.DecOff[2*i+1])/2.
            newFocX[i]   = (self.ScanParam.FocX[2*i]   + self.ScanParam.FocX[2*i+1])/2.
            newFocY[i]   = (self.ScanParam.FocY[2*i]   + self.ScanParam.FocY[2*i+1])/2.
            newFocZ[i]   = (self.ScanParam.FocZ[2*i]   + self.ScanParam.FocZ[2*i+1])/2.

        self.Data        = as_column_major_storage(newData)
        self.DataWeights = as_column_major_storage(newWeig)
        self.FlagHandler = ReaFlagHandler.createFlagHandler(newFlag)

        self.ScanParam.BasLat = as_column_major_storage(newBasLat)
        self.ScanParam.BasLon = as_column_major_storage(newBasLon)
        self.ScanParam.Az     = as_column_major_storage(newAz)
        self.ScanParam.El     = as_column_major_storage(newEl)
        self.ScanParam.AzOff  = as_column_major_storage(newAzOff)
        self.ScanParam.ElOff  = as_column_major_storage(newElOff)
        self.ScanParam.LatOff = as_column_major_storage(newLatOff)
        self.ScanParam.LonOff = as_column_major_storage(newLonOff)
        self.ScanParam.Rot    = as_column_major_storage(newRot)
        self.ScanParam.ParAngle = as_column_major_storage(newPar)
        self.ScanParam.LST    = as_column_major_storage(newLST)
        self.ScanParam.MJD    = as_column_major_storage(newMJD)
        self.ScanParam.RA     = as_column_major_storage(newRA)
        self.ScanParam.Dec    = as_column_major_storage(newDec)
        self.ScanParam.RAOff  = as_column_major_storage(newRAOff)
        self.ScanParam.DecOff = as_column_major_storage(newDecOff)
        self.ScanParam.FocX   = as_column_major_storage(newFocX)
        self.ScanParam.FocY   = as_column_major_storage(newFocY)
        self.ScanParam.FocZ   = as_column_major_storage(newFocZ)
        self.ScanParam.FlagHandler = ReaFlagHandler.createFlagHandler(newFlags)


        self.ScanParam.NInt = NInt/2
        for i in xrange(len(self.ScanParam.SubscanNum)):
            self.ScanParam.SubscanIndex[0][i] = self.ScanParam.SubscanIndex[0][i]/2
            self.ScanParam.SubscanIndex[1][i] = self.ScanParam.SubscanIndex[1][i]/2

        self._DataAna__resetStatistics()


    # -------------------------------------------------------------------
    # computeWeight: fill DataWeights attribute
    # -------------------------------------------------------------------
    def computeWeight(self,method='rms',subscan=0, lolim=0.1, hilim=10.0):
        """compute weights and store them in DataWeights attribute

        Parameters
        method : str
            type of weighting (default='rms')
            * 'rms' : use 1/rms^2
            * 'wrms' : user sqrt(nInt) / rms^2
            * 'pow' : use 1/pow^2, where pow is the mean power between
                      frequencies lolim and hilim (in Hz)
                      - lolim  : low frequency limit for 'pow' method
                              default=0.1 Hz
                      - hilim  : high freq. limit for 'pow' method
                              default=10.0 Hz
                      hilim and lolim are ignored unless method='pow'
        subscan : bool
            compute weight by subscan? ignored if method='pow'
        """
        if not self.__statisticsDone:
            self.__statistics()

        if method == 'rms':
            if subscan:
                subnum = self.ScanParam.SubscanNum
                subrms = self.ChanRms_s
                subin = self.ScanParam.SubscanIndex
                for s in xrange(len(subnum)):
                    r = subrms[:, s]
                    weight = np.zeros(r.shape, np.float)
                    for ch in xrange(len(r)):
                        if (r[ch] > 0.0):
                            weight[ch] = 1./r[ch]**2  #

                for i in xrange(subin[0, s], subin[1, s]):
                    self.DataWeights[i,:] = weight.astype(np.float32)

            else:
                r = self.ChanRms
                weight = np.zeros(r.shape, np.float)
                for i in xrange(len(r)):
                    if str(r[i]) != str(float('nan')):
                        weight[i] = 1./r[i]**2  # NaNs will have zero weight

                for i in xrange(0, self.ScanParam.NInt):
                    self.DataWeights[i,:] = weight.astype(np.float32)

        elif method == 'wrms':
            r = self.ChanRms
            weight = np.zeros(r.shape, np.float)
            for i in xrange(len(r)):
                if str(r[i]) != str(float('nan')):
                    weight[i] = 1./r[i]**2  # NaNs will have zero weight
            weight = weight*np.sqrt(self.ScanParam.NInt)

            for i in xrange(0, self.ScanParam.NInt):
                self.DataWeights[i,:] = weight.astype(np.float32)

        elif method == 'pow':
            (c, x, y) = self.plotFFT('all', returnSpectrum=1, plot=0)
            chanListAll = self.ReceiverArray.UsedChannels
            weights = np.zeros(chanListAll.shape, np.float)
            ind = 0
            for i in xrange(len(weights)):
                if chanListAll[i] in c:
                    xc = x[ind][:]
                    yc = y[ind][:]
                    mask = np.where( np.bitwise_and((xc > lolim), \
                                            (xc < hilim)), 1, 0 )
                    pows = fStat.f_mean(np.compress(mask, yc))
                    weights[i] = 1./(pows**2)
                    ind = ind+1

            for i in xrange(0, self.ScanParam.NInt):
                self.DataWeights[i,:] = weights.astype(np.float32)

        else:
            self.MessHand.error("Unknown weighting method - no weight computed")
            return

    def slidingWeight(self,chanList=[],nbInteg=50):
        """compute weights using 1/rms^2, where rms is computed in
             sliding windows of size nbInteg

        Parameters
        ----------
        chanList : list of int
            the list of channels to compute
        nbInteg : int
            size of windows (default: 20)
        """
        chanList = self.ReceiverArray.checkChanList(chanList)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        for c in chanList:
            index = self.ReceiverArray.getChanIndex(c)[0]
            rms = fStat.slidingrms(self.Data[:, index],
                                   self.FlagHandler._aFlags[:, index],
                                   nbInteg)
            wei = 1./rms**2
            self.DataWeights[:, index] = wei.astype(self.DataWeights.dtype)

# -------------------------------------------------------------------
# ---- plotting methods ---------------------------------------------
# -------------------------------------------------------------------
    def plotMean(self,chanList=[], \
                 channelFlag=[], plotFlaggedChannels=0, \
                 dataFlag=[], plotFlaggedData=0, \
                 limitsX=[],limitsY=[], \
                 style='l', ci=1, overplot=0, plotMap=0):
        """plot mean flux value vs. subscan number

        Parameters
        ----------
        chanList : list of int
            list of channels
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                +----------------------------------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +================================================================+
                | 'None' |  False      | all data                                |
                +----------------------------------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +----------------------------------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +----------------------------------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +----------------------------------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +----------------------------------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +----------------------------------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +----------------------------------------------------------------+
        plotMap : bool
            plot as a 2D map?
        """

        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        dataX = self.getChanListData('subscan', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
        dataY = self.getChanListData('mean_s', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)

        xLabel = "Subscan #"
        yLabel = "Mean flux [arb.u.]"

        self.MessHand.info("plotting Mean values per subscan")
        if not self.__statisticsDone:
            self.MessHand.warning(" plotting outdated statistics")

        if plotMap:
            Plot.draw(np.transpose(dataY), \
                      sizeX=[min(dataX[0]), max(dataX[0])], sizeY=[1, len(chanList)],\
                      limitsX=limitsX,\
                      labelX=xLabel, labelY='Channel #', \
                      caption=self.ScanParam.caption(), wedge=1)
        else:
            MultiPlot.plot(chanList, dataX, dataY,\
                           limitsX = limitsX, limitsY = limitsY, \
                           labelX = xLabel, labelY = yLabel, caption=self.ScanParam.caption(), \
                           style=style, ci=ci, overplot=overplot)

    #----------------------------------------------------------------------------
    def plotRms(self,chanList=[], \
                channelFlag=[], plotFlaggedChannels=False, \
                dataFlag=[], plotFlaggedData=False, \
                limitsX=[],limitsY=[], \
                style='l', ci=1, overplot=False, plotMap=False):
        """plot flux r.m.s. vs. subscan number

        Parameters
        ----------
        chanList : list of int
            list of channels
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                +----------------------------------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +================================================================+
                | 'None' |  False      | all data                                |
                +----------------------------------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +----------------------------------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +----------------------------------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +----------------------------------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +----------------------------------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +----------------------------------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +----------------------------------------------------------------+
        style : str
            'l' for line, 'p' for point
        limitsX, limitsY : float array
            the limits in X and Y
        ci : int
            color index
        overplot : bool
            do we overplot ?
        plotMap : bool
            plot as a 2D map?
        """
        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if not self.__statisticsDone:
            self.__statistics()

        dataX = self.getChanListData('subscan', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
        dataY = self.getChanListData('rms_s', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)

        xLabel = "Subscan #"
        yLabel = "Flux r.m.s. [arb.u.]"

        self.MessHand.info("plotting r.m.s. per subscan")
        if not plotMap:

            MultiPlot.plot(chanList, dataX, dataY,\
                           limitsX = limitsX, limitsY = limitsY, \
                           labelX = xLabel, labelY = yLabel, caption=self.ScanParam.caption(), \
                           style=style, ci=ci, overplot=overplot)
        else:
            Plot.draw(np.transpose(dataY), \
                      sizeX=[min(dataX[0]), max(dataX[0])], sizeY=[1, len(chanList)],\
                      limitsX=limitsX,\
                      labelX=xLabel, labelY='Channel #', caption=self.ScanParam.caption(), wedge=1)


    #----------------------------------------------------------------------------
    def plotMeanChan(self,chanList=[], \
                     channelFlag=[], plotFlaggedChannels=0, \
                     dataFlag=[], plotFlaggedData=0, \
                     limitsX=[],limitsY=[], \
                     style='p', ci=1, overplot=0):
        """PLotting the MEAN value for each subscan against channel number.

        Parameters
        ----------
        chanList : list of int
            list of channels
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                +----------------------------------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +================================================================+
                | 'None' |  False      | all data                                |
                +----------------------------------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +----------------------------------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +----------------------------------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +----------------------------------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +----------------------------------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +----------------------------------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +----------------------------------------------------------------+
        style : str
            'l' for line, 'p' for point
        limitsX, limitsY : float array
            the limits in X and Y
        ci : int
            color index
        overplot : bool
            do we overplot ?
        """
        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList,
                                                     flag=channelFlag,
                                                     getFlagged=plotFlaggedChannels)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if not self.__statisticsDone:
            self.__statistics()

        self.MessHand.info("plotting Mean values per channel")
        dataY = self.getChanListData('mean', chanList,
                                     channelFlag=channelFlag,
                                     getFlaggedChannels=plotFlaggedChannels,
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
        dataY = np.array(dataY)
        dataX = chanList
        Plot.plot(dataX, np.ravel(dataY), overplot=overplot, ci=ci,\
                  limitsX=limitsX, limitsY=limitsY,\
                  labelX='Channel Number', labelY='MEAN value for each subscan',\
                  caption=self.ScanParam.caption(),)

    #----------------------------------------------------------------------------
    def plotRmsChan(self,chanList=[], \
                    channelFlag=[], plotFlaggedChannels=0, \
                    dataFlag=[], plotFlaggedData=0, \
                    limitsX=[],limitsY=[], \
                    style='p', ci=1, overplot=0, subscan = 0, logY=0):
        """PLotting the RMS value for each subscan against channel number.

        Parameters
        ----------
        chanList : list of int
            list of channels
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                +----------------------------------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +================================================================+
                | 'None' |  False      | all data                                |
                +----------------------------------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +----------------------------------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +----------------------------------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +----------------------------------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +----------------------------------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +----------------------------------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +----------------------------------------------------------------+
        style : str
            'l' for line, 'p' for point
        limitsX, limitsY : float array
            the limits in X and Y
        ci : int
            color index
        overplot : bool
            do we overplot ?
        subscan : bool
           plot by subscans ?
        logY : bool
           plot Y in log ?
        """

        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)
        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        if not self.__statisticsDone:
            self.__statistics()

        if subscan:
            dataY = self.getChanListData('rms_s', chanList, \
                                         channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                         dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
            labY = 'RMS value for each subscan'
            nbSubscan = dataY.shape[1]
        else:
            dataY = self.getChanListData('rms', chanList, \
                                         channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                         dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
            labY = 'RMS value for the complete scan'
            nbSubscan = 1
        self.MessHand.info("plotting r.m.s. per channel")

        arrayX = np.ones((nbSubscan), np.float32)
        dataX = []
        for n in chanList:
            dataX.extend(n*arrayX)
        Plot.plot(dataX, np.ravel(dataY), overplot=overplot, ci=ci,\
                  limitsX=limitsX, limitsY=limitsY,\
                  labelX='Channel Number', labelY=labY,\
                  caption=self.ScanParam.caption(), logY=logY)

    #----------------------------------------------------------------------------
    def plotFFT(self,chanList=[], \
                channelFlag=[], plotFlaggedChannels=0, \
                dataFlag=[], plotFlaggedData=0, \
                limitsX=[],limitsY=[], \
                style='l', ci=1, overplot=0, logX=1,logY=1,\
                windowSize=0,windowing=3,returnSpectra=0):
        """plot FFT of signal

        Parameters
        ----------
        chanList : list of int
            list of channels
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                +----------------------------------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +================================================================+
                | 'None' |  False      | all data                                |
                +----------------------------------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +----------------------------------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +----------------------------------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +----------------------------------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +----------------------------------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +----------------------------------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +----------------------------------------------------------------+
        limitsX, limitsY : float array
            the limits in X and Y
        style : str
            'p' for point, 'l' for line
        ci : int
            color index
        overplot : bool
            do we overplot ?
        logX, logY : bool
            do we plot X and or Y in log scale ?
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        windowSize  : int
            length of chunks to compute FFT on and to average
                                (default: 0 = compute on the entire data serie)
        returnSpectra : bool
            do we return spectra ?

        Returns
        -------
        tuple
           if requested return the tuple (chanList, freqFFT, modFFT)
        """

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)
        nChan = len(chanList)

        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        # We use only MJD values for fft. They are the correct time stamps.
        mjd = self.getChanData('mjd', chanList[0], flag='None')

        freqFFT = []
        modFFT  = []

        # TODO: compute by subscan
        for chan in chanList:
            flux  = self.getChanData('flux', chan, flag='None')
            num = self.ReceiverArray.getChanIndex(chan)[0]
            if not flux.flags.contiguous:
                flux = flux.copy()

            if dataFlag in ['', 'None']:
                maskOk = np.nonzero(np.ones(flux.shape, np.int8))
            else:
                if plotFlaggedData:
                    maskOk = np.nonzero(self.FlagHandler.isSetMask(dataFlag, dim=1, index=num))
                else:
                    maskOk = np.nonzero(self.FlagHandler.isUnsetMask(dataFlag, dim=1, index=num))

            theFluxOk = np.zeros(flux.shape, np.float)
            np.put(theFluxOk, maskOk, np.take(flux, maskOk))

            oneFFT = FilterFFT(mjd, theFluxOk)
            oneFFT.doFFT(windowSize=windowSize, windowing=windowing)
            freq = copy.copy(oneFFT.Freq)
            dens = copy.copy(oneFFT.Power)

            # Remove the Zero frequency to use the log scale
            if logX:
                freq = freq[1:]
                dens = dens[1:]

            freqFFT.append(freq)
            # We plot the PSD (power) in amplitude units (that's V_rms / sqrt(Hz)
            modFFT.append(np.sqrt(dens))  # sqrt(Power)

        xLabel = "Frequency [Hz]"
        yLabel = "sqrt(PSD) [rms / sqrt(Hz)]"

        MultiPlot.plot(chanList, freqFFT, modFFT,\
                       limitsX = limitsX, limitsY = limitsY,\
                       labelX = xLabel, labelY = yLabel, caption=self.ScanParam.caption(),\
                       style=style, ci=ci, overplot=overplot, logX=logX, logY=logY)

        if returnSpectra:
            return(chanList, freqFFT, modFFT)


    #----------------------------------------------------------------------------
    def plotDataGram(self,chanNum=-1, \
                     flag=[], plotFlagged=0, \
                     n=512,limitsZ=[]):
        """plot DataGram of signal

        Parameters
        ----------
        chanNum : int
            channel number to plot
        flag : list of int
            plot data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data
                +----------------------------------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +================================================================+
                | 'None' |  False      | all data                                |
                +----------------------------------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +----------------------------------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +----------------------------------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +----------------------------------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +----------------------------------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +----------------------------------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +----------------------------------------------------------------+
        n : int
            Number of points for the ffts
        limitsZ : float array
            limits for the color scale
        """

        if chanNum == -1:
            chanNum = self.ReceiverArray.RefChannel
        time = self.getChanData('mjd', chanNum, flag=flag, getFlagged=plotFlagged)
        flux = self.getChanData('flux', chanNum, flag=flag, getFlagged=plotFlagged)

        oneFFT = FilterFFT(time, flux)
        oneFFT.plotDataGram(n=n, limitsZ=limitsZ)

    #----------------------------------------------------------------------------
    def bandRms(self,chanList=[],low=1.,high=10., \
                channelFlag=[], getFlaggedChannels=0, \
                dataFlag=[], getFlaggedData=0, \
                windowSize=0,windowing=3):
        """compute rms in some spectral range

        Parameters
        ----------
        chanList : list of int
            list of channels
        low, high : float
            range limits (in Hz)
        channelFlag : list of int
            retrieve data from channels flagged or unflagged accordingly
        getFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            retrieve data flagged or unflagged accordingly
        getFlaggedData : bool
            dataFlag revers to flagged/unflagged data
                                          flag   | getFlagged | Retrieve..
                                          'None' |  0         | all data
                                          []     |  0         | unflagged data (default)
                                          []     |  1         | data with at least one flag set
                                          1      |  0         | data with flag 1 not set
                                          1      |  1         | data with flag 1 set
                                          [1,2]  |  0         | data with neither flag 1 nor flag 2 set
                                          [1,2]  |  1         | data with either flag 1 or flag 2 set
        windowing : int
            windowing function used to compute FFTs (default: Hamming, see FFT.applyWindow)
        windowSize  : int
            length of chunks to compute FFT on and to average
                                (default: 0 = compute on the entire data serie)
        """

        if getFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=getFlaggedChannels)

        # We use only MJD values for fft. They are the correct time stamps.
        time = self.getChanListData('mjd', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=getFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=getFlaggedData)
        flux = self.getChanListData('flux', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=getFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=getFlaggedData)

        for n in xrange(len(chanList)):
            oneFFT = FilterFFT(time[n], flux[n])
            oneFFT.doFFT(windowSize=windowSize, windowing=windowing)
            mask = np.nonzero(greater(oneFFT.Freq, low) and np.less(oneFFT.Freq, high))
            total = 0.
            for k in mask:
                total += oneFFT.Power[k]
            total = np.sqrt(total * oneFFT.SamplFreq / oneFFT.N)
            self.MessHand.info("Chan %i: rms in [%f,%f Hz] = %g"%(chanList[n], low, high, total))




    #----------------------------------------------------------------------------
    # time shifting routines

    def __timeShiftChan(self, chan, step, shiftFlags=True):
        """time shift channel by step

        Parameters
        ----------
        chan : int
            channel number
        step : int
            number of time stamps
        shiftFlags : bool
            also shift flags? default yes
        """

        chan          = self.ReceiverArray.checkChanList(chan)
        chanListIndex = self.ReceiverArray.getChanIndex(chan)

        nSamp = self.Data.shape[0]

        if (step > 0):
            # shift data
            temp = copy.deepcopy(self.Data[0:nSamp-step, chanListIndex])
            self.Data[step:nSamp, chanListIndex] = temp
            # shift flags
            if shiftFlags:
                temp = copy.deepcopy(self.FlagHandler._aFlags[0:nSamp-step, chanListIndex])
                self.FlagHandler._aFlags[step:nSamp, chanListIndex] = temp
            # flag beginning
            mask = np.zeros(nSamp, np.int8)
            mask[0:step] = 1
            self.FlagHandler.setOnMask(mask, 1, dim=1, index=chanListIndex)
        else:
            if (step < 0):
                # shift data
                self.Data[0:nSamp-abs(step), chanListIndex] = \
                         self.Data[abs(step):nSamp, chanListIndex]
                # shift flags
                if shiftFlags:
                    self.FlagHandler._aFlags[0:nSamp-abs(step), chanListIndex] = \
                                             self.FlagHandler._aFlags[abs(step):nSamp, chanListIndex]
                # flag end
                mask = np.zeros(nSamp, np.int8)
                mask[nSamp-abs(step):nSamp] = 1
                self.FlagHandler.setOnMask(mask, 1, dim=1, index=chanListIndex)


    def timeShiftChanList(self,step, chanList=[],shiftFlags=True):
        """time shift list of channels by list of steps

        Parameters
        ----------
        chanList : list of int
            channel list
        steps : list of int
            list of number of time stamps
        shiftFlags : bool
            also shift flags? default yes
        """

        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        for i in xrange(len(chanList)):
            self.__timeShiftChan(chanList[i], steps[i], shiftFlags)


    def computeCorTimeShift(self,shiftAz,shiftEl,chanList=[],refChan=-1,distlim=-1.):
        """computes mean of absolute correlations for all channel pairs with mutual
             distance smaller than distlim, given time shifts in azimuth and elevation
             directions. To be used by timeshiftAzEl.

        Parameters
        ----------
        shiftAz : float
            time shift in azimuth. unit: milliseconds per arcsecond
        shiftEl : float
            time shift in elevation. unit: milliseconds per arcsecond
        chanList : list of int
            the list of channels to consider
        refChan : int
            reference channel (timeshift 0)
        distlim : float
            consider only correlations on receiver separations
                                 smaller than this value (arcseconds)
        """

        # create a copy of the data array
        chanList        = self.ReceiverArray.checkChanList(chanList)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)
        refChanIndex = self.ReceiverArray.getChanIndex(refChan)
        tempData = copy.deepcopy(self)

        # get the channel separations
        # TODO : Use the proper routine... ScanParam.getChanSep()
        offAz = np.take(self.ReceiverArray.Offsets[0,:], chanListIndexes) - \
                self.ReceiverArray.Offsets[0, refChanIndex]
        offEl = np.take(self.ReceiverArray.Offsets[1,:], chanListIndexes) - \
                self.ReceiverArray.Offsets[1, refChanIndex]

        timestep = average(self.ScanParam.LST[1:20]-self.ScanParam.LST[0:19])*1000.

        # project channel separations onto direction of time shift
        shiftsteps = []
        for i in xrange(len(offAz)):
            timeshift = np.dot(np.array([offAz[i], offEl[i]]), np.array([shiftAz, shiftEl]))
            if (timeshift > 0):
                shiftsteps.append(int(0.5+timeshift/timestep))
            else:
                shiftsteps.append(int(timeshift/timestep-0.5))

        tempData.timeShiftChanList(chanList, shiftsteps)

        # compute correlations
        # tempData.__resetStatistics()
        # tempData.computeWeights(chanList=[])
        dist, corr = tempData.plotCorDist(chanList=chanList, upperlim=distlim, plot=0)

        # return mean of absolute values of the correlations
        return average(abs(corr))



    def timeshiftAzEl(self,chanList=[],refChan=-1,check=1,distlim=300.,shiftmax=10.):
        """computes time shifts of all channels, with respect to a reference
             channel, which MAXIMIZES the correlated noise across the array

        Parameters
        ----------
        chanList : list of int
            the list of channels to consider
        refChan : int
            reference channel (will get timeshift=0)
        check : bool
            check the chanList first ( default: yes )
        distlim : float
            consider only correlations on receiver separations
                                 smaller than this value (arcseconds)
        shiftmax : float
            maximum timeshift (absolute value) in milliseconds per arcsecond

        Notes
        -----
        Not implemented
        """
