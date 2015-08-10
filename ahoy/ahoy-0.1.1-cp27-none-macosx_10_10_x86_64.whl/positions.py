from __future__ import print_function, division
import numpy as np
from ciabatta import fields, vector
from ciabatta.meta import make_repr_str


class Positions(object):

    def __init__(self, r_0):
        self.r = r_0
        self.r_0 = self.r.copy()

    @property
    def n(self):
        return self.r.shape[0]

    @property
    def dim(self):
        return self.r.shape[1]

    @property
    def r_mag(self):
        return vector.vector_mag(self.r)

    @property
    def dr(self):
        return self.r - self.r_0

    @property
    def dr_mag(self):
        return vector.vector_mag(self.dr)

    @property
    def r_w(self):
        return self.r

    @property
    def r_w_mag(self):
        return vector.vector_mag(self.r_w)

    def __repr__(self):
        fs = [('n', self.n), ('dim', self.dim)]
        return make_repr_str(self, fs)


class PeriodicPositions(Positions):

    def __init__(self, L, r_0):
        super(PeriodicPositions, self).__init__(r_0)
        self.L = L

    @property
    def volume(self):
        return np.product(self.L)

    @property
    def r_w(self):
        wraps = self.get_wraps()
        r_w = self.r.copy()
        for i_dim in np.where(np.isfinite(self.L))[0]:
            r_w[:, i_dim] -= wraps[:, i_dim] * self.L[i_dim]
        return r_w

    def get_density_field(self, dx):
        return fields.density(self.r_w, self.L, dx)

    def get_wraps(self):
        wraps = np.zeros(self.r.shape, dtype=np.int)
        for i_dim in np.where(np.isfinite(self.L))[0]:
            wraps_mag = ((np.abs(self.r[:, i_dim]) + self.L[i_dim] / 2.0) //
                         self.L[i_dim])
            wraps[:, i_dim] = np.sign(self.r[:, i_dim]) * wraps_mag
        return wraps

    def __repr__(self):
        fs = [('n', self.n), ('dim', self.dim), ('L', self.L)]
        return make_repr_str(self, fs)


class NonePositions(object):

    def __repr__(self):
        fs = []
        return make_repr_str(self, fs)


def positions_factory(spatial_flag, periodic_flag, n, dim=None,
                      L=None, origin_flags=None,
                      rng=None, obstructor=None):
    if not spatial_flag:
        return NonePositions()
    elif not periodic_flag:
        r_0 = np.zeros([n, dim])
        return Positions(r_0)
    else:
        r_0 = get_uniform_points(n, L, origin_flags, rng, obstructor)
        return PeriodicPositions(L, r_0)


def get_uniform_points(n, L, origin_flags=None, rng=None, obstructor=None):
    dim = L.shape[0]
    if origin_flags is None:
        origin_flags = np.zeros([dim], dtype=np.bool)
    if rng is None:
        rng = np.random
    r = np.zeros([n, dim])
    for i_n in range(n):
        while True:
            for i_dim in range(dim):
                if np.isinf(L[i_dim]) or origin_flags[i_dim]:
                    r[i_n, i_dim] = 0.0
                else:
                    r[i_n, i_dim] = rng.uniform(-L[i_dim] / 2.0,
                                                L[i_dim] / 2.0)
            if obstructor is None:
                break
            elif not obstructor.get_obstructeds(np.array([r[i_n]]))[0]:
                break
    return r
