from __future__ import print_function, division
from ciabatta.meta import make_repr_str


class Time(object):
    def __init__(self):
        self.t = 0.0

    def iterate(self, dt):
        self.t += dt

    def __repr__(self):
        fs = [('t', self.t)]
        return make_repr_str(self, fs)
