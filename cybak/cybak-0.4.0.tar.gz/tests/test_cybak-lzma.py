#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cybackup
----------------------------------

Tests for `cybackup` module.
"""

import unittest
import tempfile

from cybackup import backuplzma

class ConfigFixture(unittest.TestCase):

    def setUp(self):
        # make a config file object with testable properties
        fil = tempfile.TemporaryFile()
        fil.write('[SECTION1]\ndir1=../\ndir2=~\ndirlist=./zsh_src/,/python')
        
class TestCybackup(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass

class ConfigTests(ConfigFixture):

    def test_configbhv(self):
       pass  

if __name__ == '__main__':
    unittest.main()
