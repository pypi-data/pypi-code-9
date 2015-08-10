from __future__ import print_function, division
from abc import ABCMeta, abstractmethod
import numpy as np
from ciabatta.meta import make_repr_str
from ahoy.ring_buffer import CylinderBuffer
from ahoy import measurers, c_measurers


def get_K(t, dt, t_rot_0):
    A = 0.5
    ts = np.arange(0.0, t, dt)
    gs = ts / t_rot_0
    K = np.exp(-gs) * (1.0 - A * (gs + (gs ** 2) / 2.0))
    K[K < 0.0] *= np.abs(K[K >= 0.0].sum() / K[K < 0.0].sum())
    K /= np.sum(K * -ts * dt)
    return K


class DcDxMeasurer(measurers.Measurer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_dc_dxs(self):
        return


class SpatialDcDxMeasurer(DcDxMeasurer):

    def __init__(self, directions, grad_c_measurer):
        self.directions = directions
        self.grad_c_measurer = grad_c_measurer

    def get_dc_dxs(self):
        grad_c = self.grad_c_measurer.get_grad_cs()
        return np.sum(self.directions.u * grad_c, axis=-1)

    def __repr__(self):
        fs = [('grad_c_measurer', self.grad_c_measurer)]
        return make_repr_str(self, fs)


class TemporalDcDxMeasurer(DcDxMeasurer):

    def __init__(self, c_measurer, v_0, dt_mem, t_mem, t_rot_0,
                 time):
        self.c_measurer = c_measurer
        self.v_0 = v_0
        self.dt_mem = dt_mem
        self.t_mem = t_mem
        cs = self.c_measurer.get_cs()
        n = cs.shape[0]
        self.K_dt = get_K(self.t_mem, self.dt_mem, t_rot_0) * self.dt_mem
        self.c_mem = CylinderBuffer(n, self.K_dt.shape[0])
        self.time = time

        # Optimisation, only calculate dc_dx when c memory is updated.
        self.dc_dx_cache = np.zeros([n])
        self.t_last_update = 0.0

    def _iterate(self):
        cs = self.c_measurer.get_cs()
        self.c_mem.update(cs)

    def _get_dc_dxs(self):
        return self.c_mem.integral_transform(self.K_dt) / self.v_0

    def iterate(self):
        t_now = self.time.t
        if t_now - self.t_last_update > 0.99 * self.dt_mem:
            self._iterate()
            self.dc_dx_cache = self._get_dc_dxs()
            self.t_last_update = t_now

    def get_dc_dxs(self):
        self.iterate()
        return self.dc_dx_cache

    def __repr__(self):
        fs = [('c_measurer', self.c_measurer), ('v_0', self.v_0),
              ('dt_mem', self.dt_mem), ('t_mem', self.t_mem),
              ('t_last_update', self.t_last_update)]
        return make_repr_str(self, fs)


def dc_dx_factory(temporal_chemo_flag,
                  ds=None,
                  ps=None, v_0=None, dt_mem=None, t_mem=None, t_rot_0=None, time=None,
                  c_field_flag=None, c_field=None):
    if temporal_chemo_flag:
        return temporal_dc_dx_factory(ps, v_0, dt_mem, t_mem, t_rot_0, time,
                                      c_field_flag, c_field)
    else:
        return spatial_dc_dx_factory(ds, c_field_flag, c_field, ps)


def spatial_dc_dx_factory(ds, c_field_flag=None, c_field=None, ps=None):
    if not c_field_flag:
        grad_c_measurer = c_measurers.ConstantGradCMeasurer(ds.n, ds.dim)
    else:
        grad_c_measurer = c_measurers.FieldGradCMeasurer(c_field, ps)
    return SpatialDcDxMeasurer(ds, grad_c_measurer)


def temporal_dc_dx_factory(ps, v_0, dt_mem, t_mem, t_rot_0, time,
                           c_field_flag=None, c_field=None):
    if not c_field_flag:
        c_measurer = c_measurers.LinearCMeasurer(ps)
    else:
        c_measurer = c_measurers.FieldCMeasurer(c_field, ps)
    return TemporalDcDxMeasurer(c_measurer, v_0, dt_mem, t_mem, t_rot_0, time)
