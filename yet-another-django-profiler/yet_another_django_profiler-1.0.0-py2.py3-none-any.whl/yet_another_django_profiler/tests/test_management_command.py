# encoding: utf-8
# Created by Jeremy Bowman on Fri Feb 21 17:28:37 EST 2014
# Copyright (c) 2014, 2015 Safari Books Online. All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-clause BSD license.  See the LICENSE file for details.
"""
Yet Another Django Profiler management command tests
"""

from __future__ import unicode_literals

import platform
import re
import os
import sys
from tempfile import NamedTemporaryFile

from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six.moves import cStringIO as StringIO
from django.utils.text import force_text

import pytest


class ManagementCommandCases(object):

    def test_call_graph(self):
        """Using "profile" without a parameter should yield a PDF call graph"""
        f = NamedTemporaryFile(delete=False)
        f.close()
        output = self._run_command(path=f.name)
        assert 'Wrote call graph to {}'.format(f.name) in output
        assert os.path.getsize(f.name) > 4
        with open(f.name, 'rb') as pdf:
            assert pdf.read(4) == b'%PDF'
        os.unlink(f.name)

    def test_calls_by_count(self):
        """Using "-s calls" should show a table of function calls sorted by call count"""
        output = self._run_command(sort='calls')
        assert 'Ordered by: call count' in output

    def test_calls_by_cumulative(self):
        """Using "-s cumulative" should show a table of function calls sorted by cumulative time"""
        output = self._run_command(sort='cumulative')
        assert 'Ordered by: cumulative time' in output

    def test_calls_by_file_name(self):
        """Using "-s file" should show a table of function calls sorted by file name"""
        output = self._run_command(sort='file')
        assert 'Ordered by: file name' in output

    def test_calls_by_function_name(self):
        """Using "-s name" should show a table of function calls sorted by function name"""
        output = self._run_command(sort='name')
        assert 'Ordered by: function name' in output

    def test_calls_by_function_name_file_and_line(self):
        """Using "-s nfl" should show a table of function calls sorted by function name, file, and line"""
        output = self._run_command(sort='nfl')
        assert 'Ordered by: name/file/line' in output

    def test_calls_by_line_number(self):
        """Using "-s line" should show a table of function calls sorted by line_number"""
        output = self._run_command(sort='line')
        assert 'Ordered by: line number' in output

    def test_calls_by_module(self):
        """Using "-s module" should show a table of function calls sorted by file name"""
        output = self._run_command(sort='module')
        assert 'Ordered by: file name' in output

    def test_calls_by_primitive_call_count(self):
        """Using "-s pcalls" should show a table of function calls sorted by primitive call count"""
        output = self._run_command(sort='pcalls')
        assert re.search(r'Ordered by: (primitive )?call count', force_text(output, 'utf-8'))

    def test_calls_by_stdname(self):
        """Using "-s stdname" should show a table of function calls sorted by standard name"""
        output = self._run_command(sort='stdname')
        assert 'Ordered by: standard name' in output

    def test_calls_by_time(self):
        """Using "-s time" should show a table of function calls sorted by internal time"""
        output = self._run_command(sort='time')
        assert 'Ordered by: internal time' in output

    def test_default_fraction(self):
        """By default, the fraction of displayed function calls should be 0.2"""
        output = self._run_command(sort='time')
        assert 'due to restriction <0.2>' in output

    def test_custom_fraction(self):
        """It should be possible to specify the fraction of displayed function calls"""
        output = self._run_command(sort='time', fraction='0.3')
        assert 'due to restriction <0.3>' in output

    def test_max_calls(self):
        """It should be possible to specify the maximum number of displayed function calls"""
        output = self._run_command(sort='time', max_calls='5')
        assert 'to 5 due to restriction <5>' in output

    def test_pattern(self):
        """It should be possible to specify a regular expression filter pattern"""
        output = self._run_command(sort='time', pattern='test')
        assert re.search(r"due to restriction <u?'test'>", force_text(output, 'utf-8'))

    def _run_command(self, **options):
        """Run the profile command with the given options on the diffsettings command and capture the output"""
        output = StringIO()
        options = options.copy()
        options['backend'] = 'cProfile'
        options['testing'] = True
        for option in ('fraction', 'max_calls', 'path', 'pattern', 'sort'):
            if option not in options:
                options[option] = None
        call_command('profile', 'diffsettings', stdout=output, **options)
        text = output.getvalue()
        assert 'INSTALLED_APPS' in text
        return text


@override_settings(YADP_ENABLED=True)
class CProfileCommandTest(TestCase, ManagementCommandCases):
    """Management command tests using cProfile"""

    def test_backend(self):
        """The cProfile profiling backend should be used"""
        from yet_another_django_profiler.conf import settings
        assert settings.YADP_PROFILER_BACKEND == 'cProfile'


@pytest.mark.skipif(platform.python_implementation() != 'CPython' or sys.version_info[:2] == (3, 2),
                    reason='yappi does not yet work in this Python implementation')
@override_settings(YADP_ENABLED=True, YADP_PROFILER_BACKEND='yappi')
class YappiCommandTest(TestCase, ManagementCommandCases):
    """Management command tests using Yappi instead of cProfile"""

    def test_backend(self):
        """The Yappi profiling backend should be used"""
        from yet_another_django_profiler.conf import settings
        assert settings.YADP_PROFILER_BACKEND == 'yappi'
