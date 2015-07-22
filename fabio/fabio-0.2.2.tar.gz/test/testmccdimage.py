#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch
28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest
import sys
import os
import numpy

try:
    from .utilstest import UtilsTest
except (ValueError, SystemError):
    from utilstest import UtilsTest

logger = UtilsTest.get_logger(__file__)
fabio = sys.modules["fabio"]
from fabio.tifimage import tifimage
from fabio.marccdimage import marccdimage

# statistics come from fit2d I think
# filename dim1 dim2 min max mean stddev
TESTIMAGES = """corkcont2_H_0089.mccd      2048 2048  0  354    7.2611 14.639
                corkcont2_H_0089.mccd.bz2  2048 2048  0  354    7.2611 14.639
                corkcont2_H_0089.mccd.gz   2048 2048  0  354    7.2611 14.639
                somedata_0001.mccd         1024 1024  0  20721  128.37 136.23
                somedata_0001.mccd.bz2     1024 1024  0  20721  128.37 136.23
                somedata_0001.mccd.gz      1024 1024  0  20721  128.37 136.23"""


class TestNormalTiffOK(unittest.TestCase):
    """
    check we can read normal tifs as well as mccd
    """

    def setUp(self):
        """
        create an image 
        """
        self.image = os.path.join(UtilsTest.tempdir, "tifimagewrite_test0000.tif")
        self.imdata = numpy.zeros((24, 24), numpy.uint16)
        self.imdata[12:14, 15:17] = 42
        obj = tifimage(self.imdata, {})
        obj.write(self.image)

    def test_read_openimage(self):
        from fabio.openimage import openimage
        obj = openimage(self.image)
        if obj.data.astype(int).tostring() != self.imdata.astype(int).tostring():
            logger.info("%s %s" % (type(self.imdata), self.imdata.dtype))
            logger.info("%s %s" % (type(obj.data), obj.data.dtype))
            logger.info("%s %s" % (obj.data - self.imdata))
        self.assertEqual(obj.data.astype(int).tostring(),
                          self.imdata.astype(int).tostring())

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        os.unlink(self.image)


class TestFlatMccds(unittest.TestCase):
    def setUp(self):
        self.fn = {}
        for i in ["corkcont2_H_0089.mccd", "somedata_0001.mccd"]:
            self.fn[i] = UtilsTest.getimage(i + ".bz2")[:-4]
            self.fn[i + ".bz2"] = self.fn[i] + ".bz2"
            self.fn[i + ".gz"] = self.fn[i] + ".gz"
        for i in self.fn:
            assert os.path.exists(self.fn[i])

    def test_read(self):
        """ check we can read MarCCD images"""
        for line in TESTIMAGES.split("\n"):
            vals = line.split()
            name = vals[0]
            dim1, dim2 = [int(x) for x in vals[1:3]]
            mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
            obj = marccdimage()
            obj.read(self.fn[name])
            self.assertAlmostEqual(mini, obj.getmin(), 2, "getmin")
            self.assertAlmostEqual(maxi, obj.getmax(), 2, "getmax")
            self.assertAlmostEqual(mean, obj.getmean(), 2, "getmean")
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, "getstddev")
            self.assertEqual(dim1, obj.dim1, "dim1")
            self.assertEqual(dim2, obj.dim2, "dim2")


def test_suite_all_mccd():
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestNormalTiffOK("test_read_openimage"))
    testSuite.addTest(TestFlatMccds("test_read"))
    return testSuite

if __name__ == '__main__':
    mysuite = test_suite_all_mccd()
    runner = unittest.TextTestRunner()
    runner.run(mysuite)
