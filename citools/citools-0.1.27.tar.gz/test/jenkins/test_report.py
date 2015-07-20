from unittest import TestCase
from citools.jenkins.report import Report
from assertpy import assert_that


class TestJenkinsReport(TestCase):
    def setUp(self):
        self.report = Report()

    def test_jenkins_report(self):
        assert_that(self.report.fix_url("http://localhost//test")).is_equal_to("http://localhost/test")
