#!/usr/bin/env python2.2
# Copyright (C) 2014
# Institut d'Astrophysique Spatiale
#
# Forked from the BoA project
#
"""
NAM: MamboMBFits.py (file)
DES: this module defines the MamboMBFits class, which contains both
a Mambo fits file  and an MB-Fits file, and  provides methods to do
conversions between these two formats.
VER: 24.05.2004
HIS: 17.02.2004  F. Schuller      Initial version
     17.02.2004 Initial version, from merging  of the mambo2MBFits
                and MB2MamboFits modules

  17-18.02.2004 Complete  restructuration  of the code  to a  more
                object-oriented style. Definition of a MamboMBFits
                class that contains two attributes of the FitsFile
                class, and  provides methods to  do conversions in
                both directions. The code  to do these conversions
                has been split to many sub-functions.
     27.02.2004 More stuff related to coordinates is now converted
                from Mambo to MB-FITS
     01.03.2004 Same  stuff (Astronomical  basis  frame) converted
                from MB-FITS to Mambo
     09.03.2004 More stuff converted.  Changes (also in Mambo.xml)
                to allow  the use of 'Ok'  rather than 'None'  for
                keywords that are "manually" processed
     10.03.2004 Implemented the convertFebepar method
     11.03.2004 More keywords converted: FREQUENC, TELSIZM...
     18.03.2004 Add conversion of  Fast Scanning observations from
                MAMBO to MB-FITS
     19.03.2004 The same for converting from MB-FITS to MAMBO
     06.05.2004 Adapted for use within BoA
     12.05.2004 Some small corrections for BoA
     24.05.2004 Some corrections to work with real APEX files
        09.2004 a few more corrections after observing at APEX
     FS050202   minor modif. for compatibility with APEX control PC

"""

__date__ =     '02.02.2005'

# try:
from mbfits import *
# except ImportError:
#  from BoaMBfits import *

from numpy.oldnumeric import *
import string
import math
from time import time
from XmlStructure import *
from slalib.slalib import *      # all slalib functions are called sla_...

try:
    import Entities
except ImportError:
    import BoaEntities as Entities

class MamboMBFits:
    """
    DES: Objects of this class contain two attributes of the FitsFile
    class. The 'Mambo' attribute stores the data as they appear in a
    MAMBO FITS file, and the 'MBfits' attribute contains the data in
    the MB-FITS format. Methods to do conversions in both directions
    are provided by this class.
    """


#*************************************************************************

    #-----------------------------------------------------------------------
    # __init__() - Instanciation of a new MamboMBFits object
    #-----------------------------------------------------------------------
    def __init__(self, mamboName, mbName):
        """
        DES: Instanciation of a new MamboMBFits object.
        INP: (str) mamboName = name of the Mambo file
             (str) mbName = name of the MB-FITS file
             in both cases, the .fits extension is appended if not present
        """

        if mamboName[-5:] != '.fits':
            mamboName = mamboName+'.fits'
        if mbName[-5:] != '.fits':
            mbName = mbName+'.fits'
        self.Mambo  = FitsFile(mamboName, "MAMBO")
        self.MBfits = FitsFile(mbName, "MBFITS")

    #-----------------------------------------------------------------------
    # convertMambo2MBFits()
    # Here is the method used to convert a MAMBO file to an MB-Fits file
    #-----------------------------------------------------------------------
    def convertMambo2MBFits(self):
        """
        DES: This function reads in the content of a Mambo FITS file,
        and writes out the data and associated parameters to a file
        conforming to the MB-FITS format.
        """

        # First step: read the content of the Mambo FITS file
        self.readMambo()
        # Create the output MB-FITS file, and generate the first tables
        self.initMB()

        # Process the content of the Primary Header - this must be done before
        # the ARRAYDATA table is created, because some info (e.g. USEFEED) present
        # in the MAMBO Primary Header are required to format the ARRAYDATA Table
        self.convertMamboPrimary()

        # Fill the FEBEPAR-MBFITS table with the Receiver Channel Parameters
        # of the Mambo-37 or Mambo-117 frontend
        self.fillFebepar()

        # Now generate the ARRAYDATA, DATAPAR and MONITOR tables
        self.processMamboData()

        # Everything is done, the MB-FITS file can be closed
        self.MBfits.close()


    #-----------------------------------------------------------------------
    # convertMB2MamboFits()
    # Here is the method used to convert an MB-FITS file to a Mambo file
    #-----------------------------------------------------------------------
    def convertMB2MamboFits(self):
        """
        DES: This function reads in the content of an MB-FITS file,
        and writes out the data to a file in the Mambo-FITS format,
        and the associated parameters to a RCP file.
        """

        # read the content of the MB-FITS file
        self.readMBfits()
        # generate the output MAMBO file
        self.initMambo()
        # fill the primary header with values found in MB-FITS keywords
        self.fillMamboPrimary()
        # Generate a RCP file from the content of the FEBEPAR table
        self.convertFebepar()
        # Finally fill the subscans and data tables
        self.fillMamboData()
        # close the output MAMBO file
        if (self.FastScan):
            self.Data.Header.updateKeyword('EXTNAME', '', 'data')
        self.Mambo.close()


#*************************************************************************

    #-----------------------------------------------------------------------
    # The following methods perform small steps of the conversion
    #-----------------------------------------------------------------------

    def readMambo(self):
        """
        DES: This fills the TableList in the Mambo attribute with the
        content of the MAMBO FITS file.
        """

        self.Mambo.open()
        self.Mambo.read()
        self.Mambo.close()
        # Store the content of the Primary header in the PrimaryMambo attribute
        self.PrimaryMambo = self.Mambo.TableList[0].Header


    def readMBfits(self):
        """
        DES: This fills the TableList in the MBfits attribute with the
        content of the MB-FITS file.
        """

        self.MBfits.open()
        self.MBfits.read()
        self.MBfits.close()
        # Store some keywords that will be useful in various places
        scanType = self.MBfits.TableList[1].Header.KeywordDict['SCANTYPE'][0]
        self.Scantype = {'SCANTYPE': scanType}
        self.NameFEBE = self.MBfits.TableList[2].Header.KeywordDict['FEBE'][0]
        self.Scannum = self.MBfits.TableList[1].Header.KeywordDict['SCANNUM'][0]
        try:
            self.FastScan = self.MBfits.TableList[1].Header.KeywordDict['FASTSCAN'][0]
        except:
            # self.FastScan = 0
            self.FastScan = 1

    def initMambo(self):
        """
        DES: Create a file in the Mambo FITS format. This generates only the
        Primary header and subscan table, because the number of feeds must be
        written in the Primary header before the data table is created.
        """

        name = self.Mambo.currentFileName
        # Instanciate a new FitsFile, so that the XmlStruc global variable used
        # in mbfits.py contains the XML description of MAMBO files, not MB-FITS
        self.Mambo = FitsFile("!"+name, "MAMBO")
        self.Mambo.create()     # Primary Header -> HDU = 1
        # An object of the Table class is required so that the parent
        # of the 'subscans' and 'data' tables is the 'Primary' table
        self.PrimaryMambo = Table('Primary', Parent=self.Mambo)
        self.PrimaryMambo.HduNum = 1

        # Generate the 'subscan' table ('data' table will be created later)
        self.Subscans = Table('subscans', self.PrimaryMambo)
        self.Subscans.create()


    def initMB(self):
        """
        DES: This generates the first three tables in the MB-FITS file
        (Primary header, SCAN-MBFITS and FEBEPAR-MBFITS tables).
        """

        nameMB = self.MBfits.currentFileName
        self.MBfits.currentFileName = "!"+nameMB
        self.MBfits.create()        #  Primary Header -> HDU = 1
        # A Table object is required to be able to use mbfits' methods
        self.PrimaryMB = Table('Primary', self.MBfits)
        self.PrimaryMB.HduNum = 1
        self.Scan = Table('SCAN-MBFITS', self.MBfits)
        self.Scan.create()          # SCAN-MBFITS Table -> HDU = 2
        self.Febe = Table('FEBEPAR-MBFITS', self.Scan)
        self.Febe.create()          # FEBEPAR-MBFITS Table -> HDU = 3

    def convertMamboPrimary(self):
        """
        DES: This generates in the MB-FITS file all the header keywords that
        have one direct equivalent in the MAMBO primary header.
        """

        keys = self.PrimaryMambo.Keywords
        # Extract the XML description of the MAMBO Primary Header
        xmlMambo = XmlStructure('MAMBO')
        tab = xmlMambo.XmlScan.tables['Primary']
        tblHeader = tab.getElementsByTagName('HEADER')[0]

        for key in keys:
            if (config.DEBUG):
                print "Dealing with Primary keyword ...", key
            tmp = self.PrimaryMambo.KeywordDict[key]
            val = tmp[0]		# Value found in the MAMBO file

            # Look for this keyword in the XML list of elements
            for x in tblHeader.childNodes:
                if x.nodeType == x.ELEMENT_NODE:
                    txt = x.childNodes[0].data	# Here is the text element
                    if (txt == key):
                        equiv = x.getAttribute('mbfitsEq')
                        if ((equiv != 'None') & (equiv != 'Ok')):
                            equivKey = str(equiv[0:string.find(equiv, "(")])
                            equivTab = equiv[string.find(equiv, "(")+1:string.find(equiv, ")")]
                            if (equivTab == "Primary"):
                                self.PrimaryMB.Header.updateKeyword(equivKey, '', val)
                            elif (equivTab == "SCAN-MBFITS"):
                                self.Scan.Header.updateKeyword(equivKey, '', val)
                            elif (equivTab == "FEBEPAR-MBFITS"):
                                self.Febe.Header.updateKeyword(equivKey, '', val)

        #--------------------------------------------------------------------------
        # Lots of things have to be done "manually"
        #--------------------------------------------------------------------------
        # combine Frontend and Backend names in FEBE
        front = self.PrimaryMambo.KeywordDict['FRONTEND']
        back = self.PrimaryMambo.KeywordDict['BACKEND']
        self.NameFEBE = front[0]+(8-len(front[0]))*" "+'-'+back[0]
        self.Febe.Header.updateKeyword('FEBE', '', self.NameFEBE)
        self.Scan.BinTable.addTableRow([self.NameFEBE])
        # USEAC and USEDC are combined in NUSEFEED
        useAC = self.PrimaryMambo.KeywordDict['NRECAC'][0]
        useDC = self.PrimaryMambo.KeywordDict['NRECDC'][0]
        nbFeed = useAC+useDC
        self.Febe.Header.updateKeyword('NUSEFEED', '', nbFeed)
        self.Febe.Header.updateKeyword('FEBEFEED', '', nbFeed)
        # FEBEBAND and NUSEBAND keywords: both are equal to 1 for receivers
        self.Febe.Header.updateKeyword('FEBEBAND', '', 1)
        self.Febe.Header.updateKeyword('NUSEBAND', '', 1)
        # Now the column sizes have to be adjusted
        self.Febe.BinTable.updateDimension('FEEDOFFX')
        self.Febe.BinTable.updateDimension('FEEDOFFY')
        self.Febe.BinTable.updateDimension('POLTY')
        self.Febe.BinTable.updateDimension('POLA')
        self.Febe.BinTable.updateDimension('APEREFF')
        self.Febe.BinTable.updateDimension('BEAMEFF')
        self.Febe.BinTable.updateDimension('ETAFSS')
        self.Febe.BinTable.updateDimension('HPBW')
        self.Febe.BinTable.updateDimension('ANTGAIN')
        self.Febe.BinTable.updateDimension('TCAL')
        self.Febe.BinTable.updateDimension('BOLDCOFF')
        self.Febe.BinTable.updateDimension('FLATFIEL')
        self.Febe.BinTable.updateDimension('GAINIMAG')
        # 2D arrays (feeds x band) since v 1.55
        self.Febe.BinTable.setVariableLengthDimension('USEFEED', nbFeed, 1)
        self.Febe.BinTable.setVariableLengthDimension('BESECTS', nbFeed, 1)
        self.Febe.BinTable.setVariableLengthDimension('FEEDTYPE', nbFeed, 1)

        # Some keywords are duplicated in several tables
        telescop = self.PrimaryMambo.KeywordDict['TELESCOP'][0]
        self.Scan.Header.updateKeyword('TELESCOP', '', telescop)

        #--------------------------------------------------------------------------
        # Date of observation
        dateObs = self.PrimaryMambo.KeywordDict['DATE-OBS'][0]
        self.Febe.Header.updateKeyword('DATE-OBS', '', dateObs)
        # Also convert this date to MJD
        self.DateObs = dateObs
        # MJD at this date at 0h
        self.DateMJD0, status = sla_cldj(string.atoi(dateObs[0:4]), \
                                 string.atoi(dateObs[5:7]), \
                                 string.atoi(dateObs[8:10]))
        # Add the time of day, converted to day
        day = sla_ctf2d(string.atoi(dateObs[11:13]), \
                        string.atoi(dateObs[14:16]), \
                        string.atof(dateObs[17:]))[0]
        self.DateMJD = self.DateMJD0+day

        # The time system ("TAI") must be written in the Scan header
        self.Scan.Header.updateKeyword('TIMESYS', '', 'TAI')

        #--------------------------------------------------------------------------
        # Wobbler mode and parameters
        #--------------------------------------------------------------------------
        wobmode = self.PrimaryMambo.KeywordDict['WOBMODE'][0]
        # check if the wobbler is used:
        throw = self.PrimaryMambo.KeywordDict['WOBTHROW'][0]
        if (throw):
            self.Scan.Header.updateKeyword('WOBUSED', '', 1)
            if (wobmode):
                self.Scan.Header.updateKeyword('WOBMODE', '', 'TRIANGULAR')
            else:
                self.Scan.Header.updateKeyword('WOBMODE', '', 'SQUARE')
            self.Febe.Header.updateKeyword('NPHASES', '', 2)
        else:
            self.Scan.Header.updateKeyword('WOBUSED', '', 0)
            self.Febe.Header.updateKeyword('NPHASES', '', 1)
        #--------------------------------------------------------------------------
        # Fast-scanning observations require a different processing
        fastscan = self.PrimaryMambo.KeywordDict['FASTSCAN'][0]
        if (fastscan == 'YES'):
            self.FastScan = 1
            self.Febe.Header.updateKeyword('NPHASES', '', 1)
        else:
            self.FastScan = 0
        # need an additional keyword in MB-Fits
        self.Scan.Header.addKeyword('FASTSCAN', '', self.FastScan, 'Fast scanning mode')

        #--------------------------------------------------------------------------
        # Convert the infos about the observing mode
        #--------------------------------------------------------------------------
        self.getScanType()   # This fills the self.Scantype attribute (dictionary)
        print 'Found Scan Type: ', self.Scantype['SCANTYPE']
        for key in ('SCANTYPE', 'SCANMODE', 'SCANGEOM'):
            self.Scan.Header.updateKeyword(key, '', self.Scantype[key])
        self.Febe.Header.updateKeyword('SWTCHMOD', '', self.Scantype['SWTCHMOD'])
        #--------------------------------------------------------------------------
        # fill in the info related to the Astronomical basis frame
        #--------------------------------------------------------------------------
        basisFrame = self.sbas2ctype()   # Dictionary
        for key in basisFrame.keys():
            self.Scan.Header.updateKeyword(key, '', basisFrame[key])
        #--------------------------------------------------------------------------
        # Additional stuff about coordinates
        #--------------------------------------------------------------------------
        # In the MAMBO frame, the "User native frame" is the same as the
        # "Astronomical basis frame", so that we have:
        self.Scan.Header.updateKeyword('CRVAL1', '', 0.)
        self.Scan.Header.updateKeyword('CRVAL2', '', 0.)

        # The Telescope diameter doesn't exist in MB-Fits yet => create keyword
        diam = self.PrimaryMambo.KeywordDict['TELSIZM'][0]
        # self.PrimaryMB.Header.addKeyword('DIAMETER','m',diam,'Single dish diameter')
        # exists since v. 1.54
        self.PrimaryMB.Header.updateKeyword('DIAMETER', '', diam)
        self.Scan.Header.updateKeyword('DIAMETER', '', diam)

        #--------------------------------------------------------------------------
        # Store a few infos as new attributes - they are needed in various places
        #--------------------------------------------------------------------------
        # The scan number, to be repeated in the header of the ARRAYDATA table
        self.Scannum = self.PrimaryMambo.KeywordDict['SCAN'][0]
        self.Febe.Header.updateKeyword('SCANNUM', '', self.Scannum)
        self.NbFeed = nbFeed
        self.Period = self.PrimaryMambo.KeywordDict['WOBCYCLE'][0]
        self.Throw = self.PrimaryMambo.KeywordDict['WOBTHROW'][0]/3600.  # in deg.
        # Frequency: convert GHz to Hz
        self.Frequency = self.PrimaryMambo.KeywordDict['FREQUENC'][0]*1.e9
        # In case of fast scanning, use 1/sampling rate as the period
        if (self.FastScan):
            self.Period = 1./self.PrimaryMambo.KeywordDict['SMPLRATE'][0]

    def fillMamboPrimary(self):
        """
        DES: Update the keyword values in the Mambo Primary header,
        using the equivalent keywords found in the MB-FITS file.
        """

        # Extract the XML description of the MAMBO Primary Header
        xmlMambo = XmlStructure('MAMBO')
        tab = xmlMambo.XmlScan.tables['Primary']
        tblHeader = tab.getElementsByTagName('HEADER')[0]

        # for each keyword, get the value from the MB-FITS equivalent
        for x in tblHeader.childNodes:
            if x.nodeType == x.ELEMENT_NODE:
                txt = str(x.childNodes[0].data)
                equiv = x.getAttribute('mbfitsEq')
                if ((equiv != 'None') & (equiv != 'Ok')):
                    equivKey = str(equiv[0:string.find(equiv, "(")])
                    equivTab = equiv[string.find(equiv, "(")+1:string.find(equiv, ")")]
                    if (equivTab == "Primary"):
                        try:
                            val = self.MBfits.TableList[0].Header.KeywordDict[equivKey]
                        except:
                            if (equivKey == 'DIAMETER'):
                                val = [12.]
                    elif (equivTab == "SCAN-MBFITS"):
                        try:
                            val = self.MBfits.TableList[1].Header.KeywordDict[equivKey]
                        except KeyError:
                            if equivKey == 'UTC2UT1':
                                equivKey = 'UT1UTC'
                                val = self.MBfits.TableList[1].Header.KeywordDict[equivKey]

                    elif (equivTab == "FEBEPAR-MBFITS"):
                        val = self.MBfits.TableList[2].Header.KeywordDict[equivKey]
                    if (equivTab in ["Primary", "SCAN-MBFITS", "FEBEPAR-MBFITS"]):
                        if config.DEBUG:
                            print "--> eqTab = "+equivTab
                            print "-->   txt = "+txt
                            print "--> value = "+str(val[0])

                        self.PrimaryMambo.Header.updateKeyword(txt, '', val[0])

        #--------------------------------------------------------------------------
        # Many things have to be set manually
        #--------------------------------------------------------------------------
        # Convert the infos about the observing mode
        obsMode, flag1, flag2 = self.getObsMode()
        self.PrimaryMambo.Header.updateKeyword('OBSMODE', '', obsMode)
        self.PrimaryMambo.Header.updateKeyword('SRP1FLAG', '', flag1)
        self.PrimaryMambo.Header.updateKeyword('SRP2FLAG', '', flag2)
        # Split the FrontEnd and BackEnd names
        fe_be = self.NameFEBE.split('-')
        self.PrimaryMambo.Header.updateKeyword('FRONTEND', '', fe_be[0])
        self.PrimaryMambo.Header.updateKeyword('BACKEND', '', fe_be[1])
        #--------------------------------------------------------------------------
        # Numbers of AC- and DC-coupled channels can be found in the FEEDTYPE
        # column of the FEBEPAR table
        feedType = self.MBfits.TableList[2].BinTable.Data['FEEDTYPE'][0]
        feedType = feedType.tolist()
        nbAC = feedType.count(1)
        nbDC = feedType.count(2)
        if ((nbAC == 0) & (nbDC == 0)):     # when trying to convert heterodyne
            nbAC = len(feedType)              # data to the Mambo format
        self.PrimaryMambo.Header.updateKeyword('NRECAC', '', nbAC)
        self.PrimaryMambo.Header.updateKeyword('NRECDC', '', nbDC)
        self.PrimaryMambo.Header.updateKeyword('NCHAN', '', nbAC+nbDC)
        # The reference channel is in the FEBEPAR table
        try:
            refChan = self.MBfits.TableList[2].BinTable.Data['REFFEED'][0]
        except TypeError:
            refChan = self.MBfits.TableList[2].BinTable.Data['REFFEED']
        usedChan = self.MBfits.TableList[2].BinTable.Data['USEFEED']
        usedChan = ravel(usedChan).tolist()
        numRefChan = usedChan.index(refChan)
        self.PrimaryMambo.Header.updateKeyword('RECCNTRL', '', numRefChan+1)
        # Receiver polarization: use that of the reference channel
        polar = self.MBfits.TableList[2].BinTable.Data['POLTY'][0]
        polar = polar[refChan-1]
        if (polar == 'X'):
            self.PrimaryMambo.Header.updateKeyword('RECPOLAR', '', 'NONE')
        elif (polar == 'L'):
            self.PrimaryMambo.Header.updateKeyword('RECPOLAR', '', 'LEFT')
        elif (polar == 'R'):
            self.PrimaryMambo.Header.updateKeyword('RECPOLAR', '', 'RIGHT')
        # Forward efficiency: use that of the reference channel
        forweff = self.MBfits.TableList[2].BinTable.Data['ETAFSS'][0]
        forweffVal = forweff[refChan-1, 0]   # this is still an array (?!)
        forweffVal = forweffVal[0]         # not now (20050317) on pc093
                                           # yes it is (20060116) on control
        self.PrimaryMambo.Header.updateKeyword('FORWEFF', '', forweffVal)

        # Gain/attenuation factor - added 20050317
        refGain = int(self.MBfits.TableList[2].BinTable.Data['BOLREFGN'][0][0])
        self.PrimaryMambo.Header.updateKeyword('GAIN', '', refGain)

        #--------------------------------------------------------------------------
        # Wobbler mode and parameters
        #--------------------------------------------------------------------------
        wobused = self.MBfits.TableList[1].Header.KeywordDict['WOBUSED'][0]
        if (wobused == 'T'):
            self.PrimaryMambo.Header.updateKeyword('WOBDEVCE', '', 1)
            wobmode = self.MBfits.TableList[1].Header.KeywordDict['WOBMODE'][0]
            if (wobmode == 'TRIANGULAR'):
                self.PrimaryMambo.Header.updateKeyword('WOBMODE', '', 1)
            else:
                self.PrimaryMambo.Header.updateKeyword('WOBMODE', '', 0)
        # Fast Scanning mode?
        if (self.FastScan):
            self.PrimaryMambo.Header.updateKeyword('FASTSCAN', '', 'YES')
        else:
            self.PrimaryMambo.Header.updateKeyword('FASTSCAN', '', 'NO')

        #--------------------------------------------------------------------------
        # NPHASES is required to avoid NIC crashing when loading the file
        if self.Scantype['SCANTYPE'] == 'SKYDIP':
            self.PrimaryMambo.Header.updateKeyword('NPHASES', '', 1)
        else:
            self.PrimaryMambo.Header.updateKeyword('NPHASES', '', 2)
        # if Fast Scanning, NPHASES should be set to zero
        # 20041213 - but mopsi complains when it's zero => set it to one
        if (self.FastScan):
            self.PrimaryMambo.Header.updateKeyword('NPHASES', '', 1)
        # And gain is required to compute the Y range - assume it is 10
        # 2004/3/08: use DEWANG in FEBEPAR header to store it - defined in Mambo.xml
        # self.PrimaryMambo.Header.updateKeyword('GAIN','',10)
        #

        #--------------------------------------------------------------------------
        # Coordinates and Astronomical basis frame stuff
        sbas = self.ctype2sbas()
        for key in sbas.keys():
            self.PrimaryMambo.Header.updateKeyword(key, '', sbas[key])

        #--------------------------------------------------------------------------
        # Read the updated Primary Header, to update its keyword values
        # in memory (= in the PrimaryMambo attribute)
        self.PrimaryMambo.Header.read()
        # Store the wobbler period and throw, that we be used later
        self.Period = self.PrimaryMambo.Header.KeywordDict['WOBCYCLE'][0]
        self.Throw = self.PrimaryMambo.Header.KeywordDict['WOBTHROW'][0]
        # Will need the date in MJD later
        dateObs = self.PrimaryMambo.Header.KeywordDict['DATE-OBS'][0]
        self.DateMJD0, status = sla_cldj(string.atoi(dateObs[0:4]), \
                                 string.atoi(dateObs[5:7]), \
                                 string.atoi(dateObs[8:10]))   # in day

        #--------------------------------------------------------------------------
        # 20041213 - a few patches to avoid troubles in mopsic
        tmpGain = self.PrimaryMambo.Header.KeywordDict['GAIN'][0]
        if tmpGain == 0:
            self.PrimaryMambo.Header.updateKeyword('GAIN', '', 1)
        # The HPBW seems to correspond to a 30m telescope
        # but (see also RZ's mail from 20041213)
        tmpFreq = self.PrimaryMambo.Header.KeywordDict['FREQUENC'][0]
        if tmpFreq == 0.:
            tmpFreq = 100.
        else:
            tmpFreq = tmpFreq/2.5
        self.PrimaryMambo.Header.updateKeyword('FREQUENC', '', tmpFreq)

        #--------------------------------------------------------------------------
        # Now the data table can be created
        if (self.FastScan):
            self.Data = Table('dataFast', self.PrimaryMambo)
            self.Data.create()
            self.Data.Header.updateKeyword('EXTNAME', '', 'data')
        else:
            self.Data = Table('data', self.PrimaryMambo)
            self.Data.create()


    def fillFebepar(self):
        """
        DES: This method writes one row in the FEBEPAR-MBFITS table, by
        reading the content of a Mambo RCP file, specified by the total
        number of pixels (40 or 120).
        """

        # Read the Receiver Channels Parameters
        rcp = self.readRCP()
        UseBand = [1]                 # new in v. 1.52
        Usefeed = range(1, self.NbFeed+1)	  # all feeds are used
        useAC = self.PrimaryMambo.KeywordDict['NRECAC'][0]
        useDC = self.PrimaryMambo.KeywordDict['NRECDC'][0]
        # Feedtype = useAC*'A'+useDC*'D'
        Feedtype = useAC*[1]+useDC*[2]    # say AC=1 and DC=2 (need numbers)
        Off_X, Off_Y, Bolflat = [], [], []
        for i in range(self.NbFeed):
            Off_X.append(rcp[i][1]/3600.)   # convert arcsec to deg
            Off_Y.append(rcp[i][2]/3600.)
            Bolflat.append(rcp[i][0])
        # Reference Channel
        Reffeed = self.PrimaryMambo.KeywordDict['RECCNTRL'][0]
        polar = self.PrimaryMambo.KeywordDict['RECPOLAR'][0]
        if (polar == 'NONE'):
            Polty = self.NbFeed*'X'
        elif (polar == 'LEFT'):
            Polty = self.NbFeed*'L'
        elif (polar == 'RIGHT'):
            Polty = self.NbFeed*'R'
        Pola = list(zeros(self.NbFeed, 'f'))
        dummy = list(ones(self.NbFeed, 'f'))
        Apereff = dummy
        Beameff = dummy
        forwardEff = self.PrimaryMambo.KeywordDict['FORWEFF'][0]
        Etafss = list(forwardEff*ones(self.NbFeed, 'f'))
        HPBW = dummy
        Antgain = dummy
        Gainimag = dummy

        # New in version 1.54
        bolgain = 1.
        bechans = dummy
        # New in version 1.55
        nusefeed = [self.NbFeed]
        tcal = dummy
        boldcoff = dummy

        # Put everything in one single list
        oneRow = [UseBand, nusefeed, Usefeed, bechans, Feedtype, Off_X, Off_Y]
        oneRow.extend([Reffeed, Polty, Pola, Apereff, Beameff])
        oneRow.extend([Etafss, HPBW, Antgain, tcal, 1., bolgain, boldcoff, Bolflat, Gainimag, 0., 0.])
        self.Febe.BinTable.addTableRow(oneRow)


    def convertFebepar(self):
        """
        DES: This method generates a RCP file, where the relative gains
        and offsets of pixels are stored, from the content of the FEBEPAR
        table. The output file name is <FE_name>.rcp.
        """

        FebeTab = self.MBfits.TableList[2]
        off_x = FebeTab.BinTable.Data['FEEDOFFX'][0]
        off_y = FebeTab.BinTable.Data['FEEDOFFY'][0]
        gain = FebeTab.BinTable.Data['FLATFIEL'][0,:, 0]
        used = FebeTab.BinTable.Data['USEFEED'][0]
        Fe_name = FebeTab.Header.KeywordDict['FEBE']
        Fe_name = Fe_name[0][:8]
        Fe_name = Fe_name.rstrip()
        out = file(Fe_name+".rcp", 'w')
        # Write parameters only for the feeds in use
        for i in used:
            out.write(str("%i %f %f %f %f\n"%(i[0], gain[i-1][0], gain[i-1][0], off_x[i-1], off_y[i-1])))
        out.close()


    def processMamboData(self):
        """
        DES: This method generates ARRAYDATA, DATAPAR and MONITOR tables in
        the MB-FITS file for every subscan in the MAMBO file.
        """

        #---------------------------------------------------------------
        # Collect some data to be stored in the MONITOR table
        #---------------------------------------------------------------
        pressure = self.PrimaryMambo.KeywordDict['PRESSURE'][0]
        temperat = self.PrimaryMambo.KeywordDict['TEMPERAT'][0]
        humidity = self.PrimaryMambo.KeywordDict['HUMIDITY'][0]
        refract = self.PrimaryMambo.KeywordDict['REFRACT'][0]
        foc_x = self.PrimaryMambo.KeywordDict['SFCX'][0]
        foc_y = self.PrimaryMambo.KeywordDict['SFCY'][0]
        foc_z = self.PrimaryMambo.KeywordDict['SFCZ'][0]
        focus = [foc_x, foc_y, foc_z]
        phi_x = self.PrimaryMambo.KeywordDict['SPHX'][0]
        phi_y = self.PrimaryMambo.KeywordDict['SPHY'][0]
        phi_z = self.PrimaryMambo.KeywordDict['SPHZ'][0]
        phi = [phi_x, phi_y, phi_z]


        #---------------------------------------------------------------
        # Extract the (receiver) data from the Mambo data table
        #---------------------------------------------------------------
        data = self.Mambo.TableList[2].BinTable
        UT = data.Data['UT']
        lst = data.Data['LST']
        if (self.FastScan):
            phase = data.Data['SIGNAL']
            tot = data.Data['TOT']
        else:
            phase1 = data.Data['PHASE1']
            phase2 = data.Data['PHASE2']
            tot1 = data.Data['TOT1']
            tot2 = data.Data['TOT2']
        Az = data.Data['AZ']
        El = data.Data['EL']
        Scan_off = data.Data['SCAN_COO']
        # WARNING!! The SCAN_COO contains Focus offsets for Focus scans
        if (self.Scantype['SCANTYPE'] == 'FOCUS'):
            Az_off, El_off = Scan_off[:, 0], Scan_off[:, 1]
            # they seem to be written in microns -> convert to mm
            Az_off = Az_off / 1000.
            El_off = El_off / 1000.
        else:
            Az_off = Scan_off[:, 0]/10.	# convert deciarcs to arcsec
            El_off = Scan_off[:, 1]/10.
            # They have to be written in degrees in the DATAPAR tables
            Az_off = Az_off/3600.
            El_off = El_off/3600.
        # also convert track_er to degrees
        Track_er = data.Data['TRACK_ER']/36000.
        # MJD, computed from DATE-OBS and UT
        MJD = self.DateMJD0+UT/(24.*3600.)

        # Extract the informations from the subscans table
        subscans = self.Mambo.TableList[1].BinTable
        startTimes = subscans.Data['Time']
        startTimes = startTimes[:, 0]
        epoch = subscans.Data['Epoch']
        nbSubscans = len(startTimes)
        # Will also need the longitude to convert LST to GST
        long = self.PrimaryMambo.KeywordDict['TELLONGI'][0]
        long = long*3600./15.  # in s
        eeq = sla_eqeqx(self.DateMJD0)  # Equation of the equinoxes (in rad)
        eeq = eeq*(180./math.pi)*3600./15.  # in s
        GMST0 = sla_gmst(self.DateMJD0)*(180./math.pi)*3600./15.  # GMST at
                                                             # 0h UT, in s.

        #-----------------------------------------------------------------------
        # Create one observation (i.e. ARRAYDATA + DATAPAR + MONITOR tables)
        # for each subscan in the Mambo file. Compare LST (from the data table)
        # with Time (from the subscans table) to know when a new subscan starts.
        #-----------------------------------------------------------------------
        # initialisation of row number
        nbRows = shape(lst)[0]
        numInteg = 0	# current number of integration

        for numSubscan in range(nbSubscans):
            print "Subscan: ", numSubscan+1, " / ", nbSubscans
            Arraydata = Table('ARRAYDATA-MBFITS', self.Febe)
            Arraydata.create()
            # Update number of feeds and table dimension
            Arraydata.Header.updateKeyword('NUSEFEED', '', self.NbFeed)
            Arraydata.BinTable.updateDimension('DATA')
            # Store the Scan Number (constant) and an increasing Observation number
            Arraydata.Header.updateKeyword('SCANNUM', '', self.Scannum)
            Arraydata.Header.updateKeyword('OBSNUM', '', numSubscan+1)
            # Also repeat the FeBe combination, Baseband number and date of obs.
            Arraydata.Header.updateKeyword('FEBE', '', self.NameFEBE)
            Arraydata.Header.updateKeyword('BASEBAND', '', 1)
            # And the frequency, in Hz
            # Arraydata.Header.updateKeyword('2CRVL4F','',self.Frequency)
            # better to use RESTFREQ
            Arraydata.Header.updateKeyword('RESTFREQ', '', self.Frequency)
            # timeStart: use MJD[0] - half a period to be really before the 1st datapoint
            timeStart = MJD[numInteg]-(self.Period/2.)/(3600.*24.)

            # timeStart = self.DateMJD0
            # timeStart += (startTimes[numSubscan]-GMST0-long-eeq)/86400.
            tmpTime = sla_djcal(9, timeStart)[0]  # date+time as an array, with
                                           # tmpTime[3]/1.e9 = fraction of day
            timePlus = sla_cd2tf(4, tmpTime[3]/1.e9)[1]  # Hour in the day (array)
            timeSys = str("%4i-%02i-%02iT%02i:%02i:%07.4f" % \
                          (tmpTime[0], tmpTime[1], tmpTime[2], timePlus[0],\
                           timePlus[1], timePlus[2]+timePlus[3]/1.e4))
            Arraydata.Header.updateKeyword('DATE-OBS', '', timeSys)

            # Create one MONITOR and one DATAPAR tables
            Monitor = Table('MONITOR-MBFITS', self.Febe)
            Monitor.create()
            Monitor.Header.updateKeyword('SCANNUM', '', self.Scannum)
            Monitor.Header.updateKeyword('OBSNUM', '', numSubscan+1)
            Monitor.Header.updateKeyword('DATE-OBS', '', timeSys)
            Datapar = Table('DATAPAR-MBFITS', self.Febe)
            Datapar.create()
            Datapar.Header.updateKeyword('SCANNUM', '', self.Scannum)
            Datapar.Header.updateKeyword('OBSNUM', '', numSubscan+1)
            Datapar.Header.updateKeyword('DATE-OBS', '', timeSys)
            Datapar.Header.updateKeyword('FEBE', '', self.NameFEBE)
            # Write the time (LST) at obs. start in Datapar
            Datapar.Header.updateKeyword('LST', '', startTimes[numSubscan])
            # Store OBSTYPE and SCAN parameters in the DATAPAR Header
            for key in ('OBSTYPE', 'SCANTYPE', 'SCANMODE', 'SCANGEOM'):
                Datapar.Header.updateKeyword(key, '', self.Scantype[key])
                # SCANDIR: should be sometimes ALON, sometimes ALAT,...
                if self.Scantype['SCANDIR'] != '':
                    Datapar.Header.updateKeyword('SCANDIR', '', self.Scantype['SCANDIR'])

            #---------------------------------------------------------------
            # Write a few rows in the MONITOR Table
            # ---------------------------------------------------------------
            # 2003/10/20: if SCANTYPE is FOCUS, the FOCUS_Z info is in Az_off
            Monitor.BinTable.addTableRow([MJD[numInteg], 'TAMB_P_HUMID',\
                  [temperat, pressure, humidity], 'C;mbar;%'])
            if (self.Scantype['SCANTYPE'] == 'FOCUS'):
                focus = [foc_x, foc_y, Az_off[numInteg]]
            Monitor.BinTable.addTableRow([MJD[numInteg], 'FOCUS_X_Y_Z', focus, 'mm'])
            Monitor.BinTable.addTableRow([MJD[numInteg], 'PHI_X_Y_Z', phi, 'deg'])
            Monitor.BinTable.addTableRow([MJD[numInteg], 'REFRACTIO', refract, 'arcsec'])

            #------------------------------------------------------------
            # Do a loop, while the LST is < startTime(next subscan), or
            # while numInteg is < nbRows, in case this is the last subscan,
            # to fill the ARRAYDATA and DATAPAR tables
            #------------------------------------------------------------
            if (numSubscan < nbSubscans-1):
                test = (lst[numInteg] < startTimes[numSubscan+1])
            else:
                test = (numInteg < nbRows)
            while(test):
                # Write the data row by row...
                oneRow = [MJD[numInteg]]
                if (self.FastScan):
                    oneRow.append(list(concatenate((phase[numInteg], tot[numInteg]))))
                    Arraydata.BinTable.addTableRow(oneRow)
                else:
                    oneRow.append(list(concatenate((phase1[numInteg], tot1[numInteg]))))
                    Arraydata.BinTable.addTableRow(oneRow)
                    # 2nd phase: add period/2. to get the right time stamp
                    oneRow = [MJD[numInteg]+self.Period/(2.*3600.*24.)]
                    oneRow.append(list(concatenate((phase2[numInteg], tot2[numInteg]))))
                    Arraydata.BinTable.addTableRow(oneRow)

                # Write the (Az,El) coordinates to the DATAPAR table, as well as
                # the scanning offsets; use period/2. as INTEGTIM
                # oneRow = [2*numInteg+1,0,MJD[numInteg],lst[numInteg]]
                # No more INTEGNUM nor NINTS since v. 1.54
                oneRow = [MJD[numInteg], lst[numInteg]+0.]
                if (self.FastScan):
                    oneRow.extend([self.Period, 'ON'])
                    if (self.Scantype['SCANTYPE'] == "FOCUS"):
                        oneRow.extend([0., 0.])
                        focus = [foc_x, foc_y, Az_off[numInteg]]
                    else:
                        oneRow.extend([Az_off[numInteg], El_off[numInteg]])
                    oneRow.extend([Az[numInteg], El[numInteg]])
                    # oneRow.extend([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
                    # angles and rotation matrix (7 values) replaced with only one angle in v. 1.54
                    oneRow.extend([0., 0., 0., 0., 0., 0., 0., 0., 0.])
                    oneRow.extend([focus, phi])
                    Datapar.BinTable.addTableRow(oneRow)
                else:
                    # 1st phase
                    oneRow.extend([self.Period/2., 'ON'])
                    if (self.Scantype['SCANTYPE'] == "FOCUS"):
                        oneRow.extend([0., 0.])
                        focus = [foc_x, foc_y, Az_off[numInteg]]
                    else:
                        oneRow.extend([Az_off[numInteg]+self.Throw/2., El_off[numInteg]])
                    oneRow.extend([Az[numInteg]+self.Throw/2., El[numInteg]])
                    # oneRow.extend([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
                    # angles and rotation matrix (7 values) replaced with only one angle in v. 1.54
                    oneRow.extend([0., 0., 0., 0., 0., 0., 0., 0., 0.])
                    oneRow.extend([focus, phi])
                    Datapar.BinTable.addTableRow(oneRow)

                    # 2nd phase
                    # oneRow = [2*numInteg+2,0,MJD[numInteg]+self.Period/(2.*3600.*24.)]
                    # No more INTEGNUM nor NINTS since v. 1.54
                    oneRow = [MJD[numInteg]+self.Period/(2.*3600.*24.)]
                    if (self.Scantype['SCANTYPE'] == "SKYDIP"):
                        # Phase 2 is also "ON" for skydips (no wobbling)
                        oneRow.extend([lst[numInteg]+self.Period/2., self.Period/2., 'ON'])
                    else:
                        oneRow.extend([lst[numInteg]+self.Period/2., self.Period/2., 'OFF'])
                    if (self.Scantype['SCANTYPE'] == "FOCUS"):
                        oneRow.extend([0., 0.])
                    else:
                        oneRow.extend([Az_off[numInteg]-self.Throw/2., El_off[numInteg]])
                    oneRow.extend([Az[numInteg]-self.Throw/2., El[numInteg]])
                    # oneRow.extend([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
                    oneRow.extend([0., 0., 0., 0., 0., 0., 0., 0., 0.])
                    oneRow.extend([focus, phi])
                    Datapar.BinTable.addTableRow(oneRow)

                # Compute TRACKING_AZ_EL as [Az,El]+TRACK_ER
                oneRow = [MJD[numInteg], 'TRACKING_AZ_EL']
                oneRow.extend([[Az[numInteg]+Track_er[numInteg][0],\
                                El[numInteg]+Track_er[numInteg][1]]])
                oneRow.extend(['deg;deg'])
                Monitor.BinTable.addTableRow(oneRow)

                # Go to next integration
                numInteg = numInteg+1
                if (numSubscan < nbSubscans-1):
                    test = (lst[numInteg] < startTimes[numSubscan+1])
                else:
                    test = (numInteg < nbRows)


    def fillMamboData(self):
        """
        DES: This methods fills the subscans and data tables in an output MAMBO
        file, using the data previously read in from an MB-FITS file.
        """

        # Some initialisations
        feedType = self.MBfits.TableList[2].BinTable.Data['FEEDTYPE'][0]
        feedType = ravel(feedType)
        numAC = nonzero(equal(feedType, 1))
        numDC = nonzero(equal(feedType, 2))
        if ((len(numAC) == 0) & (len(numDC) == 0)):   # e.g. heterodyne data
            numAC = range(len(feedType))

        # We will loop on the observations, to generate subscans
        nbObs = self.MBfits.TableList[1].Header.KeywordDict['NOBS'][0]
        nbRecords = 0
        # Instanciate an ObsEntity object
        entity = Entities.ObsEntity()

        # Open (in read mode) the MB-FITS file, for the getObservation
        # and fill methods to work
        self.MBfits.open()
        for numObs in range(nbObs):
            listObs = self.MBfits.getObservation(self.Scannum, numObs+1, self.NameFEBE)
            if config.DEBUG:
                print listObs
            entity.fill(self.MBfits, listObs)
            # Sum over the channels - useful for heterodyne, no effect on receiver
            # entity.sumChannels()

            # Compute subscan start time, to fill Epoch and Time columns
            # Epoch: convert DATE-OBS from Year+Month+Day to float value of year
            theDate = entity.DATE_OBS    # string
            year, day, flag = sla_clyd(string.atoi(theDate[0:4]),\
                          string.atoi(theDate[5:7]), string.atoi(theDate[8:10]))
            startEpoch = year+(day-1.)/365.

            # Time: use LST[0] - Period/2.
            startTime = entity.DATAPAR_LST[0] - self.Period/2.
            # could have used the LST in Datapar Header (which corresponds to obs.
            # start) if it would have a different name than in the binary table...
            self.Subscans.BinTable.addTableRow([numObs+1, startEpoch, startTime])

            # Convert DATAPAR_MJD to UT using MJD0 (=MJD at scan start)
            UT = (entity.DATAPAR_MJD-self.DateMJD0)*(24.*3600.)

            # if this is the 1st observation, fill the header of the data table
            if (numObs == 0):
                self.Data.Header.updateKeyword('UTC', '', UT[0])
                # RA and Dec have to be precessed to epoch of obs.
                # WARNING: not very accurate !!
                # should take into account the offsets at the beginning of the scan
                # anyway, these values are not yet used by NIC or MOPSI
                sbas = self.PrimaryMambo.Header.KeywordDict['SBAS'][0]
                equinox = self.PrimaryMambo.Header.KeywordDict['EPOCH'][0]
                ra1 = self.PrimaryMambo.Header.KeywordDict['SLAM'][0]
                dec1 = self.PrimaryMambo.Header.KeywordDict['SBET'][0]
                d2r = math.pi/180.
                if (sbas in [-1, 1, 2, 3, 4]):
                    ra2, dec2 = sla_preces('FK5', equinox, startEpoch, ra1*d2r, dec1*d2r)
                    ra2 = ra2/d2r
                    dec2 = dec2/d2r
                    self.Data.Header.updateKeyword('SLAM', '', ra2)
                    self.Data.Header.updateKeyword('SBET', '', dec2)
                    self.Data.Header.updateKeyword('EPOCH', '', startEpoch)
                # Also complete the Primary header: OAZM and OELV are (almost) the
                # offsets (found in SCAN_COO) of the 1st datapoint - except for
                # Focus, where SCAN_COO stores FOCUS_Z: then, use -0.5*wobthrow
                if (self.Scantype['SCANTYPE'] == "FOCUS"):
                    self.PrimaryMambo.Header.updateKeyword('OAZM', '', -0.5*self.Throw)
                    self.PrimaryMambo.Header.updateKeyword('OELV', '', 0.)
                else:
                    tmp = 3600.*(entity.DATAPAR_LONGOFF[0] + \
                                entity.DATAPAR_LONGOFF[1])/2.
                    self.PrimaryMambo.Header.updateKeyword('OAZM', '', tmp)
                    tmp = 3600.*(entity.DATAPAR_LATOFF[0] + \
                                entity.DATAPAR_LATOFF[1])/2.
                    self.PrimaryMambo.Header.updateKeyword('OELV', '', tmp)
                # And the frequency can be found in the ARRAYDATA header
                freq = getattr(entity, 'RESTFREQ')
                freq = freq/1.e9   # convert Hz to GHz
                # Update only if non-zero - 20041213
                if freq != 0.:
                    self.PrimaryMambo.Header.updateKeyword('FREQUENC', '', freq)
                # And the sample rate can be computed from the mean of 1/time between
                # integrations (from LST in DATAPAR table)
                diff = []
                for i in range(len(entity.DATAPAR_LST)-1):
                    diff.extend([entity.DATAPAR_LST[i+1]-entity.DATAPAR_LST[i]])
                rate = average(1./array(diff))
                self.PrimaryMambo.Header.updateKeyword('SMPLRATE', '', rate)
                # For maps, at least one velocity must be non-zero
                if self.Scantype['SCANTYPE'] in ['RASTER', 'OTF', 'MAP']:
                    vlam = self.PrimaryMambo.Header.KeywordDict['VLAM'][0]
                    vbet = self.PrimaryMambo.Header.KeywordDict['VBET'][0]
                    vazm = self.PrimaryMambo.Header.KeywordDict['VAZM'][0]
                    velv = self.PrimaryMambo.Header.KeywordDict['VELV'][0]
                    if vlam == 0. and vbet == 0. and vazm == 0. and velv == 0.:
                        if config.DEBUG:
                            print "Found observing mode = map, but all velocities are zero"
                        deltaAz = entity.DATAPAR_LONGOFF[-1]-entity.DATAPAR_LONGOFF[0]
                        deltaEl = entity.DATAPAR_LATOFF[-1]-entity.DATAPAR_LATOFF[0]
                        totalTime = entity.DATAPAR_LST[-1]-entity.DATAPAR_LST[0]
                        if abs(deltaAz) > abs(deltaEl):
                            self.PrimaryMambo.Header.updateKeyword('VAZM', '', 3600.*deltaAz/totalTime)
                            if config.DEBUG:
                                print " setting VAZM to: ", 3600.*deltaAz/totalTime
                        else:
                            self.PrimaryMambo.Header.updateKeyword('VELV', '', 3600.*deltaEl/totalTime)
                            if config.DEBUG:
                                print " setting VELV to: ", 3600.*deltaEl/totalTime

            # Start to fill the data
            if (self.FastScan):
                nbInteg = len(entity.DATAPAR_MJD)
                nbRecords += nbInteg
                for numInt in range(nbInteg):
                    data = entity.ARRAYDATA_DATA[numInt, 0,:]
                    phase, tot = [], []
                    for feed in numAC:
                        phase.extend([data[feed]])
                    for feed in numDC:
                        tot.extend([data[feed]])
                    oneRow = [UT[numInt]]
                    oneRow.extend([entity.DATAPAR_LST[numInt]])
                    oneRow.extend([entity.DATAPAR_AZIMUTH[numInt]])
                    oneRow.extend([entity.DATAPAR_ELEVATIO[numInt]])
                    if (self.Scantype['SCANTYPE'] == "FOCUS"):
                        tmp = entity.DATAPAR_DFOCUS[numInt, 2]
                        # convert millimeters to microns
                        tmp = tmp*1000.
                        oneRow.extend([[tmp, 0.]])
                    else:
                        tmp = 36000.*entity.DATAPAR_LONGOFF[numInt]
                        oneRow.extend([[tmp, 36000.*entity.DATAPAR_LATOFF[numInt]]])
                    oneRow.extend([[0., 0.], 0.])
                    oneRow.extend([phase, tot])
                    self.Data.BinTable.addTableRow(oneRow)

            else:   # no Fast Scanning mode
                nbInteg = len(entity.DATAPAR_INTEGNUM)/2
                nbRecords += nbInteg
                for numInt in range(nbInteg):
                    data1 = entity.ARRAYDATA_DATA[2*numInt, 0,:]
                    data2 = entity.ARRAYDATA_DATA[2*numInt+1, 0,:]
                    phase1, phase2 = [], []
                    tot1, tot2 = [], []
                    for feed in numAC:
                        phase1.extend([data1[feed]])
                        phase2.extend([data2[feed]])
                    for feed in numDC:
                        tot1.extend([data1[feed]])
                        tot2.extend([data2[feed]])

                    oneRow = [UT[2*numInt]]
                    oneRow.extend([entity.DATAPAR_LST[2*numInt]])
                    oneRow.extend([(entity.DATAPAR_AZIMUTH[2*numInt] + \
                                    entity.DATAPAR_AZIMUTH[2*numInt+1])/2.])
                    oneRow.extend([entity.DATAPAR_ELEVATIO[2*numInt]])
                    if (self.Scantype['SCANTYPE'] == "FOCUS"):
                        tmp = entity.DATAPAR_DFOCUS[2*numInt, 2]
                        # convert millimeters to microns
                        tmp = tmp*1000.
                        oneRow.extend([[tmp, 0.]])
                    else:
                        tmp = 36000.*(entity.DATAPAR_LONGOFF[2*numInt] + \
                                      entity.DATAPAR_LONGOFF[2*numInt+1])/2.
                        oneRow.extend([[tmp, 36000.*entity.DATAPAR_LATOFF[2*numInt]]])
                    oneRow.extend([[0., 0.], 0., 0.])
                    oneRow.extend([phase1, phase2, tot1, tot2])
                    self.Data.BinTable.addTableRow(oneRow)

            if config.DEBUG:
                print "Observation number", numObs+1, " written... "
                # raw_input()

        # Update the number of records in the Primary header
        self.PrimaryMambo.Header.updateKeyword('NRECORD', '', nbRecords)
        # Before closing the MB-FITS file, also get the values of
        # Temperature, Pressure and Humidity
        listMon = self.MBfits.getTables('MONITOR-MBFITS')
        if (len(listMon)):
            firstMon = self.MBfits.TableList[listMon[0]-1]
            row_TPH = firstMon.BinTable.selectRows('MONPOINT=="TAMB_P_HUMID"')
            # The program should not crash if this Monitor point is not found!
            if (len(row_TPH)):
                TPH = row_TPH[0][2]
                self.PrimaryMambo.Header.updateKeyword('TEMPERAT', '', TPH[0])
                self.PrimaryMambo.Header.updateKeyword('PRESSURE', '', TPH[1])
                self.PrimaryMambo.Header.updateKeyword('HUMIDITY', '', TPH[2])
            else:
                # print a warning message
                print "Warning: no TAMB_P_HUMID found, TEMPERAT, PRESSURE and"
                print "HUMIDITY keywords not updated..."

            # The same for refraction
            row_Refrac = firstMon.BinTable.selectRows('MONPOINT=="REFRACTIO"')
            if (len(row_Refrac)):
                refract = row_Refrac[0][2]
                self.PrimaryMambo.Header.updateKeyword('REFRACT', '', refract[0])
            else:
                # print a warning message
                print "Warning: no REFRACTIO found, REFRACT keyword not updated..."

        # All observations have been processed, close the MB-FITS file
        self.MBfits.close()


#*************************************************************************

    #-----------------------------------------------------------------------
    # Below are some "utilities" methods
    #-----------------------------------------------------------------------

    def getScanType(self):
        """
        DES: Convert the informations about the observing type from
        Mambo format (contained in OBSMODE + SRP1FLAG + SRP2FLAG) to
        an MB-FITS SCANTYPE. Also return the SCANMODE, SCANGEOM,
        SWTCHMOD, WOBSW, OBSTYPE and SCANDIR infos. The results are
        stored in the Scantype attribute, which is a Dictionary.
        """

        self.Scantype = {'SCANTYPE':'','SCANMODE':'','SCANGEOM':'',\
                'SWTCHMOD':'WOBSW','OBSTYPE':'ON','SCANDIR':''}
        obsmode = self.PrimaryMambo.KeywordDict['OBSMODE'][0]
        flag1 = self.PrimaryMambo.KeywordDict['SRP1FLAG'][0]
        flag2 = self.PrimaryMambo.KeywordDict['SRP2FLAG'][0]
        if ((obsmode == 1 and flag1 == 1) or (obsmode == 3)):   # Skydip
            self.Scantype['SCANTYPE'] = 'SKYDIP'
            self.Scantype['SCANMODE'] = 'RASTER'
            self.Scantype['SCANGEOM'] = 'LINE'
            self.Scantype['OBSTYPE'] = 'CAL'
            self.Scantype['SWTCHMOD'] = 'NO'
            self.Scantype['SCANDIR'] = 'ALAT'
        elif (obsmode == 1):                  # On/Off
            self.Scantype['SCANTYPE'] = 'ONOFF'
            self.Scantype['SCANMODE'] = 'SAMPLE'
            self.Scantype['SCANGEOM'] = 'SINGLE'
        elif obsmode == 2:                    # Raster map
            self.Scantype['SCANTYPE'] = 'RASTER'
            self.Scantype['SCANMODE'] = 'RASTER'
            self.Scantype['SCANGEOM'] = 'RECT'
        elif (obsmode == 4 and flag2 == 1):   # Pointing
            self.Scantype['SCANTYPE'] = 'POINT'
            self.Scantype['SCANMODE'] = 'OTF'
            self.Scantype['SCANGEOM'] = 'CROSS'
            self.Scantype['SCANDIR'] = 'ALON/LAT'
        elif obsmode == 5:                    # Focus
            self.Scantype['SCANTYPE'] = 'FOCUS'
            self.Scantype['SCANMODE'] = 'SAMPLE'
            self.Scantype['SCANGEOM'] = 'SINGLE'
        else:
            raise ValueError('Unknwon observing mode...')


    def getObsMode(self):
        """
        DES: Convert the scanType (from MB-FITS) to OBSMODE + SRP1FLAG
        + SRP2FLAG as defined in the MAMBO format.
        """

        scanType = self.Scantype['SCANTYPE']
        if scanType == 'SKYDIP':
            obsmode, flag1, flag2 = 3, 1, 0
        elif scanType == 'ONOFF':
            obsmode, flag1, flag2 = 1, 0, 0
        elif scanType in ['RASTER', 'OTF', 'MAP']:
            obsmode, flag1, flag2 = 2, 0, 0
        elif scanType == 'BOLOTIP':
            obsmode, flag1, flag2 = 3, 0, 0
        elif scanType == 'POINT':
            obsmode, flag1, flag2 = 4, 0, 1
        elif scanType == 'FOCUS':
            obsmode, flag1, flag2 = 5, 0, 0
        else:
            # raise ValueError,'Unknwon observing mode...'
            # for the moment assume this is a map - we will only do maps!
            obsmode, flag1, flag2 = 2, 0, 0

        return obsmode, flag1, flag2


    def readRCP(self):
        """
        DES: Read the Receiver Channels Parameters from the file
        'MRT_2002a_120.rcp' if the number of receivers is 120, or
        'MRT_2002s2_40.rcp' if it is 40. These files are supposed
        to be in the local directory. Returns a list of tuples,
        where each tuple is (Gain,X_off,Y_off).
        """

        nbBolo = self.NbFeed
        if nbBolo == 120:
            f = file('MRT_2002a_120.rcp')
        elif nbBolo == 40:
            f = file('MRT_2002s2_40.rcp')
        else:
            raise ValueError('Total (AC+DC) number of receivers must be 120 or 40!')

        param = f.readlines()
        result = []
        for i in range(len(param)-1):	# -1: skip last line
            tmp = string.split(param[i])
            if tmp[0] != '!':			# skip comments
                result.append((string.atof(tmp[1]),\
                               string.atof(tmp[3]), string.atof(tmp[4])))
        f.close()
        return result


    def sbas2ctype(self):
        """
        DES: Converts the SBAS value to the MB-FITS keywords that define the
        Astronomical basis frame: CTYPEj, WCSNAME, RADESYS, EQUINOX, and
        eventually MOVEFRAM. All these are stored in a dictionary.
        """

        # Initialise the result dictionary
        result = {'CTYPE1':'','CTYPE2':'','WCSNAME':'','RADECSYS':'', \
                  'EQUINOX':0.,'MOVEFRAM':0}
        sbas = self.PrimaryMambo.KeywordDict['SBAS'][0]
        epoch = self.PrimaryMambo.KeywordDict['EPOCH'][0]

        if (sbas in [-1, 1, 2, 3, 4]):
            result['CTYPE1'] = 'RA---SFL'
            result['CTYPE2'] = 'DEC--SFL'
            if (sbas == -1):
                result['EQUINOX'] = 2000.
                result['RADECSYS'] = 'FK5'
            elif (sbas == 1):
                result['EQUINOX'] = 1950.
                result['RADECSYS'] = 'FK4'
            else:
                result['EQUINOX'] = epoch
        elif (sbas == 0):
            result['CTYPE1'] = 'GLON-SFL'
            result['CTYPE2'] = 'GLAT-SFL'
        elif (sbas in [6, 7, 8, 9]):
            result['CTYPE1'] = 'ELON-SFL'
            result['CTYPE2'] = 'ELAT-SFL'
        elif (sbas == 10):
            result['CTYPE1'] = 'ALON-SFL'
            result['CTYPE2'] = 'ALAT-SFL'
        else:
            result['CTYPE1'] = 'xxLN-SFL'
            result['CTYPE2'] = 'xxLT-SFL'
            result['MOVEFRAM'] = 1
            result['EQUINOX'] = epoch
            if (sbas == 11):    # Mercury
                result['CTYPE1'] = 'MELN-SFL'
                result['CTYPE2'] = 'MELT-SFL'
            elif (sbas == 12):  # Venus
                result['CTYPE1'] = 'VELN-SFL'
                result['CTYPE2'] = 'VELT-SFL'
            elif (sbas == 14):  # Mars
                result['CTYPE1'] = 'MALN-SFL'
                result['CTYPE2'] = 'MALT-SFL'
            elif (sbas == 15):  # Jupiter
                result['CTYPE1'] = 'JULN-SFL'
                result['CTYPE2'] = 'JULT-SFL'
            elif (sbas == 16):  # Saturn
                result['CTYPE1'] = 'SALN-SFL'
                result['CTYPE2'] = 'SALT-SFL'
            elif (sbas == 17):  # Uranus
                result['CTYPE1'] = 'URLN-SFL'
                result['CTYPE2'] = 'URLT-SFL'
            elif (sbas == 18):  # Neptune
                result['CTYPE1'] = 'NELN-SFL'
                result['CTYPE2'] = 'NELT-SFL'
            elif (sbas == 21):  # Moon
                result['CTYPE1'] = 'MOLN-SFL'
                result['CTYPE2'] = 'MOLT-SFL'

        return result


    def ctype2sbas(self):
        """
        DES: Converts the infos about the Astronomical basis frame from MB-FITS
        keywords (CTYPEj, EQUINOX...) to a SBAS value (+ epoch). The results
        are stored and returned in a dictionary.
        """

        # Initialise the result dictionary
        result = {'SBAS':0,'EPOCH':0.}
        ctype1 = self.MBfits.TableList[1].Header.KeywordDict['CTYPE1'][0]
        ctype2 = self.MBfits.TableList[1].Header.KeywordDict['CTYPE2'][0]
        equinox = self.MBfits.TableList[1].Header.KeywordDict['EQUINOX'][0]

        # Galactic
        if (ctype1[:4] == 'GLON') & (ctype2[:4] == 'GLAT'):
            result['SBAS'] = 0
            result['EPOCH'] = equinox

        # equatorial
        elif (ctype1[:2] == 'RA') & (ctype2[:3] == 'DEC'):
            result['EPOCH'] = equinox
            if (equinox == 2000.0):
                result['SBAS'] = -1
            elif (equinox == 1950.0):
                result['SBAS'] = 1
            else:
                result['SBAS'] = 2

        # horizontal
        elif (ctype1[:4] == 'ALON') & (ctype2[:4] == 'ALAT'):
            result['SBAS'] = 10
            result['EPOCH'] = equinox

        # ecliptic
        elif (ctype1[:4] == 'ELON') & (ctype2[:4] == 'ELAT'):
            result['EPOCH'] = equinox
            if (equinox == 1950.0):
                result['SBAS'] = 6
            else:
                result['SBAS'] = 7

        # body
        elif (ctype1[2:4] == 'LN') & (ctype2[2:4] == 'LT'):
            result['EPOCH'] = equinox
            if (ctype1[:2] == 'ME') & (ctype2[:2] == 'ME'):
                result['SBAS'] = 11
            elif (ctype1[:2] == 'VE') & (ctype2[:2] == 'VE'):
                result['SBAS'] = 12
            elif (ctype1[:2] == 'MA') & (ctype2[:2] == 'MA'):
                result['SBAS'] = 14
            elif (ctype1[:2] == 'JU') & (ctype2[:2] == 'JU'):
                result['SBAS'] = 15
            elif (ctype1[:2] == 'SA') & (ctype2[:2] == 'SA'):
                result['SBAS'] = 16
            elif (ctype1[:2] == 'UR') & (ctype2[:2] == 'UR'):
                result['SBAS'] = 17
            elif (ctype1[:2] == 'NE') & (ctype2[:2] == 'NE'):
                result['SBAS'] = 18
            elif (ctype1[:2] == 'MO') & (ctype2[:2] == 'MO'):
                result['SBAS'] = 21
            else:
                result['SBAS'] = 22

        return result
