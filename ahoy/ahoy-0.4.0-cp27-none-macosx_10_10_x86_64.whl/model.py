from __future__ import print_function, division
import numpy as np
from ciabatta.meta import make_repr_str
import ahoy
from ahoy import ships, obstructors, fields, turners


class Model(object):

    def __init__(self, seed, dt,
                 aligned_flag=False, origin_flags=None,
                 **ship_kwargs):
        # Record initial conditions
        self.seed = seed
        self.dt = dt

        # Initialise system
        self.i = 0
        self.rng = np.random.RandomState(seed)
        self.ships = ships.ships_factory(self.rng,
                                         aligned_flag=aligned_flag,
                                         origin_flags=origin_flags,
                                         **ship_kwargs)

    @property
    def aligned_flags(self):
        return np.all(self.ships.agents.directions.u_0 == 0.0, axis=0)

    @property
    def origin_flags(self):
        return np.all(self.ships.agents.positions.r_0 == 0.0, axis=0)

    def iterate(self):
        self.ships.iterate(self.dt, self.rng)
        self.i += 1

    def _get_output_dirname_agent_part(self):
        ags = self.ships.agents

        origin_str = '({})'.format(','.join(['{:d}'.format(a)
                                             for a in self.aligned_flags]))
        s = 'n={},align={}'.format(ags.positions.n, origin_str)

        # Space and swimming
        if isinstance(ags.positions, ahoy.positions.Positions):
            origin_str = '({})'.format(','.join(['{:d}'.format(o)
                                                 for o in self.origin_flags]))
            s += ',origin={},v={:g}'.format(origin_str, ags.swimmers.v_0)
            if isinstance(ags.positions, ahoy.positions.PeriodicPositions):
                def format_inf(x):
                    return '{:g}'.format(x) if np.isfinite(x) else 'i'
                L_str = '({})'.format(','.join([format_inf(e)
                                                for e in ags.positions.L]))
                s += ',L={}'.format(L_str)

        # Rudders
        for rs in ags.rudder_sets.sets:
            nm = rs.noise_measurer
            if isinstance(rs, ahoy.rudders.TumbleRudders):
                noise_str = 'p'
            elif isinstance(rs, ahoy.rudders.RotationRudders):
                noise_str = 'Dr'
            s += ',{}={:g}'.format(noise_str, nm.noise_0)
            if rs.is_chemotactic:
                type_s = 'T' if nm.is_temporal else 'S'
                side = 2 - rs.is_onesided
                s += ',chi={:.2g},side={:d},type={}'.format(nm.chi, side,
                                                           type_s)
                if nm.is_temporal:
                    measurer = nm.dc_dx_measurer
                    s += ',dtMem={:g},tMem={:g}'.format(measurer.dt_mem,
                                                        measurer.t_mem)
        return s

    def _get_output_dirname_obstruction_part(self):
        obs = self.ships.obstructor
        s = 'obs='

        if obs.__class__ is obstructors.NoneObstructor:
            s += 'NoObs'
        elif obs.__class__ is obstructors.PorousObstructor:
            if obs.turner.__class__ is turners.Turner:
                s_turner = 'stall'
            elif obs.turner.__class__ is turners.BounceBackTurner:
                s_turner = 'bback'
            elif obs.turner.__class__ is turners.ReflectTurner:
                s_turner = 'reflect'
            elif obs.turner.__class__ is turners.AlignTurner:
                s_turner = 'align'
            pf = obs.fraction_occupied
            s += 'Pore(R={:g},pf={:.2g},turn={})'.format(obs.R, pf, s_turner)
        return s

    def _get_output_dirname_field_part(self):
        c_field = self.ships.c_field
        s = 'c='
        if c_field.__class__ is fields.NoneFoodField:
            s += 'NoC'
        elif c_field.__class__ is fields.FoodField:
            s += 'C(c0={:g},cD={:g},cDelta={:g})'.format(c_field.c_0,
                                                         c_field.D,
                                                         c_field.delta)
        return s

    def get_output_dirname(self):
        s = 'ahoy_{}D,dt={:g},seed={}'.format(self.ships.dim, self.dt,
                                              self.seed)
        s += ',{}'.format(self._get_output_dirname_agent_part())
        s += ',{}'.format(self._get_output_dirname_obstruction_part())
        s += ',{}'.format(self._get_output_dirname_field_part())
        return s

    def __repr__(self):
        fs = [('seed', self.seed), ('dt', self.dt),
              ('origin_flags', self.origin_flags),
              ('aligned_flags', self.aligned_flags),
              ('i', self.i), ('rng', self.rng),
              ('ships', self.ships)
              ]
        return make_repr_str(self, fs)
