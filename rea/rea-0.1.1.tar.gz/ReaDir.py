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
..module:: ReaDir
:synopsis: contains all the method to handle list of MBFits file
"""
__version__ = '$Revision: 2706 $'
__date__ = '$Date: 2010-04-13 17:16:20 +0200 (mar. 13 avril 2010) $'

from . import ReaConfig
import os
import sys
import re
import string
import cPickle
from . import ReaMessageHandler
from . import ReaMBFits, ReaMBFitsReader
from rea.Utilities import stripFitsExtension

MessHand = ReaMessageHandler.MessHand('ReaDir')

ListDir = []
CurrentList = []

SavedFile = os.path.join(
    ReaConfig.outDir,
     '.list_' +
     ReaConfig.projID +
     '.sav')

# -------------------------------------------------------------------


def setInDir(inputDirectory=''):
    """set the input directory

    Parameters
    ----------
    inputDirectory : str
        name of input directory
    """

    global ListDir, CurrentList

    if not isinstance(inputDirectory, str):
        MessHand.error("invalid input directory" + str(inputDirectory))
        return

    if inputDirectory == '':
        MessHand.info("input directory : " + ReaConfig.inDir)
        return
    inputDirectory = inputDirectory.strip()

    if inputDirectory[-1] != '/':
        inputDirectory = inputDirectory + '/'

    if os.path.isdir(inputDirectory) == 1:
        ReaConfig.inDir = inputDirectory
        MessHand.info("input directory : " + ReaConfig.inDir)
        ListDir = []
        CurrentList = []
    else:
        MessHand.error("no such directory: " + inputDirectory)

# -------------------------------------------------------------------


def setProjectID(projectID=None):
    """set the current project ID

    Parameters
    ----------
    projectID : str
        the ESO project ID for now
    """

    global SavedFile

    if not projectID:
        MessHand.info("project ID : " + ReaConfig.projID)
        return

    # the format of the project ID changed several times
    # so, the following regular expression keeps getting more
    # complicated
    checkID = re.compile('^\w-\d{2,3}\.\w-((\d{4,4})|(\d{4,4}\w))-\d{4,4}$')

    if not checkID.match(projectID):
        MessHand.warning("not a valid APEX project ID")

    ReaConfig.projID = projectID.upper()
    SavedFile = os.path.join(
        ReaConfig.outDir,
        '.list_' +
     ReaConfig.projID +
     '.sav')

# -------------------------------------------------------------------


def setDate(date=None):
    """set the current observing date

    Parameters
    ----------
    date : str
        the observing date YYYY-MM-DD
    """

    if not date:
        MessHand.info("obs. date : " + ReaConfig.date)
        return

    checkDate = re.compile('\d{4,4}-\d{2,2}-\d{2,2}')

    if not checkDate.match(date):
        MessHand.error("not a valid observing date")
        return

    ReaConfig.date = date


# -------------------------------------------------------------------
def setOutDir(outputDirectory=''):
    """set the output directory

    Parameters
    -----------
    outputDirectory : str
        name of output directory
    """
    if not isinstance(outputDirectory, str):
        MessHand.error("invalid output directory" + str(outputDirectory))
        return

    if outputDirectory == '':
        MessHand.info("output directory : " + ReaConfig.outDir)
        return

    outputDirectory = outputDirectory.strip()

    if outputDirectory[-1] != '/':
        outputDirectory = outputDirectory + '/'

    if os.path.isdir(outputDirectory) == 1:
        ReaConfig.outDir = outputDirectory
        MessHand.info("output directory : " + ReaConfig.outDir)
    else:
        MessHand.error("no such directory: " + outputDirectory)


# -------------------------------------------------------------------
def setInFile(inputFile='?'):
    """set the input file name

    Parameters
    ----------
    inputFile : str
        name of input file
    """

    if not isinstance(inputFile, str):
        MessHand.error("invalid input file name" + str(inputFile))
        return

    if inputFile == '?':
        MessHand.info("input file : " + ReaConfig.inFile)
        return

    inputFile = stripFitsExtension(inputFile.strip())

    ReaConfig.inFile = ''

    testfiles = [inputFile,
                 inputFile + '.fits',
                 inputFile + '.fits.gz',
                 'APEX-' + inputFile + '-' + ReaConfig.projID,
                 'APEX-' + inputFile + '-' + ReaConfig.projID + '.fits',
                 'APEX-' + inputFile + '-' + ReaConfig.projID + '.fits.gz',
                 'APEX-' + inputFile + '-' +
                 ReaConfig.date + '-' + ReaConfig.projID,
                 'iram-30m-' + inputFile + '-imb.fits', 'iram-30m-' + inputFile + '-imb.fits.gz']

    for testname in testfiles:
        if os.path.isfile(os.path.join(ReaConfig.inDir, testname)) == 1 or  \
                os.path.isdir(os.path.join(ReaConfig.inDir, testname)) == 1:
            ReaConfig.inFile = os.path.join(ReaConfig.inDir, testname)
            MessHand.debug("input file = " + testname)
            return

    if ReaConfig.inFile == '':
        listing = os.listdir(ReaConfig.inDir)
        for filename in listing:
            if string.find(filename, inputFile) >= 0:
                ReaConfig.inFile = os.path.join(ReaConfig.inDir, filename)
                MessHand.debug("input file = " + testname)
                return

    MessHand.error(
        "no such file or directory: " + ReaConfig.inDir + str(inputFile))

# -------------------------------------------------------------------


def setOutFile(outputFile='?'):
    """set the output file name

    Parameters
    ----------
    outputFile : str
        name of output file
    """

    if not isinstance(outputFile, str):
        MessHand.error("invalid output file name" + str(outputFile))
        return

    if outputFile == '?':
        MessHand.info("output file : " + ReaConfig.outFile)
        return

    outputFile = outputFile.strip()

    if outputFile[-5:] != '.fits':
        outputFile = outputFile + '.fits'

    if os.path.isfile(ReaConfig.inDir + outputFile) == 1:
        ReaConfig.inFile = ReaConfig.inDir + outputFile
        MessHand.info("output file = " + ReaConfig.outFile)
    else:
        MessHand.error(
            "no such file or directory: " + ReaConfig.inDir + str(outputFile))


# -------------------------------------------------------------------
def listInDir(separator=' '):
    """list the input directory

    Parameters
    ----------
    field separator : str
         e.g. separator = '||' for moinmoin-style table
    """

    global CurrentList

    if CurrentList in [[]]:
        MessHand.warning('Current list empty, reset...')
        resetCurrentList()

    toPrint = ['Object', 'ScanType', 'NSubscans', 'FEBEList',
               'refChan', 'Date', 'MJD', 'Size']
    toPrintFormat = ['%15s', '%12s', '%3i', '%17s',
                     '%5s', '%19s', '%9.3f', '(%5.1f MB)']

    for fitsfile in CurrentList:
        if fitsfile['status']:
            # Reformat the filename for display
            displayName = stripFitsExtension(fitsfile['filename'])
            if displayName[:5] == 'APEX-' and displayName[-len(ReaConfig.projID):] == ReaConfig.projID:
                displayName = displayName[5:-len(ReaConfig.projID) - 1]
            if displayName[:12] == 'iram30m-NIKA':
                displayName = displayName[8:-4]

            outString = separator + "%7s " % displayName

            for i in range(len(toPrint)):
                outString += separator + \
                    toPrintFormat[i] % fitsfile[toPrint[i]]

            print outString + separator

    outString = separator + "%7s" % "Name"
    for i in range(len(toPrint)):
        outString += separator + re.sub(
            '\..*',
            "s",
            toPrintFormat[i].replace('i',
                                     's').replace('(',
                                                  '')) % toPrint[i]
    print outString + separator

# -------------------------------------------------------------------


def resetCurrentList():
    """reset the CurrentList to the complete List """

    global ListDir

    if ListDir in [[]]:
        findInDir(update=1, readFile=1)
    else:
        findInDir(update=1, readFile=0)


# -------------------------------------------------------------------
def selectInDir(type, value, test='eq'):
    """Make a selection in the current List

    Parameters
    ----------
    type : str
        on what type should we make the selection
    value : str
        the value of that type
    test : str
        the test to do ( default: eq -- lt, gt, le, ge)
    """
    global CurrentList
    List = []
    for fitsfile in CurrentList:
        if fitsfile['status']:
            fitsfileType = fitsfile[type]
            if test == 'eq' and fitsfileType == value:
                List.append(fitsfile)
            if test == 'lt' and fitsfileType < value:
                List.append(fitsfile)
            if test == 'gt' and fitsfileType > value:
                List.append(fitsfile)
            if test == 'le' and fitsfileType <= value:
                List.append(fitsfile)
            if test == 'ge' and fitsfileType >= value:
                List.append(fitsfile)
            if test == 'ne' and fitsfileType != value:
                List.append(fitsfile)

    CurrentList = List
    MessHand.info(
        "selected %i scan(s) with %s %s %s" %
        (len(List), type, test, value))

# -------------------------------------------------------------------


def removeScans(scanList):
    """Remove scans from the current list

    Parameters
    ----------
    scanList : list
        list of scans to remove, full filename to avoid confusion
    """
    global CurrentList

    newList = []

    for i in range(len(CurrentList)):
        if not stripFitsExtension(CurrentList[i]['filename']) in scanList:
            newList.append(CurrentList[i])

    MessHand.info("removed %i scan(s)" % (len(CurrentList) - len(newList)))

    CurrentList = newList


# -------------------------------------------------------------------
def findInDir(update=True, readFile=True):
    """populate the list of fits files in the input directory

    Parameters
    ----------
    update : bool
        find only new scans
    readFile : bool
        read the saved List if available
    """

    global ListDir, CurrentList, SavedFile

    # read the saved file if asked and available
    if update and readFile and os.path.isfile(SavedFile):
        readList(filename=SavedFile)

    if not update:
        ListDir = []

    # Keep track of what is in the ListDir right now
    filenameInListDir = []
    for fitsfile in ListDir:
        filenameInListDir.append(fitsfile['filename'])

    listing = os.listdir(ReaConfig.inDir)
    fitsfile = [filename for filename in listing
                if ReaMBFits.isDataset(os.path.join(ReaConfig.inDir, filename))]

    for filename in fitsfile:
        MessHand.debug("Processing " + filename)

        if filename not in filenameInListDir:
            fitsdesc = {'filename': filename}
            fitsdesc['path'] = ReaConfig.inDir
            fitsdesc['status'] = 1
            try:
                MessHand.warning('checkFits disabled')
                # checkFits(filename)

                dataset = ReaMBFits.importDataset(ReaConfig.inDir + filename)
                reader = ReaMBFitsReader.createReader(dataset)

                reader.openSubscan(subsnum=None)

                fitsdesc['MBFitsVer'] = reader.read('MBFitsVer')
                fitsdesc['Instrument'] = reader.read('Instrument')
                fitsdesc['ExpTime'] = reader.read('ExpTime')

                fitsdesc['Telescope'] = reader.read('Telescope')
                fitsdesc['Project'] = reader.read('Project')
                fitsdesc['Observer'] = reader.read('Observer')
                fitsdesc['Scannum'] = reader.read('ScanNum')
                fitsdesc['Date'] = reader.read('DateObs')
                fitsdesc['MJD'] = reader.read('ScanMJD')
                fitsdesc['LST'] = reader.read('ScanLST')
                fitsdesc['NSubscans'] = reader.read('NObs')
                fitsdesc['Object'] = reader.read('Object')
                fitsdesc['ScanType'] = reader.read('ScanType')
                fitsdesc['ScanMode'] = reader.read('ScanMode')
                # fitsdesc['ScanGeom']   = reader.read('ScanGeom')

                fitsdesc['FEBEList'] = reader.read('Febes')

                fitsdesc['FEBE'] = []
                fitsdesc['refChan'] = []
                for febe in fitsdesc['FEBEList']:
                    febedesc = {}
                    febedesc['FEBE'] = febe
                    # febedesc['FEBE']      = reader.read('Febe', febe=febe)
                    # #NIKA
                    febedesc['nFeed'] = reader.read('FebeFeed', febe=febe)
                    # febedesc['type']      = reader.read('FdTypCod',
                    # febe=febe)
                    febedesc['type'] = reader.read('FeedCode', febe=febe)
                    febedesc['nUsedFeed'] = reader.read('NUseFeeds', febe=febe)
                    febedesc['refChan'] = reader.read("RefFeed", febe=febe)
                    fitsdesc['FEBE'].append(febedesc)
                    fitsdesc['refChan'].append(febedesc['refChan'])

                fitsdesc[
                    'Size'] = dataset.getSize(
                ) / 1024. ** 2  # in mega bytes

                dataset.close()

                ListDir.append(fitsdesc)
            except Exception as explain:
                fitsdesc['status'] = 0
                MessHand.warning(filename +
                                 " is a bad MBFits file (" + str(explain) +
                                 "), removed from list")

    # Save the file for further use
    saveList(filename=SavedFile)

    # Reset the current list and sort by MJD:
    tempDir = {}  # key: MJD; value: list of indeces in ListDir
    for i in xrange(len(ListDir)):
        mjd = ListDir[i]['MJD']
        if not mjd in tempDir.keys():
            tempDir[mjd] = []
        tempDir[mjd].append(i)
    keys = sorted(tempDir.keys())

    CurrentList = []
    for key in keys:
        indices = tempDir[key]
        for index in indices:
            CurrentList.append(ListDir[index])

# -------------------------------------------------------------------


def saveList(filename=None):
    """save the list into a file

    Parameters
    ----------
    filename : str
        the file name
    """

    global ListDir, savedFile

    if not filename:
        filename = SavedFile

    try:
        oFile = file(filename, 'w')
    except:
        MessHand.error(" permission denied, please change outdir")
        return
    cPickle.dump(ListDir, oFile, 2)
    oFile.close()
    MessHand.longinfo(" current list successfully written to %s" % filename)

# -------------------------------------------------------------------


def readList(filename=None):
    """read the list from a file

    Parameters
    ----------
    filename : str
        the file name
    """

    global ListDir, SavedFile

    if not filename:
        filename = SavedFile

    try:
        oFile = file(filename, 'r')
    except:
        MessHand.error(" permission denied")
        return
    ListDir = cPickle.load(oFile)
    oFile.close()
    MessHand.longinfo(" current list successfully read from %s" % filename)

# -------------------------------------------------------------------
# TODO This should simplified to minimum (test that the file is a MBFITS file, and thats all)
# Most of the other function should move to the MBFitsReader class as they
# are specific


def checkFits(filename):
    """check for MBFits name structure

    Parameters
    ----------
    filename : str
        the complete name of the fitsfile
    """
    dataset = None
    try:
        dataset = ReaMBFits.importDataset(ReaConfig.inDir + filename)

        MessHand.debug("Check fits basic structure : " + str(
            len(dataset.getTables())) + " tables in dataset")

        # Get the HduNumber for primary and other tables
        tablesSCAN = dataset.getTables(EXTNAME='SCAN-MBFITS')
        tablesFEBEPAR = dataset.getTables(EXTNAME='FEBEPAR-MBFITS')
        tablesARRAYDATA = dataset.getTables(EXTNAME='ARRAYDATA-MBFITS')
        tablesMONITOR = dataset.getTables(EXTNAME='MONITOR-MBFITS')
        tablesDATAPAR = dataset.getTables(EXTNAME='DATAPAR-MBFITS')

        # Check the basic structure of the fitsfile
        if not tablesSCAN:
            dataset.close()
            raise ReaMBFits.MBFitsError("no SCAN-MBFITS tables")
        if len(tablesSCAN) > 1:
            dataset.close()
            raise ReaMBFits.MBFitsError("more than one SCAN-MBFITS tables")
        if not tablesFEBEPAR:
            dataset.close()
            raise ReaMBFits.MBFitsError("no FEBEPAR-MBFITS tables")
        if not tablesARRAYDATA:
            dataset.close()
            raise ReaMBFits.MBFitsError("no ARRAYDATA-MBFITS tables")
        if not tablesMONITOR:
            dataset.close()
            raise ReaMBFits.MBFitsError("no MONITOR-MBFITS tables")
        if not tablesDATAPAR:
            dataset.close()
            raise ReaMBFits.MBFitsError("no DATAPAR-MBFITS tables")
    # if len(tablesARRAYDATA)*len(tablesFEBEPAR) \
    # != len(tablesMONITOR) \
    # != len(tablesDATAPAR)*len(tablesFEBEPAR):
    # raise ReaMBFits.MBFitsError("number of ARRAYDATA, MONITOR and DATAPAR
    # does not match")

    # hdu = mbfits.Table(Parent=fitsFile)

        # Primary Header
        kwMBFTSVER = dataset.getKeyword('MBFTSVER')
        if not kwMBFTSVER:
            dataset.close()
            raise ReaMBFits.MBFitsError("Keyword MBFITSVER is missing")
        if kwMBFTSVER.getValue() < 1.56:
            dataset.close()
            raise ReaMBFits.MBFitsError(
                "Old MBFits version :" + str(kwMBFTSVER.getValue()))

        # SCAN-MBFITS
        MessHand.debug("Check SCAN-MBIFTS :")
        tableSCAN = tablesSCAN[0]
        tableSCAN.open()

        kwOBJECT = tableSCAN.getKeyword('OBJECT')
        if (not kwOBJECT) or (kwOBJECT.getValue() == ''):
            MessHand.info(str(filename) + " has no object name")

        kwNOBS = tableSCAN.getKeyword('NOBS')
        if not kwNOBS:
            dataset.close()
            raise ReaMBFits.MBFitsError("No NOBS keyword")

        kwNSUBS = tableSCAN.getKeyword('NSUBS')
        if not kwNSUBS:
            dataset.close()
            raise ReaMBFits.MBFitsError("No NSUBS keyword")

        # From 1.57 one should only test for NSUBS, but since Fred is
        # a silly person and changed only the NOBS keyword..
        if kwNOBS.getValue() == 0 and kwNSUBS.getValue() == 0:
            dataset.close()
            raise ReaMBFits.MBFitsError("NOBS keyword set to 0")

        # check the silly bug of cfitsio
    #    if kwNSUBS.getValue() > 98:
    #        dataset.close()
    # raise ReaMBFits.MBFitsError("More than 98 subscans, cfitsio can not
    # (yet) handle that")

        kwDIAMETER = tableSCAN.getKeyword('DIAMETER')
        if (not kwDIAMETER) or (kwDIAMETER.getValue() == '') or (kwDIAMETER.getValue() == 0):
            dataset.close()
            raise ReaMBFits.MBFitsError("DIAMETER keyword missing")

        nRows = tableSCAN.getNumRows()
        if nRows == 0:
            dataset.close()
            raise ReaMBFits.MBFitsError("No FEBEPAR in SCAN-MBFITS")
        if nRows != len(tablesFEBEPAR):
            dataset.close()
            raise ReaMBFits.MBFitsError(
                "SCAN-MBFITS mismatch the number of FEBEPAR")

        allFEBE = tableSCAN.getColumn('FEBE').read()
        SCANNUM = tableSCAN.getKeyword('SCANNUM').getValue()

        tableSCAN.close()

        # FEBEPAR-MBFITS
        MessHand.debug(
            "Check FEBEPAR tables (" + str(len(tablesFEBEPAR)) + "table(s))")

        for tableFEBEPAR in tablesFEBEPAR:
    # MessHand.debug("Check FEBEPAR ( hdu ="+str(numHdu)+")")
            tableFEBEPAR.open()

            if tableFEBEPAR.getNumRows() == 0:
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBEPAR table empty")
            kwFEBE = tableFEBEPAR.getKeyword('FEBE')
            if (not kwFEBE) or (kwFEBE.getValue() in ['', 'None']):
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBE name not defined")
            if not kwFEBE.getValue() in allFEBE:
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBE not listed in SCAN-MBFITS")
            lSCANNUM = tableFEBEPAR.getKeyword('SCANNUM').getValue()
            if lSCANNUM != SCANNUM:
                dataset.close()
                raise ReaMBFits.MBFitsError(
                    "SCANNUM does not match SCAN-MBFITS")

            tableFEBEPAR.close()

        # ARRAYDATA-MBFITS
        MessHand.debug(
            "Check ARRAYDATA tables (" + str(len(tablesARRAYDATA)) + "table(s))")

        arraydata_empty = 1

        for tableARRAYDATA in tablesARRAYDATA:
    # MessHand.debug("Check ARRAYDATA ( hdu ="+str(numHdu)+")")
            tableARRAYDATA.open()

            if tableARRAYDATA.getNumRows() != 0:
                arraydata_empty = 0
            RESTFREQ = tableARRAYDATA.getKeyword('RESTFREQ').getValue()
            if RESTFREQ == 0:
                dataset.close()
                raise ReaMBFits.MBFitsError("RESTFREQ null")
            kwFEBE = tableARRAYDATA.getKeyword('FEBE')
            if (not kwFEBE) or (kwFEBE.getValue() in ['', 'None']):
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBE name not defined")
            if not kwFEBE.getValue() in allFEBE:
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBE not listed in SCAN-MBFITS")
            lSCANNUM = tableARRAYDATA.getKeyword('SCANNUM').getValue()
            if lSCANNUM != SCANNUM:
                dataset.close()
                raise ReaMBFits.MBFitsError(
                    "SCANNUM does not match SCAN-MBFITS")

            tableARRAYDATA.close()

        if arraydata_empty:
            dataset.close()
            raise ReaMBFits.MBFitsError("All ARRAYDATA tables empty")

        # DATAPAR-MBFITS
        MessHand.debug(
            "Check DATAPAR tables (" + str(len(tablesDATAPAR)) + "table(s))")

        datapar_empty = 1
        for tableDATAPAR in tablesDATAPAR:
    # MessHand.debug(" Check DATAPAR ( hdu ="+str(numHdu)+")")
            tableDATAPAR.open()

            if tableDATAPAR.getNumRows() != 0:
                datapar_empty = 0
            kwFEBE = tableDATAPAR.getKeyword('FEBE')
            if (not kwFEBE) or (kwFEBE.getValue() in ['', 'None']):
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBE name not defined")
            if not kwFEBE.getValue() in allFEBE:
                dataset.close()
                raise ReaMBFits.MBFitsError("FEBE not listed in SCAN-MBFITS")
            lSCANNUM = tableDATAPAR.getKeyword('SCANNUM').getValue()
            if lSCANNUM != SCANNUM:
                dataset.close()
                raise ReaMBFits.MBFitsError(
                    "SCANNUM does not match SCAN-MBFITS")

            tableDATAPAR.close()

        if datapar_empty:
            dataset.close()
            raise ReaMBFits.MBFitsError("All DATAPAR tables empty")

        # Check that corresponding ARRAYDATA and DATAPAR tables have same
        # numbers of rows
        nSubs = kwNSUBS.getValue()
        for iSubs in xrange(1, nSubs + 1):
            for febe in allFEBE:
                tableARRAYDATA = dataset.getTables(
                    EXTNAME="ARRAYDATA-MBFITS",
                    SUBSNUM=iSubs,
                    FEBE=febe)
                tableDATAPAR = dataset.getTables(
                    EXTNAME="DATAPAR-MBFITS",
                    SUBSNUM=iSubs,
                    FEBE=febe)
                tableARRAYDATA = tableARRAYDATA[0]
                tableDATAPAR = tableDATAPAR[0]

                tableARRAYDATA.open()
                tableDATAPAR.open()

                nRows1 = tableARRAYDATA.getNumRows()
                nRows2 = tableDATAPAR.getNumRows()

                tableARRAYDATA.close()
                tableDATAPAR.close()

                if nRows1 != nRows2:
                    MessHand.warning(filename + " different number of rows in ARRAYDATA and DATAPAR" +
                                     " for subscan %i - still readable" % (iSubs))

                kwRESTFREQ = tableARRAYDATA.getKeyword('RESTFREQ')
                if not kwRESTFREQ:
                    dataset.close()
                    raise ReaMBFits.MBFitsError("No RESTFREQ keyword")

                if kwRESTFREQ.getValue() == 0:
                    dataset.close()
                    raise ReaMBFits.MBFitsError("RESTFREQ set to 0")
        # Close open files
        dataset.close()
    except:
        # Close open files
        if dataset:
            dataset.close()
        raise
