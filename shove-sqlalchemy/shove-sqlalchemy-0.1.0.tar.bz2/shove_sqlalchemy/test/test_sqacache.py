# -*- coding: utf-8 -*-
'''shove sqlalchemy cache tests'''

from stuf.six import unittest
from shove.test.test_cache import CacheCull


class TestDBCache(CacheCull, unittest.TestCase):

    initstring = 'sqlite:///'