import consts
from math import sqrt, exp, erf, pi, log
import ConfigParser

class SimParams(object):

    INPUT_PARAMS_LINES = {
        0  : 'r_p',
        2  : 'r_d',
        3  : 'geom',
        5  : 'pressure',
        6  : 'T_g',
        7  : 'T_e',
        8  : 'T_i',
        9  : 'n_e',
        10 : 'phi_p',
        11 : 'phi_d',
        12 : 'dr',
        13 : 'I', #Steady state current
        14 : 'dt',
        15 : 'NSP',
        17 : 'ntimes',
        18 : 'ions',
    }

    GEOM_TYPES = {
        1 : 'spherical',
        2 : 'cylindrical',
    }

    def __init__(self, file_with_params, input_params=True, debye_fraction_user=None):

        self.debye_fraction_user = debye_fraction_user

        if input_params:
            self.params = self.read_params_from_inputparams(file_with_params, debye_fraction_user=self.debye_fraction_user)
        else:
            self.params = self.read_params_from_config(file_with_params)

        self.geometry = SimParams.GEOM_TYPES[int(self.params['geom'])]
        self.cparams = self.compute_cparams(self.params)
        self.sparams = self.compute_sparams(self.params, self.cparams, debye_fraction_user=self.debye_fraction_user)

    @staticmethod
    def read_params_from_inputparams(input_params, **kwargs):
        debye_fraction_user = kwargs.get('debye_fraction_user', None)
        params = dict()
        keys = SimParams.INPUT_PARAMS_LINES.keys()

        with open(input_params) as f:
            lines = f.readlines()

        for iline, line in enumerate(lines):
            if iline in keys:
                new_key = SimParams.INPUT_PARAMS_LINES[iline]
                new_value = float(line.split('!')[0])
                params[new_key] = new_value

        params['sigma_cs'] = 6e-20
        params['VmaxElectronCollision'] = 2.5e6
        params['P_coll'] = 0.02
        params['N_grid_user'] = 1000
        if debye_fraction_user is not None:
            params['debye_fraction_user'] = debye_fraction_user

        return params

    def read_params_from_config(self, config_file):
        cfg = ConfigParser.RawConfigParser()
        cfg.read(config_file)

        params = {}

        params['pressure'] = cfg.getfloat('simulation', 'pressure')
        params['T_g'] = cfg.getfloat('simulation', 'T_g')
        params['T_e'] = cfg.getfloat('simulation', 'T_e')
        params['T_i'] = cfg.getfloat('simulation', 'T_i')
        params['n_e'] = cfg.getfloat('simulation', 'n_e')
        params['r_p'] = cfg.getfloat('simulation', 'r_p')
        params['r_d'] = cfg.getfloat('simulation', 'r_d')
        params['phi_p'] = cfg.getfloat('simulation', 'phi_p')
        params['phi_d'] = cfg.getfloat('simulation', 'phi_d')
        params['sigma_cs'] = cfg.getfloat('simulation', 'sigma_cs')
        params['VmaxElectronCollision'] = cfg.getfloat('simulation', 'VmaxElectronCollision')
        params['P_coll'] = cfg.getfloat('simulation', 'P_coll')
        params['N_grid_user'] = cfg.getfloat('simulation', 'N_grid_user')
        params['NSP'] = cfg.getfloat('simulation', 'NSP')
        if self.debye_fraction_user is not None:
            params['debye_fraction_user'] = self.debye_fraction_user

        return params

    def compute_cparams(self, params):

        cparams = {}
        cparams['omega_pl'] = sqrt(params['n_e'] * consts.elementary_charge**2/(consts.epsilon_0*consts.m_e))
        cparams['debye'] = sqrt(consts.epsilon_0 * consts.k*params['T_e'] / (params['n_e'] * consts.e**2))
        cparams['n_g'] = params['pressure'] / (consts.k * params['T_g'])
        cparams['v_thermal'] = sqrt(consts.k * params['T_e'] / consts.m_e)
        if self.geometry == 'spherical':
            cparams['v_drift'] = params['I'] / (consts.e * 4.0 *
                                                consts.pi * params['r_d']**2 *
                                                params['n_e']) 
        return cparams

    def compute_sparams(self, params, cparams, debye_fraction_user=None):
        sparams = {}

        #cell size assuming dr is one tenth of debye length
        sparams['dr_debye'] = cparams['debye'] / 10.0
        #number of grid points
        sparams['number_of_grid_points_debye'] = (params['r_d'] - params['r_p']) / sparams['dr_debye']

        if debye_fraction_user is not None:
            #debye user fraction
            sparams['dr_debye_user'] = cparams['debye'] / self.debye_fraction_user
            #number of grid points
            sparams['number_of_grid_points_debye_user'] = (params['r_d'] - params['r_p']) / sparams['dr_debye_user']
            #time for electron to travel half of dr_debye_user:
            sparams['dt_thermal_debye_user'] = sparams['dr_debye_user'] / (2 * cparams['v_thermal'])

        #timestep estimated from plasma frequency:
        sparams['dt_omega_pl'] = 0.1 / cparams['omega_pl']
        #timestep estimated from probability of collision in one timestep:
        sparams['dt_coll'] = -1 / (params['sigma_cs'] * params['VmaxElectronCollision'] * cparams['n_g']) * log(1 - params['P_coll'])
        #grid_size as specified by user
        sparams['dr_user'] = (params['r_d'] - params['r_p']) / (params['N_grid_user'] - 1)
        #time for electron to travel half of dr_user:
        sparams['dt_thermal_user'] = sparams['dr_user'] / (2 * cparams['v_thermal'])
        #time for electron to travel half of dr_debye:
        sparams['dt_thermal_debye'] = sparams['dr_debye'] / (2 * cparams['v_thermal'])
        #volume of computational domain:
        if self.geometry == 'spherical':
            sparams['volume_domain'] = 4.0/3.0 * pi * (params['r_d']**3 - params['r_p']**3)
        else:
            sparams['volume_domain'] = pi * (params['r_d']**2 - params['r_p']**2)
        #approximate weight of particle:
        sparams['weight_global'] = sparams['volume_domain'] * params['n_e'] / params['NSP']

        return sparams

    def print_params(self, name):
        self.print_dict(self.params, name)

    def print_cparams(self, name):
        self.print_dict(self.cparams, name)

    def print_sparams(self, name):
        self.print_dict(self.sparams, name)

    @staticmethod
    def print_dict(dictionary, name):
        print '{}:'.format(name)
        for key in sorted(dictionary.keys()):
            print '{} = {:g}'.format(key, dictionary[key])
        print

    #pylint: disable=R0914
    def OML_exact(self, r_sheath, n_sheath, particle):
        params, cparams, sparams = self.params, self.cparams, self.sparams
        assert cparams, sparams

        if particle == 'electron':
            T = params['T_e']
            m = consts.m_e
            ## watch out!!! this needs to be a charge of given particle (positive or negative)
            charge = -consts.e
        elif particle == 'argon_ion':
            T = params['T_i']
            m = 39.948 * consts.atomic_mass
            charge = consts.e
        else:
            raise NotImplementedError('only electron and argon_ion are implemented')

        if self.geometry == 'spherical':

            mean = sqrt(8 * consts.k * T / (pi * m))
            Ss = 4 * pi * r_sheath ** 2

            return n_sheath / 4 * charge * mean * Ss * (1-(1-(params['r_p'] / r_sheath)**2) * \
                   exp((charge * params['phi_p']) / (consts.k * T * ((r_sheath / params['r_p'])**2-1))))

        elif self.geometry == 'cylindrical':
            # this formula is taken from Chen, chapter Electrin probes, page 130:
            # there is uncertainty in which order to apply functions (erf and sqrt),
            # this approach was verified by Granowski
            s = r_sheath
            a = self.params['r_p']
            eta = - charge * self.params['phi_p'] / (consts.k * T)
            Phi = a**2 / (s**2 - a**2) * eta
            F = s/a * erf(sqrt(Phi)) + exp(eta) * (1 - erf(sqrt(eta + Phi)))
            # surface of probe (taking probe 1 m long)
            A_a = 2 * pi * a
            mean = sqrt(8 * consts.k * T / (pi * m))
            j_r = 1.0 / 4.0 * n_sheath * mean
            current = charge * A_a * j_r * F

            return current
        else:
            raise NotImplementedError('only spherical and cylindrical geomteries are implemented')

    def OML_simplified(self, particle):
        params, cparams, sparams = self.params, self.cparams, self.sparams
        assert cparams, sparams

        if particle == 'electron':
            T = params['T_e']
            m = consts.m_e
            ## watch out!!! this needs to be a charge of given particle (positive or negative)
            charge = -consts.e

        elif particle == 'argon_ion':
            T = params['T_i']
            m = 39.948 * consts.atomic_mass
            charge = consts.e
        else:
            raise NotImplementedError('only electron and argon_ion are implemented')

        if self.geometry == 'spherical':
            mean = sqrt(8 * consts.k * T / (pi * m))
            Sp = 4 * pi * params['r_p']**2
            current = params['n_e'] / 4 * charge * mean * Sp * (1 - (charge * params['phi_p']) / (consts.k * T))

            return current
        elif self.geometry == 'cylindrical':
            # again from Chen, page 131
            # surface of probe (taking probe 1 m long)
            A_a = 2 * pi * self.params['r_p']
            mean = sqrt(8 * consts.k * T / (pi * m))
            j_r = 1.0 / 4.0 * self.params['n_e'] * mean
            eta = - charge * self.params['phi_p'] / (consts.k * T)
            F = 2.0 / sqrt(pi) * sqrt(eta + 1)
            current = charge * A_a * j_r * F

            return current

        else:
            raise NotImplementedError('only spherical and cylindrical geomteries are implemented')
