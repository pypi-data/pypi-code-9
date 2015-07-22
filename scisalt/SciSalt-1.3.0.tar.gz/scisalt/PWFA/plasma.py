import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import slactrac as _sltr


class Plasma(object):
    """
    A class for relating plasma density to plasma frequency :math:`\\omega_p` and ion focusing force.

    Input either:

    * Plasma density *n_p* in SI units
    * Plasma density *n_p_cgs* in CGS units
    """
    def __init__(self, n_p=None, n_p_cgs=None):
        if n_p is None and n_p_cgs is None:
            raise ValueError('Keywords n_p and n_p_cgs cannot both be None')
        elif n_p is not None and n_p_cgs is not None:
            raise ValueError('Keywords n_p and n_p_cgs cannot both be specified')
        elif n_p is not None:
            self.n_p = n_p
        elif n_p_cgs is not None:
            self.n_p_cgs = n_p_cgs

    @property
    def n_p(self):
        """
        Plasma density in SI units
        """
        return self._n_p

    @n_p.setter
    def n_p(self, n_p):
        self._n_p = n_p

    @property
    def w_p(self):
        """
        Plasma frequency :math:`\\omega_p` for given plasma density
        """
        return _np.sqrt(self.n_p * _np.power(_sltr.e, 2) / (_sltr.m_e * _sltr.epsilon_0))

    def k_ion(self, E):
        """
        Geometric focusing force due to ion column for given plasma density as a function of *E*
        """
        return self.n_p * _np.power(_sltr.e, 2) / (2*_sltr.GeV2joule(E) * _sltr.epsilon_0)

    @property
    def n_p_cgs(self):
        """
        Plasma density in CGS units
        """
        return self.n_p / 1e6

    @n_p_cgs.setter
    def n_p_cgs(self, n_p_cgs):
        self.n_p = n_p_cgs * 1e6
