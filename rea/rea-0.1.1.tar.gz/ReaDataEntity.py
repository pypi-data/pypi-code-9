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
.. module:: ReaDataEntity
   :synopsis: contains the Rea data entity class

"""


__version__ =  '$Revision: 2768 $'
__date__ =     '$Date: 2010-09-01 09:54:53 +0200 (mer. 01 sept. 2010) $'
# __tag__=      '$Name:  $'

#----------------------------------------------------------------------------------
#----- Import ---------------------------------------------------------------------
#----------------------------------------------------------------------------------

import os, string, time, cPickle, gc, copy

import numpy as np

from pyslalib import slalib


from rea           import ReaMBFits, ReaMBFitsReader, ReaFlagHandler
from rea           import ReaMessageHandler, ReaCommandHistory, ReaConfig, ReaDir, Utilities
from rea.Bogli     import Plot, MultiPlot, Forms
from rea.fortran   import fUtilities, fStat
from rea.Utilities import attrStr, compressNan, prettyPrintList
from rea.Utilities import fitGaussian, modelgauss

#----------------------------------------------------------------------------------
#----- ReceiverArray Class -------------------------------------------------------
#----------------------------------------------------------------------------------

class Telescope:
    """..class:: Telescope
    :synopsis: Define all the useful parameters of a telescope
    """

    def __init__(self):
        """Instanciation of a Telescope object """

        self.Name = ""                    # Telescope name
        self.Diameter  = 0.0              # in m
        self.Longitude = 0.0              # telescope longitude (in deg)
        self.Latitude  = 0.0              # telescope latitude  (in deg)
        self.Elevation = 0.0              # telescope altitude  (in m)

    def set(self, name="", diameter=0.0, longitude=0.0, latitude=0.0, elevation=0.0):
        """Set all Telescope parameters

        Parameters
        ----------
        name : str
            name of the telescope
        diameter : float
            diameter of the telescope [m]
        longitude, latitude : float
            position of the telescope [deg]
        elevation : float
            elevation of the telescope [m]
        name : str
             (Default value = "")
        """

        self.Name      = name
        self.Diameter  = diameter
        self.Longitude = longitude
        self.Latitude  = latitude
        self.Elevation = elevation

    def __str__(self):
        """Defines a string which is shown when the print instruction is used."""
        return self.Name + " (" + "%3i m)" % self.Diameter

#----------------------------------------------------------------------------------
#----- ReceiverArray Class -------------------------------------------------------
#----------------------------------------------------------------------------------

class ReceiverArray:
    """Define all the useful parameters of a receiver array"""

    def __init__(self, nChannels=0):
        """Instanciation of a ReceiverArray object

        Parameters
        ----------
        nChannels : int
            number of channels
        """

        # Add a MessHand attribute - new MessageHandler 20050303
        self.__MessHand = ReaMessageHandler.MessHand(self.__module__)

        self.FeBe = ""                             # Backend Frontend combinaison
        self.Telescope = Telescope()

        self.TransmitionCurve = np.array([], np.float32)  # 2D (frequency vs transmition)
        self.EffectiveFrequency  = 0.0             # Hz

        self.NChannels     = nChannels              # The total number of channels
        self.NUsedChannels = nChannels              # Number of channels in use, i.e. size of data
        self.RefChannel    = 0                      # The reference Channel
        self.UsedChannels  = np.arange(nChannels)+1    # List of used Channels (to map to data array)
        self.CurrChanList  = np.arange(nChannels)+1    # Current list of used array

        self.Offsets    = np.zeros((2, nChannels), np.float32)  # The so called RCP in arcsec
        self.FWHM       = np.zeros((2, nChannels), np.float32)  # Corresponding FWHM of modelled gaussian (major-minor) (arcsec)
        self.Tilt       = np.zeros(nChannels, np.float32)              # with tilt in degree
        self.AddIndex   = []                                     # an additionnal index list


        self.Gain       = np.ones(nChannels, np.float32)  # Normalized gains (for point sources)
        self.ExtGain    = np.ones(nChannels, np.float32)  # Normalized gains (for extended emission, skynoise)
        self.JyPerCount = 1.                        # Jy / count conversion factor
        self.BEGain     = 1.                        # Backend attenuation factor (new v. 1.61)
        self.FEGain     = 0.                        # Frontend amplifier gain (actually the gain
                                                    # is 2^FEGain) - new v. 1.61
        self.DCOff      = np.zeros(nChannels, np.float32) # DC offsets

        self.DewCabin   = ""                        # Description of the Dewar location (CASS or NASMYTH), used for derotation...
        self.DewUser    = 0.                        # Dewar angle (user relative to coord. system)
        self.DewExtra   = 0.                        # Extra dewar rotation angle

        # Derived parameters
        self.BeamSize = 0.                                       # size of the beam in arcsec
        self.ChannelSep = np.zeros((nChannels, nChannels), np.float32)   # the separation between channels

        self.FeedType    = []                      # array defining the type of the used feed
        self.FeedCode    = {}                      # Dictionnary describing the feed type
                                                   # FeedCode of 1 will be sky feeds

        self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros(nChannels, np.int32))
        self.cflags       = {'NOT CONNECTED'  : 1,
                             'BAD SENSITIVITY': 2,
                             'LOW SENSITIVITY': 3,
                             'DARK RECEIVER' : 4,
                             'TEMPORARY'      : 8 }

    #----------------------------------------------------------------------------
    def __str__(self):
        """Defines a string which is shown when the print instruction is used."""

        out = self.FeBe
        out += " - %3i/%3i/%3i channels at %3i GHz (%s)" % \
               (self.FlagHandler.nUnset(), \
                len(self.UsedChannels), \
                self.NChannels, \
                int(self.EffectiveFrequency/1.e9), \
                self.printCurrChanList())

        # out += " on " + self.Telescope.Name + " (" + \
        #       "%3i m" % self.Telescope.Diameter + \
        #       " - %4.1f\" default beam)" % self.BeamSize

        out += " - FE/BE Gain: %2i/%3i" %\
               (2.**self.FEGain, self.BEGain)

        if ReaConfig.DEBUG > 2:
            out += "\n" + \
                   attrStr(self, ['Telescope', '_ReceiverArray__MessHand']) + \
                   "\n"

        return out

    # ---------------------------------------------------------------------
    def __fillFromMBFits(self, reader, febe, baseband, subscan, flag=1):
        """fill a ReceiverArray object using the MBFitsReader object reader.

        Parameters
        ----------
        reader : MBFitsReader
            a MBFitsReader object
        febe : str
            frontend-backend name to select
        baseband : int
            baseband number to select
        subscans : list of int
            list of subscans numbers to read in
        flag : int
            flag for not connected feeds (default: 1 'NOT CONNECTED')
        """

        try:

            # MBFit files can have several UseBand take the first
            # corresponding to the baseband
            useBand = reader.read("UseBand", febe=febe)
            indexBaseband = -1
            for iBand in np.arange(len(useBand)):
                if useBand[iBand] == baseband:
                    indexBaseband = iBand

            # TODO: Why some parameters needs indexBaseband and some other not
            nChannels    = reader.read("FebeFeed", febe=febe)
            self.NChannels = nChannels
            usedChannels = reader.read("UseFeed", febe=febe)[indexBaseband]
            if len(usedChannels.shape) == 3:
                print "TODO : Should be move to the reader !!!!"
                print "TODO : Actually comes from the IMBFITS format have TFORM = 168J instead of 1PJ(168)"
                usedChannels = usedChannels[0,:, 0]
            nbUsedChan   = reader.read("NUseFeeds", febe=febe)[indexBaseband]
            usedChannels = usedChannels[:nbUsedChan] # TODO: Is it really necessary ?!?
            refChannel   = reader.read("RefFeed",  febe=febe)

            # FEEDTYPE: tells us which channels are real receivers, which are "dark"
            feedType   = reader.read("FeedType", febe=febe)[indexBaseband]
            feedString = reader.read("FeedCode", febe=febe)

            # TODO : This should probably also go to the reader...
            # Convert FeedCode to dictionnary
            feedCode = {}
            listType = feedString.split(',')
            goodType = []
            for i in range(len(listType)):
                num_type = listType[i].split(':')
                if len(num_type) > 1:
                    feedCode[num_type[1]] = int(num_type[0])
                    if num_type[1] in ReaConfig.goodFeedList:
                        goodType.append(int(num_type[0]))

            print goodType
            self.Offsets       = np.zeros((2, nChannels), np.float32)
            self.Gain          = np.ones((nChannels), np.float32)
            self.ExtGain       = np.ones((nChannels), np.float32)

            # Read ALL the offsets, non sky feeds (having -9999 offsets) will be set to 0
            offsets = (np.array([reader.read("FeedOffX", febe=febe),\
                                 reader.read("FeedOffY", febe=febe)])*3600.).astype(np.float32)
            if (offsets.ndim == 1):  # when only one pixel
                offsets = np.transpose(np.array([offsets]))
            # FEBEPAR_FLATFIEL contains one array of gains
            self.Gain  = reader.read("FlatField", febe=febe)[indexBaseband]

            # DC offsets (reseted before scan start)
            self.DCOff = reader.read("DCoffset", febe=febe)[indexBaseband]

            # FE and BE Gains
            gains = reader._readGains(febe=febe)
            self.FEGain   = gains[0]
            if isinstance(gains[1], type(np.array([0]))):
                self.BEGain   = gains[1][indexBaseband]
            else:
                self.BEGain   = gains[1]

            self.JyPerCount    = reader.read("BolCalFc", febe=febe)

            self.UsedChannels  = usedChannels
            self.CurrChanList  = usedChannels
            self.NUsedChannels = len(usedChannels)
            self.RefChannel    = refChannel

            # remember 0 indexed numbering
            usedChannels = usedChannels-1

            self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros((nChannels), np.int32))

            # TODO: This is wrong, too complicated

            # Setting the initial Flags
            # in two steps: flag all, and unflag the UsedChannels...

            #   ... first flag all with -1 meaning not used ...
            for num in np.arange(nChannels):
                if 0 <= num < nChannels:
                    self.FlagHandler.setOnIndex(num, flag)

            #   ... second unflag the used channels
            if isinstance(feedType[0], np.int64):
                for i in np.arange(self.NUsedChannels):
                    num = usedChannels[i]
                    if 0 <= num < nChannels and feedType[i] in goodType and not np.isnan(offsets[0, num]) and not np.isnan(offsets[1, num]):
                        self.FlagHandler.unsetOnIndex(num, flag)
                    elif 0 <= num < nChannels:
                        self.FlagHandler.setOnIndex(num, flag)
                        # put the offsets of non sky feeds to Nan
                        offsets[0, num] = float('Nan')
                        offsets[1, num] = float('Nan')
                    else:
                        self.__MessHand.warning(str(num+1)+' channel not in the range')
                self.Offsets  = offsets

            # Check that the reference channel is used
            if self.FlagHandler.isSetOnIndex(self.getChanIndex(self.RefChannel)):
                self.__MessHand.warning('Reference channel not used')
                self.__MessHand.warning('Put Reference channel on first unflagged channel')
                self.RefChannel = self.UsedChannels[np.where(self.FlagHandler.getFlags() == 0)[0][0]]


            self.FeedCode = feedCode
            self.FeedType = feedType

            # The Channel separations can be computed
            self._ReceiverArray__computeChanSep()
            self.FeBe = febe
            # Store the telescope properties
            self.Telescope.set(reader.read("Telescope",      febe=febe),\
                               float(reader.read("Diameter", febe=febe)),\
                               float(reader.read("SiteLong", febe=febe)),\
                               float(reader.read("SiteLat",  febe=febe)),\
                               float(reader.read("SiteElev", febe=febe)))

            # And observing frequency
            try:
                freq = float(reader.read("RestFreq", febe=febe, baseband=baseband, subsnum=subscan))
            except:
                freq = 0.
            if (freq == 0.):
                freq = 2.5e11   # assume 1.2mm if not available
                self.__MessHand.warning('No frequency found in the file, assuming 1.2mm')

            self.EffectiveFrequency = freq

            # The telescope beamSize can be computed
            self.__computeBeamSize()

            # Dewar rotation angles
            try:
                self.DewCabin = reader.read("DewCabin", febe=febe)
                self.DewUser  = reader.read("DewUser",  febe=febe)
                self.DewExtra = reader.read("DewExtra", febe=febe, subsnum=subscan)
            except:
                self.__MessHand.warning('No DewUser or DewExtra keyword')

        except Exception as data:
            raise

    # ---------------------------------------------------------------------

    def get(self,dataType,flag=[],getFlagged=0):
        """get receivers offsets or gain according to flag.

        Parameters
        ----------
        dataType : {'ReceiverPositionX/Y', 'BoloPosX/Y', 'BoloX/Y', 'bX/Y', 'off_X/Y', 'ReceiverGain','Gain'}
             type of data
        flag : list of int
             retrieve data flagged or unflagged accordingly
        getFlagged : bool
             flag revers to flagged/unflagged data

                                 +--------+------------+-----------------------------------------+
                                 | flag   | getFlagged | Retrieve..                              |
                                 +========+============+=========================================+
                                 | 'None' |  False     | all data                                |
                                 +--------+------------+-----------------------------------------+
                                 | []     |  False     | unflagged data (default)                |
                                 +--------+------------+-----------------------------------------+
                                 | []     |  True      | data with at least one flag set         |
                                 +--------+------------+-----------------------------------------+
                                 | 1      |  False     | data with flag 1 not set                |
                                 +--------+------------+-----------------------------------------+
                                 | 1      |  True      | data with flag 1 set                    |
                                 +--------+------------+-----------------------------------------+
                                 | [1,2]  |  False     | data with neither flag 1 nor flag 2 set |
                                 +--------+------------+-----------------------------------------+
                                 | [1,2]  |  True      | data with either flag 1 or flag 2 set   |
                                 +--------+------------+-----------------------------------------+

        Returns
        -------
        float array
              the requested data
        """
        dataType = dataType.lower()

        # retrieve the data... (offsets are in arcsec)
        if dataType in ['receiverpositionx', 'boloposx', 'bolox', 'bx', 'off_x']:
            dataArray = self.Offsets[0,:]
        elif dataType in ['receiverpositiony', 'boloposy', 'boloy', 'by', 'off_y']:
            dataArray = self.Offsets[1,:]
        elif dataType in ['receivergain', 'gain']:
            dataArray = self.Gain

        # .. and only return the desired flag
        if flag in ['', 'None']:
            return dataArray
        else:
            if getFlagged:
                mask = self.FlagHandler.isSetMask(flag)
            else:
                mask = self.FlagHandler.isUnsetMask(flag)
            return np.compress(mask, dataArray)

    # ---------------------------------------------------------------------
    def flipOffsets(self):
        """flips the sign in Az/El of channel offsets. Used to convert (old) APEX-SZ
             scans into the same convention as for LABOCA
        """
        self.Offsets = -self.Offsets

    # ---------------------------------------------------------------------
    def readMopsicRcp(self,rcpFile='rea.rcp'):
        """update receiver channel offsets from a simple ascii file


        channelNumber AzOffset ElOffset Major(FWHM) Minor(FWHN) Tilt Gain


        with unit of arcsec and degree

        Parameters
        ----------
        rcpFile : str
            the filename to read in
        """

        try:
            f = file(os.path.join(ReaConfig.rcpPath, rcpFile))
        except IOError:
            self.__MessHand.error("could not open file %s"%(file))
            return

        # Read the file and put the values in 1 list and 2 arrays

        asciiFile = f.readlines()
        f.close()

        Number    = []
        AzOffset  = []
        ElOffset  = []
        MinorFWHM = []
        MajorFWHM = []
        nTilt     = []
        nGain     = []

        for i in range(0, len(asciiFile)):

            # Skip comment lines
            if asciiFile[i][0] == "!":
                continue

            if asciiFile[i].find("no fit") > 0:
                continue

            # Split lines and fill arrays
            tmp = asciiFile[i].split()
            Number.append(int(tmp[0]))
            AzOffset.append(float(tmp[1]))
            ElOffset.append(float(tmp[2]))
            MinorFWHM.append(float(tmp[3]))
            MajorFWHM.append(float(tmp[4]))
            nTilt.append(float(tmp[5]))
            nGain.append(float(tmp[6]))

        AzOffset  = np.array(AzOffset)
        ElOffset  = np.array(ElOffset)
        MinorFWHM = np.array(MinorFWHM)
        MajorFWHM = np.array(MajorFWHM)
        nTilt     = np.array(nTilt)
        nGain     = np.array(nGain)

        # Process the array
        refChan = self.RefChannel
        Offsets = self.Offsets
        Gain    = self.Gain

        # FB260307 usually Tilt and FWHM are not instantiated
        if self.Tilt.shape[0] == 0:
            nc = Gain.shape[0]
            Tilt = np.zeros(nc, np.float32)
            FWHM = np.zeros((2, nc), np.float32)
        else:
            FWHM    = self.FWHM
            Tilt    = self.Tilt

        # If the reference channel is in the list remove its offsets
        # from the other ones and replace them but the one already
        # existing, otherwise we have to assume that they are aligned
        if refChan in Number:
            refIndex = np.nonzero(np.equal(Number, refChan))
            print refIndex, AzOffset[refIndex], ElOffset[refIndex]
            AzOffset = AzOffset - AzOffset[refIndex] + Offsets[0, refChan-1]
            ElOffset = ElOffset - ElOffset[refIndex] + Offsets[1, refChan-1]
            # FB260307 I dont understand this, so here assume 0,0 is reference channel
            # AzOffset = AzOffset - AzOffset[refIndex]
            # ElOffset = ElOffset - ElOffset[refIndex]

        # Replace the offsets
        for i in range(len(Number)):
            Offsets[0, Number[i]-1] = AzOffset[i]
            Offsets[1, Number[i]-1] = ElOffset[i]
            FWHM[:, Number[i]-1]    = np.array([MajorFWHM[i], MinorFWHM[i]], np.float32)
            Tilt[Number[i]-1]      = nTilt[i]
            Gain[Number[i]-1]      = nGain[i]


        self.Offsets = Offsets
        self.FWHM    = FWHM
        self.Tilt    = Tilt
        self.Gain    = Gain

        # delete local variable
        del AzOffset, ElOffset, MinorFWHM, MajorFWHM, nTilt, nGain
        del Offsets, FWHM, Tilt, Gain

        # recompute separations between channels
        self._ReceiverArray__computeChanSep()

    # ---------------------------------------------------------------------
    def writeMopsicRcp(self,rcpFile='rea.rcp'):
        """store current Receiver Channel Parameters (Offsets,
             Gain) to a file with mopsi like format

        Parameters
        ----------
        rcpFile : str
             complete name of output file (in ReaConfig.rcpPath)
        """

        try:
            f = file(os.path.join(ReaConfig.rcpPath, rcpFile), 'w')
        except IOError:
            self.__MessHand.error("could not open file %s in write mode"%(rcpFile))
            return

        # FB260307 in case Tilt and FWHM are not dimensioned yet
        if self.Tilt.shape[0] == 0:
            nc = self.Gain.shape[0]
            self.Tilt = np.zeros(nc, np.float32)
            self.FWHM = np.zeros((2, nc), np.float32)

        # Write header
        f.write("! Chan # Az/EL offset Major/Minor FWHM Tilt Gain\n")
        # Write parameters for all channels
        for i in range(len(self.Gain)):
            f.write("%i %f %f %f %f %f %f\n" % \
                    (i+1, self.Offsets[0, i], self.Offsets[1, i],\
                     self.FWHM[0, i], self.FWHM[1, i],\
                     self.Tilt[i], self.Gain[i]))
        f.close()

    # ---------------------------------------------------------------------

    def readAszcaRCP_matlab(self, beamfile, calfile):
        """read Receiver Channel Parameters for Aszca (attributes Offsets,
        Gain and ChannelSep) from the content of a file

        Notes
        -----
        USING CALIBRATION/BEAM PARAMETER FILES FROM THE MATLAB
        PIPELINE

        Parameters
        ----------
        beamfile : str
             complete name of file containing beam parameters
        calfile : str
             complete name of file containing calibrations

        """


        b = file(beamfile)
        c = file(calfile)

        # read and process RCP file
        beam = b.readlines()
        b.close()
        cal = c.readlines()
        c.close()
        offX, offY, gain, flat = [], [], [], []   # local lists to store X and Y offsets and Gain
        fwhmx, fwhmy, tilt = [], [], []
        timeconst = []

        for i in range(len(beam)):
            if beam[i][0] != '%':              # skip comments
                tmp = string.split(beam[i])
                offX.append((-1.)*3600.*string.atof(tmp[1]))
                offY.append((-1.)*3600.*string.atof(tmp[2]))
                fwhmx.append(3600.*string.atof(tmp[4]))
                fwhmy.append(3600.*string.atof(tmp[5]))
                tilt.append(string.atof(tmp[6]))

        for i in range(len(cal)):
            if cal[i][0] != '%':              # skip comments
                tmp = string.split(cal[i])
                gain.append(1./string.atof(tmp[2]))
                flat.append(1./string.atof(tmp[2]))

        # set the attributes to default values
        nChannels = len(gain)

        # offX=(-1.)*offX*3600.
        # offY=(-1.)*offY*3600.
        # fwhmx=fwhmx*3600.
        # fwhmy=fwhmy*3600.

        self.NChannels     = nChannels
        self.NUsedChannels = nChannels
        self.Offsets       = np.zeros((nChannels, nChannels), np.float32)
        self.Gain          = np.zeros((nChannels), np.float32)
        self.ExtGain       = np.zeros((nChannels), np.float32)
        self.FWHM          = np.zeros((nChannels, nChannels), np.float32)
        self.Tilt          = np.zeros((nChannels), np.float32)
        self.TimeConst     = np.zeros((nChannels), np.float32)

        self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros((nChannels), np.int32))

        # By default use all the channels :
        self.UsedChannels = np.arange(nChannels)+1
        self.CurrChanList = np.arange(nChannels)+1

        # Remember RCP file are written in arcsec
        self.Offsets = np.array([offX, offY], np.float32)
        self.Gain    = np.array(gain, np.float32)
        self.ExtGain = np.array(flat, np.float32)
        self.FWHM    = np.array([fwhmx, fwhmy], np.float32)
        self.Tilt    = np.array(tilt, np.float32)
        # self.TimeConst  = array(timeconst, np.float32)

        # recompute separations between channels
        self._ReceiverArray__computeChanSep()



    def readAszcaRCP(self, rcpFile):
        """readRCPfile (method) update Receiver Channel Parameters for Aszca (attributes Offsets,
             Gain and ChannelSep) from the content of a file.
             Also read beam shape and time constant

        channelNumber Gain Flat AzOffset ElOffset Major(FWHM) Minor(FWHN) Tilt ?? TimeConstant

        Parameters
        ----------
        rcpFile : str
             complete name of file to read in
        """

        try:
            f = file(os.path.join(ReaConfig.rcpPath, rcpFile))
        except IOError:
            self.__MessHand.error("could not open file %s"%(rcpFile))
            return

        # read and process RCP file
        param = f.readlines()
        f.close()
        offX, offY, gain, flat = [], [], [], []   # local lists to store X and Y offsets and Gain
        fwhmx, fwhmy, tilt = [], [], []
        timeconst = []

        for i in range(len(param)):	        # -1: skip last line
            if param[i][0] != '!':              # skip comments
                tmp = string.split(param[i])
                offX.append(string.atof(tmp[3]))
                offY.append(string.atof(tmp[4]))
                gain.append(string.atof(tmp[1]))
                flat.append(string.atof(tmp[2]))
                fwhmx.append(string.atof(tmp[5]))
                fwhmy.append(string.atof(tmp[6]))
                tilt.append(string.atof(tmp[7]))
                timeconst.append(string.atof(tmp[9]))

        # set the attributes to default values
        nChannels = len(gain)

        self.NChannels     = nChannels
        self.NUsedChannels = nChannels
        self.Offsets       = np.zeros((nChannels, nChannels), np.float32)
        self.Gain          = np.zeros((nChannels), np.float32)
        self.ExtGain       = np.zeros((nChannels), np.float32)
        self.FWHM          = np.zeros((nChannels, nChannels), np.float32)
        self.Tilt          = np.zeros((nChannels), np.float32)
        self.TimeConst     = np.zeros((nChannels), np.float32)

        self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros((nChannels), np.int32))

        # By default use all the channels :
        self.UsedChannels = np.arange(nChannels)+1
        self.CurrChanList = np.arange(nChannels)+1

        # Remember RCP file are written in arcsec
        self.Offsets = np.array([offX, offY], np.float32)
        self.Gain    = np.array(gain, np.float32)
        self.ExtGain = np.array(flat, np.float32)
        self.FWHM    = np.array([fwhmx, fwhmy], np.float32)
        self.Tilt    = np.array(tilt, np.float32)
        self.TimeConst  = np.array(timeconst, np.float32)

        # recompute separations between channels
        self._ReceiverArray__computeChanSep()


    # ---------------------------------------------------------------------
    def readRCPfile(self, rcpFile):
        """update Receiver Channel Parameters (attributes Offsets,
             Gain and ChannelSep) from the content of a file.
             Also read beam shape if available

        Parameters
        ----------
        rcpFile : string
            complete name of file to read in
        """

        try:
            f = file(os.path.join(ReaConfig.rcpPath, rcpFile))
        except IOError:
            self.__MessHand.error("could not open file %s"%(rcpFile))
            return

        # read and process RCP file
        param = f.readlines()
        f.close()
        offX, offY, gain, flat = [], [], [], []   # local lists to store X and Y offsets and Gain
        fwhmx, fwhmy, tilt = [], [], []

        for i in range(len(param)-1):	        # -1: skip last line
            if param[i][0] != '!':              # skip comments
                tmp = string.split(param[i])
                offX.append(string.atof(tmp[3]))
                offY.append(string.atof(tmp[4]))
                gain.append(string.atof(tmp[1]))
                flat.append(string.atof(tmp[2]))
                if len(tmp) > 5:
                    if tmp[7]:
                        fwhmx.append(string.atof(tmp[5]))
                        fwhmy.append(string.atof(tmp[6]))
                        tilt.append(string.atof(tmp[7]))

        # set the attributes to default values
        nChannels = len(gain)

        self.NChannels     = nChannels
        self.NUsedChannels = nChannels
        self.Offsets       = np.zeros((nChannels, nChannels), np.float32)
        self.Gain          = np.zeros((nChannels), np.float32)
        self.ExtGain       = np.zeros((nChannels), np.float32)
        self.FWHM          = np.zeros((nChannels, nChannels), np.float32)
        self.Tilt          = np.zeros((nChannels), np.float32)

        self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros((nChannels), np.int32))


        # By default use all the channels :
        self.RefChannel   = 1
        self.UsedChannels = np.arange(nChannels)+1
        self.CurrChanList = np.arange(nChannels)+1

        # Remember RCP file are written in arcsec
        self.Offsets = np.array([offX, offY], np.float32)
        self.Gain    = np.array(gain, np.float32)
        self.ExtGain = np.array(flat, np.float32)
        self.FWHM    = np.array([fwhmx, fwhmy], np.float32)
        self.Tilt    = np.array(tilt, np.float32)

        # recompute separations between channels
        self._ReceiverArray__computeChanSep()

    # --------------------------------------------------------------------
    def updateRCP(self,rcpFile,scale=1.,readTimeConst=False):
        """update only offsets and gains from the content of a file

        Parameters
        ----------
        rcpFile : str
            complete name of file to read in
        scale   : float
            scale factor to tune initial guess ASZCA rcp
        readTimeConst : bool
            do we read Time Constant
        """

        try:
            f = file(os.path.join(ReaConfig.rcpPath, rcpFile))
        except IOError:
            self.__MessHand.error("could not open file %s"%(rcpFile))
            return

        # read and process RCP file
        param = f.readlines()
        f.close()
        offsets = self.Offsets
        gain    = self.Gain
        flat    = self.ExtGain

        # FB260307 if Tilt and FWHM are not dimensioned
        if self.Tilt.shape[0] == 0:
            nc = gain.shape[0]
            Tilt = np.zeros(nc, np.float32)
            FWHM = np.zeros((2, nc), np.float32)
        else:
            FWHM    = self.FWHM
            Tilt    = self.Tilt

        if readTimeConst:
            nc = gain.shape[0]
            TimeConst = np.zeros(nc, np.int32)

        flagList = []
        for i in range(len(param)):
            if param[i][0] not in ['!', '#', 'n']:    # skip comments
                tmp = string.split(param[i])
                num = string.atoi(tmp[0])
                offsets[0, num-1] = string.atof(tmp[3])
                offsets[1, num-1] = string.atof(tmp[4])
                gain[num-1]      = string.atof(tmp[1])
                flat[num-1]      = string.atof(tmp[2])
                if len(tmp) > 7:
                    FWHM[0, num-1] = string.atof(tmp[5])
                    FWHM[1, num-1] = string.atof(tmp[6])
                    Tilt[num-1]  = string.atof(tmp[7])
                    if len(tmp) > 8:
                        flagList.append(num)
                if readTimeConst:
                    TimeConst[num-1] = string.atoi(tmp[8])


        self.Offsets   = offsets*scale
        self.Gain      = gain
        self.ExtGain   = flat
        self.FWHM      = FWHM
        self.Tilt      = Tilt
        if readTimeConst:
            self.TimeConst = TimeConst

        # recompute separations between channels
        self._ReceiverArray__computeChanSep()
        # if flagList:
        #    self._flagChannels(chanList=flagList,flag=1)
        # return flagList

    # ---------------------------------------------------------------------
    def writeRCPfile(self,rcpFile='rcpRea.rcp'):
        """store current Receiver Channel Parameters (Offsets,
             Gains, Beam shape) to a file with mopsi like format

        Chan  Gain ExtGain offX offY widX widY angl |

        Parameters
        ----------
        rcpfile : str
             complete name of output file
        """

        try:
            output = file(os.path.join(ReaConfig.rcpPath, rcpFile), 'w')
        except IOError:
            self.__MessHand.error("could not open file %s in write mode"%(rcpFile))
            return

        # FB260307 in case Tilt and FWHM are not dimensioned yet
        if self.Tilt.shape[0] == 0:
            nc = self.Gain.shape[0]
            self.Tilt = np.zeros(nc, np.float32)
            self.FWHM = np.zeros((2, nc), np.float32)

        output.write("!"+rcpFile+"\n")

        output.write('! Chan  Gain       ExtGain  offX       offY    widX  widY  angl\n')

        # Write parameters for all channels
        for i, chan in enumerate(self.UsedChannels):
            output.write("%5i %10.7f %10.7f %10.3f %10.3f %5.2f %5.2f %5.2f \n"%( chan,\
                self.Gain[i], self.ExtGain[i],\
                self.Offsets[0, i], self.Offsets[1, i],\
                self.FWHM[0, i], self.FWHM[1, i], self.Tilt[i] ))

        output.write("\n")
        output.close()

    #----------------------------------------------------------------------------
    def retrieveRCP(self,MJD=0,filename=None):
        """update the current Received Channel Parameter - see updateRCp() -
             with the proper rcp file given an MJD date

        Parameters
        ----------
        MJD : float
            MJD date to look for
        filename : str
            the filename to look for (default 'FeBe'.rcps)
        """

        if not filename:
            filename = self.FeBe+'.rcps'

        try:
            f = file(os.path.join(ReaConfig.rcpPath, filename))
        except IOError:
            self.__MessHand.error("could not open "+filename)
            return

        param = f.readlines()
        f.close()

        mjdstart = []
        mjdstop = []
        rcp = []
        for i in range(len(param)):
            if param[i][0] not in ['!', '#', 'n']:    # skip comments
                tmp = string.split(param[i])
                mjdstart.append(string.atof(tmp[0]))
                mjdstop.append(string.atof(tmp[1]))
                sr = tmp[2]
                rcp.append(sr)

        mjdstart = np.array(mjdstart)
        mjdstop =  np.array(mjdstop)

        rcpname = -1

        for i in range(len(mjdstart)):
            low = mjdstart[i]
            high = mjdstop[i]
            if low <= MJD and MJD < high:
                rcpname = rcp[i]

        self.__MessHand.longinfo("Retrieved "+rcpname+" from "+filename)

        flagList = self.updateRCP(rcpname)
        # return flagList


    #----------------------------------------------------------------------------
    def readAdditionnalIndexFile(self,indexFile='match.dat', refColumn=0, indexColumn=1, comment=['!', '#', ';']):
        """Read a list of additional index from an ASCII file, to be used with selectAdditionnalIndex()

        Parameters
        ----------
        indexFile : str
            the name of the file to read the ...
        refColumn : int
            the column of channel number and ... (default 0, the first column)
        indexColumn : int
            the column to match the channel with (default 1, the second column)
        comment : list of char
            comment character (default ['!', '#', ';'])
        """

        try:
            f = file(indexFile)
        except IOError:
            self.__MessHand.error("could not open file %s"%(indexFile))
            return

        # read and process RCP file
        fileContent = f.readlines()
        f.close()

        boloIndex, addIndex = [], []

        for i in xrange(len(fileContent)):
            # skip comments
            if fileContent[i][0] in comment:
                continue

            tmp = string.split(fileContent[i])
            boloIndex.append(string.atoi(tmp[refColumn]))
            addIndex.append(tmp[indexColumn])

        s_addIndex = [None]*self.NChannels

        # Reorder if necessary
        for i in xrange(len(boloIndex)):
            s_addIndex[boloIndex[i]-1] = addIndex[i]

        self.AddIndex = s_addIndex

    #----------------------------------------------------------------------------
    def selectAdditionnalIndex(self,value=None):
        """Select according to the additionnal Index

        Parameters
        ----------
        value : str
            the value to test

        Returns
        -------
        list
            the corresponding list

        """

        addIndex = self.AddIndex
        List = []
        for index in range(len(addIndex)):
            if addIndex[index] == str(value):
                List.append(index+1)

        # Check for observed channels
        if List != []:
            List = self.checkChanList(List)

        self.__MessHand.info("selected %i channel(s) with index eq %s"%(len(List), value))

        return List

    #----------------------------------------------------------------------------
    def checkChanList(self,inList,flag=[],getFlagged=0):
        """Return a list of valid channels

        Parameters
        ----------
        inList : list of int or string
            list of channel numbers to get, or empty list to get the complete list of unflagged channels, or
            'all' or 'al' or 'a' to get the complete list of channels
        flag : list of int
            retrieve data flagged or unflagged accordingly
        getFlagged : bool
            flag revers to flagged/unflagged data

            +--------+------------+-----------------------------------------+
            | flag   | getFlagged | Retrieve..                              |
            +========+============+=========================================+
            | 'None' |  False     | all data                                |
            +--------+------------+-----------------------------------------+
            | []     |  False     | unflagged data (default)                |
            +--------+------------+-----------------------------------------+
            | []     |  True      | data with at least one flag set         |
            +--------+------------+-----------------------------------------+
            | 1      |  False     | data with flag 1 not set                |
            +--------+------------+-----------------------------------------+
            | 1      |  True      | data with flag 1 set                    |
            +--------+------------+-----------------------------------------+
            | [1,2]  |  False     | data with neither flag 1 nor flag 2 set |
            +--------+------------+-----------------------------------------+
            | [1,2]  |  True      | data with either flag 1 or flag 2 set   |
            +--------+------------+-----------------------------------------+

        Returns
        -------
        int array
             list of channel numbers
        """

        chanList = []
        if inList in ['all', 'al', 'a']:
            inList = self.UsedChannels
        elif inList == []:
            inList = self.CurrChanList
        elif isinstance(inList, int):
            inList = [inList]

        UsedChannels = self.UsedChannels

        if flag in ['', 'None']:
            for num in inList:
                if num in UsedChannels:
                    chanList.append(num)
        else:
            if getFlagged:
                for num in inList:
                    if (num in UsedChannels) and \
                       self.FlagHandler.isSetOnIndex(num-1, flag):
                        chanList.append(num)
            else:
                for num in inList:
                    if num in UsedChannels and \
                       self.FlagHandler.isUnsetOnIndex(num-1, flag):
                        chanList.append(num)
        return np.array(chanList)

    #----------------------------------------------------------------------------
    def setCurrChanList(self,chanList='?'):
        """set list of channels to be treated

        Parameters
        ----------
        chanList : list of int or string or '?'
             list of channels, or string '?' to get current list of channels,
             or string 'a' or 'al' or 'all' to set current list to all possible channels.
        """

        if chanList in ["all", "al", "a"]:
            self.CurrChanList = self.checkChanList('all')
        elif isinstance(chanList, list):
            self.CurrChanList = self.checkChanList(chanList)
        else:
            self.__MessHand.error("channel list required ")

        self.__MessHand.info("selected channels = " + self.printCurrChanList())

    #----------------------------------------------------------------------------
    def printCurrChanList(self):
        """print the current channel list in somehow "clever" way

        Returns
        ------
        str
           a pretty list of the currently selected channels
        """

        return prettyPrintList(self.CurrChanList)

    #----------------------------------------------------------------------------
    def plotArray(self,overplot=False, num=False, limitsX=[], limitsY=[], ci=3, ellipses=False, colorAddIndex=False):
        """plot the receiver parameters

        Parameters
        ----------
        overplot: bool
            do we overplot ?
        num : bool
            do we print chan numbers ?
        limitsX, limitsY : list of 2 ints, optional
            limits in X and Y
        ellipses : bool
            do we plot ellipses instead of circle ?
        colorAddIndex : bool
            do we use the additionnal index for color ?
        """

        offsetsX, offsetsY = self.Offsets
        refChannel         = self.RefChannel
        if ellipses:
            beamSize       = self.FWHM/2
            beamTilt       = self.Tilt
        else:
            nc             = self.NChannels
            beamSize       = np.ones([2, nc])*self.BeamSize/2
            beamTilt       = np.zeros(nc)


        if colorAddIndex:
            uniqAddIndex   = np.unique(self.AddIndex).tolist()
            colorIndex     = [uniqAddIndex.index(i) for i in self.AddIndex]
        else:
            colorIndex     = np.zeros(self.NChannels, np.int)+ci

        offsetsX           = offsetsX - offsetsX[self.getChanIndex(refChannel)]
        offsetsY           = offsetsY - offsetsY[self.getChanIndex(refChannel)]

        # TODO plot circles which diameter is propto gain

        if not overplot:
            if not limitsX:
                limitsX = [np.nanmin(offsetsX), np.nanmax(offsetsX)]
            if not limitsY:
                limitsY = [np.nanmin(offsetsY), np.nanmax(offsetsY)]

            # empty plot
            Plot.plot(offsetsX, offsetsY, \
                      limitsX=limitsX, limitsY=limitsY, \
                      caption = self.FeBe, \
                      labelX ="\gD Az ['']", labelY="\gD El ['']",\
                      aspect=1, nodata=1)

        # plot the flagged channel in grey
        mask = self.FlagHandler.isSetMask()
        offsetFlagged   = np.compress(mask, [offsetsX, offsetsY], axis=1)
        beamSizeFlagged = np.compress(mask, beamSize, axis=1)
        beamTiltFlagged = np.compress(mask, beamTilt)

        if offsetFlagged.shape[1] != 0:
            for iOffset, iSize, iTilt in zip(offsetFlagged.transpose(), beamSizeFlagged.transpose(), beamTilt):
                Forms.ellipse(iOffset[0], iOffset[1],\
                                  iSize[0], iSize[1], iTilt, ci=14)

        # overplot used channels
        for i in self.UsedChannels:
            if self.FlagHandler.isUnsetOnIndex(i-1):
                # RefChannel in red
                if i == refChannel:
                    Forms.ellipse(offsetsX[i-1], offsetsY[i-1], beamSize[0][i-1], beamSize[1][i-1], beamTilt[i-1], ci=2)
                else:
                    Forms.ellipse(offsetsX[i-1], offsetsY[i-1], beamSize[0][i-1], beamSize[1][i-1], beamTilt[i-1], ci=colorIndex[i-1])

        # overplot the channels number for the UsedChannels only
        if num:
            for i in self.UsedChannels:
                if self.FlagHandler.isUnsetOnIndex(i-1):
                    Plot.xyout(offsetsX[i-1], offsetsY[i-1], str(i))

    # ----------------------------------------------------------------------------
    # def plotGain(self, style='idl4'):
    #     """
    #     DES: plot the gain of the Array
    #     INP: (str) style : the style to be used (default idl4)
    #     WAR: the receiver without know offsets should be flagged
    #     """

    # This function needs a special treatment.
    # Do not delete unless you know what you are doing.

    #     NCP = 4
    #     receiverPositionX = self.get('ReceiverPositionX')
    #     receiverPositionY = self.get('ReceiverPositionY')
    #     receiverGain      = self.get('ReceiverGain')
    #     nX = 100
    #     nY = 100
    #     X = np.arange(nX,np.float32)/(nX)*\
    #         (np.max(receiverPositionX)-np.min(receiverPositionX))\
    #         +np.min(receiverPositionX)
    #     Y = np.arange(nY,np.float32)/(nY)*\
    #         (np.max(receiverPositionY)-np.min(receiverPositionY))\
    #         +np.min(receiverPositionY)
    # TODO: This is unknown....
    #     import interpsf
    #     image = interp.interpsf(NCP,\
    #                             receiverPositionX,\
    #                             receiverPositionY,\
    #                             receiverGain,\
    #                             X,Y)

    # Flag data outside of the array, assume the array is embeded in a circle
    #     image = ravel(image)
    #     imageX = np.transpose(np.array([X]*nY))
    #     imageY = np.array([Y]*nX)
    #     dist = np.ravel(np.sqrt(imageX**2+imageY**2))
    #     maxDist = np.max(np.sqrt(receiverPositionX**2+receiverPositionY**2))
    #     image = np.where(np.greater_equal(maxDist,dist),image,float('Nan'))
    #     image = np.reshape(image,[nX,nY])


    #     Plot.draw(image,sizeX=[np.min(X),np.max(X)],\
    #               sizeY=[np.min(Y),np.max(Y)],\
    #               aspect=1,wedge=1,nan=1,caption = self.FeBe, \
    #               labelX ="\gD Az ['']", labelY="\gD El ['']", style=style)

    #     self.plotArray(overplot=1)

    #----------------------------------------------------------------------------
    def __computeBeamSize(self):
        """Compute the beam size in arcsec, airy pattern formulae"""

        c0 = 299792458.0	                        #speed of light m/s

        self.BeamSize = 1.22*c0/(self.EffectiveFrequency) / \
                        self.Telescope.Diameter / \
                        (np.pi/180.0/3600)                 # airy pattern in arcsec

    #----------------------------------------------------------------------------
    def getChanSep(self,chanList=[]):
        """return the channel separation in both direction from the reference channel

        Parameters
        ----------
        chanList : array
           the desired channel list

        Returns
        -------
        tuple of arrays
           the channel separation in array parameter system wrt the reference channel
        """

        chanIndex = self.getChanIndex(chanList)
        refChanIndex = self.getChanIndex(self.RefChannel)

        boloAz = np.take(self.Offsets[0,:], chanIndex)-self.Offsets[0, refChanIndex]
        boloEl = np.take(self.Offsets[1,:], chanIndex)-self.Offsets[1, refChanIndex]

        # if "NASMYTH" in self.DewCabin:
        #     NInt = np.size(cosNAS)
        #     chanOffsets = np.array([[boloAz], [boloEl]]).repeat(NInt, axis=1)
        #     for index in np.arange(NInt):
        #         chanOffsets[:,index] = np.dot(np.array([[cosNAS[index], -sinNAS[index]],[sinNAS[index],cosNAS[index]]]),chanOffsets[:,index])
        #     boloAz = chanOffsets[0,:]
        #     boloEl = chanOffsets[1,:]

        return boloAz, boloEl

    #----------------------------------------------------------------------------
    def __computeChanSep(self):
        """Compute separation between pixels [arcsec]"""

        nc = self.NChannels
        ChannelSep = np.zeros((nc, nc), np.float32)
        Parameters = self.Offsets
        if (nc > 1): # to avoid crash for single-pixel receivers
            for i in range(nc):
                dx = Parameters[0, i] - Parameters[0,:]
                dy = Parameters[1, i] - Parameters[1,:]
                ChannelSep[i,:] = np.sqrt(dx*dx + dy*dy)

        self.ChannelSep = ChannelSep

    #----------------------------------------------------------------------------
    def fourpixels(self):
        """returns a list of 4 non-flagged channel numbers, selected as follows:
             - the reference channel
             - the two closest neighbours to the ref
             - the furthest one

        Returns
        ------
        list
           list of pixels
        """

        ok = self.checkChanList([])  # non-flagged channels
        ok = ok - 1       # python numbering
        ref = self.RefChannel - 1
        refSep = self.ChannelSep[ref,:] # distances to ref chan
        refSep = np.take(refSep, ok)     # keep only unflagged ones
        result = [self.RefChannel]
        # now find the nearest neighbour
        minsep = np.max(refSep)
        minNum = 0
        for i in range(len(ok)):
            if refSep[i] < minsep and refSep[i] > 0:
                minsep = refSep[i]
                minNum = ok[i]+1
        result.append(minNum)
        # do it again to find the next neighbour and the furthest away
        minsep2 = np.max(refSep)
        minNum2 = 0
        for i in range(len(ok)):
            if refSep[i] < minsep2 and refSep[i] > minsep:
                minsep2 = refSep[i]
                minNum2 = ok[i]+1
            if refSep[i] == np.max(refSep):
                maxNum = ok[i]+1
        result.append(minNum2)
        result.append(maxNum)
        return result

    #----------------------------------------------------------------------------
    def flag(self,chanList=[],flag=1):
        """assign flags to a list of channels

        Parameters
        ----------
        chanList : int array
            list the channels to be flaged
        flag : int
            flag values (default 1)

        Returns
        -------
        int
           number of flag channels
        """

        chanList = self.checkChanList(chanList, flag='None', getFlagged=0)
        chanListIndexes = self.getChanIndex(chanList)

        nChannels = self.NChannels

        if self.RefChannel in chanList and flag != 0 :
            self.__MessHand.warning('Reference channel flagged')

        countFlag = 0
        flaggedChan = []

        for index, chan in zip(chanListIndexes, chanList):
            if self.FlagHandler.isUnsetOnIndex(index, flag):
                self.FlagHandler.setOnIndex(index, flag)
                countFlag += 1
                flaggedChan.append(chan)
        self.__MessHand.info(' %i channel(s) flagged (%s) with flag %s' %\
                             (countFlag, str(flaggedChan), str(flag)))

        self.__MessHand.debug("Flags="+str(self.FlagHandler.getFlags()))

        return countFlag
    #----------------------------------------------------------------------------

    def unflag(self,chanList=[],flag=[]):
        """unflags a list of channels

        Parameters
        ----------
        chanList : int array
            list of channels to be unflaged (default all)
        flag : int list
            flag values to remove (default []: unset all flags)

        Returns
        -------
        int
           number of unflag channels
        """

        chanList = self.checkChanList(chanList, flag='None', getFlagged=0)
        chanListIndexes = self.getChanIndex(chanList)

        nChannels = self.NChannels

        countFlag = 0
        flaggedChan = []

        for index, chan in zip(chanListIndexes, chanList):
            if self.FlagHandler.isSetOnIndex(index, flag):
                self.FlagHandler.unsetOnIndex(index, flag)
                countFlag += 1
                flaggedChan.append(chan)
        self.__MessHand.info(' %i channel(s) unflagged (%s) with flag %s' %\
                             (countFlag, str(flaggedChan), str(flag)))

        self.__MessHand.debug("Flags="+str(self.FlagHandler.getFlags()))

        return countFlag

    #----------------------------------------------------------------------------

    def rotateArray(self, angle):
        """rotate array offsets by a given angle

        Parameters
        ----------
        angle : float
           angle (in degree)
        """
        # TODO: rotate w.r.t optical axis
        angle = np.radians(angle)
        rotMatrix = np.array([[np.cos(angle), -1.*np.sin(angle)], [np.sin(angle), np.cos(angle)]], 'f')
        nc = self.NChannels
        for i in range(nc):
            self.Offsets[:, i] = np.dot(rotMatrix, self.Offsets[:, i])

    def rotateDewar(self):
        """rotate array using dewar rotation angle"""

        self.rotateArray(self.DewUser+self.DewExtra)

    #----------------------------------------------------------------------------
    def getChanIndex(self,chanList=[]):
        """convert from channel ID to index in UsedChannel

        Parameters
        ----------
        chanList : int array
            the channel ID

        Returns
        -------
        int list
            the corresponding index (-1 if failed)
        """

        if isinstance(chanList, int):
            chanList = [chanList]

        indexing      = np.arange(self.NUsedChannels)
        usedChannels  = self.UsedChannels

        outIndexes = []
        notUsedChannel = []

        for chan in chanList:
            out, n = fUtilities.icompress(indexing, usedChannels, chan)
            if n == 1:
                outIndexes.append(out[0])
            else:
                outIndexes.append(-1)
                notUsedChannel.append(chan)

        if notUsedChannel:
            self.__MessHand.error("channel %s not used"%str(notUsedChannel))

        return np.array(outIndexes)


#----------------------------------------------------------------------------------
#----- ScanParameter Class -------------------------------------------------------
#----------------------------------------------------------------------------------

class ScanParameter:
    """..class:: ScanParameter (class)
    :synopsis: Define all parameters (coordinates, time) for a scan
    """

    def __init__(self):
        """Instanciation of a new ScanParameter object """

        self.__MessHand = ReaMessageHandler.MessHand(self.__module__)

        # General parameters about the SCAN type and geometry
        self.ScanNum  = 0
        self.DateObs  = ""
        self.ScanType = ""
        self.ScanMode = ""
        self.ScanDir  = []  # will be a list of strings
        self.LineLen  = 0.0
        self.LineYsp  = 0.0
        self.AzVel    = 0.0
        self.Tau      = 0.0

        # Object
        self.Object   = ""        # Object name
        self.Equinox  = 2000.0    # Default Equinox J2000
        self.Basis    = ("", "")  # Astronomical Basis Frame should be ('ALON-SFL', 'ALAT-SFL')
        self.Coord    = (0.0, 0.0) # object coordinates in the basis frame
        self.Frames   = ""        # basis + user frames, e.g. "EQEQHO"

        # Wobbler
        self.WobUsed    = 0
        self.WobMode    = ""
        self.WobThrow   = 0.0
        self.WobCycle   = 0.0
        self.WobblerSta = []     # LIST of strings (strings don't support arrays)
        self.WobblerPos = np.array([], np.float32)
        # this will contain pairs of On-Off integration numbers, if wobbler used
        self.OnOffPairs  = []

        # Pointing and focus status at scan start
        self.Nula     = 0.0
        self.Nule     = 0.0
        self.Colstart = 0.0

        # Total number of integrations:
        self.NInt     = 0

        # Focus positions: X, Y, Z, XTILT, YTILT
        self.FocX    = np.array([], np.float32)
        self.FocY    = np.array([], np.float32)
        self.FocZ    = np.array([], np.float32)
        self.PhiX    = np.array([], np.float32)
        self.PhiY    = np.array([], np.float32)

        # Telescope coordinates in User and Basis systems
        self.LST      = np.array([], np.float32)
        self.MJD      = np.array([], np.float32)
        self.UT       = np.array([], np.float32)
        self.Az       = np.array([], np.float32)   # This is always absolute Az
        self.El       = np.array([], np.float32)   # This is always absolute El

        # added 20080707 MN
        self.MeanRa   = np.array([], np.float32)
        self.MeanDec  = np.array([], np.float32)

        self.LonOff   = np.array([], np.float32)   # Offsets in User native frame
        self.LatOff   = np.array([], np.float32)
        self.BasLon   = np.array([], np.float32)   # Absolute positions in Astron. basis frame
        self.BasLat   = np.array([], np.float32)
        self.Rot      = np.array([], np.float32)
        self.LonPole  = np.array([], np.float32)
        self.LatPole  = np.array([], np.float32)
        self.NoddingState = np.array([], np.int0)  # array of integers
        self.AddLonWT = 0       # add wobbler throw to get right azimuth offset?
        self.AddLatWT = 0       # add wobbler throw to get right elev. offset?
        # Galactic coordinates
        self.GLon     = np.array([], np.float32)
        self.GLat     = np.array([], np.float32)
        self.GalAngle = np.array([], np.float32)

        # Offsets in horizontal and equatorial systems
        self.AzOff    = np.array([], np.float32)
        self.ElOff    = np.array([], np.float32)
        self.RAOff    = np.array([], np.float32)
        self.DecOff   = np.array([], np.float32)
        # Source position in equatorial system
        self.RA0      = 0.
        self.Dec0     = 0.
        # Telescope positions in equatorial system (source + offsets)
        self.RA       = np.array([], np.float32)
        self.Dec      = np.array([], np.float32)
        # Parallactic angle = rotation between HO and EQ
        self.ParAngle = np.array([], np.float32)

        # Source coordinates in basis frame for a moving target
        self.Mcrval1  = np.array([], np.float32)
        self.Mcrval2  = np.array([], np.float32)

        # Arrays representing 'subscans'
        self.NObs         = 0                 # Number of subscans in dataset
        self.SubscanNum   = []                # list of integers
        self.SubscanIndex = np.array([], np.int)     # Start/end indices of subscans
        self.SubscanType  = []                # List of strings, ('REF', 'ON', 'OFF'...)
        self.SubscanTime  = []

        # Refraction: one value per subscan
        self.Refraction   = []

        # Ambient temperature - use only value at start
        self.T_amb        = 273.

        # He3 temperature: values and timestamps
        self.TimeHe3      = []  # timestamps in Monitor
        self.TempHe3      = []  # corresponding values
        self.He3Temp      = []  # interpolated to MJD(data)

        # Wind speed and direction:
        self.WindSpeed    = [] # m/s
        self.WindDir      = []
        self.TimeWind     = []

        # pwv
        self.PWV          = [] # mm

        # Bias aplitude, QDAC amplitude, and Bias potsetting to calculate Bias voltage:
        self.BiasAmplitude  = [] # Numeric array per subscan
        self.QdacAmplitude  = [] # Numeric array per subscan
        self.BiasPotsetting = [] # Numeric array per subscan
        self.GainSetting    = []

        # Flags by integration (independant of channels)
        self.FlagHandler = ReaFlagHandler.createFlagHandler(np.array([], np.int32))
        self.iflags = {'TURNAROUND'                   : 1,
                       'ACCELERATION THRESHOLD'       : 2,
                       'ELEVATION VELOCITY THRESHOLD' : 3,
                       'SUBSCAN FLAGGED'              : 7,
                       'TEMPORARY'                    : 8,
                       'BLANK DATA'                   : 9 }

    #----------------------------------------------------------------------------
    def __str__(self):
        """Defines a string, shown when the print instruction is used."""

        out = "Scan number %s : %s  %s on %s contains %3i subscan(s), %5i/%5i records" %\
              (str(self.ScanNum),\
               self.ScanMode,\
               self.ScanType,\
               self.Object,\
               len(self.SubscanNum),\
               self.FlagHandler.nUnset(), \
               len(self.LST))

        if ReaConfig.DEBUG > 2:
            out += "\n" + \
                   attrStr(self, ['_ScanParameter__MessHand']) + \
                   "\n"

        return out

    # ---------------------------------------------------------------------
    # Overload addition operator: used to combine two datasets
    # ---------------------------------------------------------------------
    def __add__(self, other):
        result = copy.deepcopy(self)
        result._coadd(other)
        return result

    def _coadd(self, other):
        # TODO: check that it makes sense to co-add these two datasets
        # TODO: check for missing keywords/attributes!!!
        #
        self.LST           = np.concatenate((self.LST,         other.LST))
        self.MJD           = np.concatenate((self.MJD,         other.MJD))
        self.Az            = np.concatenate((self.Az,          other.Az))
        self.El            = np.concatenate((self.El,          other.El))
        self.RA            = np.concatenate((self.RA,          other.RA))
        self.Dec           = np.concatenate((self.Dec,         other.Dec))
        self.MeanRa        = np.concatenate((self.MeanRa,      other.MeanRa))
        self.MeanDec       = np.concatenate((self.MeanDec,     other.MeanDec))
        self.AzOff         = np.concatenate((self.AzOff,       other.AzOff))
        self.ElOff         = np.concatenate((self.ElOff,       other.ElOff))
        self.RAOff         = np.concatenate((self.RAOff,       other.RAOff))
        self.DecOff        = np.concatenate((self.DecOff,      other.DecOff))
        self.LonOff        = np.concatenate((self.LonOff,      other.LonOff))
        self.LatOff        = np.concatenate((self.LatOff,      other.LatOff))
        self.BasLon        = np.concatenate((self.BasLon,      other.BasLon))
        self.BasLat        = np.concatenate((self.BasLat,      other.BasLat))
        self.LonPole       = np.concatenate((self.LonPole,     other.LonPole))
        self.LatPole       = np.concatenate((self.LatPole,     other.LatPole))
        self.Rot           = np.concatenate((self.Rot,         other.Rot))
        self.ParAngle      = np.concatenate((self.ParAngle,    other.ParAngle))
        self.NoddingState  = np.concatenate((self.NoddingState, other.NoddingState))
        self.UT            = np.concatenate((self.UT,          other.UT))
        self.WobblerPos    = np.concatenate((self.WobblerPos,  other.WobblerPos))
        self.FocX          = np.concatenate((self.FocX,        other.FocX))
        self.FocY          = np.concatenate((self.FocY,        other.FocY))
        self.FocZ          = np.concatenate((self.FocZ,        other.FocZ))
        self.PhiX          = np.concatenate((self.PhiX,        other.PhiX))
        self.PhiY          = np.concatenate((self.PhiY,        other.PhiY))

        slfFlags  = np.concatenate((self.FlagHandler.getFlags(), other.FlagHandler.getFlags()))
        self.FlagHandler = ReaFlagHandler.createFlagHandler(slfFlags)

        # Update subscans-related infos - specific case, some attributes are lists
        self.SubscanNum.extend(other.SubscanNum)
        self.SubscanType.extend(other.SubscanType)
        # SubscanIndex: take into account that we merged two datasets
        # integ number of the last point in dataset 1
        max1 = self.SubscanIndex[1, -1]
        self.SubscanIndex = np.transpose(np.concatenate((np.transpose(self.SubscanIndex),
                                                   np.transpose(other.SubscanIndex+max1))))
        self.NInt = self.NInt + other.NInt
        self.NObs = self.NObs + other.NObs

    #----------------------------------------------------------------------------
    def caption(self):
        """Return a short caption of the scan """

        out = "Scan: %i (%s) -* %s *- %s" %\
              (self.ScanNum, prettyPrintList(self.SubscanNum), self.Object, self.DateObs)
        return out

    # ---------------------------------------------------------------------
    def __fillFromMBFits(self,reader,febe,baseband,subscans,flag=9,\
                       readHe=0,readAzEl0=0,readT=0,readWind=0,readBias=0,readPWV=0):
        """fill a ScanParam object using the MBFitsReader object reader.

        Parameters
        ----------
        reader : MBFitsReader
           MBFitsReader object
        febe : str
           frontend-backend name to select
        baseband : int
           baseband number to select
        subscans : list of int
           list of subscans numbers to read in
        flag : int
           flag for blanked integrations (default: 9 'BLANK DATA')
        readHe, readAzEl0, readT, readWind, readBias : bool
           Extra parameters for LABOCA see TimelineData.read
        """

        self.__MessHand.debug('start of ScanParam.fillFroMBfits')
        try:
            # Some infos about the SCAN - do not change from one obs to the other
            self.ScanNum  = reader.read("ScanNum")
            self.DateObs  = reader.read("DateObs")
            self.ScanType = reader.read("ScanType")
            self.ScanMode = reader.read("ScanMode", subsnum=subscans[0])

            self.Object   = reader.read("Object")
            self.Equinox  = reader.read("Equinox")
            self.Basis    = reader.read("Basis")
            self.Coord    = reader.read("Coord")

            # Description of Basis and User frames
            self.Frames   = reader.read("UsrFrame", subsnum=subscans[0])

            try:
                WobUsed = reader.read("WobUsed")
            except:
                self.__MessHand.warning("No Info on Wobler")
                WobUsed = 'F'
            if (not WobUsed) or (WobUsed == 'F'):
                self.WobUsed  = 0
                self.WobCycle = 0.
                self.WobThrow = 0.
                self.WobMode  = ""
            else:
                self.WobUsed  = 1
                self.WobCycle = float(reader.read("WobCycle"))
                self.WobThrow = reader.read("WobThrow")
                self.WobMode  = reader.read("WobMode")

            # self.Nula     = reader.read("Nula",febe=febe)
            # self.Nule     = reader.read("Nule",febe=febe)
            # self.Colstart = reader.read("Colstart",febe=febe)

            self.DeltaCA  = float(reader.read("DeltaCA"))
            self.DeltaIE  = float(reader.read("DeltaIE"))

            # Time differences between UT1, UTC and TAI
            self.TAIUTC = float(reader.read("TAIUTC"))
            self.UTCUT1 = float(reader.read("UTCUT1"))

            nIntegSubscan = {}
            nIntegTotal = 0
            for subscan in subscans:
                subscanWasOpened = reader.openSubscan(subsnum=subscan)

                nIntegSubscan[subscan] = reader.read("NInteg", \
                                                     subsnum=subscan, \
                                                     febe=febe, \
                                                     baseband=baseband)
                nIntegTotal += nIntegSubscan[subscan]

                if subscanWasOpened:
                    reader.closeSubscan(subsnum=subscan)

            self.NInt = nIntegTotal
            self.NObs = reader.read("NObs")

            LST     = np.zeros((nIntegTotal), np.float32)
            MJD     = np.zeros((nIntegTotal), np.float64)   # Use Float64 for MJD
            Az      = np.zeros((nIntegTotal), np.float32)
            El      = np.zeros((nIntegTotal), np.float32)
            MeanRa  = np.zeros((nIntegTotal), np.float32)
            MeanDec = np.zeros((nIntegTotal), np.float32)
            LonOff  = np.zeros((nIntegTotal), np.float32)
            LatOff  = np.zeros((nIntegTotal), np.float32)
            BasLon  = np.zeros((nIntegTotal), np.float32)
            BasLat  = np.zeros((nIntegTotal), np.float32)
            LonPole = np.zeros((nIntegTotal), np.float32)
            LatPole = np.zeros((nIntegTotal), np.float32)
            Rot     = np.zeros((nIntegTotal), np.float32)
            Mcrval1 = np.zeros((nIntegTotal), np.float32)
            Mcrval2 = np.zeros((nIntegTotal), np.float32)
            # Focus positions
            FocX    = np.zeros((nIntegTotal), np.float32)
            FocY    = np.zeros((nIntegTotal), np.float32)
            FocZ    = np.zeros((nIntegTotal), np.float32)
            PhiX    = np.zeros((nIntegTotal), np.float32)
            PhiY    = np.zeros((nIntegTotal), np.float32)

            # Subscan info:
            SubscanNum  = []
            SubscanType = []
            SubscanDir  = []

            # compute index for 1st subscan start and end using python-style numbering:
            # starting at zero, and ending at nb_elements since last element is excluded
            # WARNING: in fortran modules, will have to use [start+1, end]
            subscan_start = [0]
            subscan_end = [nIntegSubscan[subscans[0]]]

            # Now fill local arrays one subscan after the other
            tmpLen = 0

            for subscan in subscans:
                nbData = nIntegSubscan[subscan]
                if nbData:
                    subscanWasOpened = reader.openSubscan(subsnum=subscan)

                    if tmpLen:  # means it's not the 1st subscan
                        subscan_start.append(subscan_end[-1])
                        subscan_end.append(subscan_end[-1]+nbData)

                    MJD[tmpLen:tmpLen+nbData] = reader.read("MJD",
                                                            subsnum=subscan, febe=febe).astype(np.float64)

                    LST[tmpLen:tmpLen+nbData]     = reader.read("LST",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)
                    Az[tmpLen:tmpLen+nbData]      = reader.read("Az",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)
                    El[tmpLen:tmpLen+nbData]      = reader.read("El",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)

                    try:
                        MeanRa[tmpLen:tmpLen+nbData]  = reader.read("Ra",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        MeanDec[tmpLen:tmpLen+nbData] = reader.read("Dec",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                    except:
                        MeanRa = []
                        MeanDec = []

                    LonOff[tmpLen:tmpLen+nbData]  = reader.read("LonOff",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)
                    LatOff[tmpLen:tmpLen+nbData]  = reader.read("LatOff",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)
                    BasLon[tmpLen:tmpLen+nbData]  = reader.read("BasLon",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)
                    BasLat[tmpLen:tmpLen+nbData]  = reader.read("BasLat",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)
                    Rot[tmpLen:tmpLen+nbData]     = reader.read("RotAngle",
                                                                subsnum=subscan,
                                                                febe=febe).astype(np.float32)

                    if self.WobUsed:
                        self.WobblerSta.extend(reader.read("WobblerSta", subsnum=subscan, febe=febe))

                    # Refraction
                    if self.Frames[:2] == 'HO':
                        self.Refraction.append(reader.read("Refract", subsnum=subscan))
                    else:
                        self.Refraction.append([0])

                    # Ambient temperature at scan start
                    if readT and subscan == subscans[0]:
                        self.T_amb = reader.read("T_amb", subsnum=subscan)
                        self.T_amb = 273.15 + self.T_amb[0]

                    # TODO : Avoid that....
                    if reader.getType() == "ApexMBFitsReader":
                        # Read data not present in IRAM MB-FITS:
                        LonPole[tmpLen:tmpLen+nbData] = reader.read("LonPole",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        LatPole[tmpLen:tmpLen+nbData] = reader.read("LatPole",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)

                        # Coordinates for a moving target
                        Mcrval1[tmpLen:tmpLen+nbData] = reader.read("MVAL1",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        Mcrval2[tmpLen:tmpLen+nbData] = reader.read("MVAL2",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)

                        # Focus positions
                        FocX[tmpLen:tmpLen+nbData]    = reader.read("FocX",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        FocY[tmpLen:tmpLen+nbData]    = reader.read("FocY",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        FocZ[tmpLen:tmpLen+nbData]    = reader.read("FocZ",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        PhiX[tmpLen:tmpLen+nbData]    = reader.read("PhiX",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)
                        PhiY[tmpLen:tmpLen+nbData]    = reader.read("PhiY",
                                                                    subsnum=subscan,
                                                                    febe=febe).astype(np.float32)

                        if readHe:
                            # He3 temperature - WARNING: specific to LABOCA!
                            tmpHe3, timeHe3 = reader.read("TempHe", subsnum=subscan)
                            # Interpolate to the data timestamps
                            mjd     = 86400.*(MJD[tmpLen:tmpLen+nbData] - MJD[0])
                            timeHe3 = 86400.*(timeHe3 - MJD[0])
                            tmpInterp = np.interp(mjd, timeHe3, tmpHe3)

                            self.TimeHe3.extend(timeHe3)
                            self.TempHe3.extend(tmpHe3)
                            self.He3Temp.extend(tmpInterp)

                        if readBias:
                            biasAmplitude  = reader.read("BiasAmplitude", subsnum=subscan)
                            qdacAmplitude  = reader.read("QdacAmplitude", subsnum=subscan)
                            biasPotsetting = reader.read("BiasPotsetting", subsnum=subscan)
                            gainSetting    = reader.read("GainSetting", subsnum=subscan)
                            self.BiasAmplitude.append(biasAmplitude)
                            self.QdacAmplitude.append(qdacAmplitude)
                            self.BiasPotsetting.append(biasPotsetting)
                            self.GainSetting.append(gainSetting)

                        if readWind:
                            windSpeed, windDir, timeWind = reader.read("WindSpeedDir",
                                                                       subsnum=subscan)
                            self.WindSpeed.append(windSpeed)
                            self.WindDir.append(windDir)
                            self.TimeWind.append(timeWind)

                        if readPWV:
                            pwv = reader.read("PWV", subsnum=subscan)
                            self.PWV.append(pwv)

                    #
                    # Fill the subscans related fields
                    SubscanNum.append(subscan)
                    # Subscan type (REF, ON, OFF)
                    SubscanType.append(reader.read("ObsType", subsnum=subscan, febe=febe))
                    # Subscan direction
                    try:
                        SubscanDir.append(reader.read("ScanDir", subsnum=subscan, febe=febe))
                    except:
                        self.__MessHand.warning("Can not find ScanDir in file")
                    # LST time at subscan start
                    self.SubscanTime.append(LST[tmpLen])

                    # Compute float value of subscan start time, using SLALIB
                    date_tmp = reader.read("SubsStart", subsnum=subscan, febe=febe) # string, e.g. 2003-06-08T20:41:21
                    if date_tmp:
                        year, day, status = slalib.sla_clyd(string.atof(date_tmp[0:4]),
                                                     string.atof(date_tmp[5:7]),
                                                     string.atof(date_tmp[8:10]))
                        date_flt = year + (day-1.)/365.
                    else:
                        date_flt = 0.

                    tmpLen += nbData

                    # The following is needed for pointing scans, to generate a .dat
                    # file that is used to compute pointing model
                    if readAzEl0 and subscan == subscans[0]:
                        antenna, encoder = reader.read("AzEl0", subsnum=subscans[0])
                        self.EncAz0 = encoder[0]
                        self.EncEl0 = encoder[1]
                        self.AntAz0 = antenna[0]
                        self.AntEl0 = antenna[1]
                        # when these are requested, we also need the following:
                        self.PDeltaCA = reader.read("PDeltaCA")
                        self.PDeltaIE = reader.read("PDeltaIE")
                        self.FDeltaCA = reader.read("FDeltaCA")
                        self.FDeltaIE = reader.read("FDeltaIE")

                    # Everything has been read, close the file
                    if subscanWasOpened:
                        reader.closeSubscan(subsnum=subscan)

                else:
                    # nbData = 0: subscan not readable (no data)
                    self.__MessHand.warning("Subscan %i not readable (no data)"%(subscan))

            # The following attributes are for the full scan
            NoddingState = np.zeros(nIntegTotal, np.int0)
            UT           = np.zeros(nIntegTotal, np.float32)
            WobblerPos   = np.zeros(nIntegTotal, np.float32)
            SubscanIndex = np.array([subscan_start, subscan_end], np.int)

            # At reading flag the data with blanked LST
            self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros(nIntegTotal, np.int32))
            flagValue = reader.getBlankFloat()
            mask = np.equal(LST, flagValue)
            self.FlagHandler.setOnMask(mask, self.iflags['BLANK DATA'])

            self.LST          = Utilities.as_column_major_storage(LST)
            self.MJD          = Utilities.as_column_major_storage(MJD)
            self.Az           = Utilities.as_column_major_storage(Az)
            if MeanRa:
                self.MeanRa       = Utilities.as_column_major_storage(MeanRa)
                self.MeanDec      = Utilities.as_column_major_storage(MeanDec)
            self.El           = Utilities.as_column_major_storage(El)
            self.LonOff       = Utilities.as_column_major_storage(LonOff)
            self.LatOff       = Utilities.as_column_major_storage(LatOff)
            self.BasLon       = Utilities.as_column_major_storage(BasLon)
            self.BasLat       = Utilities.as_column_major_storage(BasLat)
            self.LonPole      = Utilities.as_column_major_storage(LonPole)
            self.LatPole      = Utilities.as_column_major_storage(LatPole)
            self.Rot          = Utilities.as_column_major_storage(Rot)
            self.NoddingState = Utilities.as_column_major_storage(NoddingState)
            self.UT           = Utilities.as_column_major_storage(UT)
            self.WobblerPos   = Utilities.as_column_major_storage(WobblerPos)
            self.SubscanIndex = Utilities.as_column_major_storage(SubscanIndex)
            self.FocX         = Utilities.as_column_major_storage(FocX)
            self.FocY         = Utilities.as_column_major_storage(FocY)
            self.FocZ         = Utilities.as_column_major_storage(FocZ)
            self.PhiX         = Utilities.as_column_major_storage(PhiX)
            self.PhiY         = Utilities.as_column_major_storage(PhiY)
            self.SubscanNum   = SubscanNum
            self.SubscanType  = SubscanType
            self.ScanDir      = SubscanDir

            # Usefull when having NASMYTH arrays
            self.cosNAS        = np.cos((np.radians(-self.El)))
            self.sinNAS        = np.sin((np.radians(-self.El)))

            self.Mcrval1      = Utilities.as_column_major_storage(Mcrval1)
            self.Mcrval2      = Utilities.as_column_major_storage(Mcrval2)

            del LST, MJD, Az, El, LonOff, LatOff, BasLon, BasLat, \
                LonPole, LatPole, Rot, NoddingState, \
                UT, WobblerPos, SubscanIndex, \
                FocX, FocY, FocZ, PhiX, PhiY

            if self.NInt:
                # at least one subscan successfully read
                # Compute the missing coordinates / offsets
                self.computeRa0De0()

                if self.Frames[-2:] == 'HO':            # user frame = horizontal
                    self.AzOff = copy.copy(self.LonOff) # then we already have the HO offsets
                    self.ElOff = copy.copy(self.LatOff)
                else:
                    self.computeAzElOffsets()

                if self.Frames[:2] == 'EQ':   # basis frame = equatorial
                    if fStat.f_rms(self.BasLon, fStat.f_mean(self.BasLon)):
                        # if not constant
                        self.RA  = copy.copy(self.BasLon) # RA, Dec already available
                        self.Dec = copy.copy(self.BasLat)
                else:
                    # changed 20080717 MN
                    # if basis fram is horizontal, try to read ra, dec from
                    # meanRa, meanDec (not all MBFits versions)
                    if (self.MeanRa) and (self.MeanDec):
                        self.RA  = copy.copy(self.MeanRa)
                        self.Dec = copy.copy(self.MeanDec)
                    else:
                        self.__MessHand.warning('No equatorial coordinte information')
                        self.__MessHand.warning('Computing RA/Dec from telescope coordinates')
                        self.computeRaDec()
                if self.Frames[-2:] == 'EQ':             # user frame = equatorial
                    self.RAOff = copy.copy(self.LonOff)  # then we already have the EQ offsets
                    self.DecOff = copy.copy(self.LatOff)
                else:
                    self.computeRaDecOffsets()
                self.computeParAngle()

            else:
                self.__MessHand.warning("No subscans readable, no data")

        except Exception as data:
            raise

    #----------------------------------------------------------------------------
    def __he3SmoothInterpolate(self,flag=[], getFlagged=0):
        """this is a *function* which *returns* an array with He3 temperatures
             interpolated to the data timestamps, with a smoothing (boxcar window
             applied) before interpolating

        Parameters
        ----------
        flag : list of int
           retrieve data flagged or unflagged accordingly
        getFlagged : bool
           getFlagged : flag revers to flagged/unflagged data

                                 +--------+------------+-----------------------------------------+
                                 | flag   | getFlagged | Retrieve..                              |
                                 +========+============+=========================================+
                                 | 'None' |  False     | all data                                |
                                 +--------+------------+-----------------------------------------+
                                 | []     |  False     | unflagged data (default)                |
                                 +--------+------------+-----------------------------------------+
                                 | []     |  True      | data with at least one flag set         |
                                 +--------+------------+-----------------------------------------+
                                 | 1      |  False     | data with flag 1 not set                |
                                 +--------+------------+-----------------------------------------+
                                 | 1      |  True      | data with flag 1 set                    |
                                 +--------+------------+-----------------------------------------+
                                 | [1,2]  |  False     | data with neither flag 1 nor flag 2 set |
                                 +--------+------------+-----------------------------------------+
                                 | [1,2]  |  True      | data with either flag 1 or flag 2 set   |
                                 +--------+------------+-----------------------------------------+
        Returns
        -------
        float array
           interpolated He3 temperatures are returned

        """
        if not len(self.TimeHe3):
            self.__MessHand.error("No He3 temperature available - returning")
            self.__MessHand.error("You should use 'read(<scan>,readHe=1)'")
            return

        he3time = np.array(self.TimeHe3)  # timestamps in Monitor table
        he3temp = np.array(self.TempHe3)  # corresponding values
        mjd = self.get('mjd', flag=flag, getFlagged=getFlagged)

        # smooth he3temp monitor points
        nb = int(np.max(he3time))+1
        newx = np.arange(nb, dtype=np.float)
        newy = np.zeros(nb, dtype=np.float)

        # compute max. of delta time
        tmptime = he3time[1::]-he3time[:-1]
        tmptime = tmptime.tolist()
        tmptime.append(2.*he3time[0])  # delta time between start and 1st datapoint
        deltatime = int(np.max(tmptime)/2.+1)

        # smoothing
        for i in range(nb):
            mask = np.nonzero(np.less(abs(he3time - newx[i]), deltatime))
            newy[i] = fStat.f_mean(np.take(he3temp, mask))

        # interpolate he3temp to a regular time grid
        dt = fStat.f_median (mjd[1::]-mjd[:-1])  # delta time
        n = int(np.max(mjd)/dt)+1
        tt = dt*np.array(range(n), 'f')  # regular timestream covering the scan
        yy = np.interp(tt, newx, newy)

        # finally interpolate he3temp to original time stamps
        he3T = np.interp(mjd, tt, yy)
        return he3T

    #----------------------------------------------------------------------------
    #----------------------------------------------------------------------------
    def computeRa0De0(self):
        """compute source coordinates in equatorial system """

        self.__MessHand.debug('start of ScanParam.computeRa0De0')
        if self.Frames[:2] == 'EQ':   # basis frame = equatorial
            self.RA0  = self.Coord[0]
            self.Dec0 = self.Coord[1]
        elif self.Frames[:2] == 'HO': # basis frame = horizontal
            az0 = np.radians(self.Coord[0])
            # el0 = self.Coord[1] * np.pi/180.
            el0  = np.radians(self.Coord[1] - self.Refraction[0][0])
            phi = np.radians(self.Telescope.Latitude)
            ha, dec = slalib.sla_h2e(az0, el0, phi)
            # last = gmst + data.ReceiverArray.Telescope.Longitude * np.pi/180. + slalib.sla_eqeqx(mjd)
            # + UT1-TAI...
            lst0 = np.radians(self.LST[0] * 360./86400.)
            ra = lst0 - ha # in equinox = obs. date, precess to J2000
            date = self.DateObs
            year, day, status = slalib.sla_calyd(int(date[:4]), int(date[5:7]), int(date[8:10]))
            ra_0, de_0 = slalib.sla_preces ('FK5', float(year)+float(day)/365.25, 2000., ra, dec)
            self.RA0  = np.degrees(ra_0)
            self.Dec0 = np.degrees(de_0)

        else:   # other systems not supported yet
            self.__MessHand.warning('Unsupported astronomical basis frame: '+self.Frames[:2])
            self.__MessHand.warning('RA, Dec of the source not computed')

    #----------------------------------------------------------------------------
    def computeAzElOffsets(self):
        """compute telescope Az, El offsets w.r.t. the source, using antenna
             Az, El and RA, Dec of the source"""

        self.__MessHand.debug('start of ScanParam.computeAzElOffsets')
        nb = self.NInt
        AzOff = np.zeros((nb), np.float32)
        ElOff = np.zeros((nb), np.float32)
        ra0 = np.radians(self.RA0)
        de0 = np.radians(self.Dec0)
        # Precess to date of obs.
        mjd0 = self.MJD[0]
        epoch = slalib.sla_epj(mjd0)
        ra0, de0 = slalib.sla_map(ra0, de0, 0, 0, 0, 0, 2000, mjd0)  # precess + mean to apparent

        TAI_TT  = 32.184
        TAI_UTC = -1.*self.TAIUTC
        UTC_UT1 = self.UTCUT1
        TAI_UT1 = TAI_UTC + UTC_UT1
        beta = np.radians(self.Telescope.Longitude)
        phi = np.radians(self.Telescope.Latitude)

        # convert RA0, Dec0 to Az0, El0 for each time stamp
        for i in np.arange(nb):
            mjd = self.MJD[i]   # this is MJD TAI
            mjd_ut1 = mjd + TAI_UT1/86400. # MJD UT1
            mjd_ut1 -= TAI_UTC/86400 # NIKA (30m alreay in UTC)
            mjd_tt = mjd + TAI_TT/86400.    # MJD TT, = TDB within a few ms
            mjd_tt -= TAI_TT/86400. # NIKA (30m in UTC)
            gmst = slalib.sla_gmsta(int(mjd_ut1), mjd_ut1-int(mjd_ut1))
            lst = gmst + beta + slalib.sla_eqeqx(mjd_tt)
            ha = lst - ra0
            az0, el0 = slalib.sla_e2h(ha, de0, phi)
            AzOff[i] = np.radians(self.Az[i]) - az0
            AzOff[i] = slalib.sla_drange(AzOff[i])
            AzOff[i] = np.degrees(AzOff[i]) * np.cos(np.radians(self.El[i]))
            ElOff[i] = np.radians(self.El[i]) - el0
            ElOff[i] = np.degrees(slalib.sla_drange(ElOff[i]))
        self.AzOff = Utilities.as_column_major_storage(AzOff)
        self.ElOff = Utilities.as_column_major_storage(ElOff)

    #----------------------------------------------------------------------------
    def computeRaDec(self):
        """compute telescope RA, Dec positions from Az, El"""

        self.__MessHand.debug('start of ScanParam.computeRaDec')
        nb = self.NInt
        ra  = np.zeros((nb), np.float32)
        dec = np.zeros((nb), np.float32)
        az  = np.radians(self.Az)
        el  = np.radians(self.El - self.Refraction[0][0])
        phi = np.radians(self.Telescope.Latitude)
        mjd0 = self.MJD[0]

        # convert Az, El to RA, Dec for each time stamp
        for i in np.arange(nb):
            lst = np.radians(self.LST[i] * 360./86400.) # lst in radians
            ha, dec0 = slalib.sla_dh2e(az[i], el[i], phi) # radians, radians
            ra0 = lst - ha # in equinox = obs. date, precess to J2000
            ra_0, de_0 = slalib.sla_amp(ra0, dec0, mjd0, 2000.)  # precess + apparent to mean
            ra[i]  = np.degrees(ra_0)
            dec[i] = np.degrees(de_0)
        self.RA  = Utilities.as_column_major_storage(ra)
        self.Dec = Utilities.as_column_major_storage(dec)

    #----------------------------------------------------------------------------
    def computeRaDecOffsets(self):
        """compute telescope RA, Dec offsets w.r.t. the source, GLS projection"""

        # TODO : Projection here
        self.__MessHand.debug('start of ScanParam.computeRaDecOffsets')
        self.RAOff = (self.RA - self.RA0)*np.cos(np.radians(self.Dec))
        self.DecOff = self.Dec - self.Dec0

    #----------------------------------------------------------------------------
    def computeParAngle(self):
        """compute parallactic angle"""

        self.__MessHand.debug('start of ScanParam.computeParAngle')
        nb = self.NInt
        parAng = np.zeros((nb), np.float32)
        lst = np.radians(self.LST * 360./86400.)
        ra  = np.radians(self.RA)
        ha = lst - ra
        dec = np.radians(self.Dec)
        phi = np.radians(self.Telescope.Latitude)
        for i in np.arange(nb):
            ang = slalib.sla_pa (ha[i], dec[i], phi)
            parAng[i] = np.degrees(ang)  # in degrees
        self.ParAngle = Utilities.as_column_major_storage(parAng)

    #----------------------------------------------------------------------------
    def computeGal(self):
        """compute telescope GLon, GLat positions from RA, Dec"""

        self.__MessHand.debug('start of ScanParam.computeGal')
        nb = self.NInt
        gl  = np.zeros((nb), np.float32)
        gb = np.zeros((nb), np.float32)
        ra  = np.radians(self.RA)
        dec = np.radians(self.Dec)
        # convert RA,Dec to gl,gb for each time stamp
        for i in np.arange(nb):
            tmpgl, tmpgb = slalib.sla_eqgal(ra[i], dec[i])
            gl[i] = np.degrees(tmpgl)
            if gl[i] > 180.:
                gl[i] = gl[i]-360.
            gb[i] = np.degrees(tmpgb)
        self.GLon = Utilities.as_column_major_storage(gl)
        self.GLat = Utilities.as_column_major_storage(gb)

    #----------------------------------------------------------------------------
    def computeGalAngle(self):
        """compute angle EQ to GAL"""

        self.__MessHand.debug('start of ScanParam.computeGalAngle')
        nb = self.NInt
        galAng = np.zeros((nb), np.float32)
        ra  = np.radians(self.RA)
        dec = np.radians(self.Dec+1.)
        gl  = np.radians(self.GLon)
        gb  = np.radians(self.GLat)
        for i in np.arange(nb):
            gl1, gb1 = slalib.sla_eqgal(ra[i], dec[i])
            if gl1 > np.pi:
                gl1 = gl1-2.*np.pi
            ang = arctan((gl1-gl[i])/(gb1-gb[i]))
            galAng[i] = np.degrees(ang)  # in degrees
        self.GalAngle = Utilities.as_column_major_storage(galAng)

    #----------------------------------------------------------------------------
    #----------------------------------------------------------------------------
    def flipOffsets(self,system='eq'):
        """change sign of telescope offsets w.r.t. reference position

        Parameters
        ----------
        system : str, 'eq' or 'ho'
           to flip RA/Dec offsets or Az/El  offsets (default: 'eq')
        """
        if string.upper(system) == 'EQ':
            self.RA = 2.*self.RA0 - self.RA
            self.Dec = 2.*self.Dec0 - self.Dec
            self.RAOff = -1.*self.RAOff
            self.DecOff = -1.*self.DecOff
        elif string.upper(system) == 'HO':
            self.AzOff = -1.*self.AzOff
            self.ElOff = -1.*self.ElOff
        else:
            self.__MessHand.error('Unkown coordinate system')

    #
    # Methods related with chopped data
    #----------------------------------------------------------------------------
    def computeOnOff(self):
        """determine ON-OFF pairs from content of WobblerSta, and fill
             OnOffPairs attribute with pairs of integration numbers.
             The result is a 2 x Nb_Integ. array of integers.
        """

        # Get number of integrations
        nd = self.NInt
        num1, num2 = 0, 0

        if self.OnOffPairs:
            # if already exists, may be of type array
            # => convert to list for appending new pairs
            self.OnOffPairs = self.OnOffPairs.tolist()
        while ((num1 < nd-1) & (num2 < nd-1)):
            # Initialise flags, set when one ON-OFF pair is found
            okOn, okOff = 0, 0
            # Find the next (ON,OFF) pair
            while ((okOn == 0) & (num1 < nd-1)):
                if (self.WobblerSta[num1] not in ['ON', 1]):
                    num1 += 1
                else:
                    okOn = 1
            num2 = num1+1
            while ((okOff == 0) & (num2 < nd)):
                if (self.WobblerSta[num2] in ['ON', 1]):
                    num1 = num2
                    num2 += 1
                else:
                    okOff = 1

            if (okOn & okOff):
                self.OnOffPairs.append([num1, num2])
                num1 += 1

        if self.OnOffPairs:
            self.OnOffPairs = np.array(self.OnOffPairs)
            self.NInt = len(self.OnOffPairs[:, 0])


    #----------------------------------------------------------------------------
    def _phaseDiffParam(self):
        """Compute the phase differences for data associated parameters.
             Times are average of ON and OFF, coordinates are ON positions.
        """

        # compute times: (time(on)+time(off)) / 2.
        self.LST = (np.take(self.LST, self.OnOffPairs[:, 0]) + \
                                np.take(self.LST, self.OnOffPairs[:, 1]))/2.
        self.MJD = (np.take(self.MJD, self.OnOffPairs[:, 0]) + \
                                np.take(self.MJD, self.OnOffPairs[:, 1]))/2.
        self.UT = (np.take(self.UT, self.OnOffPairs[:, 0]) + \
                                np.take(self.UT, self.OnOffPairs[:, 1]))/2.

        # compute positions = position(on)
        self.Az      = np.take(self.Az,      self.OnOffPairs[:, 0])
        self.El      = np.take(self.El,      self.OnOffPairs[:, 0])
        self.AzOff   = np.take(self.AzOff,   self.OnOffPairs[:, 0])
        self.ElOff   = np.take(self.ElOff,   self.OnOffPairs[:, 0])
        self.RA      = np.take(self.RA,      self.OnOffPairs[:, 0])
        self.Dec     = np.take(self.Dec,     self.OnOffPairs[:, 0])
        self.MeanRa  = np.take(self.MeanRa,  self.OnOffPairs[:, 0])
        self.MeanDec = np.take(self.MeanDec, self.OnOffPairs[:, 0])
        self.RAOff   = np.take(self.RAOff,   self.OnOffPairs[:, 0])
        self.DecOff  = np.take(self.DecOff,  self.OnOffPairs[:, 0])
        self.LonOff  = np.take(self.LonOff,  self.OnOffPairs[:, 0])
        self.LatOff  = np.take(self.LatOff,  self.OnOffPairs[:, 0])
        self.BasLon  = np.take(self.BasLon,  self.OnOffPairs[:, 0])
        self.BasLat  = np.take(self.BasLat,  self.OnOffPairs[:, 0])
        self.LonPole = np.take(self.LonPole, self.OnOffPairs[:, 0])
        self.LatPole = np.take(self.LatPole, self.OnOffPairs[:, 0])
        self.Rot     = np.take(self.Rot,     self.OnOffPairs[:, 0])
        self.ParAngle = np.take(self.ParAngle, self.OnOffPairs[:, 0])

        # Focus positions: use average of ON and OFF positions
        self.FocX   = (np.take(self.FocX, self.OnOffPairs[:, 0]) + \
                        np.take(self.FocX, self.OnOffPairs[:, 1]))/2.
        self.FocY   = (np.take(self.FocY, self.OnOffPairs[:, 0]) + \
                        np.take(self.FocY, self.OnOffPairs[:, 1]))/2.
        self.FocZ   = (np.take(self.FocZ, self.OnOffPairs[:, 0]) + \
                        np.take(self.FocZ, self.OnOffPairs[:, 1]))/2.
        self.PhiX   = (np.take(self.PhiX, self.OnOffPairs[:, 0]) + \
                        np.take(self.PhiX, self.OnOffPairs[:, 1]))/2.
        self.PhiY   = (np.take(self.PhiY, self.OnOffPairs[:, 0]) + \
                        np.take(self.PhiY, self.OnOffPairs[:, 1]))/2.

        # Flag: could use the max of flag1 and flag2 (if one is flagged,
        # then the phase diff should also be flagged) - for now, use binary_or:

        slfFlags = self.FlagHandler.getFlags()
        slfFlags = np.take(slfFlags, self.OnOffPairs[:, 0]) | \
                   np.take(slfFlags, self.OnOffPairs[:, 1])
        self.FlagHandler = ReaFlagHandler.createFlagHandler(slfFlags)

    #----------------------------------------------------------------------------
    def selectPhase(self, phase):
        """Keep only parameters (times, positions) associated with
             Data(ON) or Data(OFF)

        Parameters
        ----------
        phase : int
            phase to keep, 1=ON, 2=OFF
        """

        ph = phase-1  # index in OnOffPairs: 0 = ON, 1 = OFF
        self.LST     = np.take(self.LST,     self.OnOffPairs[:, ph])
        self.MJD     = np.take(self.MJD,     self.OnOffPairs[:, ph])
        self.UT      = np.take(self.UT,      self.OnOffPairs[:, ph])
        self.Az      = np.take(self.Az,      self.OnOffPairs[:, ph])
        self.El      = np.take(self.El,      self.OnOffPairs[:, ph])
        self.MeanRa  = np.take(self.MeanRa,  self.OnOffPairs[:, ph])
        self.MeanDec = np.take(self.MeanDec, self.OnOffPairs[:, ph])
        self.LonOff  = np.take(self.LonOff,  self.OnOffPairs[:, ph])
        self.LatOff  = np.take(self.LatOff,  self.OnOffPairs[:, ph])
        self.BasLon  = np.take(self.BasLon,  self.OnOffPairs[:, ph])
        self.BasLat  = np.take(self.BasLat,  self.OnOffPairs[:, ph])
        self.LonPole = np.take(self.LonPole, self.OnOffPairs[:, ph])
        self.LatPole = np.take(self.LatPole, self.OnOffPairs[:, ph])
        self.Rot     = np.take(self.Rot,     self.OnOffPairs[:, ph])
        self.FocX    = np.take(self.FocX,    self.OnOffPairs[:, ph])
        self.FocY    = np.take(self.FocY,    self.OnOffPairs[:, ph])
        self.FocZ    = np.take(self.FocZ,    self.OnOffPairs[:, ph])
        self.PhiX    = np.take(self.PhiX,    self.OnOffPairs[:, ph])
        self.PhiY    = np.take(self.PhiY,    self.OnOffPairs[:, ph])
        # self.Flags   = np.take(self.Flags,   self.OnOffPairs[:,ph])

        slfFlags = self.FlagHandler.getFlags()
        slfFlags = np.take(slfFlags, self.OnOffPairs[:, ph])
        self.FlagHandler = ReaFlagHandler.createFlagHandler(slfFlags)


    def __computeSubIndex(self):
        """Compute start and end indices per subscan """

        self.__MessHand.debug('computeSubIndex start...')
        for i in range(len(self.SubscanTime)):
            # build array of indices where LST > LST_0
            after = np.nonzero(greater(self.LST, self.SubscanTime[i]))
            self.SubscanIndex[0, i] = after[0]

        self.SubscanIndex[1, 0:-1] = self.SubscanIndex[0, 1:]
        self.SubscanIndex[1, -1] = len(self.LST)
        self.__MessHand.debug('... computeSubIndex end')


    #----------------------------------------------------------------------------
    def get(self,dataType=' ', flag=[], getFlagged=0, subscans=[]):
        """get data of the ScanParam class

        Parameters
        ----------
        dataType : {'LST', 'MJD', 'UT', 'Az', 'El', 'AzOff', 'ElOff', '...'}
            type of data, case insensitive
        flag : list of int
            retrieve data flagged or unflagged accordingly
        getFlagged : bool
            flag revers to flagged/unflagged data

                                 +--------+------------+-----------------------------------------+
                                 | flag   | getFlagged | Retrieve..                              |
                                 +========+============+=========================================+
                                 | 'None' |  False     | all data                                |
                                 +--------+------------+-----------------------------------------+
                                 | []     |  False     | unflagged data (default)                |
                                 +--------+------------+-----------------------------------------+
                                 | []     |  True      | data with at least one flag set         |
                                 +--------+------------+-----------------------------------------+
                                 | 1      |  False     | data with flag 1 not set                |
                                 +--------+------------+-----------------------------------------+
                                 | 1      |  True      | data with flag 1 set                    |
                                 +--------+------------+-----------------------------------------+
                                 | [1,2]  |  False     | data with neither flag 1 nor flag 2 set |
                                 +--------+------------+-----------------------------------------+
                                 | [1,2]  |  True      | data with either flag 1 or flag 2 set   |
                                 +--------+------------+-----------------------------------------+
        subscans : list of int
            optionnally select subscan(s)

        Returns
        -------
        array of float
            the requested data, returned data are in the stored unit,
            except for offsets which are converted to arcsec

        Notes
        -----
        MJD are in seconds since the beginning of the scan
        offsets are in arcsec other angle in degree

        az/el and az/el offsets are corrected from Wobler Throw if applicable
        ra/dec and ra/dec offsets are not corrected from Wobler Throw # TODO
        """

        dataType = dataType.lower()

        # retrieve the data... (offsets are in arcsec)
        if dataType in ['lst']:
            dataArray = self.LST
        elif dataType in ['mjd']:
            dataArray = (self.MJD - self.MJD[0])*86400. # in seconds since the beginning of the scan
        elif dataType in ['azimuth', 'az']:
            dataArray = self.Az
            if self.AddLatWT != 0:
                dataArray = dataArray+self.AddLatWT*self.WobThrow
        elif dataType in ['elevation', 'el']:
            dataArray = self.El
            if self.AddLonWT != 0:
                dataArray = dataArray+self.AddLonWT*self.WobThrow
        elif dataType in ['azimuthelevation', 'azel']:
            dataArray = np.transpose(np.array([self.Az, self.El]))
            if self.AddLatWT != 0 or self.AddLonWT != 0 :
                dataArray = dataArray + np.array([self.AddLatWT, self.AddLonWT])*self.WobThrow
        elif dataType in ['cosnasmyth', 'cosnas']:
            dataArray = self.cosNAS
        elif dataType in ['sinnasmyth', 'sinnas']:
            dataArray = self.sinNAS
        elif dataType in ['azimuthoffset', 'azoff', 'azo']:
            dataArray = self.AzOff*3600.
            if self.AddLatWT != 0:
                dataArray = dataArray+self.AddLatWT*self.WobThrow
        elif dataType in ['elevationoffset', 'eloff', 'elo']:
            dataArray = self.ElOff*3600.
            if self.AddLonWT != 0:
                dataArray = dataArray+self.AddLonWT*self.WobThrow
        elif dataType in ['azimuthelevationoffset', 'azeloff', 'azelo', 'azo']:
            dataArray = np.transpose(np.array([self.AzOff, self.ElOff])*3600)
            if self.AddLatWT != 0 or self.AddLonWT != 0 :
                dataArray = dataArray + np.array([self.AddLatWT, self.AddLonWT])*self.WobThrow
        elif dataType in ['lonoff']:
            dataArray = self.LonOff*3600.
        elif dataType in ['latoff']:
            dataArray = self.LatOff*3600.
        elif dataType in ['ut']:
            dataArray = self.UT
        elif dataType in ['focus-x', 'focusx', 'focx']:
            dataArray = self.FocX
        elif dataType in ['focus-y', 'focusy', 'focy']:
            dataArray = self.FocY
        elif dataType in ['focus-z', 'focusz', 'focz']:
            dataArray = self.FocZ
        elif dataType in ['focus-xtitl']:
            dataArray = self.PhiX
        elif dataType in ['focus-ytilt']:
            dataArray = self.PhiY
        elif dataType in ['baslon']:
            dataArray = self.BasLon
        elif dataType in ['baslat']:
            dataArray = self.BasLat
        elif dataType in ['ra']:
            dataArray = self.RA
        elif dataType in ['dec']:
            dataArray = self.Dec
        elif dataType in ['meanra']:
            dataArray = self.MeanRa
        elif dataType in ['meandec']:
            dataArray = self.MeanDec
        elif dataType in ['raoff', 'raoffset']:
            dataArray = self.RAOff * 3600.
        elif dataType in ['decoff', 'decoffset']:
            dataArray = self.DecOff * 3600.
        elif dataType in ['glon']:
            dataArray = self.GLon
        elif dataType in ['glat']:
            dataArray = self.GLat
        elif dataType in ['het', 'hetemp']:
            dataArray = self.He3Temp
        elif dataType in ['azspeed']:
            azimuth   = self.Az
            dt        = self.get('deltat', flag='None')
            elev      = self.El
            dataArray = (azimuth[1::]-azimuth[:-1])*np.cos(np.radians(elev[1::]))/dt[:-1]
            dataArray = 3600.*np.concatenate((dataArray, [dataArray[-1]]))
        elif dataType in ['elspeed']:
            elevation = self.El
            dt        = self.get('deltat', flag='None')
            dataArray = (elevation[1::]-elevation[:-1])/dt[:-1]
            dataArray = 3600.*np.concatenate((dataArray, [dataArray[-1]]))
        elif dataType in ['azacc']:
            dt        = self.get('deltat', flag='None')
            azspeed   = self.get('azspeed', flag='None')
            dataArray = (azspeed[1::]-azspeed[:-1])/dt[:-1]
            dataArray = np.concatenate((dataArray, [dataArray[-1]]))
        elif dataType in ['elacc']:
            dt        = self.get('deltat', flag='None')
            elspeed   = self.get('elspeed', flag='None')
            dataArray = (elspeed[1::]-elspeed[:-1])/dt[:-1]
            dataArray = np.concatenate((dataArray, [dataArray[-1]]))
        elif dataType in ['speed']:
            azimuthSpeed   = self.get('azspeed', flag='None')
            elevationSpeed = self.get('elspeed', flag='None')
            dataArray = np.sqrt(azimuthSpeed**2+elevationSpeed**2)
        elif dataType in ['acc', 'accel']:
            azimuthAcc   = self.get('azacc', flag='None')
            elevationAcc = self.get('elacc', flag='None')
            dataArray = np.sqrt(azimuthAcc**2+elevationAcc**2)
        elif dataType in ['deltat']:
            MJD  = (self.MJD - self.MJD[0])*86400.
            dt   = MJD[1::]-MJD[:-1]
            bad  = np.nonzero(np.equal(dt, 0.))
            good = np.nonzero(np.not_equal(dt, 0))
            if bad:
                for nbad in bad:
                    dt[nbad] = np.min(np.take(dt, good))
            dt = np.concatenate((dt, [np.min(dt)]))
            dataArray = dt
        elif dataType in ['phase', 'wob', 'wobbler']:
            dataArray = self.WobblerSta

        # Check if subscans was asked
        if subscans:
            # Create a mask representing the asked subscans
            subscanMask = np.zeros(dataArray.shape[0])

            SubscanNum   = self.SubscanNum
            SubscanIndex = self.SubscanIndex

            for subscan in subscans:
                if subscan in SubscanNum:
                    isub = SubscanNum.index(subscan)
                    subscanMask[SubscanIndex[0, isub]:SubscanIndex[1, isub]] = 1
                else:
                    self.MessHand.error("subscan "+subscan+" does not exist")
                    return
        else:
            subscanMask = np.ones(dataArray.shape[0])

        # Extract that mask from the data
        dataArray = np.compress(subscanMask, dataArray, axis=0)

        # .. and only return the desired flag
        if flag in ['', 'None']:
            return dataArray
        else:
            if getFlagged:
                mask = self.FlagHandler.isSetMask(flag)
            else:
                mask = self.FlagHandler.isUnsetMask(flag)
            mask = np.compress(subscanMask, mask, axis=0)

            return np.compress(mask, dataArray, axis=0)

    #----------------------------------------------------------------------------

    def flag(self,dataType='', below='?', above='?', flag=1):
        """flag data based on dataType

        Parameters
        ----------
        dataType : {'LST', 'MJD', 'Az', 'El', 'AzOff', 'ElOff', 'focX', 'focY', 'focZ'}
            type of data to flag, case insensitive
        below : float
            flag dataType < below (default max)
        above : float
            flag dataType > above (default min)
        flag : int
            flag values (default 1)

        Notes
        -----
        below and above should be in unit of the flagged data,
        except for 'Lon' and 'Lat' where they should be in arcsec
        """

        self.__MessHand.debug("flag start...")

        # flag on dataType
        dataTest = self.get(dataType=dataType, flag='None')

        # default inputs
        if above == '?':
            above = np.min(dataTest)
        if below == '?':
            below = np.max(dataTest)

        mask = np.where(np.bitwise_and(dataTest >= above, dataTest <= below), 1, 0)

        if len(np.nonzero(mask)) > 0:
            n0 = self.FlagHandler.nSet(flag)
            self.FlagHandler.setOnMask(mask, flag)
            n1 = self.FlagHandler.nSet(flag)
            if (n1-n0):
                self.__MessHand.info("%5i timestamps flagged (%5.2f %%) with flag %s"
                                     % ((n1-n0), 100.*float(n1-n0)/self.NInt, str(flag)))
            else:
                self.__MessHand.warning("Nothing flagged")
        else:
            self.__MessHand.warning("Nothing flagged")

        self.__MessHand.debug("flag end")

    #----------------------------------------------------------------------------

    def unflag(self,dataType='', below='?', above='?', flag=[]):
        """unflag data based on dataType

        Parameters
        ----------
        dataType : {'LST', 'MJD', 'Az', 'El', 'AzOff', 'ElOff', 'focX', 'focY', 'focZ'}
            type of data to unflag, case insensitive
        below : float
            flag dataType < below (default max)
        above : float
            flag dataType > above (default min)
        flag : list of int
            flag values ([] : unset all flags)


        Notes
        -----
        below and above should be in unit of the flagged data,
        except for 'Lon' and 'Lat' where they should be in arcsec
        """

        self.__MessHand.debug("unflag start...")

        # flag on dataType
        dataTest = self.get(dataType=dataType, flag='None')

        # default inputs
        if above == '?':
            above = np.min(dataTest)
        if below == '?':
            below = np.max(dataTest)

        mask = np.where(np.bitwise_and(dataTest >= above, dataTest <= below), 1, 0)

        if len(np.nonzero(mask)) > 0:
            n0 = self.FlagHandler.nUnset(flag)
            self.FlagHandler.unsetOnMask(mask, flag)
            n1 = self.FlagHandler.nUnset(flag)
            if (n1-n0):
                self.__MessHand.info("%5i timestamps unflagged (%5.2f %%) with flag %s"
                                     % ((n1-n0), 100.*float(n1-n0)/self.NInt, str(flag)))
            else:
                self.__MessHand.warning("Nothing unflagged")
        else:
            self.__MessHand.warning("Nothing unflagged")

        self.__MessHand.debug("unflag end")

    #----------------------------------------------------------------------------
    def _computeSubscanEfficiency(self):
        """compute the scan efficiencies wrt subscans dead time

        Returns
        -------
        float
            return % of time spent IN subscans wrt total scan length
        """

        # The following variables should contain all the needed information
        # We do not use flagging info, we just compute the SubScan Efficiency

        MJD          = self.MJD             # Use MJD because LST could be flagged
        Nobs         = self.NObs
        SubscanIndex = self.SubscanIndex

        ScanDuration = MJD[-1]-MJD[0]
        SubscanDuration = 0
        for i in np.arange(Nobs):
            SubscanDuration += MJD[SubscanIndex[1, i]-1]-MJD[SubscanIndex[0, i]]

        return SubscanDuration/ScanDuration*100

    #----------------------------------------------------------------------------
    def plotAzimuth(self,flag=[],plotFlagged=0, \
                    limitsX=[],limitsY=[], \
                    style='l',ci=1,overplot=False,aspect=True):
        """plot time series of azimuth

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """

        dataX = self.get('MJD', flag=flag, getFlagged=plotFlagged)
        dataY = self.get('Azimuth', flag=flag, getFlagged=plotFlagged)

        xLabel = "MJD [sec]"
        yLabel = "Az [Deg]"

        Plot.plot(dataX, dataY,\
                  limitsX = limitsX, limitsY = limitsY, \
                  labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                  style=style, ci=ci, overplot=overplot, aspect=aspect)

    #----------------------------------------------------------------------------
    def plotElevation(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],
                      style='l',ci=1,overplot=False,aspect=True):
        """plot time series of elevation

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """
        dataX = self.get('MJD', flag=flag, getFlagged=plotFlagged)
        dataY = self.get('Elevation', flag=flag, getFlagged=plotFlagged)

        xLabel = "MJD [sec]"
        yLabel = "El [Deg]"

        Plot.plot(dataX, dataY,\
                  limitsX = limitsX, limitsY = limitsY, \
                  labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                  style=style, ci=ci, overplot=overplot, aspect=aspect)

    #----------------------------------------------------------------------------
    def plotAzEl(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],style='l',
                 ci=1,overplot=0,aspect=1):
        """plot azimuth vs. elevation

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """

        dataX = self.get('Azimuth', flag=flag, getFlagged=plotFlagged)
        dataY = self.get('Elevation', flag=flag, getFlagged=plotFlagged)

        xLabel = "Az [Deg]"
        yLabel = "El [Deg]"

        Plot.plot(dataX, dataY,\
                  limitsX = limitsX, limitsY = limitsY, \
                  labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                  style=style, ci=ci, overplot=overplot, aspect=aspect)

    #----------------------------------------------------------------------------
    def plotElevationOffset(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],
                            style='l',ci=1,overplot=False,aspect=True):
        """plot time series of elevation offset

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """

        dataX = self.get('MJD', flag=flag, getFlagged=plotFlagged)
        dataY = self.get('ElevationOffset', flag=flag, getFlagged=plotFlagged)

        xLabel = "MJD [sec]"
        yLabel = "\GD El ['']"

        Plot.plot(dataX, dataY,\
                  limitsX = limitsX, limitsY = limitsY, \
                  labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                  style=style, ci=ci, overplot=overplot, aspect=aspect)
    #----------------------------------------------------------------------------
    def plotAzimuthOffset(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],
                          style='l',ci=1,overplot=False,aspect=True):
        """plot time series of azimuth offset

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """

        dataX = self.get('MJD', flag=flag, getFlagged=plotFlagged)
        dataY = self.get('AzimuthOffset', flag=flag, getFlagged=plotFlagged)

        xLabel = "MJD [sec]"
        yLabel = "\gD Az ['']"

        Plot.plot(dataX, dataY,\
                  limitsX = limitsX, limitsY = limitsY, \
                  labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                  style=style, ci=ci, overplot=overplot, aspect=aspect)

    #----------------------------------------------------------------------------
    def plotAzElOffset(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],
                       style='l',ci=1,overplot=False,aspect=True,caption='',num=True):
        """plot elevation offset versus azimuth offset

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        num : bool
            do we overplot subscan numbers ?
        """

        NObs         = self.NObs
        SubscanNum   = self.SubscanNum
        SubscanIndex = self.SubscanIndex
        dataX        = self.get('AzimuthOffset', flag=flag, getFlagged=plotFlagged)
        dataY        = self.get('ElevationOffset', flag=flag, getFlagged=plotFlagged)


        if not overplot:
            xLabel = "\gD Az ['']"
            yLabel = "\gD El ['']"
            if not caption:
                caption = self.caption()
            Plot.plot(dataX, dataY,\
                      limitsX = limitsX, limitsY = limitsY, \
                      labelX = xLabel, labelY = yLabel, caption=caption, \
                      style=style, ci=ci, aspect=aspect, nodata=1)

        # for i in np.arange(NObs):
        for obs in SubscanNum:
            dataX = self.get('AzimuthOffset', flag=flag, getFlagged=plotFlagged, subscans=[obs])
            dataY = self.get('ElevationOffset', flag=flag, getFlagged=plotFlagged, subscans=[obs])
            if (dataX.shape[0] > 0):
                Plot.plot(dataX, dataY, style=style, ci=ci, overplot=1)
                if num:
                    Plot.xyout(dataX[0], dataY[0], str(obs))

    #----------------------------------------------------------------------------
    def plotAzElSpeed(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],
                      style='l',ci=1,overplot=False,aspect=True):
        """plot azimuth and elevation speed

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """

        MJD            = self.get('MJD', flag=flag, getFlagged=plotFlagged)
        azimuthSpeed   = self.get('azspeed', flag=flag, getFlagged=plotFlagged)
        elevationSpeed = self.get('elspeed', flag=flag, getFlagged=plotFlagged)

        xLabel = "MJD (sec)"
        yLabel = "|Speed| [''/s]"

        MultiPlot.plot(['Azimuth', 'Elevation', 'Combined'],\
                       [MJD[:-1], MJD[:-1], MJD[:-1]],\
                       [abs(azimuthSpeed[:-1]), abs(elevationSpeed[:-1]),\
                        np.sqrt(azimuthSpeed[:-1]**2+elevationSpeed[:-1]**2)],\
                       limitsX = limitsX, limitsY = limitsY, \
                       labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                       style=style, ci=ci, overplot=overplot)

    #----------------------------------------------------------------------------
    def plotAzElAcceleration(self,flag=[],plotFlagged=0,limitsX=[],limitsY=[],
                             style='l',ci=1,overplot=False,aspect=True):
        """plot azimuth and elevation acceleration

        Parameters
        ----------
        flag : list of int
            retrieve data flagged or unflagged accordingly
        plotFlagged : bool
            flag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        aspect : bool
            do we keep aspect ratio ?
        """

        MJD       = self.get('MJD', flag=flag, getFlagged=plotFlagged)
        azimuthAccel   = self.get('azacc', flag=flag, getFlagged=plotFlagged)
        elevationAccel = self.get('elacc', flag=flag, getFlagged=plotFlagged)

        xLabel = "MJD (sec)"
        yLabel = "|Acceleration| [''/s^2]"

        MultiPlot.plot(['Azimuth', 'Elevation', 'Combined'],\
                       [MJD[:-2], MJD[:-2], MJD[:-2]],\
                       [abs(azimuthAccel), abs(elevationAccel),
                        np.sqrt(azimuthAccel**2+elevationAccel**2)],\
                       limitsX = limitsX, limitsY = limitsY, \
                       labelX = xLabel, labelY = yLabel, caption=self.caption(), \
                       style=style, ci=ci, overplot=overplot)


    #----------------------------------------------------------------------------
    # Subscan related methods
    #----------------------------------------------------------------------------

    def findSubscanByOffset(self,off=60.,combine=10):
        """compute subscan indices by looking for sufficient spatial offset
        (in any direction, but in the az/el system)

        Parameters
        ----------
        off : float
            minimum spatial offset between subscans, in az/el system, in arcseconds
        combine : int
             number of found subscans to combine into one
                    (useful for somewhat irregular scan patterns)
        """

        # get az/el offsets
        azoff = self.get('AzimuthOffset', flag='None')  # in arcsec
        eloff = self.get('ElevationOffset', flag='None')

        SubIndex = [0]
        sizeAzoff = np.size(azoff)

        oldpos = [azoff[0], eloff[0]]

        for i in range(sizeAzoff):
            newpos = [azoff[i], eloff[i]]
            dist = np.sqrt((oldpos[0]-newpos[0])**2+(oldpos[1]-newpos[1])**2)
            if (dist > off):
                SubIndex.append(i)
                oldpos = copy.deepcopy(newpos)

        # combine subscans found in this way
        NewSubIndex = [0]
        cycle = 0
        for index in SubIndex:
            cycle += 1
            if (cycle == combine):
                NewSubIndex.append(index)
                cycle = 0

        NewSubIndex.append(np.size(azoff))

        # Reinitialise Subscan related attributes
        self.SubscanIndex = []
        self.SubscanNum   = []
        self.SubscanType  = []

        nb = len(NewSubIndex)-1
        for i in range(nb):
            self.SubscanIndex.append([NewSubIndex[i], NewSubIndex[i+1]])
            self.SubscanNum.append(i+1)
            self.SubscanType.append('ON')

        self.SubscanIndex = np.transpose(self.SubscanIndex)
        self.NObs = nb
        self.__MessHand.info(str("Found %i subscans"%(nb)))


    #----------------------------------------------------

    def findSubscanFB(self,azMax=1000.,eq=0):
        """compute subscan indices from steps in az, el

        Parameters
        ----------
        azMax : float
             azimuth offset where subscans are marked
        eq : bool
             for EQ scan patterns
        """

        # Retrieve all Az, El offsets (even if some are flagged) to
        # indices refering to the complete dataset
        if eq:
            azOff = self.get('raoff', flag='None')  # in arcsec
            elOff = self.get('decoff', flag='None')
        else:
            azOff = self.get('AzimuthOffset', flag='None')  # in arcsec
            elOff = self.get('ElevationOffset', flag='None')

        SubIndex = [0]

        if (abs(azOff[0]) <= azMax):
            SubPos = [0]
        else:
            if (azOff[0] > 0):
                SubPos = [1]
            else:
                SubPos = [-1]

        sizeAzoff = np.size(azOff)
        inside = 0
        if abs(azOff[0]) < azMax:
            inside = 1

        for i in range(sizeAzoff):
            if inside:
                if (abs(azOff[i]) > azMax):
                    inside = 0
                    SubIndex.append(i)
                    if (azOff[i] > 0):
                        SubPos.append(1)
                    else:
                        SubPos.append(-1)
            else:
                if (abs(azOff[i]) <= azMax):
                    inside = 1
                    SubIndex.append(i)
                    SubPos.append(0)

        SubIndex.append(sizeAzoff)

        self.SubscanIndex = np.array([SubIndex[:-1], SubIndex[1::]])
        self.SubscanNum   = []
        self.SubscanType  = []
        nb = self.SubscanIndex.shape[1]
        self.NObs = nb

        for i in range(nb):
            self.SubscanNum.append(i+1)
            self.SubscanType.append('ON')

        self.SubscanPos = SubPos

        self.__MessHand.info(str("Found %i subscans"%(nb)))



    #----------------------------------------------------------------------------
    def findSubscan(self,direction='El',combine=1):
        """compute subscan indices for circular scans by looking for sign change in az/el speed

        Parameters:
        -----------
        direction : {'El' or 'Az'}
             direction in which to look for stationary points
        combine : int
             number of found subscans to combine into one
                                (useful for irregular scan patterns)
        """

        # scan speed in az/el
        if (direction == 'Az' or direction == 'az'):
            azsp = self.get('AzSpeed', flag='None')
        else:
            azsp = self.get('ElSpeed', flag='None')

        # replace zeroes with a small epsilon
        eps = 0.00001
        azsp0 = (np.where(azsp == 0, eps, 0))
        azsp = azsp+azsp0

        # find where sign changes
        sgn = azsp[1::]*azsp[:-1]
        sgn = sgn/(abs(sgn))

        # mask=(np.nonzero(where(np.less(sgn,0),1,0)))
        mask = np.nonzero(np.where(sgn < 0, 1, 0))

        # make sure there are at least smin=20 timestamps in each subscan
        SubIndex = []
        smin = 20
        last = 0
        for i in range(len(mask)-1):
            if (mask[i]-last > smin):
                SubIndex.append(mask[i])
            last = mask[i]

        # combine subscans found in this way
        NewSubIndex = [0]
        cycle = 0
        for index in SubIndex:
            cycle += 1
            if (cycle == combine):
                NewSubIndex.append(index)
                cycle = 0

        NewSubIndex.append(np.size(azsp))

        # Reinitialise Subscan related attributes
        self.SubscanIndex = []
        self.SubscanNum   = []
        self.SubscanType  = []

        nb = len(NewSubIndex)-1
        for i in range(nb):
            self.SubscanIndex.append([NewSubIndex[i], NewSubIndex[i+1]])
            self.SubscanNum.append(i+1)
            self.SubscanType.append('ON')

        self.SubscanIndex = np.transpose(self.SubscanIndex)
        self.NObs = nb
        self.__MessHand.info(str("Found %i subscans"%(nb)))


    #----------------------------------------------------------------------------

    def findSubscanSpiral(self,threshold=1500.,combine=1):
        """compute subscan indices for spiral scans by looking for large acceleration

        Parameters
        ----------
        theshold : float
             mark new subscan where acceleration exceeds this value
        combine : int
             number of found subscans to combine into one
                    (useful for somewhat irregular scan patterns)        """

        # scan speed in az/el
        acc = self.get('acc', flag='None')

        mask = np.nonzero(np.where(acc > threshold, 1, 0))

        # make sure there are at least smin=400 timestamps in each subscan
        SubIndex = []
        smin = 400
        last = 0
        for i in range(len(mask)-1):
            if (mask[i]-last > smin):
                SubIndex.append(mask[i])
            last = mask[i]

        # combine subscans found in this way
        NewSubIndex = [0]
        cycle = 0
        for index in SubIndex:
            cycle += 1
            if (cycle == combine):
                NewSubIndex.append(index)
                cycle = 0

        NewSubIndex.append(np.size(acc))

        # Reinitialise Subscan related attributes
        self.SubscanIndex = []
        self.SubscanNum   = []
        self.SubscanType  = []

        nb = len(NewSubIndex)-1
        for i in range(nb):
            self.SubscanIndex.append([NewSubIndex[i], NewSubIndex[i+1]])
            self.SubscanNum.append(i+1)
            self.SubscanType.append('ON')

        self.SubscanIndex = np.transpose(self.SubscanIndex)
        self.NObs = nb
        self.__MessHand.info(str("Found %i subscans"%(nb)))


    #----------------------------------------------------------------------------

    def findSubscanByFlagArray(self, gflags):

        gflags = np.where(gflags > 0, 1, 0)

        flagVal = gflags[0]
        SubFlags = [flagVal]
        SubIndex = [0]
        for i in range(len(gflags)):
            if (gflags[i] != flagVal):
                flagVal = gflags[i]
                SubIndex.append(i)
                SubFlags.append(flagVal)
        SubIndex.append(np.size(gflags))

        # Reinitialise Subscan related attributes
        self.SubscanIndex = []
        self.SubscanNum   = []
        self.SubscanType  = []

        nb = len(SubIndex)-1
        for i in range(nb):
            self.SubscanIndex.append([SubIndex[i], SubIndex[i+1]])
            self.SubscanNum.append(i+1)
            if (SubFlags[i] > 0):
                self.SubscanType.append('OFF')
            else:
                self.SubscanType.append('ON')

        self.SubscanIndex = np.transpose(self.SubscanIndex)
        self.NObs = nb
        self.__MessHand.info(str("Found %i subscans"%(nb)))

    #----------------------------------------------------------------------------

    def findSubscanCircle(self,combine=1):
        """compute subscan indices for ''families of circles''

        Parameters
        ----------
        combine : int
             number of found subscans to combine into one
                    (useful for somewhat irregular scan patterns)
        """

        # compute scan speed
        azSpeed   = self.get('azspeed', flag='None', getFlagged=0)
        elSpeed   = self.get('elspeed', flag='None', getFlagged=0)
        speed     = np.sqrt(azSpeed**2+elSpeed**2)
        medSpeed  = fStat.f_median(speed)
        offSpeed  = abs(speed-medSpeed)
        kern = np.array(range(100))*0.0+1.0
        a = np.convolve(offSpeed, kern)
        medOff = fStat.f_median(np.array(a))
        threshold = medOff*10.

        lrg = np.where(a > threshold, 1, 0)
        mask = np.nonzero(lrg)

        # make sure there are at least smin=400 timestamps in each subscan
        SubIndex = []
        smin = 400
        last = 0
        for i in range(len(mask)-1):
            if (mask[i]-last > smin):
                SubIndex.append(mask[i])
            last = mask[i]

        # combine subscans found in this way
        NewSubIndex = [0]
        cycle = 0
        for index in SubIndex:
            cycle += 1
            if (cycle == combine):
                NewSubIndex.append(index)
                cycle = 0

        NewSubIndex.append(np.size(speed))

        # Reinitialise Subscan related attributes
        self.SubscanIndex = []
        self.SubscanNum   = []
        self.SubscanType  = []

        nb = len(NewSubIndex)-1
        for i in range(nb):
            self.SubscanIndex.append([NewSubIndex[i], NewSubIndex[i+1]])
            self.SubscanNum.append(i+1)
            self.SubscanType.append('ON')

        self.SubscanIndex = np.transpose(self.SubscanIndex)
        self.NObs = nb
        self.__MessHand.info(str("Found %i subscans"%(nb)))

        # SET FLAGS
        # put the flags on the ScanParam flag array
        # self.FlagHandler.setOnMask(mask,iFlags=flag)
        # put the flags on the main flag array
        # for chan in chanListIndices:
        #    self.FlagHandler.setOnMask(mask, self.rflags['INTEGRATION FLAGGED'], \
        #                               dim=1, index=chan)



    #----------------------------------------------------------------------------


    def findSubscanSteps(self,threshold=1.):
        """compute subscan indices from steps in az, el

        Parameters
        ----------
        threshold : float
             value (in arcsec^2) of (d_az^2 + d_el^2) step
             used to detect turnovers / stationnary points
        """

        # Retrieve all Az, El offsets (even if some are flagged) to
        # indices refering to the complete dataset
        azOff = self.get('AzimuthOffset', flag='None')  # in arcsec
        elOff = self.get('ElevationOffset', flag='None')

        # 1st derivative
        d_az = azOff[1::] - azOff[:-1]
        d_el = elOff[1::] - elOff[:-1]

        # compute squared radius
        radius = (d_az*d_az) + (d_el*d_el)
        # radius go  below 10. at turnovers and stationary positions
        # TODO: the latter could be used to estimate noise
        # compute difference with threshold to look at its sign
        radius_1 = radius - threshold
        diff_radius_1 = radius_1[1::] * radius_1[:-1]
        # this is negative when the sign of radius_1 has changed
        mask = np.nonzero(np.where(np.less(diff_radius_1, 0), 1, 0))

        # Reinitialise Subscan related attributes
        self.SubscanIndex = []
        self.SubscanNum   = []
        self.SubscanType  = []

        nb = len(mask)-1
        for i in range(nb):
            self.SubscanIndex.append([mask[i], mask[i+1]-1])  # -1: the gaps
                                    # between subscans are not in any subscan
            self.SubscanNum.append(i+1)
            self.SubscanType.append('ON')

        self.SubscanIndex = np.transpose(self.SubscanIndex)
        self.NObs = nb
        self.__MessHand.info(str("Found %i subscans"%(nb)))

    #----------------------------------------------------------------------------

    def plotSubscan(self):
        """generate a plot showing starting and ending times of subscans """

        index = self.SubscanIndex
        nbSub = len(self.SubscanNum)
        mjd = self.get('mjd', flag='None')
        mini = mjd[index[0, 0]]
        maxi = mjd[index[1, -1]-1]
        maxSub = np.max(self.SubscanNum)
        Plot.plot([mini, maxi], [0, 0], limitsY=[-1, maxSub], style='l',\
                  labelX='MJD - MJD[0] (s)', labelY='Subscan number')
        for num in range(nbSub):
            Plot.plot([mjd[index[0, num]], mjd[index[1, num]-1]],\
                      [self.SubscanNum[num], self.SubscanNum[num]],\
                      style='l', overplot=1)


    def plotSubscanOffsets(self,overplot=0):
        """Use four colours to show subscans on the Az, El pattern

        Parameters
        ----------
        overplot : bool
            if set, do not plot AzElOffset - assume these have been plotted already
        """

        if not overplot:
            self.plotAzElOffset()
        index = self.SubscanIndex
        nbSub = len(self.SubscanNum)
        azOff = 3600. * self.LonOff
        elOff = 3600. * self.LatOff

        for num in range(nbSub):
            Plot.plot(azOff[index[0, num]:index[1, num]-1],\
                      elOff[index[0, num]:index[1, num]-1],\
                      style='p', overplot=1, ci=num-4*int(num/4.)+2)


#----------------------------------------------------------------------------------
#----- Rea Data Entity Class ------------------------------------------------------
#----------------------------------------------------------------------------------
class TimelineData:
    """..class: TimelineData
    :synopsis: Objects of this class store the data and associated
         parameters of a scan, which can contain several observations
         (or subscans).
         They also contain additional arrays in which the current
         results of the data reduction are stored.
         This class also provides the interface between the MB-FITS
         files and Rea, by the means of the fillFromMBFits() method.
    """

    def __init__(self):
        """Instanciation of a new TimelineData object.
             All attributes are defined and set to default values.
        """

        # Add a MessHand attribute - new MessageHandler
        self.MessHand = ReaMessageHandler.MessHand(self.__module__)

        # Dictionary containing status informations
        self.Status_Dic = {'Gain_Ele_Cor_Done':0}
        self.Status_Dic['Baseline_Cor_Ord'] = 0
        self.Status_Dic['Noi_Cor_Done'] = 0
        self.Status_Dic['Opa_Cor_Done'] = 0
        self.Status_Dic['Flux_Cal_Done'] = 0
        self.Status_Dic['Pha_Dif_Done'] = 0
        # ...to be completed...

        # Initialisation of all other attributes
        # All are arrays of floats, except when stated
        self.Data        = np.array([], np.float32)
        self.DataBackup  = np.array([], np.float32)   # The backup copy of data
        self.DataWeights = np.array([], np.float32)
        self.Weight      = np.array([], np.float32) # TODO: move to ReceiverArray

        self.ReceiverArray = ReceiverArray() # Contains all the array parameters
        self.ScanParam      = ScanParameter()  # contains all coordinates and times

        # Statistics
        self.ChanRms  =  np.array([], np.float32)
        self.ChanMean =  np.array([], np.float32)
        self.ChanMed  =  np.array([], np.float32)
        self.ChanRms_s  =  np.array([], np.float32)  # Per subscans
        self.ChanMean_s =  np.array([], np.float32)
        self.ChanMed_s  =  np.array([], np.float32)

        # File name
        self.FileName = ''

        # Flags:
        dataFlags = np.array([], np.int8)
        dataFlags.shape = (0, 0)
        self.FlagHandler = ReaFlagHandler.createFlagHandler(dataFlags)

        self.dflags = {'SPIKE'              : 1,
                       'GLITCH TYPE 1'      : 2,
                       'GLITCH TYPE 2'      : 3,
                       'SQUID FLUX JUMP'    : 4,
                       'DEMOD RAILED'       : 5,
                       'TEMPORARY'          : 8 }
        # Reserved flag values:
        self.rflags = {'INTEGRATION FLAGGED': 6,
                       'CHANNEL FLAGGED'    : 7 }

    def reset(self):
        """Reset all attributes - useful before reading a new file """

        # Keep the same ReceiverArray and ScanParam object --
        # otherwise shortcut will be lost !
        ReceiverArray = self.ReceiverArray
        ScanParam = self.ScanParam

        ReceiverArray.__init__()
        ScanParam.__init__()

        # Also keep Message handler to keep trace of max. weight
        MessHand = self.MessHand

        self.__init__()
        self.ReceiverArray = ReceiverArray
        self.ScanParam      = ScanParam
        self.MessHand       = MessHand

        gc.collect()


    def __str__(self):
        """Defines a string which is shown when the print instruction is
             used. It contains the sizes and typecodes of all attributes.
        """

        if not self._existData():
            return "No data read in yet\n"

        out = self.ScanParam.__str__()+"\n"
        out += self.ReceiverArray.__str__()+"\n"

        if ReaConfig.DEBUG > 2:
            out += "\n" + \
                   attrStr(self, ['MessHand', 'ReceiverArray', 'Map', 'ScanParam']) + \
                   "\n"

        return out

    # ---------------------------------------------------------------------
    # Overload addition operator: used to combine two datasets
    # ---------------------------------------------------------------------
    def __add__(self, other):
        # TODO: check that it makes sense to co-add these two datasets
        # (e.g. same bolo array, same source if pointing...)
        result = copy.deepcopy(self)
        result._coadd(other)
        return result

    def _coadd(self, other):
        # Special case of addition, applied to 'self' rather than returning a result
        self.ScanParam._coadd(other.ScanParam)

        self.Data        = np.concatenate((self.Data,        other.Data))
        self.DataWeights = np.concatenate((self.DataWeights, other.DataWeights))
        self.DataBackup  = np.concatenate((self.DataBackup,  other.DataBackup))
        # self.CorrelatedNoise    = np.concatenate((self.CorrelatedNoise,    other.CorrelatedNoise))

        slfFlags  = np.concatenate((self.FlagHandler.getFlags(), other.FlagHandler.getFlags()))
        self.FlagHandler = ReaFlagHandler.createFlagHandler(slfFlags)


    # ---------------------------------------------------------------------
    # General Input/Output methods
    # ---------------------------------------------------------------------
    def read(self,inFile='',febe='',baseband=0,subscans=[],update=False,phase=0, \
             channelFlag=1, integrationFlag=9, \
             readHe=0,readAzEl0=0,readT=0,readWind=0,readBias=0,readPWV=0):
        """read a data entity object

        Parameters
        ----------
        inFile : str
             scan number / path to the dataset to be read
        subscans : list of int
             subscan numbers to read (default: all)
        update : bool
             if true, do not reset previous entity object
        phase : int
             phase to be stored (default: phase diff)
        channelFlag : list of int
             flag for not connected feeds (default: 1 'NOT CONNECTED')
        integrationFlag : list of int
             flag for blanked integrations (default: 9 'BLANK DATA')
        readHe : bool
             do we read LABOCA He3 tempe?
        readAzEl0 : bool
             do we read monitor Az, El(0)?
        readT : bool
             do we read T_amb from monitor? (def: no)
        readWind : bool
             do we read wind speed, dir...? (def: no)
        readBias : bool
             do we need ASZCa bias settings? (def: no)
        readPWV  : bool
             do we read pwv? (def: no)

        Returns :
        ---------
        int
           status : 0 if reading ok, <> 0 if an error occured
                   (see ReaDataAnalyser.read for error codes description)
        """
        t0 = time.clock()

        if isinstance(inFile, type(1)):
            inFile = str(inFile)

        status = 0
        if update:
            newData = TimelineData()
            status = newData.read(inFile, febe, baseband, subscans, update=0, phase=phase)
            self._coadd(newData)
            # free memory
            newData = 0
            gc.collect()

        else:
            ReaCommandHistory.tagHistory()

            if not inFile == '':
                ReaDir.setInFile(inFile)

            # Open dataset and create MBFitsReader:
            datasetWasOpen = 0
            try:
                dataset = ReaMBFits.importDataset(ReaConfig.inFile)
            except:
                self.MessHand.error(" could not open dataset %s"%(inFile))
                status = -1
                return status

            reader = ReaMBFitsReader.createReader(dataset)

            # Reset the currData if data already present
            if self._existData():
                self.reset()

            nSub = reader.openSubscan(subsnum=None)

            # Determine febe to be used:
            febesDataset = reader.read("Febes")
            if febe:
                if febe in febesDataset:
                    useFebe = febe
                else:
                    self.MessHand.error(" no data for Febe %s in dataset %s" \
                                        % (febe, inFile))
                    status = -2
                    return status
            else:
                if len(febesDataset) == 1:
                    # Only one febe in dataset: ok
                    useFebe = febesDataset[0]
                # elif isinstance(febesDataset, type('test')):
                # only one string - IRAM case
                #     useFebe = febesDataset
                elif len(febesDataset) == 0:
                    # No febe in dataset: not ok
                    self.MessHand.error(" no Febe data in dataset %s" \
                                        % (inFile))
                    status = -2
                    return status
                else:
                    # More than one febe in dataset: not ok
                    self.MessHand.error(" must specify Febe for dataset %s : found febes = %s" \
                                        % (inFile, str(febesDataset)))
                    status = -2
                    return status

            # Determine baseband to be used:
            basebandsDataset = reader.read("UseBand", febe=useFebe)
            if baseband:
                if baseband in basebandsDataset:
                    useBaseband = baseband
                else:
                    self.MessHand.error(" no data for baseband %s in dataset %s" \
                                        % (baseband, inFile))
                    status = -3
                    return status
            else:
                if len(basebandsDataset) == 1:
                    # Only one baseband in dataset: ok
                    useBaseband = basebandsDataset[0]
                elif len(basebandsDataset) == 0:
                    # No baseband in dataset: not ok
                    self.MessHand.error(" no baseband data in dataset %s" \
                                        % (inFile))
                    status = -3
                    return status
                else:
                    # More than one baseband in dataset: not ok
                    self.MessHand.error(" must specify baseband for dataset %s" \
                                        % (inFile))
                    status = -3
                    return status

            # Determine subscans to be used:
            subscansDataset = reader.read("Subscans")
            if not subscansDataset:
                self.MessHand.error(" no subscan data in dataset %s" \
                                    % (inFile))
                status = -4
                return status
            if not subscans:
                useSubscans = subscansDataset
            else:
                # Check whether all specified subscans are present:
                for subscan in subscans:
                    if not subscan in subscansDataset:
                        self.MessHand.error(" no data for subscan %d in dataset %s" \
                                            % (subscan, inFile))
                        status = -4
                        return status
                useSubscans = subscans

            # fillFromMBFits: here is most of the work done
            # ---------------
            # Use 1st subscan to define receiver array
            self.ReceiverArray._ReceiverArray__fillFromMBFits(reader=reader, \
                                                                febe=useFebe, \
                                                                baseband=useBaseband, \
                                                                subscan=useSubscans[0], \
                                                                flag=channelFlag)

            # Copy the Telescope object to ScanParam: we need the latitude there
            self.ScanParam.Telescope = self.ReceiverArray.Telescope

            # Fill ScanParam related attributes
            self.ScanParam._ScanParameter__fillFromMBFits(reader=reader,
                                                          febe=useFebe,
                                                          baseband=useBaseband,
                                                          subscans=useSubscans,
                                                          flag=integrationFlag, \
                                                          readHe=readHe, readAzEl0=readAzEl0,
                                                          readT=readT, readWind=readWind,
                                                          readBias=readBias, readPWV=readPWV)

            self._TimelineData__fillFromMBFits(reader=reader, \
                                             febe=useFebe, \
                                             baseband=useBaseband, \
                                             subscans=useSubscans)

            # Now report channels flagged at read
            usedChannels = self.ReceiverArray.UsedChannels
            arrayFlagHandler = self.ReceiverArray.FlagHandler
            timeFlagHandler  = self.ScanParam.FlagHandler
            dataFlagHandler  = self.FlagHandler

            if timeFlagHandler.nSet() > 0:
                timeMask = timeFlagHandler.isSetMask()
            else:
                timeMask = None
            for chan in usedChannels:
                index = self.ReceiverArray.getChanIndex(chan)[0]
                if arrayFlagHandler.isSetOnIndex(chan-1):
                    dataFlagHandler.setAll(self.rflags['CHANNEL FLAGGED'], \
                                           dim=1, index=index)
                if timeMask:
                    dataFlagHandler.setOnMask(timeMask, \
                                              self.rflags['INTEGRATION FLAGGED'], \
                                              dim=1, index=index)

            # now choose phase to be stored in Rea
            # Compute integration numbers for both phases
#             if self.ScanParam.WobUsed:
#                 self.ScanParam.computeOnOff()
#             if phase == 0:
# compute phase diff, if needed
#                 if self.ScanParam.OnOffPairs:
#                     self._phaseDiff()
#             else:
# return appropriate phase, if exists
#                 if not (self.ScanParam.OnOffPairs):
#                     self.MessHand.warning("Only one phase in these data -" +\
#                                           " returning complete dataset")
#                 else:
#                     self.selectPhase(phase)

            dataset.close()

            t1 = time.clock()
            self.MessHand.debug(str(len(subscans))+" subscan(s) read  "+str(t1-t0))
            t0 = t1

            # store file name in the TimelineData object
            self.FileName = inFile
            # Display some general infos about the file
            self.MessHand.info(self.__str__())

            # At read time make the current channel selection equal the total channel list
            self.ReceiverArray.setCurrChanList('all')

            self.MessHand.debug(" Dataset "+inFile+" has been read")

            gc.collect()
            return status

    # ---------------------------------------------------------------------
    def __fillFromMBFits(self, reader, febe, baseband, subscans):
        """fill a TimelineData object using the MBFitsReader object reader.

        Parameters
        ----------
        reader : MBFitsReader
            MBFitsReader object
        baseband : int
            baseband number to select
        subscans : list of int
            list of subscans numbers to read in
        """

        self.MessHand.debug('start of fillFromMBfits')
        t0 = time.clock()

        # Now get the data
        nInt = self.ScanParam.NInt
        nUseFeed = reader.read("NUseFeed", \
                               subsnum=subscans[0], \
                               febe=febe, \
                               baseband=baseband)
        subsIndex = 0
        Data = np.zeros((nInt, nUseFeed), np.float32)
        for subscan in subscans:
            if subscan in self.ScanParam.SubscanNum:
                # this means ScanParam.__fillFromMBFits worked fine
                subscanWasOpened = reader.openSubscan(subsnum=subscan)
                subscanStart = self.ScanParam.SubscanIndex[0, subsIndex]
                subscanStop  = self.ScanParam.SubscanIndex[1, subsIndex]
                subsIndex += 1

                tmpData = reader.read("Data",
                                      subsnum=subscan,
                                      febe=febe,
                                      baseband=baseband)

                if len(tmpData.shape) == 3 and tmpData.shape[2] == 1:
                    self.MessHand.error('This should not happens')
                    tmpData = tmpData[:,:, 0]
                if tmpData.shape[0] > subscanStop - subscanStart:
                    # Happens when more rows in ARRAYDATA than DATAPAR
                    tmpData = tmpData[:subscanStop - subscanStart,:]
                Data[subscanStart:subscanStop] = tmpData.astype(np.float32)

                if subscanWasOpened:
                    reader.closeSubscan(subsnum=subscan)

        # Add the DC offsets to the signals
        # for i in range(self.ReceiverArray.NUsedChannels):
            # Note: for LABOCA-ABBA the ordering of DCOff may be wrong
            # (see Dirk's e-mail 2006/09/09)
            # Data[:,i] = Data[:,i] + np.array(self.ReceiverArray.DCOff[i]).astype(np.float32)
            # Commented out 2006/9/17 - no meaningful unit in LABOCA data

        # Apply gain factor - Note: to convert to Volts, one would have to divide
        # by 32768. in the specific case of LABOCA-ABBA - We need to know the
        # ADC dynamic range, not in MB-FITS format definition
        Data = Data / np.array(self.ReceiverArray.BEGain).astype(np.float32)
        # Also correct for frontend gain
        Data = Data / (np.array(2.**self.ReceiverArray.FEGain).astype(np.float32))
        self.Data = Utilities.as_column_major_storage(Data)

        # Initialise Data Weights
        self.DataWeights = Utilities.as_column_major_storage(np.ones((nInt, nUseFeed), np.float32))

        # The other arrays can be initalised to appropriate sizes
        # Extract the numbers of channels (= pixels) and datapoints
        dataShape = self.Data.shape
        self.FlagHandler = ReaFlagHandler.createFlagHandler(np.zeros(dataShape, np.int8))

        t1 = time.clock()
        self.MessHand.debug(" Complementary information filled "+str(t1-t0))

        self.MessHand.debug('end of fillFromMBfits')

    # -------------------------------------------------------------------
    def dumpData(self,filename='ReaData.sav'):
        """save the current TimelineData object to a file

        Parameters
        ----------
        filename : str
            name of the output file
        """
        # filename = self.outDir+filename
        try:
            f = file(os.path.join(ReaConfig.outDir, filename), 'w')
        except IOError:
            self.MessHand.error(" permission denied, please change outdir")
            return
        cPickle.dump(self, f, 2)
        f.close()
        self.MessHand.longinfo(" current data successfully written to %s"%filename)
    # -------------------------------------------------------------------
    def restoreData(self,filename='ReaData.sav'):
        """restore a TimelineData object previously saved in a file, and
             set it as the currData attribute of ReaB

        Parameters
        ----------
        filename : name of the input file
        """
        # filename = self.outDir+filename
        try:
            f = file(os.path.join(ReaConfig.outDir, filename))
        except IOError:
            self.MessHand.error(" could not open file %s"%(filename))
            return
        self = cPickle.load(f)
        f.close()

    # -------------------------------------------------------------------
    def backup(self):
        """backup the data"""

        self.DataBackup = copy.copy(self.Data)

    # -------------------------------------------------------------------
    def restore(self):
        """restore the backuped the data """

        self.Data = copy.copy(self.DataBackup)

    # -------------------------------------------------------------------
    def saveMambo(self,inName='',outName=''):
        """convert an MB-Fits file to the MAMBO FITS format, readable
             by MOPSIC

        Parameters
        ----------
        inName : str
            name of the MB-Fits file (optional)
        outName : str
            name of the MAMBO output file (optional)
        """

        # if input name is not given, use that of the current file
        if inName == '':
            inName = self.FileName
        # if output name is not given, simply use the scan number
        if outName == '':
            # outName = self.outDir+str(self.scanNum)
            outName = str(self.ScanParam.ScanNum)
        # Now use the MamboMBFits.py module
        m = MamboMBFits.MamboMBFits(outName, inName)
        try:
            m.convertMB2MamboFits()
            self.MessHand.setMess(3, " MB-FITS file "+inName)
            self.MessHand.setMess(3, " successfully converted to "+outName)
        except:
            self.MessHand.setMess(1, " something got wrong in MB to MAMBO conversion")
            raise

    # -------------------------------------------------------------------
    def saveExchange(self, filename="", overwrite=False):
        """save information from the TimelineData object to a
             Fits file for exchange with other reduction packages

        Parameters
        ----------
        filename : str
            name of the Fits file (optional)
        overwrite : bool
             Overwrite existing file (optional)
        """

        # if file name is not given, simply use the scan number
        if filename == '':
            filename = "%s.fits" % str(self.ScanParam.ScanNum)
        filename = os.path.join(ReaConfig.outDir, filename)

        if overwrite:
            if os.path.exists(filename):
                os.remove(filename)

        # Keywords for the PrimaryHeader:
        keywords = []
        keywords.append(ReaMBFits.Keyword(name="CREATOR", \
                                          value="REA", \
                                          datatype="10A", \
                                          comment="ID of program that created this file"))
        keywords.append(ReaMBFits.Keyword(name="TIME", \
                                          value=time.strftime("%Y-%m-%d:%H:%M:%S"), \
                                          datatype="20A", \
                                          comment="Time of creation"))
        keywords.append(ReaMBFits.Keyword(name="MBFITS", \
                                          value=self.FileName, \
                                          datatype="30A", \
                                          comment="Name of original MBFits dataset"))
        keywords.append(ReaMBFits.Keyword(name="SCAN", \
                                          value=str(self.ScanParam.ScanNum), \
                                          datatype="10A", \
                                          comment="Scan number"))
        keywords.append(ReaMBFits.Keyword(name="OBJECT", \
                                          value=self.ScanParam.Object, \
                                          datatype="30A", \
                                          comment="Object observed"))
        keywords.append(ReaMBFits.Keyword(name="FEBE", \
                                          value=self.ReceiverArray.FeBe, \
                                          datatype="17A", \
                                          comment="Frontend-backend ID"))

        ds = ReaMBFits.createDataset(filename, filename, keywords, "")

        # DATA Table:
        keywords = []
        keywords.append(ReaMBFits.Keyword(name="EXTNAME", \
                                          value="DATA", \
                                          datatype="20A"))

        colinfos = []
        colinfos.append(ReaMBFits.ColumnInfo(name="MJD", \
                                             datatype="D", \
                                             description="Mjd"))
        colinfos.append(ReaMBFits.ColumnInfo(name="DATA", \
                                             datatype="E", \
                                             repeat=self.Data.shape[1], \
                                             description="Processed signal"))
        tData = ds.addTable(keywords=keywords, colinfos=colinfos)

        colMJD = tData.getColumn("MJD")
        colData = tData.getColumn("DATA")

        colMJD.write(1, self.ScanParam.MJD)
        colData.write(1, self.Data)

        # FLAGS Table:
        keywords = []
        keywords.append(ReaMBFits.Keyword(name="EXTNAME", \
                                          value="FLAGS", \
                                          datatype="20A"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG1", \
                                          value="SPIKE", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG2", \
                                          value="GLITCH TYPE 1", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG3", \
                                          value="GLITCH TYPE 2", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG4", \
                                          value="SQUID FLUX JUMP", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG5", \
                                          value="DEMOD RAILED", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG6", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG7", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="DFLAG8", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))

        keywords.append(ReaMBFits.Keyword(name="IFLAG1", \
                                          value="TURNAROUND", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG2", \
                                          value="ACCELERATION THRESHOLD", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG3", \
                                          value="ELEVATION VELOCITY THRESHOLD", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG4", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG5", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG6", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG7", \
                                          value="SUBSCAN FLAGGED", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="IFLAG8", \
                                          value="", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        for iflag in np.arange(9, 33):
            keywords.append(ReaMBFits.Keyword(name="IFLAG%d"%iflag, \
                                              value="", \
                                              datatype="20A", \
                                          comment="Description of flag"))


        colinfos = []
        colinfos.append(ReaMBFits.ColumnInfo(name="MJD", \
                                             datatype="D", \
                                             description="Mjd"))
        colinfos.append(ReaMBFits.ColumnInfo(name="DATAFLAG", \
                                             datatype="B", \
                                             repeat=self.FlagHandler.getFlags().shape[1], \
                                             description="Flag per channel and Mjd"))
        colinfos.append(ReaMBFits.ColumnInfo(name="INTEGFLAG", \
                                             datatype="J", \
                                             description="Flag per Mjd"))
        tFlags = ds.addTable(keywords=keywords, colinfos=colinfos)

        colMJD = tFlags.getColumn("MJD")
        colDataflag = tFlags.getColumn("DATAFLAG")
        colIntegflag = tFlags.getColumn("INTEGFLAG")

        colMJD.write(1, self.ScanParam.MJD)

        # Clear the Rea specific flags from DataFlags:
        dFlags = copy.copy(self.FlagHandler.getFlags())
        flagHandler = ReaFlagHandler.createFlagHandler(dFlags)

        flagHandler.unsetAll([self.rflags['INTEGRATION FLAGGED'], \
                              self.rflags['CHANNEL FLAGGED'], \
                              self.dflags['TEMPORARY'] ])
        colDataflag.write(1, flagHandler.getFlags())
        colIntegflag.write(1, self.ScanParam.FlagHandler.getFlags())


        # CHANNELFLAGS Table:
        keywords = []
        keywords.append(ReaMBFits.Keyword(name="EXTNAME", \
                                          value="CHANNELFLAGS", \
                                          datatype="20A"))

        keywords.append(ReaMBFits.Keyword(name="CFLAG1", \
                                          value="NOT CONNECTED", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="CFLAG2", \
                                          value="BAD SENSITIVITY", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="CFLAG3", \
                                          value="LOW SENSITIVITY", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        keywords.append(ReaMBFits.Keyword(name="CFLAG4", \
                                          value="DARK RECEIVER", \
                                          datatype="20A", \
                                          comment="Description of flag"))
        for iflag in np.arange(5, 33):
            keywords.append(ReaMBFits.Keyword(name="CFLAG%d"%iflag, \
                                              value="", \
                                              datatype="20A", \
                                          comment="Description of flag"))


        colinfos = []
        colinfos.append(ReaMBFits.ColumnInfo(name="CHANNEL", \
                                             datatype="J", \
                                             description="Channel number"))
        colinfos.append(ReaMBFits.ColumnInfo(name="FLAG", \
                                             datatype="J", \
                                             description="Flag per channel"))
        tCflags = ds.addTable(keywords=keywords, colinfos=colinfos)

        colChannel = tCflags.getColumn("CHANNEL")
        colFlag = tCflags.getColumn("FLAG")

        colChannel.write(1, np.arange(self.ReceiverArray.NChannels)+1)

        colFlag.write(1, self.ReceiverArray.FlagHandler.getFlags())


        # SUBSCANS Table:
        keywords = []
        keywords.append(ReaMBFits.Keyword(name="EXTNAME", \
                                          value="SUBSCANS", \
                                          datatype="20A"))

        colinfos = []
        colinfos.append(ReaMBFits.ColumnInfo(name="SUBSNUM", \
                                             datatype="J", \
                                             description="Subscan number"))
        colinfos.append(ReaMBFits.ColumnInfo(name="ISTART", \
                                             datatype="J", \
                                             description="Start index of subscan"))
        colinfos.append(ReaMBFits.ColumnInfo(name="IEND", \
                                             datatype="J", \
                                             description="Stop index of subscan"))
        colinfos.append(ReaMBFits.ColumnInfo(name="TYPE", \
                                             datatype="A", \
                                             repeat=10, \
                                             description="Subscan type"))
        colinfos.append(ReaMBFits.ColumnInfo(name="TIME", \
                                             datatype="E", \
                                             description="Subscan duration"))


        tSubs = ds.addTable(keywords=keywords, colinfos=colinfos)

        colNum = tSubs.getColumn("SUBSNUM")
        colStart = tSubs.getColumn("ISTART")
        colEnd = tSubs.getColumn("IEND")
        colType = tSubs.getColumn("TYPE")
        colTime = tSubs.getColumn("TIME")

        colNum.write(1, self.ScanParam.SubscanNum)
        colStart.write(1, self.ScanParam.SubscanIndex[0])
        colEnd.write(1, self.ScanParam.SubscanIndex[1]-1)
        colType.write(1, self.ScanParam.SubscanType)
        colTime.write(1, self.ScanParam.SubscanTime)


        # HISTORY Table:
        keywords = []
        keywords.append(ReaMBFits.Keyword(name="EXTNAME", \
                                          value="HISTORY", \
                                          datatype="20A"))

        colinfos = []
        colinfos.append(ReaMBFits.ColumnInfo(name="PROGID", \
                                             datatype="A", \
                                             repeat=10, \
                                             description="ID of program"))
        colinfos.append(ReaMBFits.ColumnInfo(name="COMMAND", \
                                             datatype="A", \
                                             repeat=100, \
                                             description="Command"))
        tHist = ds.addTable(keywords=keywords, colinfos=colinfos)

        commands = ReaCommandHistory.getHistory(-1)
        progIDs = ["REA"]*len(commands)
        if commands:
            colProgID = tHist.getColumn("PROGID")
            colCommand = tHist.getColumn("COMMAND")

            colProgID.write(1, progIDs)
            colCommand.write(1, commands)



        ds.close()

    # -------------------------------------------------------------------
    def loadExchange(self, filename=""):
        """read information from a Fits file for exchange with other
             reduction packages into the TimelineData object

        Parameters
        ----------
        filename: str
            name of the Fits file
        """
        filename = os.path.join(ReaConfig.outDir, filename)

        try:
            ds = ReaMBFits.importDataset(filename)
        except:
            self.MessHand.setMess(1, " could not load file %s" % filename)
            raise

        # Check information in Primary Header:
        mbfitsFile = ds.getKeyword("MBFITS").getValue()
        if mbfitsFile != self.FileName:
            self.MessHand.setMess(1, " MBFitsFile in file %s does not match" % filename)
            raise

        febe = ds.getKeyword("FEBE").getValue()
        if febe != self.ReceiverArray.FeBe:
            self.MessHand.setMess(1, " FeBe in file %s does not match" % filename)
            raise

        # DATA Table:
        tData = ds.getTables(EXTNAME="DATA")[0]
        tData.open()

        colMJD = tData.getColumn("MJD")
        colData = tData.getColumn("DATA")

        self.ScanParam.MJD = colMJD.read().astype(np.float64)
        self.Data = colData.read().astype(np.float32)

        tData.close()

        # FLAGS Table:
        tFlags = ds.getTables(EXTNAME="FLAGS")[0]
        tFlags.open()

        colDataflag = tFlags.getColumn("DATAFLAG")
        colIntegflag = tFlags.getColumn("INTEGFLAG")

        dataFlags = colDataflag.read().astype(np.int8)
        timeFlags = colIntegflag.read().astype(np.int32)

        tFlags.close()

        # CHANNELFLAGS Table:
        tCflags = ds.getTables(EXTNAME="CHANNELFLAGS")[0]
        tCflags.open()

        colFlag = tCflags.getColumn("FLAG")

        arrayFlags = colFlag.read().astype(np.int32)

        tCflags.close()

        # Adjust the flags:
        usedChannels = self.ReceiverArray.UsedChannels
        dataFlagHandler = ReaFlagHandler.createFlagHandler(dataFlags)
        timeFlagHandler = ReaFlagHandler.createFlagHandler(timeFlags)
        arrayFlagHandler = ReaFlagHandler.createFlagHandler(arrayFlags)

        if timeFlagHandler.nSet() > 0:
            timeMask = timeFlagHandler.isSetMask()
        else:
            timeMask = None
        for chan in usedChannels:
            index = self.ReceiverArray.getChanIndex(chan)[0]
            if arrayFlagHandler.isSetOnIndex(chan-1):
                dataFlagHandler.setAll(self.rflags['CHANNEL FLAGGED'], dim=1, index=index)
            if timeMask:
                dataFlagHandler.setOnMask(timeMask, \
                                          self.rflags['INTEGRATION FLAGGED'], \
                                          dim=1, index=index)

        self.FlagHandler = dataFlagHandler
        self.ScanParam.FlagHandler = timeFlagHandler
        self.ReceiverArray.FlagHandler = arrayFlagHandler


        # SUBSCANS Table:
        tSubs = ds.getTables(EXTNAME="SUBSCANS")[0]
        tSubs.open()

        colNum = tSubs.getColumn("SUBSNUM")
        colStart = tSubs.getColumn("ISTART")
        colEnd = tSubs.getColumn("IEND")
        colType = tSubs.getColumn("TYPE")
        colTime = tSubs.getColumn("TIME")

        self.ScanParam.SubscanNum = colNum.read().tolist()
        self.ScanParam.NObs = len(self.ScanParam.SubscanNum)
        iStarts = colStart.read().astype(Int)
        iEnds = colEnd.read().astype(Int) + 1
        self.ScanParam.SubscanIndex = np.array([iStarts, iEnds], Int)
        self.ScanParam.SubscanType = colType.read()
        self.ScanParam.SubscanTime = colTime.read().tolist()

        tSubs.close()


        ds.close()


    # ---------------------------------------------------------------------
    # Methods for computing phase differences
    # ---------------------------------------------------------------------

    def _phaseDiff(self):
        """phaseDiff (method) Compute phase differences: call ScanParam.phaseDiffParam for
             coordinates and times, and compute Data(ON) - Data(OFF)
        """

        # phase diff on positions and times
        t0 = time.clock()
        self.MessHand.debug("Entering ScanParam.phaseDiff")
        self.ScanParam._phaseDiffParam()
        t1 = time.clock()
        self.MessHand.debug("end of ScanParam.phaseDiff() "+str(t1-t0))

        # phase diff on data: ON - OFF
        self.Data = np.take(self.Data, self.ScanParam.OnOffPairs[:, 0]) - \
                    np.take(self.Data, self.ScanParam.OnOffPairs[:, 1])
        # Do not initialize backup on phasediff
        # self.DataBackup = copy.deepcopy(self.Data)
        # CorrelatedNoise also not initialised
        # self.CorrelatedNoise = take(self.CorrelatedNoise,self.ScanParam.OnOffPairs[:,0]) - \
        #                        take(self.CorrelatedNoise,self.ScanParam.OnOffPairs[:,1])
        # Flags: use binary_or of ON and OFF flags
        slfFlags = self.FlagHandler.getFlags()
        slfFlags = np.take(slfFlags, self.ScanParam.OnOffPairs[:, 0]) | \
                   np.take(slfFlags, self.ScanParam.OnOffPairs[:, 1])
        self.FlagHandler = ReaFlagHandler.createFlagHandler(slfFlags)

        # Weights: use average of ON and OFF
        self.DataWeights = (np.take(self.DataWeights, self.ScanParam.OnOffPairs[:, 0]) + \
                                np.take(self.DataWeights, self.ScanParam.OnOffPairs[:, 1]))/2.

        self.ScanParam._ScanParameter__computeSubIndex()

    def selectPhase(self, phase):
        """selectPhase (method) Keep only Data(ON) or Data(OFF)

        Parameters
        ----------
        phase : int
            phase to keep, 1=ON, 2=OFF
        """

        # BROKEN : because of Subscan Index calculation

        # Select times and positions
        self.ScanParam.selectPhase(phase)

        # select data
        ph = phase-1  # index in OnOffPairs: 0 = ON, 1 = OFF
        self.Data       = np.take(self.Data, self.ScanParam.OnOffPairs[:, ph])
        # Do not initialize backup on phase
        # self.DataBackup = copy.deepcopy(self.Data)
        self.CorrelatedNoise    = np.take(self.CorrelatedNoise, self.ScanParam.OnOffPairs[:, ph])
        self.DataWeights = np.take(self.DataWeights, self.ScanParam.OnOffPairs[:, ph])

        slfFlags = self.FlagHandler.getFlags()
        slfFlags = np.take(slfFlags, self.ScanParam.OnOffPairs[:, ph])
        self.FlagHandler = ReaFlagHandler.createFlagHandler(slfFlags)

        self.ScanParam._ScanParameter__computeSubIndex()

    #----------------------------------------------------------------------------
    def _existData(self):
        """check if the TimelineData object has been filled with data

        Returns
        -------
        int
            0 if no data, 1 otherwise
        """
        if (len(self.Data) > 0):
            return 1
        else:
            return 0

    #----------------------------------------------------------------------------
    #----- Data extraction ------------------------------------------------------
    #----------------------------------------------------------------------------
    def getChanData(self,dataType=' ',chan='None', flag=[], getFlagged=0,
                    flag2=None, subscans=[]):
        """get data for one channel

        Parameters
        ----------
        dataType : str
            type of data in
                 'flux', 'signal', 'weight'
                 'lst','mjd', 'ut'
                 'focus-x','focusx','focx','focus-y', 'focusy', 'focy'
                 'azimuthelevationoffset', 'azeloff','azelo', 'aeo'
                 'azimuthelevation','azel'
                 'speed', 'azspeed','elspeed'
                 'acc','accel', 'azacc','elacc'
                 'ra','dec'
                 'raoff','raoffset', 'decoff','decoffset'
                 'het','hetemp'
                 'phase','wob','wobbler'
                 'flags', 'flag'
                 'skynoise', 'sn', 'correlatednoise', 'cn'
                 'mean', 'median', 'med', 'rms'
                 'mean_s', 'rms_s', 'subscan'
        chan : list of int
            channel number
        flag : list of int
            retrieve data flagged or unflagged accordingly
        getFlagged : bool
            getFlagged : flag revers to flagged/unflagged data

                    +--------+------------+-----------------------------------------+
                    | flag   | getFlagged | Retrieve..                              |
                    +========+============+=========================================+
                    | 'None' |  False     | all data                                |
                    +--------+------------+-----------------------------------------+
                    | []     |  False     | unflagged data (default)                |
                    +--------+------------+-----------------------------------------+
                    | []     |  True      | data with at least one flag set         |
                    +--------+------------+-----------------------------------------+
                    | 1      |  False     | data with flag 1 not set                |
                    +--------+------------+-----------------------------------------+
                    | 1      |  True      | data with flag 1 set                    |
                    +--------+------------+-----------------------------------------+
                    | [1,2]  |  False     | data with neither flag 1 nor flag 2 set |
                    +--------+------------+-----------------------------------------+
                    | [1,2]  |  True      | data with either flag 1 or flag 2 set   |
                    +--------+------------+-----------------------------------------+
        subscans : list of int
            list of wanted subscan (default all)
        flag2 : list of int, optional
            second array of flags to check

        Returns
        -------
        float array
            data of one channel

        Notes
        -----
        Horizontal coordinates will be corrected from NASMYTH and Dewar angle  if applicable
        Equatorial coordinates are not corrected for channel offsets # TODO !
        offsets are in arcsec other angle in degree
        speed and acceleration only applies to the reference pixel
        """

        self.MessHand.debug("getChanData start...")
        # if the channel is not given take the reference channel as default
        if chan in ['None', 'none', '']:
            chan = self.ReceiverArray.RefChannel

        # retrieve the corresponding channel index
        chanIndex = self.ReceiverArray.getChanIndex(chan)[0]

        if chanIndex == -1:
            self.MessHand.error("channel not used")
            return

        dataType = dataType.lower()

        # retrieve data
        if dataType in ['flux', 'signal']:
            dataArray = self.Data[:, chanIndex]

        elif dataType in ['weight']:
            dataArray = self.DataWeights[:, chanIndex]

        elif dataType in ['lst', 'mjd', 'ut']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['focus-x', 'focusx', 'focx',\
                          'focus-y', 'focusy', 'focy',\
                          'focus-z', 'focusz', 'focz',\
                          'focus-xtilt', 'focus-ytilt']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['azimuthelevationoffset', 'azeloff', 'azelo', 'aeo', 'azimuthoffset', 'azoff', 'azo', 'elevationoffset', 'eloff']:
            dataArray   = self.ScanParam.get(dataType='AzimuthElevationOffset', flag='None')
            chanOffsets = np.array(self.ReceiverArray.getChanSep([chan]))[:, 0]
            if "NASMYTH" in self.ReceiverArray.DewCabin:
                cosNAS = self.ScanParam.get('cosNAS', flag='None')
                sinNAS = self.ScanParam.get('sinNAS', flag='None')
                chanOffsets = np.transpose(np.vstack( ( chanOffsets[0] * cosNAS + chanOffsets[1] * -sinNAS,
                                                        chanOffsets[0] * sinNAS + chanOffsets[1] *  cosNAS ) ) )
            dataArray = dataArray + chanOffsets

        elif dataType in ['azimuthelevation', 'azel', 'azimuth', 'az', 'elevation', 'el']:
            dataArray = self.ScanParam.get(dataType='AzimuthElevation', flag='None')
            chanOffsets = np.array(self.ReceiverArray.getChanSep([chan]))[:, 0]
            if "NASMYTH" in self.ReceiverArray.DewCabin:
                cosNAS = self.ScanParam.get('cosNAS', flag='None')
                sinNAS = self.ScanParam.get('sinNAS', flag='None')
                chanOffsets = np.transpose(np.vstack( ( chanOffsets[0] * cosNAS + chanOffsets[1] * -sinNAS,
                                                        chanOffsets[0] * sinNAS + chanOffsets[1] *  cosNAS ) ) )

            # add the channel offset in deg.
            dataArray = dataArray + chanOffsets / 3600.

        elif dataType in ['azspeed', 'elspeed']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['acc', 'accel']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['azacc', 'elacc']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['speed']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['ra', 'dec']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['raoff', 'raoffset']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['decoff', 'decoffset']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['het', 'hetemp']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['phase', 'wob', 'wobbler']:
            dataArray = self.ScanParam.get(dataType=dataType, flag='None')

        elif dataType in ['flags', 'flag']:
            dataArray = self.FlagHandler.getFlags()[:, chanIndex]

        elif dataType in ['skynoise', 'sn', 'correlatednoise', 'cn']:
            dataArray = self.CorrelatedNoise[:, chanIndex]

        # The following types are computed per scan (and not per integration)

        elif dataType in ['mean']:
            dataArray = self.ChanMean[chanIndex]
            return dataArray

        elif dataType in ['median', 'med']:
            dataArray = self.ChanMed[chanIndex]
            return dataArray

        elif dataType in ['rms']:
            dataArray = self.ChanRms[chanIndex]
            return dataArray

        # The following types are computed per subscan (and not per integration)
        # and make sense only on phase diff'ed data
        # WARNING: for these cases, no flag filtering is done, because we only
        # have flags per integration - NO SUBSCAN FLAGGING YET
        # Therefore, return the array before going to second step, which would crash

        elif dataType in ['mean_s']:
            dataArray = self.ChanMean_s[chanIndex]
            return dataArray

        elif dataType in ['rms_s']:
            dataArray = self.ChanRms_s[chanIndex]
            return dataArray

        elif dataType in ['subscan']:
            dataArray = self.ScanParam.SubscanNum
            return dataArray

        else:
            self.MessHand.error("Unknown data")
            return

        dataFlags = self.FlagHandler.getFlags()[:, chanIndex].astype(np.int32)

        # Check if subscans was asked
        if subscans:
            # Create a mask representing the asked subscans
            mask = np.zeros(dataArray.shape[0])

            SubscanNum   = self.ScanParam.SubscanNum
            SubscanIndex = self.ScanParam.SubscanIndex

            for subscan in subscans:
                if subscan in SubscanNum:
                    isub = SubscanNum.index(subscan)
                    mask[SubscanIndex[0, isub]:SubscanIndex[1, isub]] = 1
                else:
                    self.MessHand.error("subscan "+subscan+" does not exist")
                    return

            # Extract that mask from the data
            dataArray = np.compress(mask, dataArray, axis=0)
            dataFlags = np.compress(mask, dataFlags, axis=0)


        # .. and only return the desired flag
        dataFlagHandler = ReaFlagHandler.createFlagHandler(dataFlags)
        if flag in ['Blank', 'blank']:
            mask = dataFlagHandler.isSetMask()
            dataArray = np.where(mask, float('Nan'), dataArray)
        elif flag not in ['', 'None'] :
            if getFlagged:
                mask = dataFlagHandler.isSetMask(flag)
                if flag2 != None and flag2.any():
                    flagHandler2 = ReaFlagHandler.createFlagHandler(flag2.astype(np.int32))
                    mask2 = flagHandler2.isSetMask(flag)
                    bitwise_or(mask, mask2, mask)
            else:
                mask = dataFlagHandler.isUnsetMask(flag)
                if flag2 != None and flag2.any():
                    flagHandler2 = ReaFlagHandler.createFlagHandler(flag2.astype(np.int32))
                    mask2 = flagHandler2.isUnsetMask(flag)
                    mask = np.bitwise_and(mask, mask2)
            dataArray = np.compress(mask, dataArray, axis=0)

        # For backward compatibilities, let allow az or el request
        if dataType in ['azimuthoffset', 'azoff', 'azo', 'azimuth', 'az']:
            dataArray = dataArray[:, 0]
        elif dataType in ['elevationoffset', 'eloff', 'elo', 'evation', 'el']:
            dataArray = dataArray[:, 1]

        return dataArray

        self.MessHand.debug("... end getChanData")

    #----------------------------------------------------------------------------
    def getChanListData(self,type=' ',chanList=[],\
                        channelFlag=[], getFlaggedChannels=0, \
                        dataFlag=[], getFlaggedData=0, dataFlag2=None, \
                        subscans=[]):
        """get data for list of channels

        Parameters
        ----------
        type : str
            type of data
        chan : list of int
            channel list
        channelFlag : list of int
            retrieve data from channels flagged or unflagged accordingly
        getFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            retrieve data flagged or unflagged accordingly
        getFlaggedData : bool
            dataFlag revers to flagged/unflagged data

                    +--------+------------+-----------------------------------------+
                    | flag   | getFlagged | Retrieve..                              |
                    +========+============+=========================================+
                    | 'None' |  False     | all data                                |
                    +--------+------------+-----------------------------------------+
                    | []     |  False     | unflagged data (default)                |
                    +--------+------------+-----------------------------------------+
                    | []     |  True      | data with at least one flag set         |
                    +--------+------------+-----------------------------------------+
                    | 1      |  False     | data with flag 1 not set                |
                    +--------+------------+-----------------------------------------+
                    | 1      |  True      | data with flag 1 set                    |
                    +--------+------------+-----------------------------------------+
                    | [1,2]  |  False     | data with neither flag 1 nor flag 2 set |
                    +--------+------------+-----------------------------------------+
                    | [1,2]  |  True      | data with either flag 1 or flag 2 set   |
                    +--------+------------+-----------------------------------------+
        dataFlag2 : list of int, optionnal
            second array of flags to check (optional)

        Returns
        -------
        float array
            data of the input list of channels
        """

        t0 = time.clock()

        if getFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=getFlaggedChannels)
        result = []

        for i in chanList:
            # Get data chan by chan
            result.append(self.getChanData(type, i,\
                                           flag=dataFlag, getFlagged=getFlaggedData, flag2=dataFlag2,\
                                           subscans=subscans))

        t1 = time.clock()
        self.MessHand.debug(" cutting data for a list of channels: " +\
                                   str(t1-t0))
        return result

    #--------------------------------------------------------------------------------

    def _removeReservedFlagValues(self, flag, removeFlags=[]):
        """Removes the reserved flag values defined in self.rflag from list of flag values

        Parameters
        ----------
        flag : list of int
            flag values (integers, strings, and [] allowed)
        removeFlags : list of int
            flag value to be removed.

        Returns
        -------
        list of i
            flag values with reserved values removed.
            If the resulting is empty, None is returned to avoid confilcts
            with the notation that [] means all allowed flag values
        """
        if not isinstance(flag, type("")):
            if flag == []:
                flag = self.FlagHandler.getValidFlagValues()
            if isinstance(flag, type(1)):
                flag = [flag]

            if removeFlags == []:
                removeFlags = self.rflags.values()
            if isinstance(removeFlags, type(1)):
                removeFlags = [removeFlags]

            for rflag in removeFlags:
                while rflag in flag:
                    flag.remove(rflag)

            if flag == []:
                flag = None
        return flag



    #----------------------------------------------------------------------------
    #----- Methods to plot various kinds of data  -------------------------------
    #----------------------------------------------------------------------------
    def signal(self,chanList=[],
               channelFlag=[], plotFlaggedChannels=0, \
               dataFlag=[], plotFlaggedData=0, \
               limitsX=[],limitsY=[], \
               style='l', ci=1, overplot=False, plotMap=False, skynoise=False,
               caption='', subscan=False, noerase=False):
        """plot time series of flux density

        Parameters
        ----------
        chanList : list of int
            list of channels to be plotted
        channelFlag : list of int
            plot data from channels flagged or unflagged accordingly
        plotFlaggedChannels : bool
            channelFlag revers to flagged/unflagged data
        dataFlag : list of int
            plot data flagged or unflagged accordingly
        plotFlaggedData : bool
            dataFlag revers to flagged/unflagged data

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        plotMap : bool
            plot 2D images instead of timelines
        skynoise : bool
            plot correlated noise (default 0)
        caption : str
            plot title, default = scan info
        subscan : bool
            plot vertical lines between subscans
        noerase : bool
            do not clear the window
        """

        if plotMap == 1:
            flag = 'Blank'

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

        dataX = self.getChanListData('MJD', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
        xLabel = "MJD - MJD(0) [sec]"

        if skynoise:
            dataY = self.getChanListData('skynoise', chanList, \
                                         channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                         dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
            yLabel = "flux density [arb.u.]"
        else:
            dataY = self.getChanListData('flux', chanList, \
                                         channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                         dataFlag=dataFlag, getFlaggedData=plotFlaggedData)
            yLabel = "Flux density [Jy]"

        self.MessHand.info("plotting signal")

        if not caption:
            caption = self.ScanParam.caption()
        if not plotMap:
            MultiPlot.plot(chanList, dataX, dataY,\
                           limitsX = limitsX, limitsY = limitsY,\
                           labelX = xLabel, labelY = yLabel, caption=caption,\
                           style=style, ci=ci, overplot=overplot,
                           noerase=noerase)
        else:
            dataX, nNan = compressNan(dataX)
            if nNan != 0:
                nan = 1
            else:
                nan = 0
            if not caption:
                cap = self.ScanParam.caption()
            Plot.draw(np.transpose(dataY), \
                      sizeX=[np.min(dataX), np.max(dataX)], sizeY=[1, len(chanList)],\
                      limitsX=limitsX,\
                      labelX=xLabel, labelY='Channel #', caption=cap, \
                      wedge=1, nan=nan, noerase=noerase)

        if subscan == 1:# and not plotMap:
            oldStyle = style
            if limitsY == []:
                lower = np.min(np.ravel(dataY))
                upper = np.max(np.ravel(dataY))
                lower = lower-(upper-lower)*0.2
                upper = upper+(upper-lower)*0.2
            else:
                upper = limitsY[1]
                lower = limitsY[0]
            mjd = self.getChanData(dataType='MJD', chan=1, flag='None', getFlagged=0,\
                                 flag2=None, subscans=[])
            # mjd= (self.MJD - self.MJD[0])*86400.
            for i in range(self.ScanParam.SubscanNum[-2]):
                dataY = []
                dataX = []
                t = mjd[self.ScanParam.SubscanIndex[1, i]]
                for c in chanList:
                    dataY.append([lower, upper])
                    dataX.append([t, t])
                MultiPlot.plot(chanList, dataX, dataY,\
                           limitsX = limitsX, limitsY = limitsY,\
                           labelX = xLabel, labelY = yLabel, caption=caption,\
                           style='l', ci=ci+1, overplot=1,\
                           noerase=noerase)
            style = oldStyle
    #----------------------------------------------------------------------------
    def plotCorrel(self, chanRef=-1, chanList=[],
                   channelFlag=[], plotFlaggedChannels=0, \
                   dataFlag=[], plotFlaggedData=0, \
                   skynoise=False,\
                   limitsX=[], limitsY=[], \
                   style='p', ci=1, overplot=0):
        """plot flux density of a list of channels vs. flux density of a
             reference channel

        Parameters
        ----------
        chanRef : int
            reference channel number (default : is the first in chanList)
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

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        skynoise : bool
            plot against the skynoise of chanRef (default :  no)
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        overplot : bool
            do we overplot ?
        """

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)

        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        if chanRef == -1:
            chanRef = chanList[0]

        # dataY: remove datapoints where chanRef is flagged
        # retrieve the corresponding channel index
        chanIndex = self.ReceiverArray.getChanIndex(chanRef)[0]
        if chanIndex ==  -1:
            self.MessHand.error("chanRef: channel not used")
            return

        # retrieve flags
        refFlags = self.FlagHandler.getFlags()[:, chanIndex].astype(np.int32)
        dataY = self.getChanListData('flux', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData, \
                                     dataFlag2 = refFlags.astype('i'))

        # dataX: for each chan, remove flagged datapoints
        dataX = []
        for c in chanList:
            chanIndex = self.ReceiverArray.getChanIndex(c)[0]
            chanFlags = self.FlagHandler.getFlags()[:, chanIndex].astype(np.int32)
            if skynoise:
                dataX.append(self.getChanData('skynoise', chanRef, \
                                              flag=dataFlag, \
                                              getFlagged=plotFlaggedData, \
                                              flag2 = chanFlags.astype('i')))
            else:
                dataX.append(self.getChanData('flux', chanRef, \
                                              flag=dataFlag, \
                                              getFlagged=plotFlaggedData, \
                                              flag2 = chanFlags.astype('i')))


        if skynoise:
            xLabel = "CorrelatedNoise -- channel " + str(chanRef) + " [arb.u.]"
        else:
            xLabel = "flux density -- channel " + str(chanRef) + " [arb.u.]"

        yLabel = "flux density [arb.u.]"

        self.MessHand.info("plotting correlation")
        MultiPlot.plot(chanList, dataX, dataY,\
                       limitsX = limitsX, limitsY = limitsY, \
                       labelX = xLabel, labelY = yLabel, caption=self.ScanParam.caption(), \
                       style=style, ci=ci, overplot=overplot)

    #----------------------------------------------------------------------------
    def signalHist(self,chanList=[], \
                   channelFlag=[], plotFlaggedChannels=0, \
                   dataFlag=[], plotFlaggedData=0, \
                   limitsX=[],limitsY=[], \
                   ci=1, overplot=0, caption='', \
                   nbin=60, fitGauss=False, subtractGauss=False, logY=False):
        """plot histogram of flux density time series

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

                +--------+-------------+-----------------------------------------+
                | flag   | plotFlagged | Retrieve..                              |
                +========+=============+=========================================+
                | 'None' |  False      | all data                                |
                +--------+-------------+-----------------------------------------+
                | []     |  False      | unflagged data (default)                |
                +--------+-------------+-----------------------------------------+
                | []     |  True       | data with at least one flag set         |
                +--------+-------------+-----------------------------------------+
                | 1      |  False      | data with flag 1 not set                |
                +--------+-------------+-----------------------------------------+
                | 1      |  True       | data with flag 1 set                    |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  False      | data with neither flag 1 nor flag 2 set |
                +--------+-------------+-----------------------------------------+
                | [1,2]  |  True       | data with either flag 1 or flag 2 set   |
                +--------+-------------+-----------------------------------------+
        limitsX, limitsY : list of 2 int
            limits in X and Y
        style : str
            line style 'l':line, 'p': point
        ci : int
            color
        nbin : int
            number of bins in histogram
        fitGauss : bool
            fit a gaussian to the data?
        subtractGauss : bool
           subtract gaussian from the data?
        logY : bool
           plot Y in log axis
        caption : str
            plot title, default = scan info
        """

        epsilon = 0.0001
        ret = []

        if subtractGauss:
            fitGauss = 1

        if plotFlaggedChannels:
            dataFlag = self._removeReservedFlagValues(dataFlag, self.rflags['CHANNEL FLAGGED'])
            if dataFlag == None:
                self.MessHand.error("no valid flags")
                return

        chanList = self.ReceiverArray.checkChanList(chanList, \
                                                     flag=channelFlag, getFlagged=plotFlaggedChannels)
        chanListIndexes = self.ReceiverArray.getChanIndex(chanList)

        if len(chanList) < 1:
            self.MessHand.error("no valid channel")
            return

        flux = self.getChanListData('flux', chanList, \
                                     channelFlag=channelFlag, getFlaggedChannels=plotFlaggedChannels, \
                                     dataFlag=dataFlag, getFlaggedData=plotFlaggedData)

        nChan = len(chanList)

        extrflux = []
        for iChan in range(nChan):
            extrflux.append(np.min(flux[iChan]))
            extrflux.append(np.max(flux[iChan]))

        minflux = np.min(extrflux)*0.8
        maxflux = np.max(extrflux)*0.8
        step = (maxflux-minflux)/nbin

        x = np.zeros(nbin, 'f')
        f = minflux
        for ix in range(len(x)):
            x[ix] = f+step/2.
            f += step

        dataX = []
        dataY = []
        maxval = []
        for iChan in range(nChan):
            hist = np.array(fStat.histogram(flux[iChan], minflux, step, nbin))
            dataY.append(hist+epsilon)
            maxval.append(np.max(hist))
            dataX.append(x)

        xLabel = "flux density [arb.u.]"
        yLabel = "distribution of flux"

        if (not subtractGauss):

            self.MessHand.info("plotting histogram of signal")

            if logY:
                limitsY = [0.2, np.max(maxval)]

            MultiPlot.plot(chanList, dataX, dataY,\
                           limitsX = limitsX, limitsY = limitsY,\
                           labelX = xLabel, labelY = yLabel, \
                           caption=self.ScanParam.caption(),\
                           style='b', ci=ci, overplot=overplot, logY=logY)

            ret = dataY

        if (fitGauss):


            # define a range of x values for a smooth plot of the fit
            npts = 200
            x = np.zeros(npts, 'f')
            f = minflux
            step = (maxflux-minflux)/(npts-1)
            for ix in range(len(x)):
                x[ix] = f
                f += step

            dataFit = []
            plotX = []
            plotY = []
            for iChan in range(nChan):
                valid_data_mask = np.where(dataY[iChan] > 2.*epsilon, 1, 0)
                xfit = np.compress(valid_data_mask, dataX[iChan])
                yfit = np.compress(valid_data_mask, dataY[iChan])
                err = np.sqrt(yfit)
                result = fitGaussian(xfit, yfit, err)

                dataFit.append(modelgauss(result.params, dataX[iChan]))
                plotX.append(x)
                plotY.append(modelgauss(result.params, x)+epsilon)

            if subtractGauss:

                dataRes = []
                extrRes = []
                for iChan in arange(nChan):
                    res = (dataY[iChan]-dataFit[iChan])/np.max(dataY[iChan])
                    dataRes.append(res)
                    extrRes.append(np.min(res))
                    extrRes.append(np.max(res))

                self.MessHand.info("plotting residuals after subtracting gaussian(s)")

                yLabel = 'residual in units of peak'

                MultiPlot.plot(chanList, dataX, dataRes,\
                               limitsX = limitsX, \
                               limitsY = [np.min(extrRes)*1.1, np.max(extrRes)*1.1],\
                               labelX = xLabel, labelY = yLabel, \
                               caption=self.ScanParam.caption(),\
                               style='b', ci=ci, overplot=0)

                ret = dataRes

            else:

                self.MessHand.info("plotting fitted gaussian(s)")

                MultiPlot.plot(chanList, plotX, plotY,\
                               limitsX = limitsX, limitsY = limitsY,\
                               labelX = xLabel, labelY = yLabel,\
                               caption=self.ScanParam.caption(),\
                               style='l', ci=2, overplot=1)

                ret = plotY

        return ret
