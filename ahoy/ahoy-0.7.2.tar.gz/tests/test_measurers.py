from __future__ import print_function, division
import numpy as np
from ahoy import stime, directions, c_measurers, dc_dx_measurers
import test


class TestLinearSpatialDcDxMeasurer(test.TestBase):

    def setUp(self):
        super(TestLinearSpatialDcDxMeasurer, self).setUp()

    def run_nd(self, dim, u_0, dc_dxs_expected):
        ds = directions.directions_nd(u_0)
        grad_c_measurer = c_measurers.ConstantGradCMeasurer(self.n, dim)
        dc_dx_measurer = dc_dx_measurers.SpatialDcDxMeasurer(ds,
                                                             grad_c_measurer)
        dc_dxs = dc_dx_measurer.get_dc_dxs()
        self.assertTrue(np.allclose(dc_dxs, dc_dxs_expected))

    def run_parallel_nd(self, dim):
        u_0 = np.zeros([self.n, dim])
        u_0[:, 0] = 1.0
        self.run_nd(dim, u_0, 1.0)

    def run_antiparallel_nd(self, dim):
        u_0 = np.zeros([self.n, dim])
        u_0[:, 0] = -1.0
        self.run_nd(dim, u_0, -1.0)

    def run_perp_nd(self, dim):
        u_0 = np.zeros([self.n, dim])
        u_0[:, 1] = -1.0
        self.run_nd(dim, u_0, 0.0)

    def test_parallel_2d(self):
        self.run_parallel_nd(2)

    def test_parallel_1d(self):
        self.run_parallel_nd(1)

    def test_antiparallel_2d(self):
        self.run_antiparallel_nd(2)

    def test_antiparallel_1d(self):
        self.run_antiparallel_nd(1)

    def test_perp_2d(self):
        self.run_perp_nd(2)


class MockPositions(object):
    def __init__(self, dim, n, v_0, u_0):
        self.r = np.zeros([n, dim])
        self.v_0 = v_0
        self.u_0 = u_0

    def iterate(self, dt):
        self.r += self.v_0 * self.u_0 * dt

    @property
    def dr(self):
        return self.r


class TestLinearTemporalDcDxMeasurer(TestLinearSpatialDcDxMeasurer):

    def setUp(self):
        super(TestLinearTemporalDcDxMeasurer, self).setUp()
        self.v_0 = 2.2
        self.dt = 0.01
        self.dt_mem = 0.05
        self.t_mem = 5.0
        self.t_rot_0 = 1.0

    def run_nd(self, dim, u_0, dc_dxs_expected):
        time = stime.Time()
        ps = MockPositions(dim, self.n, self.v_0, u_0)
        c_measurer = c_measurers.LinearCMeasurer(ps)
        dc_dx_measurer = dc_dx_measurers.TemporalDcDxMeasurer(c_measurer,
                                                              self.v_0,
                                                              self.dt_mem,
                                                              self.t_mem,
                                                              self.t_rot_0,
                                                              time)
        while time.t < 2.0 * self.t_mem:
            ps.iterate(self.dt)
            dc_dxs = dc_dx_measurer.get_dc_dxs()
            time.iterate(self.dt)
        self.assertTrue(np.allclose(dc_dxs, dc_dxs_expected))
