#!/usr/bin/env python

import unittest
import TestBooleanLogic
import TestComparisonOps
import TestConstructors

class BitArray2DTestCase( unittest.TestCase ):
    def checkVersion(self):
        import BitArray2D


testSuites = [unittest.makeSuite(BitArray2DTestCase, 'check')] 

for test_type in [
            TestConstructors,
            TestBooleanLogic,
            TestComparisonOps,
    ]:
    testSuites.append(test_type.getTestSuites('check'))

def getTestDirectory():
    try:
        return os.path.abspath(os.path.dirname(__file__))
    except:
        return '.'

import os

os.chdir(getTestDirectory())

runner = unittest.TextTestRunner()
runner.run(unittest.TestSuite(testSuites))

