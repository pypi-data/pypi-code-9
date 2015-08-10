from __future__ import print_function, division
import numpy as np
from ahoy import directions, c_measurers, dc_dx_measurers, noise_measurers
import test


class TestChemoNoiseMeasurer1D(test.TestBase):
    dim = 1
    L = np.array([0.7])
    noise_measurer_cls = noise_measurers.ChemoNoiseMeasurer

    def setUp(self):
        super(TestChemoNoiseMeasurer1D, self).setUp()
        self.noise_0 = 1.5
        self.v_0 = 2.2

    def run_valchemo(self, ds, chi, noise_expected):
        grad_c_measurer = c_measurers.ConstantGradCMeasurer(self.n, self.dim)
        dc_dx_measurer = dc_dx_measurers.SpatialDcDxMeasurer(ds,
                                                             grad_c_measurer)
        noise_measurer = self.noise_measurer_cls(self.noise_0, chi,
                                                 dc_dx_measurer)
        noise = noise_measurer.get_noise()
        self.assertTrue(np.allclose(noise, noise_expected))

    def get_ds_parallel(self):
        u_0 = np.zeros([self.n, self.dim])
        u_0[:, 0] = 1.0
        return directions.directions_nd(u_0)

    def get_ds_antiparallel(self):
        u_0 = np.zeros([self.n, self.dim])
        u_0[:, 0] = -1.0
        return directions.directions_nd(u_0)

    def test_parallel_nochemo(self):
        ds = self.get_ds_parallel()
        self.run_valchemo(ds, 0.0, self.noise_0)

    def test_antiparallel_nochemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 0.0, self.noise_0)

    def test_parallel_maxchemo(self):
        ds = self.get_ds_parallel()
        self.run_valchemo(ds, 1.0, 0.0)

    def test_antiparallel_maxchemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 1.0, 2.0 * self.noise_0)

    def test_parallel_halfchemo(self):
        ds = self.get_ds_parallel()
        self.run_valchemo(ds, 0.5, self.noise_0 / 2.0)

    def test_antiparallel_halfchemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 0.5, 1.5 * self.noise_0)


class TestChemoNoiseMeasurer2D(TestChemoNoiseMeasurer1D):
    dim = 2
    L = np.array([0.7, 1.1])

    def get_ds_perp(self):
        u_0 = np.zeros([self.n, self.dim])
        u_0[:, 1] = 1.0
        return directions.directions_nd(u_0)

    def test_perp_nochemo(self):
        ds = self.get_ds_perp()
        self.run_valchemo(ds, 0.0, self.noise_0)

    def test_perp_maxchemo(self):
        ds = self.get_ds_perp()
        self.run_valchemo(ds, 1.0, self.noise_0)

    def test_perp_halfchemo(self):
        ds = self.get_ds_perp()
        self.run_valchemo(ds, 0.5, self.noise_0)


class TestOneSidedChemoNoiseMeasurer1D(TestChemoNoiseMeasurer1D):
    noise_measurer_cls = noise_measurers.OneSidedChemoNoiseMeasurer

    def test_antiparallel_maxchemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 1.0, self.noise_0)

    def test_antiparallel_halfchemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 0.5, self.noise_0)


class TestOneSidedChemoRudderControllers2D(TestChemoNoiseMeasurer2D):
    noise_measurer_cls = noise_measurers.OneSidedChemoNoiseMeasurer

    def test_antiparallel_maxchemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 1.0, self.noise_0)

    def test_antiparallel_halfchemo(self):
        ds = self.get_ds_antiparallel()
        self.run_valchemo(ds, 0.5, self.noise_0)
