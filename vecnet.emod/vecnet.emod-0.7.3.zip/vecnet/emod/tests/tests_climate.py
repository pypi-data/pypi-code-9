# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
import sys
import os
sys.path.append("../")
from climate import ClimateDataFile
from nodeid import nodeIDToLatLong, latLongToNodeID, getParsedResolution

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "weather")

class Tests(unittest.TestCase):
    validNodeID = 336463960
    validResolution = "2.5 arcmin"
    validLatitude = -1.0416666666666714
    validLongitude = 33.91666666666666

    def setUp(self):
        pass

    def test__init__(self):
        # Check parameters
        self.assertRaises(TypeError, ClimateDataFile, 5)
        self.assertRaises(ValueError, ClimateDataFile, {}, "Not an integer")
        self.assertRaises(TypeError, ClimateDataFile, {}, {"This is not":"list, tuple, valid string, or int"})
        self.assertRaises(TypeError, ClimateDataFile, {}, [1,2], 3)
        
        # Test with no metaData
        climateDataFile = ClimateDataFile()

        # Test with unrequired metaData only
        metaData = {}
        metaData['UnrequiredItem'] = "ABC"
        self.assertRaises(KeyError, ClimateDataFile, metaData)

        # Test with required metaData
        metaData['DateCreated'] = "2 days ago"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['Tool'] = "A hammer"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['Author'] = "Someone in Egypt"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['IdReference'] = "Still don't know what this is"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['NodeCount'] = 1
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['DatavalueCount'] = 3
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['UpdateResolution'] = "What was this again"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['OriginalDataYears'] = "Yesterday-Today"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['StartDayOfYear'] = "Dec. 31"
        self.assertRaises(KeyError, ClimateDataFile, metaData)
        metaData['DataProvenance'] = "And don't know what this is either"
        climateDataFile = ClimateDataFile(metaData)
        
        # Test with nodeIDs
        nodeID = 111111
        climateDataFile = ClimateDataFile(metaData, nodeID)
        metaData['NodeCount'] = 2
        nodeIDs = [222222,333333]
        climateDataFile = ClimateDataFile(metaData, nodeIDs)

        # Test with climateData
        climateData = {222222:[5.43, 4.32, 3.21], 333333:[9.99, 8.88, 7.77]}
        climateDataFile = ClimateDataFile(metaData, nodeIDs, climateData)





    def testLoad(self):
        climateDataFile = ClimateDataFile()
        # Check parameters
        self.assertRaises(TypeError, climateDataFile.load, 1, 2)
        self.assertRaises(TypeError, climateDataFile.load, True, False)
        # Check for valid files (ie if they exist and if the json is actually json)
        self.assertRaises(IOError, climateDataFile.load, "a.json", "b.bin")
        self.assertRaises(ValueError,
                          climateDataFile.load,
                          os.path.join(base_dir,"badjson.json"),
                          os.path.join(base_dir, "shortvalid.bin"))
        # Check to see if all the required json elements are there, extra elements are ignored
        self.assertRaises(KeyError,
                          climateDataFile.load,
                          os.path.join(base_dir, "missingattributes.json"),
                          os.path.join(base_dir, "shortvalid.bin"))
        # Check to see if bin file has enough numbers
        self.assertRaises(ValueError,
                          climateDataFile.load,
                          os.path.join(base_dir, "shortvalid.json"),
                          os.path.join(base_dir, "missingdata.bin"))
        # Check bin file for valid numbers
        self.assertRaises(ValueError,
                          climateDataFile.load,
                          os.path.join(base_dir, "shortvalid.json"),
                          os.path.join(base_dir, "baddata.bin"))
        # Check json file and bin file
        jsonFile = open(os.path.join(base_dir, "shortvalid.json"), 'r')
        binFile = open(os.path.join(base_dir, "shortvalid.bin"), 'rb')
        climateDataFile.load(jsonFile, binFile)
        # Check json string
        climateDataFile.load("{    \"Metadata\": {        \"Author\": \"Me\",        \"DataProvenance\": \"No Idea\",        \"DatavalueCount\": 4,        \"DateCreated\": \"1-1-1999\",        \"IdReference\": \"NA\",        \"NodeCount\": 3,        \"OriginalDataYears\": \"BeginningOfTime-Yesterday\",        \"StartDayOfYear\": \"January 1\",        \"Tool\": \"Awesome Tool\",        \"UpdateResolution\": \"NA\"    },    \"NodeOffsets\": \"0AAAAAAE000000001AAAAAAE000000102AAAAAAE00000020\"}",
                             os.path.join(base_dir, "shortvalid.bin"))
        # Check binary as bytes
        binFile = open(os.path.join(base_dir, "shortvalid.bin"), 'rb')
        data = binFile.read()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"), data)



       
    def testSave(self):
        climateDataFile = ClimateDataFile()
        climateDataFile2 = ClimateDataFile()
        jsonFile = open(os.path.join(base_dir, "shortvalid.json"), 'r')
        binFile = open(os.path.join(base_dir, "shortvalid.json"), 'rb')
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"), os.path.join(base_dir, "shortvalid.bin"))
        # Check to parameters
        self.assertRaises(TypeError, climateDataFile.save, 1, 2)
        self.assertRaises(TypeError, climateDataFile.save, True, False)
        self.assertRaises(TypeError, climateDataFile.save, jsonFile, binFile)
        self.assertRaises(TypeError, climateDataFile.save, "result.BADEXTENSION", "result.bin")
        self.assertRaises(TypeError, climateDataFile.save, "result.json", "result.BADEXTENSION")
        # Check to see if load() was called yet
        self.assertRaises(ValueError,
                          climateDataFile2.save,
                          os.path.join(base_dir, "result.json"),
                          os.path.join(base_dir, "result.bin"))
        



    def testChangeMetaData(self):
        # Unrequired metadata
        metaData = {}
        metaData['UnrequiredItem'] = "ABC"

        # Required metadata
        metaData['DateCreated'] = "2 days ago"
        metaData['Tool'] = "A hammer"
        metaData['Author'] = "Someone in Egypt"
        metaData['IdReference'] = "Still don't know what this is"
        metaData['NodeCount'] = 1
        metaData['DatavalueCount'] = 3
        metaData['UpdateResolution'] = "What was this again"
        metaData['OriginalDataYears'] = "Yesterday-Today"
        metaData['StartDayOfYear'] = "Dec. 31"
        metaData['DataProvenance'] = "And don't know what this is either"

        climateDataFile = ClimateDataFile(metaData)

        # New unrequired metadata
        metaData = {}
        metaData['NewUnrequiredItem'] = "New"
        self.assertRaises(KeyError, ClimateDataFile, metaData)

        # New required metadata
        metaData['DateCreated'] = "3 days ago"
        metaData['Tool'] = "A screw driver"
        metaData['Author'] = "Someone in France"
        metaData['IdReference'] = "I know what this is"
        metaData['NodeCount'] = 2
        metaData['DatavalueCount'] = 50
        metaData['UpdateResolution'] = "Who was this again"
        metaData['OriginalDataYears'] = "Last week-Next week"
        metaData['StartDayOfYear'] = "Jan. 1"
        metaData['DataProvenance'] = "Something"
        
        climateDataFile.changeMetaData(metaData)
        self.assertEqual(climateDataFile.dateCreated, metaData['DateCreated'])
        self.assertEqual(climateDataFile.tool, metaData['Tool'])
        self.assertEqual(climateDataFile.author, metaData['Author'])
        self.assertEqual(climateDataFile.idReference, metaData['IdReference'])
        self.assertEqual(climateDataFile.nodeCount, metaData['NodeCount'])
        self.assertEqual(climateDataFile.dataValueCount, metaData['DatavalueCount'])
        self.assertEqual(climateDataFile.updateResolution, metaData['UpdateResolution'])
        self.assertEqual(climateDataFile.originalDataYears, metaData['OriginalDataYears'])
        self.assertEqual(climateDataFile.startDayOfYear, metaData['StartDayOfYear'])
        self.assertEqual(climateDataFile.dataProvenance, metaData['DataProvenance'])
        self.assertEqual(climateDataFile.otherMetaData['NewUnrequiredItem'], metaData['NewUnrequiredItem'])
        
        #self.assertRaises(KeyError, climateDataFile.otherMetaData['UnrequiredItem'])
        
        



        
    def testFileEquivalence(self):
        climateDataFile = ClimateDataFile()
        climateDataFile2 = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        climateDataFile.save(os.path.join(base_dir, "result1.json"),
                             os.path.join(base_dir, "result1.bin"))
        climateDataFile2.load(os.path.join(base_dir, "result1.json"),
                              os.path.join(base_dir, "result1.bin"))
        # Check to see if metaData attributes were saved and loaded properly
        self.assertEqual(climateDataFile.dateCreated, climateDataFile2.dateCreated)
        self.assertEqual(climateDataFile.tool, climateDataFile2.tool)
        self.assertEqual(climateDataFile.author, climateDataFile2.author)
        self.assertEqual(climateDataFile.idReference, climateDataFile2.idReference)
        self.assertEqual(climateDataFile.nodeCount, climateDataFile2.nodeCount)
        self.assertEqual(climateDataFile.dataValueCount, climateDataFile2.dataValueCount)
        self.assertEqual(climateDataFile.updateResolution, climateDataFile2.updateResolution)
        self.assertEqual(climateDataFile.originalDataYears, climateDataFile2.originalDataYears)
        self.assertEqual(climateDataFile.startDayOfYear, climateDataFile2.startDayOfYear)
        self.assertEqual(climateDataFile.dataProvenance, climateDataFile2.dataProvenance)

        self.assertEqual(len(climateDataFile.nodeIDs), len(climateDataFile2.nodeIDs))
        self.assertEqual(climateDataFile.nodeIDs, climateDataFile2.nodeIDs)

        
        self.assertEqual(len(climateDataFile.climateData), len(climateDataFile2.climateData))
        self.assertEqual(climateDataFile.climateData, climateDataFile2.climateData)





    def testExpectedResults(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        # Check metadata
        self.assertEqual("Me", climateDataFile.author)
        self.assertEqual("No Idea", climateDataFile.dataProvenance)
        self.assertEqual(4, climateDataFile.dataValueCount)
        self.assertEqual("1-1-1999", climateDataFile.dateCreated)
        self.assertEqual("NA", climateDataFile.idReference)
        self.assertEqual(3, climateDataFile.nodeCount)
        self.assertEqual("1990", climateDataFile.originalDataYears)
        self.assertEqual("January 1", climateDataFile.startDayOfYear)
        self.assertEqual("Awesome Tool", climateDataFile.tool)
        self.assertEqual("NA", climateDataFile.updateResolution)
        
        # Check node offsets
        nodeIDs = ['178956974', '447392430', '715827886']
        #nodeOffsets = ["00000000", "00000010", "00000020"]
        self.assertEqual(nodeIDs, climateDataFile.nodeIDs)
        #self.assertEqual(nodeOffsets, climateDataFile.nodeOffsets)
        print "A new check needs to be placed here to check node offsets. (tests:testExpectedResults)"

        # Check binary data
        climateData = {'178956974':[1.0, 2.0, 3.0, 4.0], '447392430':[11.0, 12.0, 13.0, 14.0],
                       '715827886':[21.0, 22.0, 23.0, 24.0]}
        self.assertEqual(climateData, climateDataFile.climateData)

    def testExtraJson(self):
        # Check if extra json stays when saving
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "extrajson.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        climateDataFile.save(os.path.join(base_dir, "result2.json"),
                             os.path.join(base_dir, "result2.bin"))

    def testAddNode(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        # Check parameters
        self.assertRaises(ValueError, climateDataFile.addNode, "ABC", [1.0, 2.0])
        self.assertRaises(TypeError, climateDataFile.addNode, 1.0, [1.0, 2.0])
        self.assertRaises(TypeError, climateDataFile.addNode, 12345678, {"item1":1.0, "item2":2.0})
        # Check if node already exists
        self.assertRaises(ValueError, climateDataFile.addNode, 178956974, [1.0, 2.0])
        # Test if a simple node addition works
        climateDataFile.addNode(12345678, (1.0, 2.0))
        climateDataFile.addNode(12345555, [1.0, 2.0])

    def testRemoveNode(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        self.assertRaises(ValueError, climateDataFile.removeNode, "ABC")
        self.assertRaises(TypeError, climateDataFile.removeNode, 1.0)

    def test__str__(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        print climateDataFile

    def testAddDataToNode(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))

        # Check parameters
        self.assertRaises(ValueError, climateDataFile.addDataToNode, "ABC", 1.0)
        self.assertRaises(TypeError, climateDataFile.addDataToNode, 1.0, 1.0)
        self.assertRaises(ValueError, climateDataFile.addDataToNode, 178956974, [999.0,998.0], 100)
        self.assertRaises(ValueError, climateDataFile.addDataToNode, 178956974, [999.0,998.0], -100)
        self.assertRaises(TypeError, climateDataFile.addDataToNode, 178956974, "NOT A LIST, TUPLE, OR FLOAT", 2)

        
        self.assertRaises(LookupError, climateDataFile.addDataToNode, 111, [999.0,998.0], 2)
        
        # Check if adding actually works
        climateDataFile.addDataToNode(178956974, [99.0, 98.0], 2)
        climateDataFile.addDataToNode(447392430, 52.0)
        climateDataFile.addDataToNode(715827886, (1.11, 2.22), 0)
        self.assertEqual(climateDataFile.nodeIDs[0], '178956974')
        self.assertEqual(climateDataFile.climateData['178956974'], [1.0, 2.0, 99.0, 98.0, 3.0, 4.0])
        self.assertEqual(climateDataFile.nodeIDs[1], '447392430')
        self.assertEqual(climateDataFile.climateData['447392430'], [11.0, 12.0, 13.0, 14.0, 52.0])
        self.assertEqual(climateDataFile.nodeIDs[2], '715827886')
        self.assertEqual(climateDataFile.climateData['715827886'], [1.11, 2.22, 21.0, 22.0, 23.0, 24.0])

        # Check if saving fails (it should since nodes are unequal size)
        self.assertRaises(ValueError, climateDataFile.save, "DoesntMatter.json", "DoesntMatter.bin")

        



    def testRemoveDataFromNode(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
    
        # Check parameters
        self.assertRaises(ValueError, climateDataFile.removeDataFromNode, "ABC", 1)
        self.assertRaises(TypeError, climateDataFile.removeDataFromNode, 1.0, 1)
        self.assertRaises(ValueError, climateDataFile.removeDataFromNode, 178956974, 100)
        self.assertRaises(ValueError, climateDataFile.removeDataFromNode, 178956974, -100)
        self.assertRaises(ValueError, climateDataFile.removeDataFromNode, 178956974, 1, 100)
        self.assertRaises(ValueError, climateDataFile.removeDataFromNode, 178956974, 2, 1) # Testing for negatives is not necessary since if startingIndex can't be negative, than it is impossilbe for endingIndex to be greater than it and still be negative.

        self.assertRaises(LookupError, climateDataFile.removeDataFromNode, 111, 2)

        # Check if removing actually works
        climateDataFile.removeDataFromNode(178956974, 0)
        climateDataFile.removeDataFromNode(447392430, 1, 2)
        climateDataFile.removeDataFromNode(715827886, -1)
        self.assertEqual(climateDataFile.nodeIDs[0], '178956974')
        self.assertEqual(climateDataFile.climateData['178956974'], [])
        self.assertEqual(climateDataFile.nodeIDs[1], '447392430')
        self.assertEqual(climateDataFile.climateData['447392430'], [11.0, 14.0])
        self.assertEqual(climateDataFile.nodeIDs[2], '715827886')
        self.assertEqual(climateDataFile.climateData['715827886'], [21.0, 22.0, 23.0])
        

        


    def testReplaceDataInNode(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))

        # Check parameters
        self.assertRaises(ValueError, climateDataFile.replaceDataInNode, "ABC", [999.0, 998.0], 1)
        self.assertRaises(TypeError, climateDataFile.replaceDataInNode, 1.0, [999.0, 998.0], 1)
        self.assertRaises(ValueError, climateDataFile.replaceDataInNode, 178956974, [999.0, 998.0], 100)
        self.assertRaises(ValueError, climateDataFile.replaceDataInNode, 178956974, [999.0, 998.0], -100)
        
        self.assertRaises(LookupError, climateDataFile.replaceDataInNode, 111, [999.0, 998.0], 1)

        # Check if replacing actually works
        climateDataFile.replaceDataInNode(178956974, [9999.0, 8888.0], 0)
        climateDataFile.replaceDataInNode(447392430, 1.0, 1)
        climateDataFile.replaceDataInNode(715827886, (55.0, 46.1), 3) # This also tests having more numbers to replace then there are numbers until the end (ie. 4 numbers in the list and you pick index 3 with 2 numbers to replace with. Index 3 is the last index and will replace it with the first number. The second number gets appended.)
        self.assertEqual(climateDataFile.nodeIDs[0], '178956974')
        self.assertEqual(climateDataFile.climateData['178956974'], [9999.0, 8888.0, 3.0, 4.0])
        self.assertEqual(climateDataFile.nodeIDs[1], '447392430')
        self.assertEqual(climateDataFile.climateData['447392430'], [11.0, 1.0, 13.0, 14.0])
        self.assertEqual(climateDataFile.nodeIDs[2], '715827886')
        self.assertEqual(climateDataFile.climateData['715827886'], [21.0, 22.0, 23.0, 55.0, 46.1])






    def testEVERYTHING(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        
        # Unrequired metadata
        metaData = {}
        metaData['UnrequiredItem'] = "This item is not required by ClimateDataFile."
        # Required metadata
        metaData['DateCreated'] = "2 days ago"
        metaData['Tool'] = "A hammer"
        metaData['Author'] = "Someone in Egypt"
        metaData['IdReference'] = "Still don't know what this is"
        metaData['NodeCount'] = 2
        metaData['DatavalueCount'] = 3
        metaData['UpdateResolution'] = "What was this again"
        metaData['OriginalDataYears'] = "Yesterday-Today"
        metaData['StartDayOfYear'] = "Dec. 31"
        metaData['DataProvenance'] = "And don't know what this is either"
        # Node ids
        nodeIDs = [12345, 67890]
        # Climate data
        climateData = {'12345':[1.1, 2.2, 3.3], '67890':[100.1, 200.2, 300.3]}
        # Create new
        climateDataFile = ClimateDataFile(metaData, nodeIDs, climateData)
        # Add node
        nodeID = 99999
        dataSet = [1000.1, 2000.2, 3000.3, 4000.4, 5000.5, 6000.6] # Longer list
        climateDataFile.addNode(nodeID, dataSet)
        # Remove node
        nodeID = 67890
        climateDataFile.removeNode(nodeID)
        # Add another node
        nodeID = 88888
        dataSet = [10000.1, 20000.2, 30000.3, 40000.4, 50000.5, 60000.6] # Another longer list
        climateDataFile.addNode(nodeID, dataSet)
        # Add data to node
        nodeID = 12345
        data = 4.4
        climateDataFile.addDataToNode(nodeID, data)
        # Add more data to node
        nodeID = 12345
        dataSet = [5.5, 6.6]
        climateDataFile.addDataToNode(nodeID, dataSet)
        # Remove data from node
        nodeID = 99999
        startingIndex = 1
        endingIndex = 2
        climateDataFile.removeDataFromNode(nodeID, startingIndex, endingIndex)
        # Replace data in node
        nodeID = 99999
        startingIndex = 3
        dataSet = [7777.7, 8888.8, 9999.9]
        climateDataFile.replaceDataInNode(nodeID, dataSet, startingIndex)

        # Check it all
        self.assertEqual(climateDataFile.otherMetaData['UnrequiredItem'], "This item is not required by ClimateDataFile.")
        self.assertEqual(climateDataFile.dateCreated, "2 days ago")
        self.assertEqual(climateDataFile.tool, "A hammer")
        self.assertEqual(climateDataFile.author, "Someone in Egypt")
        self.assertEqual(climateDataFile.idReference, "Still don't know what this is")
        self.assertEqual(climateDataFile.nodeCount, 3)
        self.assertEqual(climateDataFile.dataValueCount, 6)
        self.assertEqual(climateDataFile.updateResolution, "What was this again")
        self.assertEqual(climateDataFile.originalDataYears, "Yesterday-Today")
        self.assertEqual(climateDataFile.startDayOfYear, "Dec. 31")
        self.assertEqual(climateDataFile.dataProvenance, "And don't know what this is either")
        nodeIDs = ['12345', '99999', '88888']
        climateData = {'12345':[1.1, 2.2, 3.3, 4.4, 5.5, 6.6], '99999':[1000.1, 4000.4, 5000.5, 7777.7, 8888.8, 9999.9],
                       '88888':[10000.1, 20000.2, 30000.3, 40000.4, 50000.5, 60000.6]}
        self.assertEqual(len(nodeIDs), len(climateDataFile.nodeIDs))
        self.assertEqual(nodeIDs, climateDataFile.nodeIDs)
        self.assertEqual(len(climateData), len(climateDataFile.climateData))
        self.assertEqual(climateData, climateDataFile.climateData)
        
        climateDataFile.save(os.path.join(base_dir, "result3.json"),
                             os.path.join(base_dir, "result3.bin"))





    def testReturnFile(self):
        climateDataFile = ClimateDataFile()
        self.assertRaises(ValueError, climateDataFile.returnFile, "Some valid content", "not valid fileType")


    def testDecimalToHexString(self):
        climateDataFile = ClimateDataFile()
        self.assertRaises(TypeError, climateDataFile.decimalStringToHexString, 1.0, 1.0)


    def testHexStringToDecimalString(self):
        climateDataFile = ClimateDataFile()
        self.assertRaises(TypeError, climateDataFile.hexStringToDecimalString, 123)
        self.assertRaises(ValueError, climateDataFile.hexStringToDecimalString, "0xAA1RR")


    def testGetDates(self):
        climateDataFile = ClimateDataFile()
        climateDataFile.load(os.path.join(base_dir, "shortvalid.json"),
                             os.path.join(base_dir, "shortvalid.bin"))
        self.assertEqual(["01/01/1990", "01/02/1990", "01/03/1990", "01/04/1990"], climateDataFile.getDates())

    # Test nodeid.py stuff
    def testNodeIDToLatLong(self):
        self.assertRaises(ValueError, nodeIDToLatLong, "abc", self.validResolution) # NodeID must be int or string of int
        self.assertRaises(ValueError, nodeIDToLatLong, "5.0", self.validResolution) # NodeID must be int or string of int

        latitude, longitude = nodeIDToLatLong(self.validNodeID, self.validResolution)
        self.assertEqual(latitude, self.validLatitude)
        self.assertEqual(longitude, self.validLongitude)

        latitude, longitude = nodeIDToLatLong(str(self.validNodeID), self.validResolution)
        self.assertEqual(latitude, self.validLatitude)
        self.assertEqual(longitude, self.validLongitude)


    def testLatLongToNodeID(self):
        self.assertRaises(ValueError, latLongToNodeID, "abc", self.validLongitude, self.validResolution)
        self.assertRaises(ValueError, latLongToNodeID, self.validLatitude, "abc", self.validResolution)

        self.assertEqual(self.validNodeID, latLongToNodeID(self.validLatitude, self.validLongitude, self.validResolution))


    def testGetParsedResolution(self):
        self.assertRaises(ValueError, getParsedResolution, "2.5") # Too few parts
        self.assertRaises(ValueError, getParsedResolution, "a 2.5 arcmin") # Too many parts
        self.assertRaises(ValueError, getParsedResolution, "2.a arcmin") # Value must be integer or float
        self.assertRaises(ValueError, getParsedResolution, "2.5 arcminute") # Type must be degree, arcmin, or arcsec

        self.assertEqual(2.5, getParsedResolution("2.5 degree"))
        self.assertEqual(2.5 / 60, getParsedResolution("2.5 arcmin"))
        self.assertEqual(2.5 / 3600, getParsedResolution("2.5 arcsec"))
        self.assertEqual(2.0 / 60, getParsedResolution("2 arcmin"))


    def testNodeIDToLatLongToNodeID(self):
        latitude, longitude = nodeIDToLatLong(self.validNodeID, self.validResolution)
        nodeID = latLongToNodeID(latitude, longitude, self.validResolution)
        self.assertEqual(nodeID, self.validNodeID)



if __name__ == '__main__':
    unittest.main()
