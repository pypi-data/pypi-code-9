"""
distutilazy.test
-----------------

command classes to help run tests

:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import os
from os.path import abspath, basename, dirname
import sys
import fnmatch
from importlib import import_module
import unittest
from distutils.core import Command
from types import ModuleType

__version__ = "0.3.0"


def test_suite_for_modules(modules):
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader
    for module in modules:
        module_tests = test_loader.loadTestsFromModule(module)
        suite.addTests(module_tests)
    return suite


class RunTests(Command):
    description = """Run test suite"""
    user_options = [("root=", "r", "path to tests suite dir"),
                    ("pattern=", "p", "test file name pattern"),
                    ("verbosity=", "v", "verbosity level [1,2,3]"),
                    ("files=", None,
                     "run specified test files (comma separated)")]

    def initialize_options(self):
        self.root = os.path.join(os.getcwd(), 'tests')
        self.pattern = "test*.py"
        self.verbosity = 1
        self.files = None

    def finalize_options(self):
        if not os.path.exists(self.root):
            raise IOError("Failed to access root path '{}'".format(self.root))
        verbosity = min(int(self.verbosity), 3)
        if verbosity < 1:
            self.verbosity = 1
        else:
            self.verbosity = verbosity
        if self.files:
            self.files = map(lambda name: name.strip(), self.files.split(','))

    def get_modules_from_files(self, files):
        modules = []
        for file_name in files:
            directory = dirname(file_name)
            package_name = self._import_dir_as_package(directory)
            if not package_name:
                sys.path.insert(0, directory)
            module_name, _, extension = basename(file_name).rpartition('.')
            if not module_name:
                self.announce(
                    "failed to find module name from filename '{}'." +
                    "skipping this file".format(file_name))
                continue
            if package_name:
                module_name = '.' + module_name
            self.announce(
                "importing module '{}' from file '{}' ...".format(module_name,
                                                                  file_name))
            module = import_module(module_name, package=package_name)
            modules.append(module)
        return modules

    def _import_dir_as_package(self, directory, ensure=False):
        package_name = basename(directory)
        abs_dir = abspath(directory)
        if package_name:
            try:
                self.announce(
                    "importing '{0}' as package ...".format(package_name))
                package = import_module(package_name)
                if ensure and hasattr(package, '__path__') and \
                            abspath(package.__path__[0]) != abs_dir:
                    raise ImportError(
                        "directory '{}' is not a package to import".format(
                            abs_dir))
            except ImportError as err:
                self.announce(
                    "failed to import '{}'. {}".format(package_name, err))
                package_name = None
        return package_name

    def find_test_modules_from_package_path(self, package_path):
        """Import and return modules from package __all__,
        if path is found to be a package.
        """
        package_dir = dirname(package_path)
        package_name = basename(package_path)
        if package_dir:
            sys.path.insert(0, package_dir)
        try:
            self.announce(
                "importing package '{}' ...".format(package_name)
            )
            package = import_module(package_name)
            if package and hasattr(package, '__all__'):
                modules = []
                for module_name in package.__all__:
                    module = import_module('{}.{}'.format(
                        package_name, module_name))
                    if type(module) == ModuleType \
                            and module not in modules:
                        modules.append(module)
                return modules
        except ImportError as err:
            self.announce(
                "failed to import '{}'. not a package. {}".format(
                    package_name, err))
        return []

    def find_test_modules_from_test_files(self, root, pattern):
        """Return list of test modules from the the files in the path
        whose name match the pattern
        """
        modules = []
        abs_root = abspath(root)
        for (dir_path, directories, file_names) in os.walk(abs_root):
            package_name = self._import_dir_as_package(dir_path)
            if not package_name:
                sys.path.insert(0, dir_path)
            for filename in fnmatch.filter(file_names, pattern):
                module_name, _, extension = basename(filename).rpartition('.')
                if not module_name:
                    self.announce(
                        "failed to find module name from filename '{}'." +
                        "skipping this test".format(filename))
                    continue
                if package_name:
                    module_name = '.' + module_name
                self.announce(
                    "importing module '{}' from '{}' ...".format(
                        module_name, filename
                    )
                )
                try:
                    module = import_module(module_name, package_name)
                    if type(module) == ModuleType and module not in modules:
                        modules.append(module)
                except (ImportError, ValueError, SystemError) as ex:
                    self.announce(
                        "failed to import '{}' from '{}'. {}." +
                        "skipping this file!".format(module_name, filename, ex)
                    )
        return modules

    def get_test_runner(self):
        return unittest.TextTestRunner(verbosity=self.verbosity)

    def run(self):
        if self.files:
            modules = self.get_modules_from_files(self.files)
        else:
            self.announce("searching for test package modules ...")
            modules = self.find_test_modules_from_package_path(self.root)
            if not modules:
                self.announce("searching for test files ...")
                modules = self.find_test_modules_from_test_files(self.root,
                                                                 self.pattern)
        if not modules:
            self.announce("found no test files")
            return False
        suite = test_suite_for_modules(modules)
        runner = self.get_test_runner()
        self.announce("running tests ...")
        runner.run(suite)

run_tests = RunTests
