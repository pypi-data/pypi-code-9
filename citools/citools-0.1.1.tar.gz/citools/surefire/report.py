# coding=utf-8

"""

   Copyright 2015 Andreas Würl

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

from __future__ import print_function

from xml.etree import ElementTree

from .data import TestSuite, TestCase, Failure


class Report(object):
    def parse_report(self, report_file_name):
        with open(report_file_name, 'r') as report_file:
            report_tree = ElementTree.parse(report_file)

        test_suite = report_tree.getroot()

        assert test_suite.tag == 'testsuite'

        kwargs = test_suite.attrib
        kwargs['testcases'] = [self.create_testcase(testcase) for testcase in test_suite.findall('testcase')]
        kwargs['properties'] = dict((property.attrib['name'], property.attrib['value']) for property in
                                test_suite.find('properties').getchildren())

        return TestSuite(**kwargs)

    def create_testcase(self, testcase):
        kwargs = testcase.attrib
        failure = testcase.find('failure')
        children = testcase.getchildren()
        if len(children) > 0:
            print(", ".join([child.tag for child in children]))
        kwargs['failure'] = self.create_failure(failure)
        return TestCase(**kwargs)

    def create_failure(self, failure):
        return Failure(**failure.attrib) if failure is not None else None
