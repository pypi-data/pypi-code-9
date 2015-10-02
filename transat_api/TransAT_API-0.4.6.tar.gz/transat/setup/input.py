import glob
import os
import re
import copy
import collections
import sys
import numpy as np
"""

"""


class Phase(object):
    def __init__(self, data, index):
        self.data = data
        self.id = index

    def get_name(self):
        return self.data['name_of_phase'][1:-1]

    def get_index(self):
        return self.id

    def set_name(self, name):
        self.data['name_of_phase'] = '"' + name + '"'

    def set_viscosity(self, visc):
        self.data['visc'] = visc

    def set_viscosity_curve_fit(self, temperature, viscosity, path):
        self.data['visc_method'] = '"curve_fit"'
        self.data['visc_curve_fit_file'] = '"data.dat"'
        np.savetxt(os.path.join(path,'data.dat'), np.array([temperature, viscosity]).T, delimiter=' ')

    def set_density(self, rho):
        self.data['rho'] = rho

    def get_density(self):
        return self.data['rho']

class Input(object):
    def __init__(self, path):
        self.input_file = self._get_input_file(path)
        self.parse()

    @staticmethod
    def _get_input_file(path):
        try:
            return glob.glob(os.path.join(path, 'transat_mb.inp'))[0]
        except:
            print "no input file"
            sys.exit()
            return None

    def write(self):
        lines = []
        for key in self.sections.keys():
            lines.append(key + "\n")
            lines += self.sections[key].write()
            lines.append("/\n")
        with open(self.input_file, 'w') as g:
            g.writelines(lines)

    def parse(self):
        sections = collections.OrderedDict()
        with open(self.input_file, 'r') as f:
            lines = f.readlines()
            for name in self.get_sections_names(lines):
                sections[name] = self.get_section(name, lines)
        self.sections = sections

    def get_sections_names(self, lines):
        names = []
        for l in lines:
            l = l.strip()
            if l.startswith('&'):
                names.append(l)
        return names

    def get_section(self, name, lines):
        data = []
        reading = False
        for l in lines:
            l = l.strip()
            if l == name:
                reading = True
            elif l == "/":
                reading = False
            elif reading:
                data.append(l)
        if name == "&PHASES":
            return PhaseSection(data)
        elif name == "&CONTROL_PARAMETERS":
            return ControlSection(data)
        else:
            return InputSection(data)

    def get_flow_conditions(self):
        return self.sections["&FLOW_CONDITIONS"]

    def get_control_section(self):
        return self.sections["&CONTROL_PARAMETERS"]

    def set_final_time(self, time):
        self.get_flow_conditions().data['STEADY'] = ".false."
        self.get_control_section().set_final_time(time)

    def set_nbr_timestep(self, timestep):
        self.get_control_section().set_nbr_timestep(timestep)


    def set_maxit(self, maxit):
        self.get_flow_conditions().data['STEADY'] = ".true."
        self.get_control_section().set_maxit(maxit)

    def set_maxit_max(self, maxit):
        self.get_control_section().set_maxit_max(maxit)


    def get_phases(self):
        return self.sections["&PHASES"]

class InputSection(object):
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        self.data = collections.OrderedDict()
        for l in data:
            l = l.strip()
            l = l.split("=")
            if len(l) == 2:
                key = l[0].strip()
                d = l[1].strip()
                if self.is_vector(key):
                    name = self.get_vector_name(key)
                    if name not in self.data.keys():
                        self.data[name] = {}
                    self.data[name][self.get_vector_id(key)] = d
                else:
                    self.data[key] = d

    def write(self):
        raw = []
        for key in self.data.keys():
            if type(self.data[key]) is dict:
                for key2 in self.data[key].keys():
                    raw.append(key + "(" + str(key2) + ")" + " = " + str(self.data[key][key2]) + "\n")
            else:
                raw.append(key + " = " + str(self.data[key]) + "\n")
        return raw

    def is_vector(self, key):
        m = re.match(r".+\(([0-9]+)\)", key)
        if m:
            return True
        else:
            return False

    def get_vector_id(self, key):
        m = re.match(r".+\(([0-9]+)\)", key)
        if m:
            return m.group(1)
        else:
            return False

    def get_vector_name(self, key):
        m = re.match(r"(.+)\(([0-9]+)\)", key)
        if m:
            return m.group(1)
        else:
            return False



class ControlSection(InputSection):
    def __init__(self, data):
        super(ControlSection, self).__init__(data)

    def write(self):
        return super(ControlSection, self).write()

    def set_final_time(self, time):
        self.data['ctimet'] = time

    def set_nbr_timestep(self, timestep):
        self.data['NTIMET'] = timestep

    def set_maxit(self, maxit):
        self.data['MAXIT'] = maxit

    def set_maxit_max(self, maxit):
        self.data['MAXIT'] = maxit

class PhaseSection(InputSection):
    def __init__(self, data):
        super(PhaseSection, self).__init__(data)
        self.phases = []
        self._parse_phases()

    def _parse_phases(self):
        phases = []
        attributes = [a for a in self.data.keys() if type(self.data[a]) is dict]
        phase_integers = [a for a in self.data[attributes[0]].keys()]
        for integer in phase_integers:
            data = {}
            for attribute in attributes:
                if type(self.data[attribute]) is dict:
                    data[attribute] = self.data[attribute][integer]
            phases.append(Phase(copy.deepcopy(data), integer))
        self.phases = phases

    def write(self):
        self.data['nphases'] = len(self.phases)
        self.update()
        return super(PhaseSection, self).write()

    def update(self):
        attributes = [a for a in self.data.keys() if type(self.data[a]) is dict]
        for attribute in attributes:
            for phase in self.phases:
                self.data[attribute][phase.id] = phase.data[attribute]


    def get_phase_names(self):
        return [phase.get_name() for phase in self.phases]

    def get_phase(self, name):
        phase = [phase for phase in self.phases if phase.get_name() == name]
        if len(phase) == 0:
            print "No phase found with name "+str(name)
            print self.get_phase_names()
            sys.exit()
            return None
        else:
            return phase[0]
