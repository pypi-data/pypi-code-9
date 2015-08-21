from __future__ import print_function, division
import numpy as np
from ahoy import directions
import test


class TestDirections1D(test.TestBase):
    dim = 1

    def test_properties(self):
        n = 10
        u = np.zeros([n, self.dim])
        u[:, 0] = 1.0
        ds = directions.directions_nd(u)
        self.assertTrue(ds.n == n)
        self.assertTrue(ds.dim == self.dim)

    def test_u_east(self):
        u = np.zeros([self.n, self.dim])
        u[:, 0] = 1.0
        ds = directions.directions_nd(u)
        self.assertTrue(np.allclose(ds.u, u))

    def test_u_west(self):
        u = np.zeros([self.n, self.dim])
        u[:, 0] = -1.0
        ds = directions.directions_nd(u)
        self.assertTrue(np.allclose(ds.u, u))

    def test_tumble_identity(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        tumblers = np.zeros([ds.n], dtype=np.bool)
        ds_rot = ds.tumble(tumblers)
        self.assertTrue(np.allclose(ds.u_0, ds_rot.u))

    def test_tumble_magnitude_conservation(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        mags_0 = np.sum(np.square(ds.u))
        tumblers = self.rng.choice([True, False], size=ds.n)
        ds_rot = ds.tumble(tumblers)
        mags_rot = np.sum(np.square(ds_rot.u))
        self.assertTrue(np.allclose(mags_0, mags_rot))

    def test_tumble_coverage(self):
        n = 2000
        ds = directions.directions_factory(n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        tumblers = np.ones([ds.n], dtype=np.bool)
        ds_rot = ds.tumble(tumblers)
        frac_close = np.isclose(ds.u_0, ds_rot.u).sum() / float(ds.n)
        self.assertAlmostEqual(frac_close, 0.5, 1)


class TestDirections2D(TestDirections1D):
    dim = 2

    def test_u_south(self):
        u = np.zeros([self.n, self.dim])
        u[:, 1] = -1.0
        ds = directions.directions_nd(u)
        self.assertTrue(np.allclose(ds.u, u))

    def test_tumble_coverage(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        tumblers = np.ones([ds.n], dtype=np.bool)
        ds_rot = ds.tumble(tumblers, rng=self.rng)
        self.assertFalse(np.any(np.isclose(ds.u_0, ds_rot.u)))

    def test_rotate_identity(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        dth = np.zeros([ds.n])
        ds_rot = ds.rotate(dth)
        u_rot = ds_rot.u
        self.assertTrue(np.allclose(ds.u_0, u_rot))

    def test_rotate_right_angle(self):
        u_0 = np.zeros([self.n, self.dim])
        u_0[:, 0] = 1.0
        dth = np.full([self.n], np.pi / 2.0)
        ds = directions.directions_nd(u_0)
        ds_rot = ds.rotate(dth)
        u_rot = ds_rot.u
        u_rot_expected = np.zeros([self.n, self.dim])
        u_rot_expected[:, 1] = 1.0
        self.assertTrue(np.allclose(u_rot, u_rot_expected))

    def test_rotate_idempotence(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        dth = self.rng.uniform(-np.pi, np.pi, size=self.n)
        ds_rot = ds.rotate(dth)
        ds_rot = ds_rot.rotate(-dth)
        self.assertTrue(np.allclose(ds.u_0, ds_rot.u))

    def test_rotate_periodicity(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        dth = np.full([ds.n], np.pi / 2.0)
        ds_rot = ds
        for i in range(4):
            ds_rot = ds_rot.rotate(dth)
        self.assertTrue(np.allclose(ds.u_0, ds_rot.u))

    def test_rotate_magnitude_conservation(self):
        ds = directions.directions_factory(self.n, self.dim,
                                           aligned_flag=False, rng=self.rng)
        mags_0 = np.sum(np.square(ds.u))
        dth = self.rng.uniform(-np.pi, np.pi, size=self.n)
        ds_rot = ds.rotate(dth)
        mags_rot = np.sum(np.square(ds_rot.u))
        self.assertTrue(np.allclose(mags_0, mags_rot))


class TestDirectionsFactories(test.TestBase):

    def test_uniform_directions_isotropy(self):
        n = 1e5
        for dim in [1, 2]:
            u_0 = directions.get_uniform_vectors(n, dim, self.rng)
            u_net = np.mean(u_0, axis=0)
            u_net_mag = np.sqrt(np.sum(np.square(u_net)))
            self.assertTrue(u_net_mag < 1e-2)

    def test_uniform_directions_magnitude(self):
        n = 1e5
        for dim in [1, 2]:
            u_0 = directions.get_uniform_vectors(n, dim, self.rng)
            u_mags = np.sum(np.square(u_0), axis=-1)
            self.assertTrue(np.allclose(u_mags, 1.0))
