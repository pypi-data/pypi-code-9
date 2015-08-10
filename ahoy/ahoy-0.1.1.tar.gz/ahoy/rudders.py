from __future__ import print_function, division
from abc import ABCMeta, abstractmethod
import numpy as np
from ahoy import noise_measurers
from ciabatta.meta import make_repr_str
from ahoy.noise_measurers import noise_measurer_factory


class Rudders(object):

    def __init__(self, noise_measurer):
        self.noise_measurer = noise_measurer

    @property
    def is_chemotactic(self):
        return isinstance(self.noise_measurer,
                          noise_measurers.ChemoNoiseMeasurer)

    @property
    def is_onesided(self):
        return isinstance(self.noise_measurer,
                          noise_measurers.OneSidedChemoNoiseMeasurer)

    @property
    def chi(self):
        if self.is_chemotactic:
            return self.noise_measurer.chi
        else:
            return None

    def rotate(self, directions, dt, rng=None):
        noise = self.noise_measurer.get_noise()
        return self._rotate(directions, noise, dt, rng)

    def _rotate(self, directions, noise, dt, rng):
        return directions

    def __repr__(self):
        fs = [('noise_measurer', self.noise_measurer)]
        return make_repr_str(self, fs)


class RotationRudders(Rudders):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _get_dth(self, directions, noise, dt):
        return

    def _rotate(self, directions, noise, dt, rng):
        dth = self._get_dth(directions, noise, dt, rng)
        return directions.rotate(dth)


class RotationRudders2D(RotationRudders):

    def _get_dth(self, directions, noise, dt, rng):
        if rng is None:
            rng = np.random
        return rng.normal(scale=np.sqrt(2.0 * noise * dt), size=directions.n)


class TumbleRudders(Rudders):

    def _get_tumblers(self, directions, noise, dt, rng):
        if rng is None:
            rng = np.random
        return rng.uniform(size=directions.n) < noise * dt

    def _rotate(self, directions, noise, dt, rng):
        tumblers = self._get_tumblers(directions, noise, dt, rng)
        return directions.tumble(tumblers, rng)


def rotation_rudders_nd(dim, *args, **kwargs):
    if dim == 2:
        return RotationRudders2D(*args, **kwargs)
    else:
        raise NotImplementedError('No rotation rudders implemented in this '
                                  ' dimension')


def rudders_factory(tumble_flag, dim,
                    chemo_flag,
                    noise_0,
                    onesided_flag, chi,
                    temporal_chemo_flag,
                    ds,
                    ps, v_0, dt_mem, t_mem, t_rot_0, time,
                    c_field_flag, c_field):
    noise_measurer = noise_measurer_factory(chemo_flag,
                                            noise_0,
                                            onesided_flag, chi,
                                            temporal_chemo_flag,
                                            ds,
                                            ps, v_0, dt_mem, t_mem, t_rot_0, time,
                                            c_field_flag, c_field)
    if tumble_flag:
        rudders = TumbleRudders(noise_measurer)
    else:
        rudders = rotation_rudders_nd(dim, noise_measurer)
    return rudders
