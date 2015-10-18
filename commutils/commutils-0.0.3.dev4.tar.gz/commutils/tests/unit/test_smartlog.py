#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils import smartlog

class TestSmartlog(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_set_root_logger(self):
        return
        smartlog.set_root_logger(level = logging.INFO, filename=None,filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')


    def test_clear_logger(self):
        return
        smartlog.clear_logger(logger)


    def test_get_logger(self):
        return
        smartlog.get_logger(level = logging.WARNING,logname='mylog', console=True, filename=False,filemode='w')



if __name__ == '__main__':
    unittest.main()



