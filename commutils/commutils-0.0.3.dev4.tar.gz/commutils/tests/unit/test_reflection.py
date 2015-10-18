#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils import reflection

class TestReflection(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_get_script_name(self):
        return
        reflection.get_script_name(__file__)


    def test_get_script_location(self):
        return
        reflection.get_script_location(__file__)


    def test_echo_methods(self):
        return
        reflection.echo_methods(self)


    def test_echo_attributes(self):
        return
        reflection.echo_attributes(self)



if __name__ == '__main__':
    unittest.main()



