from __future__ import print_function, division
import numpy as np
from scipy.spatial.distance import pdist
from spatious.geom import sphere_volume
from spatious.distance import pdist_sq_periodic, cdist_sq_periodic


class MetroRCP(object):

    def __init__(self, r_0, L_0, R, dr_max, dL_max, rng=None):
        self.r = r_0
        self.L = L_0
        self.R = R
        self.dr_max = dr_max
        self.dL_max = dL_max
        if rng is None:
            rng = np.random.RandomState()
        self.rng = rng

    def U(self):
        sep_sq = pdist(self.r, metric='sqeuclidean')
        if np.any(sep_sq < (2.0 * self.R) ** 2):
            return np.inf
        for i_dim in range(self.dim):
            if np.any(np.abs(self.r[:, i_dim]) + self.R > self.L[i_dim] / 2.0):
                return np.inf
        return 1.0 / self.pf

    def displace_r(self):
        self.i = self.rng.randint(self.n)
        self.r_old = self.r[self.i].copy()

        dr = np.zeros([self.dim])
        for i_dim in range(self.dim):
            dr[i_dim] = self.rng.uniform(-self.dr_max * self.L[i_dim],
                                         self.dr_max * self.L[i_dim])

        self.r[self.i] += dr

    def revert_r(self):
        self.r[self.i] = self.r_old.copy()

    def displace_L(self):
        self.dL = 1.0 + self.rng.uniform(-self.dL_max, self.dL_max)
        self.L *= self.dL
        self.r *= self.dL

    def revert_L(self):
        self.L /= self.dL
        self.r /= self.dL

    def iterate(self, beta):
        U_0 = self.U()

        i = self.rng.randint(self.n + 1)
        if i < len(self.r):
            self.displace_r()
            revert = self.revert_r
        else:
            self.displace_L()
            revert = self.revert_L

        U_new = self.U()
        if np.exp(-beta * (U_new - U_0)) < self.rng.uniform():
            revert()

    @property
    def n(self):
        return self.r.shape[0]

    @property
    def dim(self):
        return self.L.shape[0]

    @property
    def V(self):
        return np.product(self.L)

    @property
    def V_full(self):
        return self.n * self.V_1

    @property
    def V_1(self):
        return sphere_volume(self.R, self.dim)

    @property
    def pf(self):
        return self.V_full / self.V


class MetroRCPPeriodic(MetroRCP):

    def __init__(self, r_0, L_0, R, dr_max, dL_max, rng=None):
        super(MetroRCPPeriodic, self).__init__(r_0, L_0, R, dr_max, dL_max,
                                               rng)
        self.sep_sq = pdist_sq_periodic(r_0, self.L)

    def U(self):
        if np.any(self.sep_sq < (2.0 * self.R) ** 2):
            return np.inf
        return 1.0 / self.pf

    def displace_r(self):
        super(MetroRCPPeriodic, self).displace_r()

        for i_dim in range(self.dim):
            r = self.r[:, i_dim]
            r[r > self.L[i_dim] / 2.0] -= self.L[i_dim]
            r[r < -self.L[i_dim] / 2.0] += self.L[i_dim]

        self.sep_sq_old = self.sep_sq[self.i].copy()
        sep_sq = cdist_sq_periodic(self.r[np.newaxis, self.i], self.r, self.L)
        self.sep_sq[self.i, :] = sep_sq
        self.sep_sq[:, self.i] = sep_sq
        self.sep_sq[self.i, self.i] = np.inf

    def revert_r(self):
        super(MetroRCPPeriodic, self).revert_r()
        self.sep_sq[self.i, :] = self.sep_sq_old.copy()
        self.sep_sq[:, self.i] = self.sep_sq_old.copy()

    def displace_L(self):
        super(MetroRCPPeriodic, self).displace_L()
        self.sep_sq *= self.dL ** 2

    def revert_L(self):
        super(MetroRCPPeriodic, self).revert_L()
        self.sep_sq /= self.dL ** 2


def metro_rcp_factory(periodic, *args, **kwargs):
    if periodic:
        return MetroRCPPeriodic(*args, **kwargs)
    else:
        return MetroRCP(*args, **kwargs)
