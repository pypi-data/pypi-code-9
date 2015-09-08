# -*- coding: utf-8 -*-
'''tests for shove-git'''

from stuf.six import unittest
from shove.test.test_store import PathStore


class TestGitStore(PathStore, unittest.TestCase):

    initstring = 'git://test4'