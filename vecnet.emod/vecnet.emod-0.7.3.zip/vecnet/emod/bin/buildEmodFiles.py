#!/usr/bin/python
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import getpass
import sys
sys.path.append("../")
try:
    from climate import ClimateDataFile
except ImportError:
    from vecnet.emod.climate import ClimateDataFile

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Please provide a csv file, desired json file name, and desired bin file name."
        exit(1)

    # Check for valid file types
    csvExtension = sys.argv[1].split(".")[-1]
    if csvExtension != "csv":
        raise TypeError("Parameter 1 should be a csv file")
    csvFileName = sys.argv[1]
    jsonExtension = sys.argv[2].split(".")[-1]
    if jsonExtension != "json":
        raise TypeError("Parameter 2 should be a json filename")
    jsonFileName = sys.argv[2]
    binExtension = sys.argv[3].split(".")[-1]
    if binExtension != "bin":
        raise TypeError("Parameter 3 should be a bin filename")
    binFileName = sys.argv[3]

    metaData = {}
    metaData['DateCreated'] = time.strftime("%m/%d/%Y")
    metaData['Tool'] = sys.argv[0]
    metaData['Author'] = getpass.getuser()

    dates = []
    nodes = {}

    # Get csv data
    csvFile = open(csvFileName, 'r')
    # For info on iterators go to https://docs.python.org/2/tutorial/classes.html#iteratorst
    lines = iter(csvFile)
    # Split line into an array via ',' and remove \n and \r
    headerRow = lines.next().strip('\n').strip('\r').split(',')
    # Initialize each node's list, but -1 because of date col
    for col in range(len(headerRow)-1):
        nodes[int(headerRow[col+1])] = []
    # Get the rest of the rows
    for line in lines:
        row = line.strip('\n').strip('\r').split(',')
        dates.append(row[0])
        # The -1 and +1 are to skip index 0, since it is for dates
        for col in range(len(row)-1):
            nodes[int(headerRow[col+1])].append(float(row[col+1]))
    csvFile.close()

    # Determine and set nodeCount and dataValueCount
    metaData['NodeCount'] = len(nodes)
    dataValueCount = len(dates)
    for node in nodes:
        if dataValueCount != len(nodes[node]):
            print "Csv file is missing data for " + node + "."
            exit(1)
    metaData['DatavalueCount'] = dataValueCount

    # Determine and set startDayOfYear
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    startDateArray = dates[0].split('/')
    startMonth = months[int(startDateArray[1])]
    startDayOfYear = startMonth + " " + startDateArray[0]
    metaData['StartDayOfYear'] = startDayOfYear

    # Determine and set originalDataYears
    startYear = startDateArray[2]
    endDateArray = dates[len(dates)-1].split('/')
    endYear = endDateArray[2]
    originalDataYears = str(startYear)
    if startYear != endYear:
        originalDataYears = originalDataYears + "-" + str(endYear)
    metaData['OriginalDataYears'] = originalDataYears

    # Get the remaining meta data from user
    metaData['IdReference'] = raw_input("Enter id reference (a unique, user-selected string that indicates the method used for generating NodeIDs in the input file): ")
    metaData['UpdateResolution'] = raw_input("Enter update resolution (time resolution of the climate file): ")
    metaData['DataProvenance'] = raw_input("Enter data provenance (source of the data): ")

    # Create node id list
    nodeIDs = []
    for node in nodes:
        nodeIDs.append(node)

    # Create climate data
    climateData = {}
    for node in nodes:
        climateData[node] = nodes[node]

    climateDataFile = ClimateDataFile(metaData, nodeIDs, climateData)
    climateDataFile.save(jsonFileName, binFileName)
