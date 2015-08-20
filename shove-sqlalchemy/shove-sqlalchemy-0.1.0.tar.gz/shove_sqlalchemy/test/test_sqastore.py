# -*- coding: utf-8 -*-
'''shove store tests'''

from stuf.six import unittest
from shove.test.test_store import Store


class TestDBStore(Store, unittest.TestCase):

    initstring = 'sqlite://'