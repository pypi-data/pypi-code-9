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

"""
SIESTA keywords (as extracted from typical fdf.log at version 3.2) All this was
done just to test if a line read from a file is it ok for siesta or not.
"""

import re
from base import BaseContainer, patterns
from os.path import join


def get_rawName(name):
    return re.sub(r'\.|_|-', '', name).lower()


def string_convert(s):
    if re.match(r'-?[0-9]+$', s):
        return int(s)
    elif re.match(patterns['real'], s):
        return float(s)
    else:
        return s


def str_list_to_number_tuple(a_list):
    '''str_list_to_number_tuple(a_list)

    Convert a list of strings to a tuple of numbers whenever possible.

    Example
    -------

    >>> str_list_to_number_tuple(['a', '1', 'b', '2.8'])
    ('a', 1, 'b', 2.8)

    '''

    return tuple(map(string_convert, a_list))


class KeyContainer(BaseContainer):
    """ Key container for siesta Keys"""

    #def __setattr__(self, attr, value):
        #if not attr in self.__dict__:
            #self.__dict__[attr] = value
        #else:
            #self.__dict__[attr].value = value
    #def __setattr__(self, keyObj):
        #if not keyObj.rawName in self.__dict__:
            #self.__dict__[keyObj.rawName] = keyObj
        #else:
            #self.__dict__[keyObj.rawName].value = value

    def addKey(self, keyObj):
        if not keyObj.rawName in self.__dict__:
            self.__dict__[keyObj.rawName] = keyObj
        #else:
            #self.__dict__[keyObj.rawName].value = value

    def __setattr__(self, attr, value):
        if not isinstance(attr, BaseKey):
            self.__dict__[attr].value = value


class BaseKey(object):
    """
    In SIESTA package there are two kinds of keys:

        Block keys: those which are defined in blocks.
        Line keys: Defined with just one line. They may require:
            o Boolean
            o String
            o Integer
            o Float
            o Float and String

    In order to use this class it must be instantiated as:
        > Key(matchobj, keyType, InputGroup)
    where:
        matchobj: a match Object from the re module. the name of the SIESTA key, eg: SystemName
        keyType: one of 'Boolean', 'String', 'Float', 'FloatString', 'Integer'
                 or 'Block'.
        InputGroup: in order to create a nice-looking fdf, a group optional
        attribute may be require. E.g: 'Labels' or 'Atoms & Species'
    This is a base class for the distinct types of siesta keys. You must feed
    it with an matched re object instance."""

    def __init__(self, matchObj, f=None, path=None):
    #def __init__(self, matchObj, ig=None):
        self.name = matchObj.group(1)

        rawName = get_rawName(self.name)
        if not rawName in self._keywords:
            raise KeyError('"%s" is not a valid SIESTA key' % (self.name))
        else:
            self.rawName = rawName

        # BlocKeys have different kind of info from matchObj
        if self.__class__ is not BlockKey:
            self._value = matchObj.group(2)
        else:
            # HERE WE MUST STOP IF WE HAVE EXTERNAL FILE
            exm = re.match(self.__class__._endPatternInputFile, matchObj.group())  # EXternalMatch
            self._value = []
            if exm:
                externalFile = exm.group(1)
                for l in open(join(path, externalFile), 'r'):
                    self._value.append(l)
                # HERE we may add to read file input File, it would be
                # nice ;)
            else:

                #self._value = []
                while True:
                    l = f.readline()
                    m = re.match(BlockKey._endPattern, l)
                    if m:
                        if self.rawName != get_rawName(m.group(1)):
                            raise KeyError('Start block keyword does not match end of block keyword')
                        break
                    mm = re.match(BlockKey._keywords[self.rawName], l)
                    if mm:
                        self._value.append(mm.group().split())
                        #
                        #if re.match(BlockKey._endPatternInputFile, mm):
                        #
                            #break
                        #self.insideBlock.append(mm.groups())
                    # CAUTION HERE!!
                    else:
                        raise IOError("Not a valid match in this group: '%s'" % self.rawName)
            self.extrainit()

        #if ig is not None:
            #self.ig = ig
        #else:
            #self.ig = InputGroup()

        # Now we test if the matched object is a valid siesta key.

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        v = self.checkValue(v)
        self._value = v

    def __repr__(self):
        return str(self.value)


class BooleanKey(BaseKey):
    _pattern = r'\s*([a-zA-Z_\-\.]+)\s+([TF]).*'
    _keywords = ['atomdebugkbgeneration', 'atomsetuponly', 'borncharge',
                 'changekgridinmd', 'coopwrite', 'diagallinone',
                 'diagdivideandconquer', 'diagnoexpert', 'diagparalleloverk',
                 'diagprerotate', 'diaguse2d', 'directphi',
                 'dmallowextrapolation', 'dmallowextrapolation',
                 'dmallowreuse', 'dmfiremixing', 'dmformattedfiles',
                 'dmformattedinput', 'dmformattedoutput', 'dmmixscf1',
                 'dmpulayavoidfirstafterkick', 'dmpulayonfile',
                 'dmrequireenergyconvergence', 'dmrequireharrisconvergence',
                 'dmusesavedm', 'fixauxiliarycell', 'fixspin', 'forceauxcell',
                 'harrisfunctional', 'longoutput', 'mdannealoption',
                 'mdfirequench', 'mdquench', 'mdrelaxcellonly',
                 'mdremoveintramolecularpressure', 'mdusesavecg',
                 'mdusesavexv', 'mdusesavezm', 'mdusestructfile',
                 'mdvariablecell', 'mullikeninscf', 'naiveauxiliarycell',
                 'neglnonoverlapint', 'noncollinearspin', 'occupationfunction',
                 'onchemicalpotential', 'onchemicalpotentialuse',
                 'onusesavelwf', 'opticalcalculation', 'optimbroyden',
                 'outputstructureonly', 'paofilter', 'paofixsplittable',
                 'paokeepfindpbug', 'paonewsplitcode', 'paooldstylepolorbs',
                 'paosoftdefault', 'paosplittailnorm', 'reinitialisedm',
                 'reparametrizepseudos', 'restrictedradialgrid',
                 'savedeltarho', 'saveelectrostaticpotential', 'savehs',
                 'saveinitialchargedensity', 'saveioniccharge',
                 'saveneutralatompotential', 'saverho', 'savetotalcharge',
                 'savetotalpotential', 'scfmustconverge',
                 'scfreadchargenetcdf', 'scfreaddeformationchargenetcdf',
                 'simulatedoping', 'singleexcitation', 'slabdipolecorrection',
                 'spinpolarized', 'usenewdiagk', 'userbasis',
                 'userbasisnetcdf', 'usesavedata', 'usestructfile',
                 'vnafilter', 'writebands', 'writecoorcerius',
                 'writecoorinitial', 'writecoorstep', 'writecoorxmol',
                 'writedenchar', 'writedm', 'writedmhistorynetcdf',
                 'writedmhshistorynetcdf', 'writedmhsnetcdf', 'writedmnetcdf',
                 'writeeigenvalues', 'writeforces', 'writeionplotfiles',
                 'writekbands', 'writekpoints', 'writemdhistory',
                 'writemdxmol', 'writewavedebug', 'writewavefunctions',
                 'writexml', 'xmlabortonerrors', 'xmlabortonwarnings',
                 'xmlwrite', 'zmcalcallforces', 'mdbroydencycleonmaxit']

    #def __init__(self, matchObj, ig=None):
        ##BaseKey.__init__(self, matchObj, ig)
        #pass

    def checkValue(self, v):
        v = v.lower()
        if v in TRUE:
            return 'T'
        elif v in FALSE:
            return 'F'
        else:
            raise SiestaError('Argument for %s object must be either "true" or "false"' % self.__class__.__name__)


class StringKey(BaseKey):
    _pattern = r'\s*([a-zA-Z_\-\.]+)\s+([a-zA-Z]+)\s*(?:#.*$|$)'
    _keywords = ['atomcoorformatout', 'atomiccoordinatesformat', 'mdtypeofrun',
                 'mmunitsdistance', 'mmunitsenergy', 'onfunctional',
                 'paobasissize', 'paobasistype', 'solutionmethod',
                 'systemlabel', 'systemname', 'xcauthors', 'xcfunctional',
                 'zmunitsangle', 'zmunitslength']

    #def __init__(self, matchObj, ig=None):
        ##BaseKey.__init__(self, matchObj, ig)
        #pass

    def checkValue(self, v):
        if re.match(r'[a-zA-Z]+', v):
            return v
        else:
            raise SiestaError('Argument for %s object must be a string' % self.__class__.__name__)


class IntegerKey(BaseKey):
    _pattern = r'\s*([a-zA-Z_\-\.]+)\s+(\d+)[^\.0-9].*'
    _keywords = ['allocreportlevel', 'dmnumberbroyden', 'dmnumberkick',
                 'dmnumberpulay', 'fdfdebug', 'maxscfiterations', 'mdfcfirst',
                 'mdfclast', 'mdfinaltimestep', 'mdinitialtimestep',
                 'mdnumcgsteps', 'meshsubdivisions', 'numberofatoms',
                 'numberofeigenstates', 'numberofspecies',
                 'onchemicalpotentialorder', 'onmaxnumiter', 'processorgridx',
                 'processorgridy', 'processorgridz', 'writemullikenpop', 'mdbroydenhistorysteps']

    #def __init__(self, matchObj, ig=None):
        ##BaseKey.__init__(self, matchObj, ig)
        #pass

    def checkValue(self, v):
        if isinstance(v, int):
            return str(v)
        elif re.match(r'\d+', v):
            return v
        else:
            raise SiestaError('Argument for %s object must be an integer' % self.__class__.__name__)


class FloatKey(BaseKey):
    _pattern = r'\s*([a-zA-Z_\-\.]+)\s+([\+-]?(?:\d+(?:\.\d*)|\d*\.d+)(?:E[\+-]\d+)?)\s*(?:#.*$|$)'
    _keywords = ['diagmemory', 'dmkickmixingweight', 'dmmixingweight',
                 'dmoccupancytolerance', 'dmtolerance', 'netcharge', 'onetol',
                 'paosoftinnerradius', 'paosoftpotential', 'paosplitnorm',
                 'paosplitnormh', 'rmaxradialgrid', 'mdbroydeninitialinversejacobian']

    #def __init__(self, matchObj, ig=None):
        ##BaseKey.__init__(self, matchObj, ig)
        #pass

    def checkValue(self, v):
        if re.match(patterns['real'], v):
            return v
        elif isinstance(v, float):
            return str(v)
        else:
            raise SiestaError('Argument for %s object must be an float' % self.__class__.__name__)


class FloatStringKey(BaseKey):
    _pattern = r'\s*([a-zA-Z_\-\.]+)\s+([\+-]?(?:\d+(?:\.\d*)?|\d*\.d+)(?:E[\+-]\d+)?)\s+(\w+(?:[\*/]\w+)?(?:\*\*\d)?).*'
    _keywords = ['basispressure', 'dmenergytolerance', 'dmharristolerance',
                 'electronictemperature', 'filtercutoff', 'filtertol', 'kbrmax',
                 'latticeconstant', 'maxbonddistance', 'mdbulkmodulus',
                 'mdfcdispl', 'mdinitialtemperature', 'mdlengthtimestep',
                 'mdmaxcgdispl', 'mdmaxforcetol', 'mdmaxstresstol', 'mdnosemass',
                 'mdparrinellorahmanmass', 'mdtargetpressure',
                 'mdtargettemperature', 'mdtaurelax', 'meshcutoff', 'mmcutoff',
                 'onchemicalpotentialrc', 'onchemicalpotentialtemperature',
                 'oneta', 'onetaalpha', 'onetabeta', 'onrclwf', 'paoenergyshift',
                 'rcspatial', 'warningminimumatomicdistance', 'wfsenergymax',
                 'wfsenergymin', 'zmforcetolangle', 'zmforcetollength',
                 'zmmaxdisplangle', 'zmmaxdispllength']

    def __init__(self, matchObj, f=None, path=None):
        BaseKey.__init__(self, matchObj, path=path)
        self.unit = matchObj.group(3)

    def checkValue(self, v):
        m = re.match(r'([\+-]?(?:\d+(?:\.\d*)?|\d*\.d+)(?:E[\+-]\d+)?)\s+(\w+(?:[\*/]\w+)?(?:\*\*\d)?)', v)
        if m:
            self.unit = m.group(2)
            return m.group(1)
        else:
            raise SiestaError('Argument for %s object must be an float followed by string' % self.__class__.__name__)

    def __repr__(self):
        return self._value + ' ' + self.unit


class BlockKey(BaseKey):
    """
    Besides passing matchObj instance, you must supply the file object
    currently processed.

    Example:
        result = []
        with open(file, 'r') as f:
            for l in f:
                m = re.match(BlockKey._pattern, l)
                if m:
                    result.append(BlockKey(m, f))
    """

    _pattern = r'\s*%block\s+(\S+).*'
    #_endPatternInputFile = r'.*<\s+(\w+(?:\.|_)).*'
    _endPatternInputFile = r'.*<\s+([\w\.]{0,256}).*'
    _endPattern = r'\s*\%endblock\s+(\S+).*'
    _keywords = {'atomiccoordinatesandatomicspecies': r'\s*({r})\s+({r})\s+({r})\s+(\d+){e}'.format(r=patterns['real'], e=patterns['end']),
                 'atomiccoordinatesorigin': r'\s*({r})\s+({r})\s+({r}){e}'.format(r=patterns['real'], e=patterns['end']),
                 'chemicalspecieslabel': r'\s*(\d+)\s+(\d+)\s+(\S+){e}'.format(e=patterns['end']),
                 'geometryconstraints': r'\s*(?:(position)|(otracosa))(?(1)\s+\w+\s+-?\d+\s+to\s+(-?\d+)|(?!)){e}'.format(e=patterns['end']),
                 'kgridmonkhorstpack': r'\s*(\d+)\s+(\d+)\s+(\d+)\s+({r}){e}'.format(r=patterns['real'], e=patterns['end']),
                 # Zmatrix regex was not fully tested
                 'zmatrix': r'\s*(?:(?:(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+({r}|\w+)\s+({r}|\w+)\s+({r}|\w+)\s+([01])\s+([01])\s+([01]))|(?:(\d+)\s+({r})\s+({r})\s+({r})\s+([01])\s+([01])\s+([01]))|(?:\b(molecule|cartesian|constants|variables|constraints)\b|\w+\s+{r}))(?:{e}|.*)'.format(r=patterns['real'], e=patterns['end']),
                 'latticevectors': r'\s*({r})\s+({r})\s+({r}){e}'.format(r=patterns['real'], e=patterns['end']),
                 'projecteddensityofstates': r'\s*({r})\s+({r})\s+({r})\s+(\d+)\s+([a-zA-Z]+){e}'.format(r=patterns['real'], e=patterns['end'])}
    _outFmt = \
        {'chemicalspecieslabel': '%3i%5i%10s\n',
        'kgridmonkhorstpack': '%4i%4i%4i%8.1f\n',
        'latticevectors': '%12.4f%12.4f%12.4f\n',
        'atomiccoordinatesorigin': '%12.4f%12.4f%12.4f\n',
        'zmatrixmolecule': '%4i%4i%4i%4i%12.4f%12.4f%12.4f%3i%3i%3i%4s\n',
        'zmatrixcartesian': '%4i%12.4f%12.4f%12.4f%3i%3i%3i\n'}


    def extrainit(self):

        if self.rawName == 'atomiccoordinatesandatomicspecies':
            self.coords = [l for l in self._value if len(l) >= 3]
            pass

        if self.rawName == 'atomiccoordinatesorigin':
            pass

        if self.rawName == 'chemicalspecieslabel':
            pass

        if self.rawName == 'geometryconstraints':
            pass

        if self.rawName == 'kgridmonkhorstpack':
            pass

        if self.rawName == 'latticevectors':
            pass

        if self.rawName == 'zmatrix':
            self.cartesianCoords = []
            self.moleculeCoords = []
            for l in self._value:
                for k in ['cartesian', 'molecule']:
                    if l[0] == k:
                        g = k
                if len(l) >= 3:
                    # This is a coordinate line
                    if g == 'cartesian':
                        self.cartesianCoords.append(l)
                    elif g == 'molecule':
                        self.moleculeCoords.append(l)
            self.coords = self.cartesianCoords + self.moleculeCoords
        pass

    #@property
    #def value(self):
        #return self._value

    #@value.setter
    #def value(self, v):
        #v = self.checkValue(v)
        #self._value = v

    def _writeToFile(self, f):
        "Write SIESTA Key data to file."

        # HEAD
        f.write('%block {}\n'.format(self.name))

    def __getitem__(self, index):
        return self._value[index]

    def __repr__(self):
        """When you say:

        >>> A = BlockKey()
        >>> print A

        It will print the string for SIESTA input."""

        _HEAD = '%block {}\n'.format(self.name)
        _TAIL = '%endblock {}\n'.format(self.name)

        lines = self.value[:]
        s = _HEAD
        if self.iszmatrix():
            fmtKey = self.get_zmatrix()
            s += ''.join(lines.pop(0)) + '\n'
        else:
            fmtKey = self.rawName

        for l in lines:
            s += BlockKey._outFmt[fmtKey] % str_list_to_number_tuple(l)
        s += _TAIL

        return s

    def checkValue(self, v):
        pass

    def iszmatrix(self):
        """ Return True if zmatrix key is defined."""
        return self.rawName == 'zmatrix'

    def get_zmatrix(self):
        ''' Return a list containg 'cartesian', 'molecule' or both. Only one of
        the two supported atm. '''
        if self.cartesianCoords:
            return 'zmatrixcartesian'
        elif self.moleculeCoords:
            return 'zmatrixmolecule'


keyTypes = [BooleanKey, FloatKey, FloatStringKey, StringKey, IntegerKey,
            BlockKey]

mandatoryKeys = ['numberofspecies', 'numberofatoms', 'chemicalspecieslabel',
                 ['atomiccoordinatesandatomicspecies', 'zmatrix']]
