from __future__ import print_function, division
import numpy as np
from ciabatta import crandom
from ciabatta.meta import make_repr_str
from spatious import vector


class Directions1D(object):

    def __init__(self, u_0):
        self.sign = np.sign(u_0[:, 0])
        self.sign_0 = self.sign.copy()

    @property
    def n(self):
        return self.u.shape[0]

    @property
    def dim(self):
        return self.u.shape[1]

    @property
    def u(self):
        return self.sign[:, np.newaxis].copy()

    @property
    def u_0(self):
        return self.sign_0[:, np.newaxis].copy()

    def tumble(self, tumblers, rng=None):
        if rng is None:
            rng = np.random
        self.sign[tumblers] = crandom.randbool(tumblers.sum(), rng=rng)
        return self

    def __repr__(self):
        fs = [('n', self.n)]
        return make_repr_str(self, fs)


class Directions2D(Directions1D):

    def __init__(self, u_0):
        self.th = np.arctan2(u_0[:, 1], u_0[:, 0])
        self.th_0 = self.th.copy()

    def _th_to_u(self, th):
        return np.array([np.cos(th), np.sin(th)]).T

    @property
    def u(self):
        return self._th_to_u(self.th)

    @property
    def u_0(self):
        return self._th_to_u(self.th_0)

    def tumble(self, tumblers, rng=None):
        if rng is None:
            rng = np.random
        self.th[tumblers] = rng.uniform(-np.pi, np.pi, size=tumblers.sum())
        return self

    def rotate(self, dth):
        self.th += dth
        return self

    def __repr__(self):
        fs = [('n', self.n)]
        return make_repr_str(self, fs)


def directions_nd(u_0):
    dim = u_0.shape[1]
    if dim == 1:
        return Directions1D(u_0)
    elif dim == 2:
        return Directions2D(u_0)


def directions_factory(n, dim, aligned_flag=False, rng=None):
    if aligned_flag:
        u_0 = get_aligned_vectors(n, dim)
    else:
        u_0 = get_uniform_vectors(n, dim, rng)
    return directions_nd(u_0)


def get_uniform_vectors(n, dim, rng=None):
    return vector.sphere_pick(n=n, d=dim, rng=rng)


def get_aligned_vectors(n, dim):
    u = np.zeros([n, dim])
    u[:, 0] = 1.0
    return u
