# tests for psj.policy doctests (.rst, .txt files)
import unittest
from Testing import ZopeTestCase as ztc
from psj.policy.testing import FunctionalTestCase


def test_suite():
    suite = unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='psj.content',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='psj.content.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='psj.policy',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'README.txt', package='psj.policy',
            test_class=FunctionalTestCase),

        ztc.FunctionalDocFileSuite(
            'README.txt', package='psj.policy.transforms',
             test_class=FunctionalTestCase),

        ])
    return suite
