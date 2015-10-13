#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
from pysqldf import load_iris, load_meat, load_births
import string
import unittest
import os


class LoadTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_iris(self):
        iris = load_iris()
        self.assertEqual(len(iris), 150)
        self.assertEqual(
            list(
                iris.columns), [
                "sepal_length", "sepal_width", "petal_length", "petal_width", "species"])

    def test_load_meat(self):
        meat = load_meat()
        self.assertEqual(len(meat), 827)
        self.assertEqual(list(meat.columns),
                         ["date",
                          "beef",
                          "veal",
                          "pork",
                          "lamb_and_mutton",
                          "broilers",
                          "other_chicken",
                          "turkey"])

    def test_load_births(self):
        births = load_births()
        self.assertEqual(len(births), 408)
        self.assertEqual(list(births.columns), ["date", "births"])
