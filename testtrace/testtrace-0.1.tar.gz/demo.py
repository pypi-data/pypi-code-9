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
Demonstration code for testtrace feature.

Just run this script and observe the output.
"""

from __future__ import absolute_import, print_function, unicode_literals

from gettext import gettext as _, ngettext
from unittest import TestCase
from unittest import TestLoader
from unittest import TestSuite

from testtrace import TracingTestResult


class AnimalBase:

    """Base class for all animals."""

    SOUND = None

    @classmethod
    def get_sound(cls):
        """Get the sound this class of animals makes."""
        return cls.SOUND


class Dog(AnimalBase):

    """A simple dog class."""

    SOUND = "bark bark"

    def bark(self):
        """Bark as a dog would."""
        return self.get_sound()


class Cat:

    """A simple cat class."""

    SOUND = "meeeow!"

    def meow(self):
        """Meow as a cat would."""
        return self.get_sound()


class DogTests(TestCase):

    """Tests for the Dog class."""

    def test_barking(self):
        """Check if a dog can bark."""
        # This is artificially verbose so that we can see multiple lines being
        # traced by the runtime trace monitor.
        dog = Dog()
        expected = "bark bark"
        actual = dog.bark()
        self.assertEqual(expected, actual)


class CatTests(TestCase):

    """Tests for the Cat class."""

    def test_meowing(self):
        """Check if a cat can meow."""
        cat = Cat()
        expected = "meeeow!"
        actual = cat.meow()
        self.assertEqual(expected, actual)


def main():
    """Main function."""
    loader = TestLoader()
    suite = TestSuite()
    suite._cleanup = False  # we want to see tests after running
    suite.addTests(loader.loadTestsFromTestCase(DogTests))
    suite.addTests(loader.loadTestsFromTestCase(CatTests))
    # NOTE: try with True/False
    result = TracingTestResult(trace_details=False)
    suite.run(result)
    dump_suite(suite, result)


def dump_suite(suite, result):
    """Dump information about a test suite and results."""
    assert isinstance(suite, TestSuite)
    assert isinstance(result, TracingTestResult)
    print(ngettext(
        "There is {0} test",
        "There are {0} tests",
        suite.countTestCases()
    ).format(suite.countTestCases()))
    for index, test in enumerate(suite, 1):
        print("{index}: {id!r}, {test}".format(
            index=index, id=test.id(), test=test))
        print(_("Referenced locations"))
        for location in result._test_to_locations[test.id()]:
            print(" - {0}".format(location))


if __name__ == "__main__":
    main()
