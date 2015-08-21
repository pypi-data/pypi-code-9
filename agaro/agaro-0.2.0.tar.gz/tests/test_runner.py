#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
from agaro import runner


class MockModel(object):

    def __init__(self, dt):
        self.dt = dt
        self.t = 0.0
        self.i = 0

    def iterate(self):
        self.t += self.dt
        self.i += 1

    def get_output_dirname(self):
        return 'MockModel'


class RunnerTest(unittest.TestCase):

    def test_runner(self):
        m = MockModel(0.01)
        r = runner.Runner(model=m, force_resume=False)
        r.iterate(n=100, t_output_every=0.1)

if __name__ == '__main__':
    unittest.main()
