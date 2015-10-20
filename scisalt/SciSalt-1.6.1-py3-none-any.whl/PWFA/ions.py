import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import scipy.constants as _spc
    import numpy as _np
    import scipy as _sp

import logging as _logging
_logger = _logging.getLogger(__name__)

# ============================
# Constants
# ============================
e      = _spc.e               # Elementary charge
c      = _spc.speed_of_light  # Speed of light
e0     = _spc.epsilon_0       # Vacuum permittivity
amu    = _spc.atomic_mass     # AMU in kg


class Ions(object):
    """
    .. versionadded:: 1.6

    A class to facilitate calculating ion motion in PWFA ion columns due to cylindrical, infinitely-long gaussian beams.
    """
    def __init__(self, A, N_e, sig_r, sig_xi, r0_big=None, n_samp=1000, order=5):
        # ============================
        # Experiment Parameters
        # ============================
        self._A      = A       # Atomic weight in amu
        self._N_e    = N_e     # Number of electrons in bunch
        self._sig_r  = sig_r   # Transverse R.M.S. width
        self._sig_xi = sig_xi  # Longitudinal R.M.S. width

    def _cos(self, x, n, lam):
        return _np.cos(n*x*2*_np.pi/lam)

    def _basic_shape(self, r0_big=None, order=4, n_samp=None):
        if r0_big is None:
            r0_big = self.sig_r * 10000

        if n_samp is None:
            n_samp = 1e4+1
        # ============================
        # Get basic shape
        # (Fourier series)
        # ============================

        x_end = self.lambda_large(r0_big)
        dx = x_end / (n_samp-1)
        x = _np.linspace(0, x_end, n_samp)
        
        y_num = self.r(x, r0_big)
        f_x = y_num / r0_big
        
        a = _np.zeros(order+1)
        for i in range(order+1):
            if i % 2 == 1:
                a[i] = _np.sum(f_x * self.r_large(i*x, r0_big))/r0_big * dx * 2/self.lambda_large(r0_big)

        out = _np.zeros(x.shape)
        for i, val in enumerate(a):
            out = out + val*self.r_large(i*x, r0_big)

        print('=======================')
        print('Initial conditions')
        print('=======================')
        print('k     = {}'.format(self.k))
        print('sig_r = {}'.format(self.sig_r))
        print('r0    = {}'.format(r0_big))
        print('a     = {}'.format(a))

        return x, y_num, out

    @property
    def lambda_small(self):
        """
        The wavelength for small (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return 2*_np.pi*_np.sqrt(2/self.k)*self.sig_r

    def lambda_large(self, r0):
        """
        The wavelength for large (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return 2*_np.sqrt(2*_np.pi/self.k)*r0

    def r_small(self, x, r0):
        """
        Approximate trajectory function for small (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return r0*_np.cos(_np.sqrt(self.k_small) * x)

    def r_large(self, x, r0):
        """
        Approximate trajectory function for large (:math:`r_0 > \\sigma_r`) oscillations.
        """
        return r0*_np.cos(x*self.omega_big(r0))

    def r(self, x, r0):
        """
        Numerically solved trajectory function for initial conditons :math:`r(0) = r_0` and :math:`r'(0) = 0`.
        """
        y1_0 = r0
        y0_0 = 0
        y0   = [y0_0, y1_0]

        y = _sp.integrate.odeint(self._func, y0, x, Dfun=self._gradient)

        return y[:, 1]

    # ============================
    # Omega for large r(0)
    # ============================
    def omega_big(self, r0):
        omega_r0 = _np.sqrt(_np.pi*self.k/2)
        return omega_r0/r0

    @property
    def m(self):
        """
        Ion mass
        """
        return amu * self.A

    @property
    def k(self):
        """
        Driving force term: :math:`r'' = -k \\left( \\frac{1-e^{-r^2/2{\\sigma_r}^2}}{r} \\right)`
        """
        try:
            return self._k
        except AttributeError:
            self._k = e**2 * self.N_e / ( (2*_np.pi)**(5/2) * e0 * self.m * c**2 * self.sig_xi)
            return self._k

    @property
    def k_small(self):
        """
        Small-angle driving force term: :math:`r'' = -k_{small} r`.

        Note: :math:`k_{small} = \\frac{k}{2{\\sigma_r^2}}`
        """
        return self.k / (2*self.sig_r**2)

    @property
    def A(self):
        """
        Ion mass in units of AMU
        """
        return self._A

    @property
    def N_e(self):
        """
        Number of electrons in bunch
        """
        return self._N_e

    @property
    def sig_r(self):
        """
        Transverse R.M.S. width
        """
        return self._sig_r

    @property
    def sig_xi(self):
        """
        Longitudinal R.M.S. width
        """
        return self._sig_xi

    # ============================
    # Force equation
    # ============================
    def _rp2(self, r):
        if r == 0:
            return 0
        return -self.k*(1-_np.exp(-r**2/(2*self.sig_r**2)))/r
    
    # ============================
    # Derivative of force eq.
    # ============================
    def _delrp2(self, r):
        return (1/r**2-_np.exp(-r**2/(2*self.sig_r**2))*(1/r**2+1/self.sig_r**2)) * self.k

    # ============================
    # First-order ODE system
    # ============================
    def _func(self, y, t):
        return [self._rp2(y[1]), y[0]]

    # ============================
    # Gradient for 1st-order ODE
    # ============================
    def _gradient(self, y, t):
        return [[0, self._delrp2(y[1])], [1, 0]]
