from __future__ import print_function, division
from ciabatta.meta import make_repr_str
from ahoy.stime import Time
from ahoy.obstructors import obstructor_factory
from ahoy.agents import agents_factory
from ahoy.fields import food_field_factory


class Ships(object):

    def __init__(self, time, ags, obstructor, c_field):
        self.time = time
        self.agents = ags
        self.obstructor = obstructor
        self.c_field = c_field

    @property
    def dim(self):
        return self.agents.directions.dim

    @property
    def t(self):
        return self.time.t

    def iterate(self, dt, rng):
        self.agents.iterate(dt, rng, self.obstructor)
        self.c_field.iterate(self.agents.positions, dt)
        self.time.iterate(dt)

    def __repr__(self):
        fs = [('time', self.time), ('agents', self.agents),
              ('obstructor', self.obstructor), ('c_field', self.c_field)]
        return make_repr_str(self, fs)


def ships_factory(rng, dim,
                  aligned_flag=None,
                  n=None, rho_0=None,
                  spatial_flag=None, v_0=None,
                  periodic_flag=None, L=None, origin_flags=None,
                  chi=None, onesided_flag=None,
                  tumble_flag=None, p_0=None, tumble_chemo_flag=None,
                  rotation_flag=None, Dr_0=None, rotation_chemo_flag=None,
                  temporal_chemo_flag=None, dt_mem=None, t_mem=None,
                  pore_flag=None, pore_turner=None, pore_R=None, pore_pf=None,
                  c_field_flag=None, c_dx=None, c_D=None, c_delta=None,
                  c_0=None):
    time = Time()
    periodic_flag = not c_field_flag
    obstructor = obstructor_factory(pore_flag, pore_turner,
                                    pore_R, L, pore_pf, rng,
                                    periodic_flag)
    c_field = food_field_factory(c_field_flag, L, c_dx, c_D, c_delta,
                                 c_0, obstructor)
    ags = agents_factory(rng, dim, aligned_flag,
                         n, rho_0,
                         chi, onesided_flag,
                         tumble_flag, p_0, tumble_chemo_flag,
                         rotation_flag, Dr_0, rotation_chemo_flag,
                         temporal_chemo_flag, dt_mem, t_mem, time,
                         spatial_flag, v_0,
                         periodic_flag, L, origin_flags, obstructor,
                         c_field_flag, c_field)
    return Ships(time, ags, obstructor, c_field)
