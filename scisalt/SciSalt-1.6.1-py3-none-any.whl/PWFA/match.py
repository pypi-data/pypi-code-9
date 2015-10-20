import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
    import slactrac as _sltr
    import scipy.constants as _spc


class Match(object):
    """
    Given a *plasma* of type :class:`Plasma <scisalt.PWFA.Plasma>` and a beam of energy *E* in GeV and normalized emittance *emit_n* in SI units, calculates match parameters
    """
    def __init__(self, plasma, E, emit_n):
        self.plasma = plasma
        self.E = E
        self.emit_n = emit_n

    @property
    def gamma(self):
        """
        Relativistic :math:`\\gamma` of beam
        """
        return _sltr.GeV2gamma(self.E)

    @gamma.setter
    def gamma(self, value):
        self.E = _sltr.gamma2GeV(value)

    @property
    def emit_n(self):
        """
        Emittance of beam
        """
        return self.emit * self.gamma

    @emit_n.setter
    def emit_n(self, value):
        self.emit = value / self.gamma

    @property
    def sigma(self):
        """
        Spot size of matched beam
        """
        return _np.power(2*_sltr.GeV2joule(self.E)*_spc.epsilon_0 / (self.plasma.n_p * _np.power(_spc.elementary_charge, 2)) , 0.25) * _np.sqrt(self.emit)

    def beta(self, E):
        """
        :math:`\\beta` function of matched beam
        """
        return 1.0 / _np.sqrt(self.plasma.k_ion(E))
        # return 1.0 / _np.sqrt(2)
