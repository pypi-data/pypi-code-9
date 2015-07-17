# encoding: utf-8
# Created by Jeremy Bowman on Fri Feb 21 17:28:37 EST 2014
# Copyright (c) 2014, 2015 Safari Books Online. All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-clause BSD license.  See the LICENSE file for details.
"""
Yet Another Django Profiler request parameters tests
"""

from __future__ import unicode_literals

import platform
import sys

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.text import force_text

import pytest

HELP_EXCERPT = 'profiling middleware'


class ParameterCases(object):
    """Parameter tests to be run for each profiler backend"""

    def test_call_graph(self):
        """Using "profile" without a parameter should yield a PDF call graph"""
        response = self._get_test_page('profile')
        assert response['Content-Type'] == 'application/pdf'

    def test_calls_by_count(self):
        """Using profile=calls should show a table of function calls sorted by call count"""
        response = self._get_test_page('profile=calls')
        self.assertContains(response, 'Ordered by: call count')

    def test_calls_by_cumulative(self):
        """Using profile=cumulative should show a table of function calls sorted by cumulative time"""
        response = self._get_test_page('profile=cumulative')
        self.assertContains(response, 'Ordered by: cumulative time')

    def test_calls_by_file_name(self):
        """Using profile=file should show a table of function calls sorted by file name"""
        response = self._get_test_page('profile=file')
        self.assertContains(response, 'Ordered by: file name')

    def test_calls_by_function_name(self):
        """Using profile=name should show a table of function calls sorted by function name"""
        response = self._get_test_page('profile=name')
        self.assertContains(response, 'Ordered by: function name')

    def test_calls_by_function_name_file_and_line(self):
        """Using profile=nfl should show a table of function calls sorted by function name, file, and line"""
        response = self._get_test_page('profile=nfl')
        self.assertContains(response, 'Ordered by: name/file/line')

    def test_calls_by_line_number(self):
        """Using profile=line should show a table of function calls sorted by line_number"""
        response = self._get_test_page('profile=line')
        self.assertContains(response, 'Ordered by: line number')

    def test_calls_by_module(self):
        """Using profile=module should show a table of function calls sorted by file name"""
        response = self._get_test_page('profile=module')
        self.assertContains(response, 'Ordered by: file name')

    def test_calls_by_primitive_call_count(self):
        """Using profile=pcalls should show a table of function calls sorted by primitive call count"""
        response = self._get_test_page('profile=pcalls')
        self.assertRegexpMatches(force_text(response.content, 'utf-8'), r'Ordered by: (primitive )?call count')

    def test_calls_by_stdname(self):
        """Using profile=stdname should show a table of function calls sorted by standard name"""
        response = self._get_test_page('profile=stdname')
        self.assertContains(response, 'Ordered by: standard name')

    def test_calls_by_time(self):
        """Using profile=time should show a table of function calls sorted by internal time"""
        response = self._get_test_page('profile=time')
        self.assertContains(response, 'Ordered by: internal time')

    def test_help(self):
        """Using profile=help should yield usage instructions"""
        response = self._get_test_page('profile=help')
        self.assertContains(response, HELP_EXCERPT)

    def test_default_fraction(self):
        """By default, the fraction of displayed function calls should be 0.2"""
        response = self._get_test_page('profile=time')
        self.assertContains(response, 'due to restriction <0.2>')

    def test_custom_fraction(self):
        """It should be possible to specify the fraction of displayed function calls"""
        response = self._get_test_page('profile=time&fraction=0.3')
        self.assertContains(response, 'due to restriction <0.3>')

    def test_max_calls(self):
        """It should be possible to specify the maximum number of displayed function calls"""
        response = self._get_test_page('profile=time&max_calls=5')
        self.assertContains(response, 'to 5 due to restriction <5>')

    def test_pattern(self):
        """It should be possible to specify a regular expression filter pattern"""
        response = self._get_test_page('profile=time&pattern=test')
        self.assertRegexpMatches(force_text(response.content, 'utf-8'), r"due to restriction <u?'test'>")

    def _get_test_page(self, params=''):
        url = reverse('test')
        if params:
            url += '?' + params
        return self.client.get(url)


@override_settings(YADP_ENABLED=True)
class CProfileTest(TestCase, ParameterCases):
    """Profiling parameter tests using cProfile"""

    def test_backend(self):
        """The cProfile profiling backend should be used"""
        from yet_another_django_profiler.conf import settings
        assert settings.YADP_PROFILER_BACKEND == 'cProfile'


@pytest.mark.skipif(platform.python_implementation() != 'CPython' or sys.version_info[:2] == (3, 2),
                    reason='yappi does not yet work in this Python implementation')
@override_settings(YADP_ENABLED=True, YADP_PROFILER_BACKEND='yappi')
class YappiTest(TestCase, ParameterCases):
    """Profiling parameter tests using Yappi instead of cProfile"""

    def test_backend(self):
        """The Yappi profiling backend should be used"""
        from yet_another_django_profiler.conf import settings
        assert settings.YADP_PROFILER_BACKEND == 'yappi'
