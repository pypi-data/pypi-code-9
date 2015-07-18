# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import sys
import unittest
from vecnet.emod.output.binnedreport import BinnedReport


base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "output")


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_2(self):
        print "Testing file: %s" % os.path.abspath(sys.modules[BinnedReport.__module__].__file__)
        vector_species_report = BinnedReport(os.path.join(base_dir, "2", "VectorSpeciesReport.json"))
        self.assertEqual(vector_species_report.channels, [u'Adult Vectors',
                                                          u'Daily EIR',
                                                          u'Daily HBR',
                                                          u'Infectious Vectors'])
        self.assertEqual(vector_species_report.get_meanings_per_axis("Vector Species"), [u'farauti'])
        self.assertEqual(vector_species_report._get_axis_number("Vector Species"), 0)
        self.assertEqual(sum(vector_species_report.get_data('Adult Vectors', "Vector Species", 'farauti')), 1034462.0)
        self.assertEqual(vector_species_report.axis, ["Vector Species"])
        self.assertRaises(KeyError,
                          vector_species_report.get_data,
                          'Adult Vectors', "Vector Species", 'non-existing species')
        self.assertRaises(KeyError,
                          vector_species_report.get_data,
                          'Adult Vectors', "non-existing axis", 'farauti')
        self.assertIsNone(vector_species_report.get_units(u'Daily EIR'))

    def test_3(self):
        # EMOD v1.8.1 and v2.0.0 output files, single species
        vector_species_report = BinnedReport(os.path.join(base_dir, "3", "VectorSpeciesReport.json"))
        self.assertEqual(vector_species_report.channels, [u'Adult Vectors',
                                                          u'Daily EIR',
                                                          u'Daily HBR',
                                                          u'Infectious Vectors'])
        self.assertEqual(vector_species_report.get_meanings_per_axis("Vector Species"), [u'farauti_low_hbr'])
        self.assertEqual(vector_species_report._get_axis_number("Vector Species"), 0)
        self.assertEqual(sum(vector_species_report.get_data('Adult Vectors', "Vector Species", 'farauti_low_hbr')), 26707021)
        self.assertEqual(vector_species_report.axis, ["Vector Species"])

    def test_4(self):
        # EMOD v1.8.1 output files, multiple species
        vector_species_report = BinnedReport(os.path.join(base_dir, "4", "VectorSpeciesReport.json"))
        self.assertEqual(vector_species_report.channels, [u'Adult Vectors',
                                                          u'Daily EIR',
                                                          u'Daily HBR',
                                                          u'Infectious Vectors'])
        self.assertEqual(vector_species_report.get_meanings_per_axis("Vector Species"),
                         [ u'farauti', u'farauti_high_hbr', u'farauti_low_hbr']
                         )
        self.assertEqual(vector_species_report._get_axis_number("Vector Species"), 0)
        self.assertEqual(sum(vector_species_report.get_data('Adult Vectors', "Vector Species", 'farauti')), 139535)
        self.assertEqual(vector_species_report.axis, ["Vector Species"])

    def test_5(self):
        # EMOD v2.0.0 output files, multiple species
        vector_species_report = BinnedReport(os.path.join(base_dir, "5", "VectorSpeciesReport.json"))
        self.assertEqual(vector_species_report.channels, [u'Adult Vectors',
                                                          u'Daily EIR',
                                                          u'Daily HBR',
                                                          u'Infectious Vectors'])
        self.assertEqual(vector_species_report.get_meanings_per_axis("Vector Species"),
                         [u'arabiensis', u'funestus', u'gambiae']
                         )
        self.assertEqual(vector_species_report._get_axis_number("Vector Species"), 0)
        self.assertEqual(sum(vector_species_report.get_data('Adult Vectors', "Vector Species", 'gambiae')), 2105011)
        self.assertEqual(vector_species_report.axis, ["Vector Species"])