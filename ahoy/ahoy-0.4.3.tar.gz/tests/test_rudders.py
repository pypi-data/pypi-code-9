import numpy as np
from scipy.optimize import curve_fit
from ahoy import directions, rudders, noise_measurers
import test


class TestRotationRudders2D(test.TestBase):
    rudders_cls = rudders.RotationRudders2D
    dim = 2

    def setUp(self):
        super(TestRotationRudders2D, self).setUp()
        self.dt = 0.005
        self.noise_0 = 2.0
        self.t_rot_expect = 1.0 / self.noise_0
        self.noise_measurer = noise_measurers.NoiseMeasurer(self.noise_0)

    def test_rudder_autocorrelation(self):
        n = 10000
        t_max = 0.5

        ds = directions.directions_factory(n, self.dim, aligned_flag=True)
        rudders = self.rudders_cls(self.noise_measurer)

        u_0 = ds.u
        ts = np.arange(0.0, t_max, self.dt)
        mean_dots = []
        for t in ts:
            ds = rudders.rotate(ds, self.dt, self.rng)
            mean_dot = np.mean(np.sum(u_0 * ds.u, axis=-1))
            mean_dots.append(mean_dot)

        def exp(t, t_rot):
            return np.exp(-t / t_rot)

        popt, pcov = curve_fit(exp, ts, mean_dots)
        t_rot_actual = popt[0]
        self.assertAlmostEqual(t_rot_actual, self.t_rot_expect, 1)

    def test_random_seeding(self):
        n = 1000
        num_iterations = 100
        rng_seed = 1

        def get_ds(npy_seed):
            rng = np.random.RandomState(rng_seed)
            np.random.seed(npy_seed)
            ds = directions.directions_factory(n, self.dim, aligned_flag=True)
            ruds = self.rudders_cls(self.noise_measurer)
            for _ in range(num_iterations):
                ds = ruds.rotate(ds, self.dt, rng)
            return ds

        ds_1 = get_ds(2)
        ds_2 = get_ds(3)

        self.assertTrue(np.allclose(ds_1.u, ds_2.u))


class TestTumbleRudders1D(TestRotationRudders2D):
    rudders_cls = rudders.TumbleRudders
    dim = 1

    def test_tumble_rate(self):
        n = 2000
        dt = 1.0
        p = self.rng.uniform(0.0, 1.0, size=n)
        noise_measurer = noise_measurers.NoiseMeasurer(p)

        n_expected = (p * dt).sum()
        # In 1D is a half chance to tumble back to the same direction.
        if self.dim == 1:
            n_expected /= 2.0
        ds = directions.directions_factory(n, self.dim, aligned_flag=False,
                                           rng=self.rng)
        u_0 = ds.u
        ruds = rudders.TumbleRudders(noise_measurer)
        ds_rot = ruds.rotate(ds, dt, self.rng)
        u_change = np.not_equal(u_0, ds_rot.u)
        n_actual = np.any(u_change, axis=-1).sum()
        err = np.abs(n_expected - n_actual) / n_expected
        self.assertTrue(err < 0.05)


class TestTumbleRudders2D(TestTumbleRudders1D):
    dim = 2
