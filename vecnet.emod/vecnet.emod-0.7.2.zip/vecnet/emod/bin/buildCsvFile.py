#!/usr/bin/python
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import time
from datetime import date, timedelta
sys.path.append("../")
try:
    from climate import ClimateDataFile
except ImportError:
    from vecnet.emod.climate import ClimateDataFile

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Please provide a json file, a bin file, and desired csv file name."
        exit(1)

    # Check for valid file types
    jsonExtension = sys.argv[1].split(".")[-1]
    if jsonExtension != "json":
        raise TypeError("Parameter 1 should be a json file")
    jsonFileName = sys.argv[1]
    binExtension = sys.argv[2].split(".")[-1]
    if binExtension != "bin":
        raise TypeError("Parameter 2 should be a bin file")
    binFileName = sys.argv[2]
    csvExtension = sys.argv[3].split(".")[-1]
    if csvExtension != "csv":
        raise TypeError("Parameter 3 should be a csv filename")
    csvFileName = sys.argv[3]

    climateDataFile = ClimateDataFile()
    climateDataFile.load(jsonFileName, binFileName)
    
    # Retrieve all necessary data
    nodeIDs = climateDataFile.nodeIDs
    climateData = climateDataFile.climateData
    startDayOfYear = climateDataFile.startDayOfYear
    dataValueCount = climateDataFile.dataValueCount
    originalDataYears = climateDataFile.originalDataYears
    
    # Fill header row
    headerRow = []
    headerRow.append("Date")
    for node in nodeIDs:
        headerRow.append(node)

    # Fill dates
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    startDayOfYearArray = startDayOfYear.split(" ")
    for month in range(len(months)):
        if startDayOfYearArray[0] == months[month]:
            startMonth = month
            break
    else:
        raise ValueError("Month name in StartDayOfYear must be in it's full name (ie January, not Jan or Jan.) StartDayOfYear was " + startDayOfYearArray[0])
    startYear = originalDataYears.split("-")[0] # Gets first year of year range (ie 1950 if it is 1950-2000)
    # This needs to be here to prevent it from incorrectly reading a date like 1955101 as 10/1/1955 instead of 1/01/1955
    if startMonth < 10:
        startMonth = "0" + str(startMonth)
    fullStartDate = str(startYear) + str(startMonth) + str(startDayOfYearArray[1])
    startDate = time.strptime(fullStartDate,'%Y%m%d')
    startDate = date(startDate.tm_year,startDate.tm_mon,startDate.tm_mday)
    dates = []
    dates.append(startDate.strftime('%m/%d/%Y'))
    for i in range(dataValueCount-1):
        newDate = startDate + timedelta(i+1)
        dates.append(newDate.strftime('%m/%d/%Y'))

    # Build lines
    lines = []
    # Add first line
    line = ""
    for item in headerRow:
        line = line + str(item) + ","
    # Remove last "," and add "\n"
    tempLine = line.rsplit(",", 1)
    empty = ""
    line = empty.join(tempLine) + "\n"
    lines.append(line)
    # Add remaining lines
    for row in range(dataValueCount):
        line = dates[row] + ","
        for node in range(len(nodeIDs)):
            line = line + str(climateData[nodeIDs[node]][row]) + ","
        # Remove last "," and add "\n"
        tempLine = line.rsplit(",", 1)
        empty = ""
        line = empty.join(tempLine) + "\n"
        lines.append(line)

    # Write lines to file
    csvFile = open(csvFileName, 'w')
    for line in lines:
        csvFile.write(line)
