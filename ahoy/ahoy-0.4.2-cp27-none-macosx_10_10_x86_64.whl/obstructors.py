from __future__ import print_function, division
from abc import ABCMeta, abstractmethod
import numpy as np
from ciabatta.meta import make_repr_str
from spatious import vector, distance, geom
from metropack import pack
from ahoy import mesh, turners


class NoneObstructor(object):

    def get_obstructeds(self, rs):
        return np.zeros([rs.shape[0]], dtype=np.bool)

    def obstruct(self, ps, drs, ds):
        return

    def get_mesh(self, L, dx):
        return mesh.uniform_mesh_factory(L, dx)

    def __repr__(self):
        fs = []
        return make_repr_str(self, fs)


class BaseObstructor(NoneObstructor):
    __metaclass__ = ABCMeta

    def __init__(self, turner):
        self.turner = turner

    def _push(self, obs, rs, drs):
        rs[obs] -= drs[obs]

    def get_obstructeds(self, rs):
        seps = self.get_seps(rs)
        return self._is_obstructed(seps)


class SphereObstructor(BaseObstructor):
    __metaclass__ = ABCMeta

    def __init__(self, turner, R, *args, **kwargs):
        super(SphereObstructor, self).__init__(turner)
        self.R = R

    def _is_obstructed(self, seps):
        return vector.vector_mag_sq(seps) < self.R ** 2.0

    @property
    def volume_sphere(self):
        return geom.sphere_volume(self.R, self.dim)

    @abstractmethod
    def _get_th_normals(self, seps):
        return

    @abstractmethod
    def get_seps(self, rs):
        return rs

    def obstruct(self, ps, drs, ds, rng=None):
        seps = self.get_seps(ps.r_w)
        obs = self._is_obstructed(seps)
        self._push(obs, ps.r, drs)
        th_normals = self._get_th_normals(seps[obs])
        self.turner.turn(obs, ds, th_normals, rng)

    def __repr__(self):
        fs = [('turner', self.turner), ('R', self.R)]
        return make_repr_str(self, fs)


class SphereObstructor2D(SphereObstructor):

    def _get_th_normals(self, seps):
        return np.arctan2(seps[:, 1], seps[:, 0])


class SingleSphereObstructor2D(SphereObstructor2D):

    def get_seps(self, rs):
        return rs

    def get_mesh(self, L, dx):
        raise NotImplementedError


class PorousObstructor(SphereObstructor2D):

    def __init__(self, turner, R, L, pf, rng, periodic_flag):
        super(PorousObstructor, self).__init__(turner, R)
        self.periodic_flag = periodic_flag
        self.L = L
        self.rs, self.R = pack.pack(self.R, self.L, pf=pf, rng=rng,
                                    periodic=periodic_flag)

    def obstruct(self, *args, **kwargs):
        if self.rs.shape[0]:
            super(PorousObstructor, self).obstruct(*args, **kwargs)

    def get_obstructeds(self, *args, **kwargs):
        if self.rs.shape[0]:
            return super(PorousObstructor, self).get_obstructeds(*args,
                                                                 **kwargs)
        else:
            return NoneObstructor.get_obstructeds(self, *args, **kwargs)

    @property
    def volume(self):
        return np.product(self.L)

    @property
    def dim(self):
        return self.L.shape[0]

    @property
    def n(self):
        return self.rs.shape[0]

    @property
    def volume_occupied(self):
        return self.n * self.volume_sphere

    @property
    def fraction_occupied(self):
        return self.volume_occupied / self.volume

    @property
    def volume_free(self):
        return self.volume - self.volume_occupied

    @property
    def fraction_free(self):
        return self.volume_free / self.volume

    def get_seps(self, rs):
        return distance.csep_periodic_close(rs, self.rs, self.L)[0]

    def get_mesh(self, L, dx):
        return mesh.porous_mesh_factory(self.rs, self.R, dx, L)

    def __repr__(self):
        fs = [('turner', self.turner), ('R', self.R), ('L', self.L),
              ('fraction_occupied', self.fraction_occupied)]
        return make_repr_str(self, fs)

turner_str_map = {
    'stall': turners.Turner(),
    'bounce_back': turners.BounceBackTurner(),
    'reflect': turners.ReflectTurner(),
    'align': turners.AlignTurner(),
}


def obstructor_factory(pore_flag, turner_str, R, L, pf, rng, periodic_flag):
    if pore_flag:
        return PorousObstructor(turner_str_map[turner_str], R, L, pf, rng,
                                periodic_flag)
    else:
        return NoneObstructor()
