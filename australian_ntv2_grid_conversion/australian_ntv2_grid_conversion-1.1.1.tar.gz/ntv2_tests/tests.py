# Path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
import random
import math
from australian_ntv2_grid_conversion import australian_ntv2_grid_conversion as angv
from ntv2_tests.known_values import KnownValues


class TestKnownValues(unittest.TestCase):
    ntv2 = angv.Ntv2()
    # Set the number of points to test when generating random values
    points_to_test = 10000
    # Bounds for latitude and longitude when generating data points
    min_lat = -48.15
    max_lat = -8.55
    min_lon = 104
    max_lon = 164
    # GDAit seems to do something strange with calculating the accuracies so as long as we are within 5 millimetres I assume all is good
    # the extra 0.0000001 is to allow for floating point errors
    gdait_accuracy = 0.0500001

    # GDAy rounds the accuracy values up to the nearest 5 millimetre value, so it is easy to test against
    @staticmethod
    def gday_acc_precision(val):
        # precision of accuracy values in millimetres (GDAy rounds the accuracy values up to the next 5mm)
        acc_precision = 5
        # adjust precision of accuracies
        return (acc_precision / 100.0) * math.ceil((100 / acc_precision) * val)

    @staticmethod
    def gdait_acc_precision(val):
        # precision of accuracy values in millimetres (GDAy rounds the accuracy values up to the next 5mm)
        acc_precision = 5
        # adjust precision of accuracies
        # return (acc_precision / 100) * math.ceil((100 / acc_precision) * val)
        return (acc_precision / 100.0) * math.ceil((100 / acc_precision) * round(val, 4))

    def test_agd66_to_gda94_conversion_gdait(self):
        """ Test the conversion from AGD66 to GDA94.

            Compares with conversion data from GDAit
            Latitudes and Longitudes should be accurate to at least 9 decimal places
            Latitude and Longitude transformation accuracies should be within self.gdait_accuracy mm
        """
        for p_agd in KnownValues.gdait_agd66_to_gda94:
            p_gda = self.ntv2.latlon_to_latlon(p_agd['agd66'][0], p_agd['agd66'][1], 'agd66', 'gda94')
            self.assertAlmostEqual(p_gda['latitude'], p_agd['gda94'][0], 9)
            self.assertAlmostEqual(p_gda['longitude'], p_agd['gda94'][1], 9)
            if isinstance(p_agd['acc'][0], str):
                self.assertTrue(isinstance(p_gda['lat_trans_acc'], str))
                self.assertTrue(isinstance(p_gda['lon_trans_acc'], str))
            else:
                self.assertAlmostEqual(self.gdait_acc_precision(p_gda['lat_trans_acc']), p_agd['acc'][0], delta=self.gdait_accuracy)
                self.assertAlmostEqual(self.gdait_acc_precision(p_gda['lon_trans_acc']), p_agd['acc'][1], delta=self.gdait_accuracy)

    def test_agd84_to_gda94_conversion_gdait(self):
        """ Test the conversion from AGD84 to GDA94.

            Compares with conversion data from GDAit
            Latitudes and Longitudes should be accurate to at least 9 decimal places
            Latitude and Longitude transformation accuracies should be within self.gdait_accuracy mm
        """
        for p_agd in KnownValues.gday_agd84_to_gda94:
            p_gda = self.ntv2.latlon_to_latlon(p_agd['agd84'][0], p_agd['agd84'][1],'agd84', 'gda94')
            self.assertAlmostEqual(p_gda['latitude'], p_agd['gda94'][0], 9)
            self.assertAlmostEqual(p_gda['longitude'], p_agd['gda94'][1], 9)
            if isinstance(p_agd['acc'][0], str):
                self.assertTrue(isinstance(p_gda['lat_trans_acc'], str))
                self.assertTrue(isinstance(p_gda['lon_trans_acc'], str))
            else:
                self.assertAlmostEqual(self.gdait_acc_precision(p_gda['lat_trans_acc']), p_agd['acc'][0], delta=self.gdait_accuracy)
                self.assertAlmostEqual(self.gdait_acc_precision(p_gda['lon_trans_acc']), p_agd['acc'][1], delta=self.gdait_accuracy)

    def test_agd66_to_gda94_conversion_gday(self):
        """ Test the conversion from AGD66 to GDA94.

            Compares with conversion data from GDAy
            Latitudes and Longitudes should be accurate to at least 9 decimal places
            Latitude and Longitude transformation accuracies should be accurate to at least 3 decimal places
        """
        for p_agd in KnownValues.gday_agd66_to_gda94:
            p_gda = self.ntv2.latlon_to_latlon(p_agd['agd66'][0], p_agd['agd66'][1], 'agd66', 'gda94')
            self.assertAlmostEqual(p_gda['latitude'], p_agd['gda94'][0], 9)
            self.assertAlmostEqual(p_gda['longitude'], p_agd['gda94'][1], 9)
            if isinstance(p_agd['acc'][0], str):
                self.assertTrue(isinstance(p_gda['lat_trans_acc'], str))
                self.assertTrue(isinstance(p_gda['lon_trans_acc'], str))
            else:
                self.assertAlmostEqual(self.gday_acc_precision(p_gda['lat_trans_acc']), p_agd['acc'][0], 3)
                self.assertAlmostEqual(self.gday_acc_precision(p_gda['lon_trans_acc']), p_agd['acc'][1], 3)

    def test_agd84_to_gda94_conversion_gday(self):
        """ Test the conversion from AGD84 to GDA94.

            Compares with conversion data from GDAy
            Latitudes and Longitudes should be accurate to at least 9 decimal places
            Latitude and Longitude transformation accuracies should be accurate to at least 3 decimal places
        """
        for p_agd in KnownValues.gday_agd84_to_gda94:
            p_gda = self.ntv2.latlon_to_latlon(p_agd['agd84'][0], p_agd['agd84'][1], 'agd84', 'gda94')
            self.assertAlmostEqual(p_gda['latitude'], p_agd['gda94'][0], 9)
            self.assertAlmostEqual(p_gda['longitude'], p_agd['gda94'][1], 9)
            if isinstance(p_agd['acc'][0], str):
                self.assertTrue(isinstance(p_gda['lat_trans_acc'], str))
                self.assertTrue(isinstance(p_gda['lon_trans_acc'], str))
            else:
                self.assertAlmostEqual(self.gday_acc_precision(p_gda['lat_trans_acc']), p_agd['acc'][0], 3)
                self.assertAlmostEqual(self.gday_acc_precision(p_gda['lon_trans_acc']), p_agd['acc'][1], 3)

    def test_agd66_to_gda94_to_agd66(self):
        """ Test the conversion from GDA94 back to AGD66 by starting in AGD66, converting to GDA94, then converting back to AGD66
            We should end up back at the same place.

            Latitudes and longitudes should be accurate to at least 9 decimal places
            Latitude and longitude transformation accuracies should be accurate to at least 9 decimal places
        """
        for j in range(0, self.points_to_test, 1):
            valid_agd66_point = False
            while valid_agd66_point is False:
                lat = random.uniform(self.min_lat, self.max_lat)
                lon = random.uniform(self.min_lon, self.max_lon)
                try:
                    gda94_pt = self.ntv2.latlon_to_latlon(lat, lon, 'agd66', 'gda94')
                    agd66_pt = self.ntv2.latlon_to_latlon(gda94_pt['latitude'], gda94_pt['longitude'], 'gda94', 'agd66')
                except ValueError:
                    continue
                else:
                    self.assertAlmostEqual(lat, agd66_pt['latitude'], 9)
                    self.assertAlmostEqual(lon, agd66_pt['longitude'], 9)
                    self.assertAlmostEqual(gda94_pt['lat_trans_acc'], agd66_pt['lat_trans_acc'], 9)
                    self.assertAlmostEqual(gda94_pt['lon_trans_acc'], agd66_pt['lon_trans_acc'], 9)
                    valid_agd66_point = True

    def test_agd84_to_gda94_to_agd84(self):
        """ Test the conversion from GDA94 back to AGD66 by starting in AGD66, converting to GDA94, then converting back to AGD66
            We should end up back at the same place.

            Latitudes and longitudes should be accurate to at least 9 decimal places
            Latitude and longitude transformation accuracies should be accurate to at least 9 decimal places
        """
        for j in range(0, self.points_to_test, 1):
            valid_agd84_point = False
            while valid_agd84_point is False:
                lat = random.uniform(self.min_lat, self.max_lat)
                lon = random.uniform(self.min_lon, self.max_lon)
                try:
                    gda94_pt = self.ntv2.latlon_to_latlon(lat, lon, 'agd84', 'gda94')
                    agd84_pt = self.ntv2.latlon_to_latlon(gda94_pt['latitude'], gda94_pt['longitude'], 'gda94', 'agd84')
                except ValueError:
                    continue
                else:
                    self.assertAlmostEqual(lat, agd84_pt['latitude'], 9)
                    self.assertAlmostEqual(lon, agd84_pt['longitude'], 9)
                    self.assertAlmostEqual(gda94_pt['lat_trans_acc'], agd84_pt['lat_trans_acc'], 9)
                    self.assertAlmostEqual(gda94_pt['lon_trans_acc'], agd84_pt['lon_trans_acc'], 9)
                    valid_agd84_point = True

if __name__ == '__main__':
    unittest.main()
