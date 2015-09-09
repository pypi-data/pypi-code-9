import unittest
import numpy as np


class TestBase(unittest.TestCase):
    n = 5
    seed = 1

    def setUp(self):
        self.rng = np.random.RandomState(self.seed)
