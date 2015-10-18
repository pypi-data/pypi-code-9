#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils import monkey_patch

class TestMonkey_patch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_as_method_of(self):
        return
        monkey_patch.as_method_of(cls)


    def test_as_method_of_cls(self):
        return
        monkey_patch.as_method_of_cls(func)


    def test_as_staticmethod_of(self):
        return
        monkey_patch.as_staticmethod_of(cls)


    def test_as_method_of_cls(self):
        return
        monkey_patch.as_method_of_cls(func)



if __name__ == '__main__':
    unittest.main()



