from __future__ import print_function, division
from itertools import product
import numpy as np
from scipy.stats import multivariate_normal
from ahoy import positions, fields
from ahoy.mesh import uniform_mesh_factory
import test


def get_nearest_cell_ids_manual(f, ps):
    rs = ps.r_w.T
    ccs = f.mesh.cellCenters.value
    drs = np.abs(ccs[:, np.newaxis, :] - rs[:, :, np.newaxis])
    for i_dim in range(ps.dim):
        drs[i_dim] = np.minimum(drs[i_dim], ps.L[i_dim] - drs[i_dim])
    dr_mags = np.sum(np.square(drs), axis=0)
    return np.argmin(dr_mags, axis=1)


class TestField1D(test.TestBase):
    L = np.array([1.6])
    dx = 0.1

    x_vals = [-L[0] / 2.012, -0.312, 0.01, 0.121, L[0] / 1.976]
    rs_special = np.array(list(product(x_vals)))

    def test_field(self):
        n = 100

        mesh = uniform_mesh_factory(self.L, self.dx)
        f = fields.Field(mesh, c_0=1.0)

        rs_random = positions.get_uniform_points(n, self.L, rng=self.rng)
        rs = np.append(rs_random, self.rs_special, axis=0)

        ps = positions.PeriodicPositions(self.L, rs)
        cids = f.get_nearest_cell_ids(ps)
        cids_manual = get_nearest_cell_ids_manual(f, ps)
        self.assertTrue(np.allclose(cids, cids_manual))


class TestField2D(TestField1D):
    L = np.array([1.0, 2.0])

    x_vals = [-L[0] / 2.012, -0.312, 0.01, 0.121, L[0] / 1.976]
    y_vals = [-L[1] / 1.99632, -0.312, 0.01, 0.121, L[1] / 2.0021]
    rs_special = np.array(list(product(x_vals, y_vals)))


class TestFoodField1D(test.TestBase):
    L = np.array([4.0])
    dx = 0.005

    def test_rho_array_uniform(self):
        dim = self.L.shape[0]
        rho_expected = 1.0 / (self.dx ** dim)

        mesh = uniform_mesh_factory(self.L, self.dx)
        r_centers = mesh.cellCenters.value.T
        ps_centers = positions.PeriodicPositions(self.L, r_centers)

        D = 1.0
        delta = 1.0
        c_0 = 1.0
        f = fields.FoodField(mesh, D, delta, c_0)
        rho_array = f._get_rho_array(ps_centers)
        self.assertTrue(np.allclose(rho_array, rho_expected))

    def test_decay_term(self):
        dim = self.L.shape[0]
        rho_expected = 1.0 / (self.dx ** dim)

        mesh = uniform_mesh_factory(self.L, self.dx)
        r_centers = mesh.cellCenters.value.T
        ps_centers = positions.PeriodicPositions(self.L, r_centers)

        dt = 0.00001
        D = 0.0
        delta = 1.0
        c_0 = 1.0
        f = fields.FoodField(mesh, D, delta, c_0)
        f.iterate(ps_centers, dt)
        c_expected = c_0 * np.exp(-delta * rho_expected * dt)
        self.assertTrue(np.allclose(f.c, c_expected))

    def test_diff_term(self):
        dim = self.L.shape[0]

        mesh = uniform_mesh_factory(self.L, self.dx)
        r_centers = mesh.cellCenters.value.T
        r_centers_mag = np.sqrt(np.sum(np.square(r_centers), axis=-1))
        i_center = np.argmin(r_centers_mag)
        ps = positions.PeriodicPositions(self.L, np.zeros((1, dim)))

        dt = 0.01
        t_max = 0.2
        D = 1.0
        delta = 0.0
        c_0 = 1.0

        c_0_array = np.zeros(mesh.cellCenters.shape[1])
        c_0_array[i_center] = c_0

        f = fields.FoodField(mesh, D, delta, c_0_array)

        for t in np.arange(0.0, t_max, dt):
            f.iterate(ps, dt)
        variance = 2.0 * D * t_max
        mean = dim * [0.0]
        cov = np.identity(dim) * variance
        mn = multivariate_normal(mean, cov)
        c_expected = (c_0 * self.dx ** dim) * mn.pdf(r_centers)
        # print(c_expected)
        # print(f.c.value)
        # import matplotlib.pyplot as plt
        # plt.plot(r_centers_mag, f.c.value, label='Got')
        # plt.plot(r_centers_mag, c_expected, label='Expected')
        # plt.legend()
        # plt.show()
        self.assertTrue(np.allclose(f.c, c_expected, atol=1e-4))

    def test_random_seeding(self):
        dim = self.L.shape[0]
        mesh = uniform_mesh_factory(self.L, self.dx)

        dt = 0.01
        t_max = 0.2
        D = 1.0
        delta = 0.0
        c_0 = 1.0

        n = 1000
        r_0 = np.zeros([n, dim])
        ps = positions.PeriodicPositions(self.L, r_0)

        def get_f(npy_seed):
            np.random.seed(npy_seed)
            f = fields.FoodField(mesh, D, delta, c_0)
            for t in np.arange(0.0, t_max, dt):
                ps.r += self.rng.uniform(-self.dx, self.dx, size=(n, dim))
                f.iterate(ps, dt)
            return f

        f_1 = get_f(2)
        f_2 = get_f(3)

        self.assertTrue(np.allclose(f_1.c.value, f_2.c.value))


class TestFoodField2D(TestFoodField1D):
    L = np.array(2 * [4.0])
    dx = 0.05
