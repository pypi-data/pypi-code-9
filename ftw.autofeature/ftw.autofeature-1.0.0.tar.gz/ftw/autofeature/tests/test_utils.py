from ftw.autofeature.utils import all_packages_installed
from ftw.autofeature.utils import combine_features
from ftw.autofeature.utils import find_extras_by_package
from ftw.autofeature.utils import find_package_by_module
from unittest2 import TestCase


class TestFindPackageByModule(TestCase):

    def test_finds_package_by_a_submodule(self):
        import ftw.autofeature.tests.test_utils
        self.assertEquals(
            u'ftw.autofeature',
            find_package_by_module(ftw.autofeature.tests.test_utils))

    def test_finds_package_by_main_module(self):
        import ftw.autofeature
        self.assertEquals(
            u'ftw.autofeature',
            find_package_by_module(ftw.autofeature))

    def test_returns_None_when_package_not_found(self):
        import os.path
        self.assertEquals(
            None,
            find_package_by_module(os.path))


class TestGetExtrasByPackage(TestCase):

    def test_returns_a_dict_with_extras(self):
        extras = find_extras_by_package(u'ftw.autofeature')
        self.assertEquals(dict, type(extras),
                          'Excpected find_extras_by_package result to be a dict.' )

        self.assertIn(u'tests', extras,
                      'Expected key "tests" to be in ftw.autofeature\'s extras.')

    def test_dependencies_are_listed_in_each_extras(self):
        self.assertIn('unittest2',
                      find_extras_by_package(u'ftw.autofeature')['tests'])


class TestAllPackagesInstalled(TestCase):

    def test_all_packages_installed(self):
        self.assertTrue(all_packages_installed(['ftw.autofeature',
                                                'unittest2']))

    def test_not_all_packages_installed(self):
        self.assertFalse(all_packages_installed(['ftw.autofeature',
                                                 'django']))


class TestCombineFeatures(TestCase):

    def test_combine_zero_features(self):
        self.assertEquals([], combine_features([]))

    def test_combine_one_feature(self):
        self.assertEquals(
            ['foo'],
            combine_features(['foo']))

    def test_combine_two_feature(self):
        self.assertItemsEqual(
            ['foo',
             'foo:bar',
             'bar',
             'bar:foo'],
            combine_features(['foo', 'bar']))

    def test_combine_three_feature(self):
        self.assertItemsEqual(
            ['one',
             'one:two',
             'one:two:three',
             'one:three',
             'one:three:two',
             'two',
             'two:one',
             'two:one:three',
             'two:three',
             'two:three:one',
             'three',
             'three:one',
             'three:one:two',
             'three:two',
             'three:two:one'],
            combine_features(['one', 'two', 'three']))
