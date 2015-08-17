# -*- coding: utf-8 -*-
import unittest
import sys
from _m2mdict import m2mdict
from unittest import TestCase

__author__ = 'dengjing'


class BaseTest(TestCase):
    def setUp(self):
        self.d = m2mdict([("img/x-jpeg", "jpg"), ("img/jpeg", "jpg"), ("img/jpeg", "jepg")])

    def runTest(self):
        self.assertEqual(len(self.d), 2)
        self.d.clear()
        self.assertEqual(len(self.d), 0)


class DelTest(TestCase):
    def setUp(self):
        self.d = m2mdict([("img/x-jpeg", "jpg"), ("img/jpeg", "jpg"), ("img/jpeg", "jepg")])

    def runTest(self):
        self.d = ~self.d
        self.assertEqual(len(self.d), 2)


if __name__ == '__main__':
    # unittest.main(argv=[sys.argv[0]])
    # d = m2mdict([("img/x-jpeg", "jpg"), ("img/jpeg", "jpg"), ("img/jpeg", "jepg")])
    # l = list([{'a': 1, 'b': 2}])
    # d.update(l)
    # print d['img/jpeg']
    # print ~d
    # print d.items()
    # print(d)
    # for k, v in d:
    #     print k, v
    # print(d._rawmap)
    # del d["jpg"]
    # print(d._rawmap)
    # print(d.items())
    # print d.items()
    # ~d
    # print((~d).items())

    # print(d.items())
    # ~d
    # d['img/jpeg'] = {'abc', 'sfsd'}
    # print(d.items())
    # ~d
    # print(d.items())
    # print(d.items())
    # print d.keys()

    # del d['img/jpeg']
    # print(d.items())
    # ~d
    # print(d.get('abc'))
    # d.clear()
    # print(d.getdefault('img/x-jpeg'))
    # d.setdefault('img/jepg', 'fdfdd')
    # print(d.getdefault('img/jepg'))
    # ~d
    # print(d.getdefault('fdfdd'))
    unittest.main()