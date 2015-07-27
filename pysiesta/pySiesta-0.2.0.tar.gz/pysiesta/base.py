# Copyright (C) 2014 Ezequiel Castillo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from re import compile
# Most common units used in SIESTA and supported by pySIESTA.
units = {'energy': ['Ry', 'eV'],
         'length': ['Ang', 'nm', 'Bohr'],
         'force': ['eV/Ang', 'nN'],
         'time': ['s', 'fs']}


#patterns = {'real': r'-?(?:\d+(?:\.\d*)?|\d*\.d+)',
            #'end': r'\s*(?:#.*$|$)',
            #'inputgroup': re.compile(r'#--.*'),
            #'blankline': re.compile(r'^\s*$'),
            #'comment': re.compile(r'#.*'),
            #'finished': re.compile(r'.*End of run.*')}
#patterns['eks'] = re.compile(r'.*E_KS\(eV\) =\s+(%s)' % patterns['real'])
#patterns['etotal'] = re.compile(r'.*Total =\s+(%s)' % patterns['real'])

patterns = {'real': r'-?(?:\d+(?:\.\d*)?|\d*\.d+)',
            'end': r'\s*(?:#.*$|$)',
            'inputgroup': compile(r'#--.*'),
            'blankline': compile(r'^\s*$'),
            'comment': compile(r'#.*'),
            'finished': compile(r'.*End of run.*')}
patterns['eks'] = compile(r'.*E_KS\(eV\) =\s+(%s)' % patterns['real'])
patterns['etotal'] = compile(r'.*Total =\s+(%s)' % patterns['real'])
patterns['endc'] = compile(patterns['end'])

TRUE = ['t', 'true', 'yes', 'tr']
FALSE = ['f', 'false', 'no']

class BaseContainer(object):

    def __getitem__(self, index):
        return self.__dict__[index]

    def __contains__(self, x):
        return x in self.__dict__

    #def __setattr__(self, attr, value):
        #self.__dict__[attr] = value


