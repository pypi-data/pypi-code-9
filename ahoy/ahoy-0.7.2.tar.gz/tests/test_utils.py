from __future__ import print_function, division
import numpy as np
from ahoy.utils import utils
import test


class TestAngleDensity(test.TestBase):

    def test_angle_density(self):
        ths = np.zeros([1000])
        dth = 0.1
        densities, th_bins = utils.angle_density(ths, dth)
        dth = th_bins[1] - th_bins[0]
        self.assertTrue(np.allclose((densities * dth).sum(), 1.0))
