#!/usr/bin/env python
# Copyright (C) 2015 Canonical
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Test tracing -- know what your tests execute.

This module implements a custom subclass of unittests ``TestResult`` that can
be used to trace the code that was referenced by particular test. This allows
to create interesting heuristics. In general this allows one to know which
tests exercise each particular line of python code.

This can be used as a base to build a "live" re-tester that uses this as
heuristics to re-run only a small subset of tests that actually check the part
of code being modified.
"""

from __future__ import absolute_import, print_function, unicode_literals

import collections
import sys
import unittest

__all__ = ('TracingTestResult', 'CodeLocation')


def trace(frame, event, arg):
    """
    Demo function that can be set as the trace callback.

    This function is only meant for developers, to see how python tracing
    operates.  See the :func:`sys.settrace()` for details.
    """
    if event == 'call':
        # If a function is being called keep tracing execution
        # inside the function but do that only for things not
        # in the standard library.
        # Skip anything in standard library
        if not frame.f_code.co_filename.startswith(sys.prefix):
            print("TRACE: frame:{frame} event:{event} arg:{arg}".format(
                frame=frame, event=event, arg=arg))
            return trace
        else:
            return
    elif event == 'line':
        # Print the instruction offset for each line of the function
        print("TRACE: location: {file}:{line} {name}()".format(
            file=frame.f_code.co_filename,
            line=frame.f_lineno,
            name=frame.f_code.co_name))


#: A named tuple with three components
# filename:
#   Filename of a python file
# lineno:
#   Line number within that file
# name:
#   Name of the function/method being executed there
CodeLocation = collections.namedtuple("CodeLocation", "filename lineno name")


class TracingTestResult(unittest.TestResult):

    """
    A tracing test result class.

    This TestResult subclass traces execution to know which lines were executed
    by a particular test. The collected data is collected inside the result as
    two attributes ``_location_to_tests`` and ``_test_to_locations``. Both of
    them are dictionaries of sets that make use of the :class:`CodeLocation`
    tuple. Tests are represented by standard `TestCase` objects.
    """

    def __init__(self, stream=None, descriptions=None, verbosity=None,
                 trace_details=False):
        """
        Initialize a new TracingTestResult.

        :param stream:
            Same as for :class:`unittest.TestResult`
        :param description:
            Same as for :class:`unittest.TestResult`
        :param verbosity:
            Same as for :class:`unittest.TestResult`
        :param trace_details:
            (optional) If True, will cause the trace to contain additional
            per-line details. By default only function-granularity is
            collected. Detailed traces use more memory.
        """
        super(TracingTestResult, self).__init__(
            stream, descriptions, verbosity)
        self._location_to_tests = collections.defaultdict(set)
        self._test_to_locations = collections.defaultdict(set)
        self._current_test = None
        self._trace_details = trace_details

    def startTest(self, test):
        """Start test execution (overridden to collect trace data)."""
        super(TracingTestResult, self).startTest(test)
        # print("Starting test: {test}".format(test=test))
        self._current_test = test
        sys.settrace(self._trace)

    def stopTest(self, test):
        """Stop test execution (overridden to collect trace data)."""
        sys.settrace(None)
        super(TracingTestResult, self).stopTest(test)
        # print("Stopped test: {test}".format(test=test))
        self._current_test = None

    def _trace(self, frame, event, arg):
        # Skip stuff that happens in standard library
        if frame.f_code.co_filename.startswith(sys.prefix):
            return
        if event == 'call':
            self._associate_with_location(frame)
            # If requested, trace with per-line precision
            if self._trace_details:
                return self._trace
        elif event == 'line':
            self._associate_with_location(frame)

    def _associate_with_location(self, frame):
        location = CodeLocation(
            frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name)
        # Associate the location with the current test
        self._location_to_tests[location].add(self._current_test.id())
        self._test_to_locations[self._current_test.id()].add(location)
