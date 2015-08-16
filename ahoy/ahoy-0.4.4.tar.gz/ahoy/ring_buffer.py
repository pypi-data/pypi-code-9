import numpy as np
from ahoy import numerics


class RingBuffer(object):
    def __init__(self, n_p):
        self.n_p = n_p
        self.a = np.zeros([self.n_p])
        self.i_zero = 0

    def _i_dec(self):
        self.i_zero -= 1
        if self.i_zero < 0:
            self.i_zero += self.n_p

    def update(self, a_new):
        self._i_dec()
        self.a[self.i_zero] = a_new

    def integral_transform(self, K):
        tot = 0.0
        for i in range(self.n_p):
            tot += self.a[(self.i_zero + i) % self.n_p] * K[i]
        return tot


class CylinderBuffer(RingBuffer):
    def __init__(self, n_l, n_p):
        self.n_l = n_l
        self.n_p = n_p
        self.a = np.zeros([self.n_l, self.n_p])
        self.i_zero = 0

        # Optimisation
        self.inds_p = np.arange(0, self.n_p, dtype=np.uint)
        self.inds_a = self.inds_p.copy()
        self.b = np.empty([self.n_l], dtype=np.float)

    def update(self, a_new):
        self._i_dec()
        self.a[:, self.i_zero] = a_new

    def integral_transform(self, K):
        numerics.integral_transform(self.a, K, self.i_zero,
                                    self.b, self.inds_p, self.inds_a)
        return self.b
