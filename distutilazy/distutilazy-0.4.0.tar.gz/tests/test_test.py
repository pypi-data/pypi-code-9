"""
distutilazy.tests.test_test
----------------------------

Tests for distutilazy.test module

:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import sys
from os.path import dirname, basename
from distutils.dist import Distribution
from unittest import TestCase, TestSuite, main

here = dirname(__file__)
sys.path.insert(0, dirname(here))
sys.path.insert(0, here)

from distutilazy.test import RunTests, test_suite_for_modules

__file__ = basename(__file__[:-1] if __file__.endswith('.pyc') else __file__)


def get_module_names(modules):
    return map(lambda m: m.__name__, modules)


class TestTest(TestCase):

    def test_find_modules_from_package_path(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        modules = test_runner.find_test_modules_from_package_path(here)
        self.assertIn('tests.test_test', get_module_names(modules))

    def test_get_modules_from_files(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        self.assertEqual(
            [], test_runner.get_modules_from_files(['none_existing_file']))
        modules = test_runner.get_modules_from_files([__file__])
        self.assertEqual(1, len(modules))
        self.assertEqual('test_test', modules.pop().__name__)

    def test_find_test_modules_from_test_files(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        modules = test_runner.find_test_modules_from_test_files(
            here, 'none_exiting_pattern')
        self.assertEqual([], modules)
        modules = test_runner.find_test_modules_from_test_files(here, __file__)
        self.assertEqual(1, len(modules))
        self.assertEqual('tests.test_test', modules.pop().__name__)
        modules = test_runner.find_test_modules_from_test_files(here, 'test_*')
        module_names = get_module_names(modules)
        self.assertIn('tests.test_test', module_names)
        self.assertIn('test_subdir', module_names)

    def test_test_suite_for_modules(self):
        self.assertIsInstance(test_suite_for_modules([]), TestSuite)

    def test_get_test_runner(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        runner = test_runner.get_test_runner()
        self.assertTrue(hasattr(runner, 'run'))
        self.assertTrue(hasattr(runner.run, '__call__'))

if __name__ == '__main__':
    main()
