from __future__ import print_function, division
import numpy as np
from ciabatta import crandom
from ciabatta.meta import make_repr_str
from spatious import vector
from spatious.vector import smallest_signed_angle as angle_dist


class Turner(object):

    def get_angle(self, th_in, *args, **kwargs):
        return th_in

    def get_norm_angle(self, *args, **kwargs):
        return vector.normalise_angle(self.get_angle(*args, **kwargs))

    def turn(self, obs, ds, *args, **kwargs):
        ds.th[obs] = self.get_norm_angle(ds.th[obs], *args, **kwargs)

    def __repr__(self):
        fs = []
        return make_repr_str(self, fs)


class BounceBackTurner(Turner):

    def get_angle(self, th_in, *args, **kwargs):
        return th_in + np.pi


class ReflectTurner(Turner):

    def get_angle(self, th_in, th_normal, *args, **kwargs):
        th_rel = th_in - th_normal
        return th_normal + np.where(th_rel == 0.0,
                                    np.pi,
                                    np.sign(th_rel) * np.pi - th_rel)


class AlignTurner(Turner):

    def get_angle(self, th_in, th_normal, rng, *args, **kwargs):
        if rng is None:
            rng = np.random
        th_rel = vector.normalise_angle(th_in - th_normal)
        antiparallels = np.isclose(np.abs(angle_dist(th_in, th_normal)), np.pi)
        signs = np.where(antiparallels,
                         crandom.randbool(antiparallels.shape[0], rng),
                         np.sign(th_rel))
        th_rel = signs * np.pi / 2.0
        return th_normal + th_rel
