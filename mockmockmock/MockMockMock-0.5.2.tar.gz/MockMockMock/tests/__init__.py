# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import AllTests


def run():
    testLoader = unittest.loader.TestLoader()
    testRunner = unittest.runner.TextTestRunner(verbosity=1)
    test = testLoader.loadTestsFromModule(AllTests)
    return testRunner.run(test)
