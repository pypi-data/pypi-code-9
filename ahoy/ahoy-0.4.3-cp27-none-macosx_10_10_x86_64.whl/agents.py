from __future__ import print_function, division
import numpy as np
from ciabatta.meta import make_repr_str
from ahoy.rudder_sets import rudder_set_factory
from ahoy.directions import directions_factory
from ahoy.positions import positions_factory
from ahoy.swimmers import swimmers_factory


class Agents(object):

    def __init__(self, directions, positions, rudder_sets, swimmers):
        self.directions = directions
        self.rudder_sets = rudder_sets
        self.positions = positions
        self.swimmers = swimmers

    def iterate(self, dt, rng, obstructor):
        self.directions = self.rudder_sets.rotate(self.directions, dt, rng)
        self.positions, dr = self.swimmers.displace(self.positions, dt)
        obstructor.obstruct(self.positions, dr, self.directions)

    @property
    def chi(self):
        return self.rudder_sets.chi

    @property
    def n(self):
        return self.directions.n

    def __repr__(self):
        fs = [('directions', self.directions), ('positions', self.positions),
              ('rudder_sets', self.rudder_sets), ('swimmers', self.swimmers)]
        return make_repr_str(self, fs)


def agents_factory(rng, dim, aligned_flag,
                   n=None, rho_0=None,
                   chi=None, onesided_flag=None,
                   tumble_flag=None, p_0=None, tumble_chemo_flag=None,
                   rotation_flag=None, Dr_0=None, rotation_chemo_flag=None,
                   temporal_chemo_flag=None, dt_mem=None, t_mem=None, time=None,
                   spatial_flag=None, v_0=None,
                   periodic_flag=None, L=None, origin_flags=None, obstructor=None,
                   c_field_flag=None, c_field=None):
    if rho_0 is not None:
        try:
            volume_free = obstructor.volume_free
        except AttributeError:
            volume_free = np.product(L)
        n = int(round(rho_0 * volume_free))
    ds = directions_factory(n, dim, aligned_flag=aligned_flag,
                            rng=rng)
    ps = positions_factory(spatial_flag, periodic_flag, n, dim, L,
                           origin_flags, rng, obstructor)
    rudder_sets = rudder_set_factory(temporal_chemo_flag,
                                     ds,
                                     ps, v_0, dt_mem, t_mem, time,
                                     c_field_flag, c_field,
                                     onesided_flag, chi,
                                     tumble_flag, p_0, tumble_chemo_flag,
                                     rotation_flag, Dr_0, dim, rotation_chemo_flag)
    swims = swimmers_factory(spatial_flag, v_0, ds)
    return Agents(ds, ps, rudder_sets, swims)
