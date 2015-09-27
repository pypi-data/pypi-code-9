__author__ = 'kaurov'
import numpy as np


sigmaT = 6.6524e-25 #cm^2
me = 9.109e-28 # g
c = 2.9979e10 # cm/s
#hbar = 4.135668e-15/2.0/np.pi # eV*s
hbar = 1.0545e-27 # erg*s
kB = 1.380648e-16 # erg/K

#
# Photoionization cross sections
#

lookup = np.zeros([10, 10, 20])
lookup[1, 1, :9] = [1.360e1,    5.000E+4,   4.298E-1, 5.475e+4, 3.288e1,    2.963e0,    0.000e0,    0,          0]
lookup[2, 2, :9] = [24.59,      5e4,        13.61,    949.2,    1.469,      3.188,      2.039,      0.4434,     2.136]
lookup[2, 1, :9] = [54.42,      5e4,        1.72,     13690,    32.88,      2.963,      0,          0,          0]
lookup[8, 8, :9] = [1.362e1,    5.380E+2,   1.240e0,  1.745E+3, 3.784e0,    1.764e1,    7.589E-2,   8.698e0,    1.271E-1]

class cross_sections:
    '''
    Class with collection of various cross sections for atomic processes.
    '''
    sigmaT = 6.6524e-25 #cm^2
    me = 9.109e-28 # g
    c = 2.9979e10 # cm/s
    # hbar = 4.135668e-15/2.0/np.pi # eV*s
    hbar = 1.0545e-27 # erg*s
    kB = 1.380648e-16 # erg/K

    const_HI_ion = 13.6057
    const_HI_ex = 10.2
    const_HeI_ion = 24.5874
    const_HeI_ex = 21.22
    const_HeII_ion = 54.41776
    const_HeII_ex = 40.82

    # Photoionization cross sections
    #
    # http://adsabs.harvard.edu/abs/1996ApJ...465..487V

    lookup = np.zeros([10, 10, 20])
    lookup[1, 1, :9] = [1.360e1,    5.000E+4,   4.298E-1, 5.475e+4, 3.288e1,    2.963e0,    0.000e0,    0,          0]
    lookup[2, 2, :9] = [24.59,      5e4,        13.61,    949.2,    1.469,      3.188,      2.039,      0.4434,     2.136]
    lookup[2, 1, :9] = [54.42,      5e4,        1.72,     13690,    32.88,      2.963,      0,          0,          0]
    lookup[8, 8, :9] = [1.362e1,    5.380E+2,   1.240e0,  1.745E+3, 3.784e0,    1.764e1,    7.589E-2,   8.698e0,    1.271E-1]

    def __init__(self, cs={'photion': 'VFKY1996', 'collion': 'AR', 'collex': 'SKD'}):
        '''
        Initialize the cross sections
        :param cs: dictionary with references to the papers which results will be used
        :return:
        '''
        if cs['collion'] in ['AR', 'BEQ', 'RBEQ']:
            self.cs = cs
        else:
            print "Bad dictionary!"
            raise "class is not initialized"

    def sigma_AR(self, E, mode):
        '''
        Hydrogen collisional ionization as in: http://xxx.lanl.gov/pdf/0906.1197v2.pdf
        Equation B4
        :param E: the energy of the electron in eV
        :return:
        '''
        if mode == 'HI':
            A=22.8
            B=-12.0
            C=1.9
            D=-22.6
            I=13.6
        if mode == 'HeI':
            A=17.8
            B=-11.0
            C=7.0
            D=-23.2
            I=24.6
        if mode == 'HeII':
            A=14.4
            B=-5.6
            C=1.9
            D=-13.3
            I=54.4
        R=13.6
        a0=0.529e-8
        u=E/I
        res = 1e-14/(u*I**2)*(A*(1.0-1.0/u)+B*(1.0-1.0/u)**2+C*np.log(u)+D*np.log(u)/u)
        if not isinstance(res, float):
            res[E <= I] = 0.0
        else:
            if E <= I:
                res=0
        return res

    def sigmaBEQ(self, T, B, U, N, Q=1.0):
        '''
        Eq. 8 Phys.Rev. A 62 052710 http://journals.aps.org/pra/pdf/10.1103/PhysRevA.62.052710
        Non-relativistic equation
        :param T: the energy of incident electron
        :param B: the binding energy
        :param U: the orbital kinetic energy
        :param N: the electron occupation number
        :param Q: a dipole constant
        :return: cross section in cm^-2
        '''
        t = T/B
        u = U/B
        a0 = 0.52918e-8 # cm
        R = 13.6057 # eV
        S = 4.0*np.pi*a0**2.0*N*(R/B)**2
        n = 1
        res = S/(t+(u+1.0)/n)*(Q*np.log(t)/2.0*(1.0-1.0/t**2)+(2.0-Q)*(1.0-1.0/t-np.log(t)/(t+1.0)))
        if not isinstance(res, float):
            res[T <= B]=0
        else:
            if T<=B:
                res=0
        return res

    def sigmaRBEQ(self, T, B, U, N, Q=1.0):
        '''
        Eq. 21 Phys.Rev. A 62 052710 http://journals.aps.org/pra/pdf/10.1103/PhysRevA.62.052710
        Relativistic equation
        :param T: the energy of incident electron
        :param B: the binding energy
        :param U: the orbital kinetic energy
        :param N: the electron occupation number
        :param Q: a dipole constant
        :return: cross section in cm^-2
        '''
        alpha = 1./137.0365999173
        mec2 = 0.511e6 # electron mass in eV
        tprime = T/mec2
        betat = np.sqrt(1.0-1.0/(1.0+tprime)**2) # Eq. 12
        bprime = B/mec2
        betab = np.sqrt(1.0-1.0/(1.0+bprime)**2) # Eq. 13
        uprime = U/mec2
        betau = np.sqrt(1.0-1.0/(1.0+uprime)**2) # Eq. 14
        t = T/B
        u = U/B
        a0 = 0.52918e-8 # cm
        R = 13.6057 # eV
        n = 1
        res = 4.0*np.pi*a0**2*alpha**4*N / \
              ((betat**2+betau**2+betab**2)*2*bprime) * \
              ( \
                  Q/2.0*(np.log(betat**2/(1.0-betat**2)) - betat**2 - np.log(2.0*bprime)) * \
                  (1.0-1.0/t**2) + \
                  (2.0-Q) * \
                  (1.0-1.0/t-np.log(t)/(t+1.0)*(1.0+2.0*tprime)/(1.0+tprime/2.0)**2+bprime**2/(1.0+tprime/2.0)**2*(t-1.0)/2.0) \
              )
        if not isinstance(res, float):
            res[T <= B]=0
        else:
            if T<=B:
                res=0
        return res

    def HI_ion_e(self, E):
        '''
        HI ionization with an electron.
        :param E: the energy of the electron
        :return: cross section in cm^-2
        '''
        if self.cs['collion'] == 'AR':
            return self.sigma_AR(E, mode='HI')
        if self.cs['collion'] == 'BEQ':
            return self.sigmaBEQ(E, self.const_HI_ion, self.const_HI_ion, 1)
        if self.cs['collion'] == 'RBEQ':
            return self.sigmaRBEQ(E, self.const_HI_ion, self.const_HI_ion, 1)

    def HeI_ion_e(self, E):
        '''
        HeI ionization with an electron.
        :param E: the energy of the electron
        :return: cross section in cm^-2
        '''
        if self.cs['collion'] == 'AR':
            return self.sigma_AR(E, mode='HeI')
        if self.cs['collion'] == 'BEQ':
            return self.sigmaBEQ(E, self.const_HeI_ion, self.const_HeI_ion, 2)
        if self.cs['collion'] == 'RBEQ':
            return self.sigmaRBEQ(E, self.const_HeI_ion, self.const_HeI_ion, 2)

    def HeII_ion_e(self, E):
        '''
        HeII ionization with an electron.
        :param E: the energy of the electron
        :return: cross section in cm^-2
        '''
        if self.cs['collion'] == 'AR':
            return self.sigma_AR(E, mode='HeII')
        if self.cs['collion'] == 'BEQ':
            return self.sigmaBEQ(E, self.const_HeII_ion, self.const_HeII_ion, 1)
        if self.cs['collion'] == 'RBEQ':
            return self.sigmaRBEQ(E, self.const_HeII_ion, self.const_HeII_ion, 1)

    def sigma_SKD(self, E, mode):
        '''
        Hydrogen collisional ionization as in: http://xxx.lanl.gov/pdf/0906.1197v2.pdf
        Equation B5
        :param E: the energy of the electron in eV
        :return:
        '''
        if mode == 'HI':
            A=0.5555
            B=0.2718
            C=0.0001
            Ebin=self.const_HI_ion
            Eexc=self.const_HI_ex
        if mode == 'HeI':
            A=0.1771
            B=-0.0822
            C=0.0356
            Ebin=self.const_HeI_ion
            Eexc=self.const_HeI_ex
        R=self.const_HI_ion
        a0=0.529e-8
        res = 4*a0**2*R/(E+Ebin+Eexc)*(A*np.log(E/R)+B+C*R/E)
        if not isinstance(res, float):
            res[E <= Eexc] = 0.0
        else:
            if E <= Eexc:
                res=0
        return res

    def HI_ex_e(self, E):
        '''
        HI excitation with an electron.
        :param E: the energy of the electron
        :return: cross section in cm^-2
        '''
        if self.cs['collex'] == 'SKD':
            return self.sigma_SKD(E, mode='HI')
        if self.cs['collex'] == 'RBEQ':
            return self.sigmaRBEQ(E, 10.2, 0.5, 1./6.0)

    def HeI_ex_e(self, E):
        '''
        HeI excitation with an electron.
        :param E: the energy of the electron
        :return: cross section in cm^-2
        '''
        if self.cs['collex'] == 'SKD':
            return self.sigma_SKD(E, mode='HeI')
        if self.cs['collex'] == 'RBEQ':
            return self.sigmaRBEQ(E, 21.2, 0.5, 1./10.0)

    def HeII_ex_e(self, E):
        '''
        HeI excitation with an electron.
        :param E: the energy of the electron
        :return: cross section in cm^-2
        '''
        if self.cs['collex'] == 'SKD':
            return self.sigma_SKD(E, mode='HeI')
        if self.cs['collex'] == 'RBEQ':
            return self.sigmaRBEQ(E, 40.82, 0.5, 1./10.0)

    def eedEdt(self, E, ne, T):
        '''
        Rate of energy loss of an electron with energy E in electron plasma with density ne and temperature T
        :param E: in ergs
        :param ne: in cm^-3
        :param T: in K
        :return: in ergs/s
        '''
        omega = c * np.sqrt(1.0 - 511e3**2 / (511e3 + E*6.24e11)**2)
        lnL = 16.3 - np.log10(ne)*1.15 + 3.45*np.log10(T/100.0) # my fit to Spitzer 1965
        return 4. * np.pi * ne * 4.8e-10**4 / 9.1e-28 / omega * lnL

    def sigmakn(self, Eg, e, gamma):
        '''
        Klein-Nishina cross section. Follows the notation of this paper:
        http://www.aanda.org/articles/aa/pdf/2009/21/aa11596-08.pdf
        However we do not use their approximation scheme.
        :param Eg: The initial energy of a photon in ergs.
        :param e: The energy of a photon after the interaction in ergs.
        :param gamma: Lorenz factor of the electron.
        :return: cross section in cm^{-2}
        '''
        Gamma = 4*e*gamma/me/c**2
        eta = e*Eg/(me*c**2)**2
        q = Eg/Gamma/(gamma*me*c**2-Eg)
        G = 2.0*q*np.log(q)+(1.0+2.0*q)*(1.0-q)+2.0*eta*q*(1.0-q)
        G[G < 0] = 0
        G[(4*gamma**2)**-1 > q] = 0
        G[q > 1] = 0
        return 3.0*sigmaT/4.0/e/gamma**2*G

    def sigmaX(self, E, Z, N):
        '''
        Photoionization cross section
        :param E: energy of a photon
        :param Z: Atomic number
        :param N: number of electrons
        :return: cross section in cm^-2
        '''
        Eth, Emax, E0, sigma0, ya, P, yw, y0, y1 = self.lookup[Z, N, :9]
        x = E/E0-y0
        y = np.sqrt(x**2+y1**2)
        F = ((x-1.0)**2+yw**2)*y**(0.5*P-5.5)*(1.0+np.sqrt(y/ya))**(-P)
        F[E<Eth] = 0.0
        return sigma0*F

    def sigmaHex(self, E):
        '''
        Excitation cross section
        :param E: Energy of incident electron in ergs
        :return: cm^-2
        '''
        return (E*6.24e11 > 10.2) * 3.75e-15 * np.log(E/2.*6.24e11) / (E*6.24e11)

    # Shull 1985
    def sigmaHion(self, E):
        '''
        Ionization cross section
        :param E: Energy of incident electron in ergs
        :return: cm^-2
        '''
        return 2.75e-15 * np.log(E/13.6*6.24e11) / (E*6.24e11)

    # CCC fits
    def sigmaHe(self, E, type = 'ion', ion_state='I'):
        '''
        Ionization and excitation cross sections for HeI and HeII
        :param E: Energy of incident electron in ergs
        :return: cm^-2
        '''
        if (type == 'ion') and (ion_state == 'I'):
            return 2.75e-15 * np.log(E/24.6*6.24e11) / (E*6.24e11)
        elif (type == 'ion') and (ion_state == 'II'):
            return 0.75e-15 * np.log(E/54.4*6.24e11) / (E*6.24e11)
        elif (type == 'ex') and (ion_state == 'I'):
            return (E*6.24e11 > 20) * 3.75e-15 * np.log(E/3.*6.24e11) / (E*6.24e11)
        elif (type == 'ex') and (ion_state == 'II'):
            return (E*6.24e11 > 41) * 0.025e-15 * np.log(E/4.6*6.24e11) / (E*6.24e11)
        else:
            return "error"

    # Secondary electron energy distribution
    def rhoE(self, E, ei):
        '''
        Energy of secondary electron
        :param E: Energy of primary electron in ergs
        :param ei: ei in ergs
        :return: Energy of secondary electron in ergs
        '''
        r = np.random.rand(len(E))
        ei_mod = ei+np.log10(E*6.24e11/100)*2/6.24e11
        temp = np.tan(r*np.pi/2.0)*(ei*(1+np.log10(E*6.24e11/ei_mod)))
        temp[temp > E/2.0] = E[temp > E/2.0]/2.0
        return temp
