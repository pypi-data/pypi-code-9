from __future__ import print_function
import glob

import os

import unittest
from assertpy import assert_that

from citools.surefire.report import Report


class TestDependencies(unittest.TestCase):
    def setUp(self):
        self.report = Report()

    def test_parsing_of_dependency_list_output(self):
        report_files = glob.glob(os.path.join(os.path.dirname(__file__), 'surefire-reports', 'TEST-*.xml'))

        reports = [self.report.parse_report(report_file) for report_file in report_files]

        assert_that(reports).is_length(39)
