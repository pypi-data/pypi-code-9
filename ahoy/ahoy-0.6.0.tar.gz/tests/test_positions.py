from __future__ import print_function, division
import numpy as np
from ahoy import positions
import test


class TestPeriodicPositions1D(test.TestBase):
    dim = 1
    L = np.array([1.7])

    def setUp(self):
        super(TestPeriodicPositions1D, self).setUp()
        self.ps = positions.positions_factory(spatial_flag=True,
                                              periodic_flag=True,
                                              n=self.n, L=self.L,
                                              rng=self.rng)

    def test_wrapping_down(self):
        dr = np.zeros_like(self.ps.r)
        self.ps.r[0, 0] = self.L[0] / 2.0
        dr[0, 0] = 0.9 * self.L[0]
        self.ps.r += np.full(self.ps.r.shape, dr)
        self.assertTrue(np.abs(self.ps.r_w[:, 0]).max() < self.L[0] / 2.0)

    def test_wrapping_up(self):
        dr = np.zeros_like(self.ps.r)
        self.ps.r[-1, 0] = -self.L[0] / 2.0
        dr[-1, 0] = -0.9 * self.L[0]
        self.ps.r += np.full(self.ps.r.shape, dr)
        self.assertTrue(np.abs(self.ps.r_w[:, 0]).max() < self.L[0] / 2.0)


class TestPeriodicPositions2D(TestPeriodicPositions1D):
    dim = 2
    L = np.array([0.5, 1.5])

    def test_wrapping_up(self):
        dr = np.zeros_like(self.ps.r)
        self.ps.r[-1, -1] = -self.L[-1] / 2.0
        dr[-1, -1] = -0.9 * self.L[-1]
        self.ps.r += np.full(self.ps.r.shape, dr)
        self.assertTrue(np.abs(self.ps.r_w[:, -1]).max() < self.L[-1] / 2.0)

    def test_partial_infinite_boundaries(self):
        L = np.array([np.inf, 1.7])
        ps = positions.positions_factory(spatial_flag=True,
                                         periodic_flag=True,
                                         n=self.n, L=L, rng=self.rng)
        dr = self.rng.uniform(-1.0, 1.0, size=ps.r.shape)
        ps.r += dr
        r_naive = ps.r_0[:, 0] + dr[:, 0]
        # Check no wrapping along infinite axis
        self.assertTrue(np.allclose(r_naive, ps.r_w[:, 0]))
        self.assertTrue(np.allclose(r_naive, ps.r[:, 0]))
        # Check done wrapping along finite axis
        self.assertTrue(np.all(np.abs(ps.r_w[:, 1]) < L[1] / 2.0))
