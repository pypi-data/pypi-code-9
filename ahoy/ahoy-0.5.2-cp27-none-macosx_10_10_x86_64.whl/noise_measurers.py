from __future__ import print_function, division
import numpy as np
from ciabatta.meta import make_repr_str
from ahoy import measurers
from ahoy.dc_dx_measurers import TemporalDcDxMeasurer, dc_dx_factory


class NoiseMeasurer(measurers.Measurer):

    def __init__(self, noise_0, *args, **kwargs):
        self.noise_0 = noise_0

    def get_noise(self):
        return self.noise_0

    def __repr__(self):
        fs = [('noise_0', self.noise_0)]
        return make_repr_str(self, fs)


class ChemoNoiseMeasurer(NoiseMeasurer):

    def __init__(self, noise_0, chi, dc_dx_measurer):
        NoiseMeasurer.__init__(self, noise_0)
        self.chi = chi
        self.dc_dx_measurer = dc_dx_measurer

    @property
    def is_temporal(self):
        return isinstance(self.dc_dx_measurer, TemporalDcDxMeasurer)

    def get_noise(self):
        dc_dxs = self.dc_dx_measurer.get_dc_dxs()
        return self.noise_0 * (1.0 - self.chi * dc_dxs)

    def __repr__(self):
        fs = [('noise_0', self.noise_0), ('chi', self.chi),
              ('dc_dx_measurer', self.dc_dx_measurer)]
        return make_repr_str(self, fs)


class OneSidedChemoNoiseMeasurer(ChemoNoiseMeasurer):

    def get_noise(self):
        noise_two_sided = super(OneSidedChemoNoiseMeasurer, self).get_noise()
        return np.minimum(self.noise_0, noise_two_sided)


def chemo_noise_measurer_factory(onesided_flag, *args, **kwargs):
    if onesided_flag:
        return OneSidedChemoNoiseMeasurer(*args, **kwargs)
    else:
        return ChemoNoiseMeasurer(*args, **kwargs)


def noise_measurer_factory(chemo_flag,
                           noise_0,
                           onesided_flag, chi,
                           temporal_chemo_flag,
                           ds,
                           ps, v_0, dt_mem, t_mem, t_rot_0, time,
                           c_field_flag, c_field):
    if chemo_flag:
        dc_dx_measurer = dc_dx_factory(temporal_chemo_flag,
                                       ds,
                                       ps, v_0, dt_mem, t_mem, t_rot_0, time,
                                       c_field_flag, c_field)
        return chemo_noise_measurer_factory(onesided_flag, noise_0, chi,
                                            dc_dx_measurer)
    else:
        return NoiseMeasurer(noise_0)
