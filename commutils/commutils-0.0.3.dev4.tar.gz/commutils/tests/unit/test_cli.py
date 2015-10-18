#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils import cli

class TestCli(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_subprocess_run(self):
        cli.subprocess_run('ls')


    def test_subprocess_check_run(self):
        cli.subprocess_check_run('ls')



if __name__ == '__main__':
    unittest.main()




