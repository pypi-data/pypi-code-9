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

__all__=['atno_to_symbol', 'symbol_to_atno', 'VdW_Radii_Symbol',
         'get_distance', 'Atom', 'Molecule', 'ZMatrix', 'Cell', 'Axis']

import os
import re
import render
import types
import numpy as np

from itertools import product

genericAtom = {'symbol': 'Xx',
               'pos': np.zeros(3),
               'label': 'generic'}

atno_to_symbol = \
        {-1: 'Du',
         0: 'Xx',
         1: 'H',
         2: 'He',
         6: 'C',
         7: 'N',
         8: 'O',
        15: 'P',
        16: 'S',
        26: 'Fe',
        29: 'Cu',
        46: 'Pd',
        47: 'Ag',
        78: 'Pt',
        79: 'Au'}

symbol_to_atno = dict([[v,k] for k,v in atno_to_symbol.items()])

atno_to_mass = \
        {1: 1.00794,
         2: 4.002602,
         6: 12.0107,
         7: 14.0067,
         8: 15.9994,
        15: 30.973762,
        16: 32.065,
        26: 55.845,
        29: 63.546,
        46: 106.42,
        47: 107.8682,
        78: 195.084,
        79: 196.966569}

VdW_Radii = \
        {1: 0.37,
         2: 0.32,
         6: 0.77,
         7: 0.75,
         8: 0.73,
        15: 1.95,
        16: 1.02,
        26: 0.75,
        29: 1.38,
        46: 2.05,
        47: 2.10,
        78: 1.28,
        79: 1.44
         }

VdW_Radii_Symbol = {atno_to_symbol[atno]: radius for atno, radius in
                    VdW_Radii.items()}

# From the now-no-existing package eTools.
def get_dirs(a_dir=None):
    if not a_dir:
        a_dir = os.curdir
    files = os.listdir(a_dir)
    return [ f for f in files if os.path.isdir(os.path.join(a_dir, f)) ]

def sort_list_of_strings(a_list):
    return sorted(a_list, key=lambda x:[int(y) for y in x.split('.')])

def is_mono_dim_list(a_list):
    for elem in a_list:
        if isinstance(elem, types.ListType):
            return False
    return True

def get_pos_from_atom(*args):
    check_arg_atoms(args)
    return [atom.pos for atom in args]

def get_distance(at1, at2):
    pos1, pos2 = get_pos_from_atom(at1, at2)
    return np.linalg.norm(pos1 - pos2)

def get_angle_from_vec(vec1, vec2):
    angle = np.arccos(np.inner(vec1, vec2)/
                      (np.linalg.norm(vec1)*np.linalg.norm(vec2)))

    return np.rad2deg(angle)

def get_angle(at1, at2, at3):
    pos1, pos2, pos3 = get_pos_from_atom(at1, at2, at3)

    vec1 = pos1 - pos2
    vec2 = pos3 - pos2

    return get_angle_from_vec(vec1, vec2)

def get_dihedral(at1, at2, at3, at4):
    pos1, pos2, pos3, pos4 = get_pos_from_atom(at1, at2, at3, at4)

    vec1 = pos1 - pos2
    vec2 = pos3 - pos2
    vec3 = - vec2
    vec4 = pos4 - pos3

    n1 = np.cross(vec1.reshape((1,3)), vec2.reshape((1,3)))
    n2 = np.cross(vec3.reshape((1,3)), vec4.reshape((1,3)))

    return get_angle_from_vec(n1, n2)

def get_point_plane_distance(point, plane):
    x0, y0, z0 = point
    a, b, c = plane
    return (a*x0 + b*y0 + c*z0)/(np.sqrt(a**2+b**2+c**2))
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def check_arg_atoms(*args):
    if len(args) is 1:
        if isinstance(args[0], (types.ListType, types.TupleType)):
            for elem in args[0]:
                if not isinstance(elem, Atom):
                    raise TypeError('%s is not an Atom instance' % (elem,))
            return args[0]
        elif not isinstance(args[0], Atom):
            raise TypeError('Not Atom Instance')
        return args
    else:
        for elem in args:
            if not isinstance(elem, Atom):
                raise TypeError('Not Atom Instance')
        return args

def get_stretching(path=None, infile=None, outfile=None):
    """
    Create xyzMovie file which contains all frames of elongation.

    Options:
        path: location of all steps folder.
        infile: The file name where to look at each subfolder.
        outfile: The file name at ./path/outfile.
    """

    import os
    import shutil

    if path is None:
        path = os.curdir
    if infile is None:
        infile = 'siesta.ANI'
    if outfile is None:
        outfile = 'xyzMovie.xyz'

    os.chdir(path)

    dirs = sorted(filter(os.path.isdir, os.listdir(path)))

    with open(outfile, 'w') as fout:
        for dir_ in dirs:
            fname = dir_+'/'+infile
            with open(fname, 'r') as fin:
                for line in fin:
                    fout.write(line)

def get_coordinatesFromSpherical(coords, rpa):
    '''Given a coord = (x0,y0,z0) of a first atom and rpa =
    (rho,polar,azimuthal) of second atom, return the coordinates (x1,y1,z1) of
    the second atom.'''
    x0, y0, z0 = coords
    rho, theta, phi = rpa
    x1 = rho * np.sin(theta) * np.cos(phi) + x0
    y1 = rho * np.sin(theta) * np.sin(phi) + y0
    z1 = rho * np.cos(theta) + z0
    return np.array([x1, y1, z1])

def mix_List(*args, **kwds):
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def check_3x1(pos):
    if not isinstance(pos, np.ndarray):
        pos = np.array(pos, dtype=float)
    if pos.size == 3:
        pos = pos.reshape((3,1))
    return pos

class Connection(object):

    def get_atoms_from_list(self, list_):

        self.atoms = []
        #atoms = []

        if len(list_) is 1:
            list_ = list_[0]

        #if type_ is 'Bond':
            #l = 2
        #elif type_ is 'Angle':
            #l = 3
        #elif type_ is 'Dihedral':
            #l = 4

        for elem in list_:
            if isinstance(elem, Atom):
                self.atoms.append(elem)
                #atoms.append(elem)
            elif isinstance(elem, Vertex):
                self.atoms.append(elem.vertex)
                #atoms.append(elem.vertex)

        #return atoms

    def order_byFirstAtom(self, atom):
        if not isinstance(atom, Atom):
            raise IOError('Argument must be Atom instance.')
        if not atom in self.atoms:
            raise NameError('Atom %s not in %s' % (atom, self))
        #if not self.connections[0] == atom or not self.connections[-1] == atom:
            #raise NameError('Neither first nor last atom is atom %s' % (atom,))
        if self.atoms[0] == atom:
            #list_ = self.connections
            pass
        elif self.atoms[-1] == atom:
            self.atoms = self.atoms[::-1]
        else:
            raise NameError('Neither first nor last atom is atom %s' % (atom,))
        return self

    def __getitem__(self, index):
        return self.atoms[index]

    def __contains__(self, atom):
        return atom in self.atoms
    def __len__(self):
        return len(self.atoms)

    def __eq__(self, other):
        return self.atoms == other.atoms[::-1]

    def __hash__(self):
        return hash(repr(sorted(self.atoms)))


class ConnectionList(object):

    def __init__(self, connections=None):
        if not connections:
            connections = []

        self.connections = connections

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_duplicates(self):
        self.connections = [connection for connection in set(self.connections)]

    def filter_byAtom(self, *args):
        if len(args) == 1 and isinstance(args[0], types.ListType):
            atoms = args[0]
        else:
            atoms = args
        check_arg_atoms(atoms)
        list_ = self.connections[:]
        for atom in atoms:
            list_ = filter(lambda connection: atom in connection, list_)

        return list_
    def __len__(self):
        return len(self.connections)

    def __getitem__(self, index):
        return self.connections[index]


class Bond(Connection):
    def __init__(self, *args):

        self.get_atoms_from_list(args)
        at1, at2 = self.atoms


        #vec1 = self.atoms[0].pos - self.atoms[1].pos

        self.distance = get_distance(at1, at2)

    def set_angle(self):
        pass

    def get_polar(self):
        angle = np.arccos(np.abs(self.atoms[1].pos[2] -
                       self.atoms[0].pos[2])/self.distance)
        return np.rad2deg(angle)

    def get_azimuthal(self):
        angle = np.arctan(np.abs(self.atoms[1].pos[1] - self.atoms[0].pos[1]) /
                          np.abs(self.atoms[1].pos[0] - self.atoms[0].pos[0]))
        return np.rad2deg(angle)
    def __add__(self):
        pass

    def __radd__(self):
        pass

    def __sub__(self):
        pass

    def __rsub__(self):
        pass

    def __repr__(self):
        return '{name} {at1} {at2} = {distance} Angstroms'.format(name=self.__class__.__name__,
                at1=self.atoms[0], at2=self.atoms[1], distance=self.distance)


class Angle(Connection):
    def __init__(self, *args):

        self.get_atoms_from_list(args)

        at1, at2, at3 = self.atoms

        #if len(args) is 1:
            #self.get_atoms_from_list(args[0])
        #elif len(args) is 3:
            #self.get_atoms_from_list(args)
        #else:
            #raise IOError('A list of three atom or three atoms needed')

        #vec1 = self.atoms[0].pos - self.atoms[1].pos
        #vec2 = self.atoms[2].pos - self.atoms[1].pos

        self.angle = get_angle(at1, at2, at3)

    def set_angle(self):
        pass

    def get_dihedralFromDummyAtom(self):
        at1, at2, at3 = self.atoms
        pos2 = get_pos_from_atom(self.atoms[2])[0]
        #dpos = [0,0,1] + pos2
        dummy = Atom('Du', [0,0,1] + pos2)
        import pdb; pdb.set_trace() # BREAKPOINT
        #return get_dihedral(at1, at2, at3, dummy)
        return get_dihedral(at1, at2, dummy, at3)
        #return get_dihedral(at1, dummy, at2, at3)
        #return get_dihedral(dummy, at1, at2, at3)

    def __add__(self):
        pass

    def __radd__(self):
        pass

    def __sub__(self):
        pass

    def __rsub__(self):
        pass

    def __repr__(self):
        return '{name} {at1} {at2} {at3} = {angle} deg'.format(name=self.__class__.__name__,
                at1=self.atoms[0], at2=self.atoms[1], at3=self.atoms[2], angle=self.angle)


class Dihedral(Connection):
    def __init__(self, *args):

        self.get_atoms_from_list(args)

        at1, at2, at3, at4 = self.atoms

        self.dihedral = get_dihedral(at1, at2, at3, at4)

    def __add__(self):
        pass

    def __radd__(self):
        pass

    def __sub__(self):
        pass

    def __rsub__(self):
        pass

    def __repr__(self):
        return '{name} {at1} {at2} {at3} {at4} = {dihedral} deg'.format(
            name=self.__class__.__name__, at1=self.atoms[0], at2=self.atoms[1],
            at3=self.atoms[2], at4=self.atoms[3], dihedral=self.dihedral)


class Atom(object):

    atomCounter = -1

    """ Atom class. Must be instantiated as:
        an_atom = Atom(symbol, x, y, z)
        where symbol is either the atomic number or the atom name.
        x, y and z are the atomic coordinates."""

    def __init__(self, symbol=None, pos=None, atno=None, label=None,
                 charge=None):

        Atom.atomCounter += 1

        if pos is None:
            pos = genericAtom['pos']
        if not symbol and not atno:
            symbol = genericAtom['symbol']
        if symbol is None and atno is None:
            symbol = genericAtom['symbol']
        elif not atno is None:
            symbol = atno_to_symbol[atno]

        self.symbol = symbol
        self.atno = symbol_to_atno[self.symbol]
        self.pos = pos
        self.label = str(Atom.atomCounter)
        self.mass = atno_to_mass[self.atno]
        self.charge = charge

    def _get_symbol(self):
        return self._symbol

    def _set_symbol(self, symbol):
        if re.match(r'[a-zA-Z]+.*', symbol):
            self._symbol = symbol
            self._atno = symbol_to_atno[symbol]
    symbol = property(_get_symbol, _set_symbol)

    def _get_position(self):
        return self._pos

    def _set_position(self, pos):
        self._pos = check_3x1(pos)
    pos = property(_get_position, _set_position)

    def _get_atomNumber(self):
        return self._atno

    def _set_atomNumber(self, atno):
        if not isinstance(atno, int):
            raise ValueError('Argument must be an integer.')
        self._atno = atno
        self._symbol = atno_to_symbol[atno]
    atno = property(_get_atomNumber, _set_atomNumber)

    def __add__(self, vec):
        vec = check_3x1(vec)
        #self.pos += vec
        self._set_position(self.pos + vec)
        return self

    def __sub__(self, vec):
        self._set_position(self.pos - vec)
        #self.pos = self.pos - vec

    def __radd__(self, an_object):
        self.__add__(an_object)

    def __rsub__(self, an_object):
        self.__sub__(an_object)

    def __repr__(self):
        return '{label}-{sym}'.format(sym=self.symbol, label=self.label)
        #return '{name}({sym!r}, {pos}, {index})'.format(
            #name=self.__class__.__name__, sym=self.symbol,
            #pos=self.pos, index=self.index)


class Molecule(object):

    moleculeCounter = -1

    def __init__(self, name='Generic', atoms=None, fromFile=None, fromList=None, cwd=None):

        Atom.atomCounter = -1
        Molecule.moleculeCounter += 1

        self.label = str(Molecule.moleculeCounter)
        if name == 'Generic':
            self.name = 'Generic' + self.label
        else:
            self.name = name

        if cwd is None:
            self.cwd = os.getcwd()
        else:
            self.cwd = cwd

        if atoms:
            self.atoms = atoms
        else:
            self.atoms = []

        self.species = {}

        if fromFile:
            self.load_fromFile(fromFile)

        if fromList:
            self.load_fromList(fromList)

        #self.get_connections()
        #self.get_structure()

    def update_mol(self):
        self.get_connections()
        self.get_structure()

    def add_atom(self, atom):
        self.atoms.append(atom)
        if atom.symbol not in self.species:
            self.species[atom.symbol] = len(self.species) + 1
        atom.specieNo = self.species[atom.symbol]

    def remove_atom(self, i):
        print 'Deleting {atom}'.format(atom=self.atoms[i])
        self.atoms.pop(i)
        self.update_mol()

    def load_fromFile(self, filename, filetype=None):
        if filetype is None:
            ft = os.path.splitext(filename)[1]
        else:
            ft = filetype
        with open(filename, 'r') as f:
            lines = f.readlines()

        self.load_fromList(lines, filetype=ft)

    def load_fromList(self, list_, filetype='.xyz'):

        if filetype == '.xyz':
            firstAtLine = 2
            lastAtLine = None
            nameCol = 0
            firstPosCol = 1
            lastPosCol = 4
            toAng = 1
        elif filetype == '.gro':
            firstAtLine = 2
            lastAtLine = -1
            nameCol = 1
            firstPosCol = 3
            lastPosCol = 6
            toAng = 10
        elif filetype == 'siestaEner':
            firstAtLine = 0
            lastAtLine = None
            nameCol = 3
            firstPosCol = 0
            lastPosCol = 3
            toAng = 1
        elif filetype == 'xyzFromSiestaOut':
            firstAtLine = 0
            lastAtLine = None
            firstPosCol = 1
            lastPosCol = 4
            # Change Bohr in Angstroms
            toAng = 1


        #with open(filename, 'r') as f:

        lines = [l.split() for l in list_[firstAtLine:lastAtLine]]
        lines = map(list, zip(*lines))
        namelst = lines[nameCol]
        lines = [map(float, a_list) for a_list in lines[firstPosCol:lastPosCol]]
        posarr = np.array(lines)*toAng
        posarr = posarr.T

        for i, pos in enumerate(posarr):
            self.add_atom(Atom(namelst[i], pos))

    def write_toString(self,fmt='xyz'):
        ss = ''
        ss += '{tot_at:5d}\n\n'.format(tot_at=len(self.atoms))
        for atom in self.atoms:
            ss += '{sym:3s}{x:13.8f}{y:13.8f}{z:13.8f}\n'.format(
                        sym=atom.symbol, x=atom.pos.item(0), y=atom.pos.item(1),
                        z=atom.pos.item(2))
        return ss

    def write_toFile(self, filename='default.xyz', fmt='xyz'):
        with open(os.path.join(self.cwd, filename), 'w') as fout:
            fout.write(self.write_toString())

    def get_dipoleMoment(self):
        muv = np.zeros(3).reshape((3,1))
        for atom in self.atoms:
            muv += atom.pos * atom.charge
        self.muv = muv
        self.mu = np.linalg.norm(muv) / 0.20819434
        return [self.mu, self.muv]

    def get_geometryCenter(self):
        asum = np.zeros(3).reshape((3,1))
        for atom in self.atoms:
            asum += atom.pos
        asum /= len(self.atoms)
        return asum

    def load_propertyFromFile(self, prop, filename):
        f = open(filename, 'r')
        for atom in self.atoms:
            try:
                q = float(f.readline())
                if not q:
                    raise Exception
            except:
                raise Warning('THIS IS A WARNING XD!!')
            setattr(atom, prop, q)
            #if prop == 'charge':
                #pass
            #else:
                #f.close()
                #raise NameError('Unknown property %s' % (prop,))

    def get_species(self):
        species = list(set([atom.symbol for atom in self.atoms]))
        self.species = {i+1: s for i, s in enumerate(species)}
        return species
        #return {i+1:specie for i, specie in enumerate(species)}
        #return OrderedDict({i+1:specie for i, specie in enumerate(species)})

    def get_connections(self):
        connections = {}
        for atom in self.atoms:
            lconnections = []
            ddist = self.get_closest_atom(atom, dist=True)
            for close_atom in ddist:
                pair_dist = VdW_Radii[atom.atno] + VdW_Radii[close_atom.atno]
                if ddist[close_atom] < pair_dist:
                    lconnections.append(close_atom)
            connections[atom] = lconnections
        self.connections = connections
        return connections

    def get_structure(self):
        G = Graph(adjList=self.connections)
        bonds = ConnectionList()
        angles = ConnectionList()
        dihedrals = ConnectionList()
        not_bonded = ConnectionList()
        for vertex1 in G.vertices:
            for vertex2 in G.vertices:
                connections = G.find_all_paths(vertex1, vertex2)
                if connections:
                    if len(connections[0]) > 1:
                        for connection in connections:
                            if len(connection) == 2:
                                #bonds.append(Bond(connection))
                                at1, at2 = G.get_atomsFromVertices(connection)
                                bonds.add_connection(Bond(at1, at2))
                            elif len(connection) == 3:
                                at1, at2, at3 = G.get_atomsFromVertices(connection)
                                angles.add_connection(Angle(at1, at2,
                                                            at3))
                            elif len(connection) == 4:
                                at1, at2, at3, at4 = G.get_atomsFromVertices(connection)
                                dihedrals.add_connection(Dihedral(at1, at2, at3,
                                                                at4))
                            #else:
                                #not_bonded.add_connection(G.get_atomsFromVertices(connection))

        for type_ in [bonds, angles, dihedrals]:
            type_.remove_duplicates()

        self.bonds = bonds
        self.angles = angles
        self.dihedrals = dihedrals
        self.not_bonded = not_bonded

    def get_closest_atom(self, atom, dist=False):
        rest = self.atoms[:]  # Make a copy.
        rest.remove(atom)
        closest_list = {an_atom: get_distance(atom, an_atom) for an_atom in rest}
        if dist:
            return closest_list
        else:
            return sorted(closest_list)

    def get_largestLengthInDirection(self, d):
        if d not in ('x', 'y', 'z'):
            raise IOError('Possible directions currently supported are "x", "y" or "z"')
        if d is 'x':
            c = 0
        elif d is 'y':
            c = 1
        elif d is 'z':
            c = 2

        allDelta = abs(np.array([self[i].pos - self[j].pos for i in xrange(len(self)) for j
                           in xrange(i,len(self))]))

        return max(allDelta.T[0][c])

    def replicate_fromCell(self, cell, n=[0,0,0]):
        molTmp = Molecule()
        for p in cell.get_latticePoints(n):
            for a in self.atoms:
                if not np.array_equal(p, np.array([0,0,0])):
                    pos = a.pos + check_3x1(p)
                    molTmp.add_atom(Atom(symbol=a.symbol, pos=pos))
        self + molTmp

    def _filter(self, func):
        return filter(func, self.atoms)

    def by_symbol(self, symbol):
        return Molecule(atoms=self._filter(lambda a: a.symbol == symbol))

    def by_xrange(self, xmin, xmax):
        return Molecule(atoms=self._filter(lambda a: xmin <= a.pos[0] <= xmax))

    def by_yrange(self, ymin, ymax):
        return Molecule(atoms=self._filter(lambda a: ymin <= a.pos[1] <= ymax))

    def by_zrange(self, zmin, zmax):
        return Molecule(atoms=self._filter(lambda a: zmin <= a.pos[2] <= zmax))
        #return self._filter(lambda a: zmin <= a.pos[2] <= zmax)
        #return Molecule(atoms=atoms)

    def reflect(self, a, b, c, d):
        '''
        Reflect all atom position through a plane whose equation is:
            ax + by + cz = d
        '''

        n2 = a**2 + b**2 + c**2
        e = np.zeros((len(self) ,3))

        for atom in self.atoms[:]:
            T = (a*atom.pos[0] + b*atom.pos[1] + c*atom.pos[2] - d) / n2
            x = atom.pos[0] - 2*T*a
            y = atom.pos[1] - 2*T*b
            z = atom.pos[2] - 2*T*c
            atom.pos = [x, y, z]

        return self

    def rotate(self, ax=None, angle=None):
        '''
        Rotate 'angle' degrees all atoms through axis object or vector [a,b,c].
        '''

        theta = float(angle)*np.pi/180.
        ax = Axis(ax)
        a, b, c = ax.ax.T[0]

        KS = 1.-np.cos(theta)
        rotMat = np.matrix( [[a**2*KS+np.cos(theta),a*b*KS-c*np.sin(theta),a*c*KS+b*np.sin(theta)],
                             [a*b*KS+c*np.sin(theta),b**2*KS+np.cos(theta),b*c*KS-a*np.sin(theta)],
                             [a*c*KS-b*np.sin(theta),b*c*KS+a*np.sin(theta),c**2*KS+np.cos(theta)]] )
        #rotMat = np.matrix( [[a**2*KS+np.cos(theta),a*b*KS+c*np.sin(theta),a*c*KS-b*np.sin(theta)],
                             #[a*b*KS-c*np.sin(theta),b**2*KS+np.cos(theta),b*c*KS+a*np.sin(theta)],
                             #[a*c*KS+b*np.sin(theta),b*c*KS-a*np.sin(theta),c**2*KS+np.cos(theta)]] )

        #for atom in self.atoms[:]:

        for atom in self.atoms[:]:
            atom.pos = rotMat * atom.pos

    def sort_by_pos(self, a=0, b=0, c=0, direc=None):
        '''
        Sort atoms by their distance to a plane whose normal vector is (a, b,
        c).
        '''

        if direc == 'x':
            a, b, c = (1, 0, 0)
        elif direc == 'y':
            a, b, c = (0, 1, 0)
        elif direc == 'z':
            a, b, c = (0, 0, 1)

        self.atoms = sorted(self.atoms, key=lambda at:
                         get_point_plane_distance(at.pos, (a,b,c)))

        return self

    def sphere(self, radius, pos=None, center_atom=None):
        if pos.any():
            center = pos
        elif center_atom:
            center = center_atom.pos
        else:
            center = np.zeros(3)
        return self._filter(lambda a: np.linalg.norm(a.pos - center) <=
                            radius**2)

    def get_image(self, cwd=None, cmdFile=None, pngOut=None, **kwargs):
        _file = self.name + '.xyz'
        self.write_to_file(_file)
        self.imagePath = render.take_snapshot(xyzFile=_file, cwd=cwd,
                                              cmdFile=cmdFile, pngOut=pngOut,
                                              simulate=False, **kwargs)
        os.remove(_file)

    def write_siestaCoords(self, fn='coordinates.data'):
        with open(fn, 'w') as f:
            for a in self.atoms:
                l = [key for value,key in self.species.items() if value==a.symbol ][0]
                f.write('{x:13.8f}{y:13.8f}{z:13.8f}{label:3d}\n'.format(
                        x=a.pos.item(0), y=a.pos.item(1),
                        z=a.pos.item(2), label=l))

    def write_siestaSpecies(self, fn='species.data'):
        with open(fn, 'w') as f:
            for elem in sorted(self.species, key=self.species.get):
                f.write('%5d%5d%5s\n' % (self.species[elem],
                                         symbol_to_atno[elem], elem))
    def switch_atomsPosition(self, ini, fin, ins):
        """
        Insert slice of atoms from atom 'ini' to atom 'fin' into position
        'ins'.

        Example
        =======

        >>> atoms = [atom1, atom2, atom3, atom4, atom5, atom6, atom7]
        switch_atomsPosition(4, 6, 2)
        >>> atoms
        [atom1, atom4, atom5, atom6, atom2, atom3, atom7]
        """

        #atoms = self.atoms[:]
        #self.atoms = self.atoms[:fp-2] + self.atoms[fp-1:lp] + self.atoms[fp-2:fp-1] + self.atoms[lp:]
        if fin < ini:
            raise IOError('"fin" value must be greater than "ini" value.')
        elif ins > ini and ins < fin:
            print('Not modifying atoms list since "ins" value is between "ini" and "fin" values')
        if ins < ini:
            self.atoms = self.atoms[:ins] + self.atoms[ini:fin+1] + self.atoms[ins:ini] + self.atoms[fin+1:]
        elif ins > ini:
            self.atoms = self.atoms[:ini] + self.atoms[fin+1:ins] + self.atoms[ini:fin+1] + self.atoms[ins:]

    def align_atomsThroughVector(self, at1, at2, vec):
        at1, at2 = check_arg_atoms(at1, at2)
        v = at2.pos - at1.pos
        v = v.T[0]
        v_ax = np.cross(v, vec)
        if not np.linalg.norm(v_ax) == 0:
            ax = Axis(ax=np.cross(v, vec))
            self - at1.pos
            self.rotate(ax, get_angle_from_vec(v, vec))
        else:
            print('Atoms %s and %s are already align to axis %s' % (at1, at2,
                                                                    vec))
        #ax = Axis(ax=np.cross(vec, v))
        #self - self.get_geometryCenter()
        #self - at1.pos

        pass
    def __add__(self, an_object):

        if isinstance(an_object, (self.__class__, Molecule)):
            #self.atoms += an_object.atoms
            for atom in an_object:
                self.add_atom(atom)

        elif isinstance(an_object, Atom):
            self.add_atom(an_object)

        elif isinstance(an_object, (types.ListType, np.ndarray)):
            v = check_3x1(an_object)
            for atom in self.atoms:
                atom + v

        else:
            raise IOError('Not addition supported of {name} object with \
                            "{obj}"'.format(name=self.__class__.__name__,
                            obj=an_object))
        return self

    def __sub__(self, an_object):

        if isinstance(an_object, (self.__class__, Molecule)):
            outMol = []
            for orig_at in self.atoms:
                if not orig_at in an_object:
                    outMol.append(orig_at)
            return Molecule(atoms=outMol)

        elif isinstance(an_object, Atom):
            for i, orig_at in enumerate(self.atoms):
                if orig_at.label == an_object.label:
                    self.remove_atom(i)

        elif isinstance(an_object, (types.ListType, np.ndarray)):
            v = check_3x1(an_object)
            for atom in self.atoms:
                atom - v

        else:
            raise IOError('Not addition supported of {name} object with \
                            "{obj}"'.format(name=self.__class__.__name__,
                            obj=an_object))
        return self

    #def __radd__(self, an_object):
        #self.__add__(an_object)

    #def __rsub__(self, an_object):
        #self.__sub__(an_object)

    def __contains__(self, atom):
        return atom in self.atoms

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Molecule(atoms=self.atoms[index])

        elif isinstance(index, int):
            return self.atoms[index]
        #return self.atoms[index-1]

    def __len__(self):
        return len(self.atoms)

    def __repr__(self):
        return '{name}({atoms})'.format(name=self.__class__.__name__,
                atoms=self.atoms)


class ZMatrix(object):

    def __init__(self, system, firstAtom=None, ZMatrixType='cartesian'):

        self.system = system
        self.firstAtom = firstAtom
        self.set_move()
        self.set_atomsZmatrixType(ZMatrixType)
        #self.set_atomsZmatrixType('molecule')

        #self.prepare_ZMatrix()

    #@property
    #def cartesian(self):
        #return filter(lambda a: a.zmatrixType == 'cartesian', self.system)

    #@property
    #def molecule(self):
        #return filter(lambda a: a.zmatrixType == 'molecule', self.system)

    def get_atomsZmatrixType(self, type_):
        return filter(lambda a: a.zmatrixType == type_, self.system)

    def prepare_ZMatrix(self):
        if self.get_atomsZmatrixType('cartesian'):
            self.prepare_cartesian()
        else:
            self.cartesian = None
        if self.get_atomsZmatrixType('molecule'):
            self.prepare_molecule()
        else:
            self.molecule = None

    def set_move(self, move=[1,1,1], *atoms):
        if atoms:
            atoms_ = check_arg_atoms(atoms)
            for atom in atoms_:
                atom.zmatMove = move
        else:
            for atom in self.system:
                atom.zmatMove = move

    def set_atomsZmatrixType(self, atomType, *args):
        if not atomType == 'cartesian' and not atomType == 'molecule':
            raise IOError('first argument must be "cartesian" or "molecule"')
        check_arg_atoms(args)
        if len(args) == 0:
            for atom in self.system.atoms:
                atom.zmatrixType = atomType
        else:
            for elem in args:
                if isinstance(elem, (Molecule, Selection)):
                    for atom in elem:
                        atom.zmatrixType = atomType
                elif isinstance(elem, Atom):
                    atom.zmatrixType = atomType
                else:
                    raise IOError('Must be Molecule or Atom objects')
        self.ZMmolecule = filter(lambda a: a.zmatrixType == 'molecule',
                                 self.system)
        self.ZMcartesian = filter(lambda a: a.zmatrixType == 'cartesian',
                                  self.system)
        self.set_adjMolList()

    #def declareFirstAtomsZmatrixMolecule(self, firstAtom=None):
        #if not firstAtom:
            ##first = self.system[0]
            #firstAtom = self.ZMmolecule[0]
        #if not isinstance(firstAtom, Atom):
            #raise IOError('Argument must be Atom object')
        #for atom in self.ZMmolecule:
            #if atom == firstAtom:
                #self.firstAtom = atom

    def set_adjMolList(self):

        self.system.get_connections()
        self.system.get_structure()
        moleculeAtoms = self.get_atomsZmatrixType('molecule')
        self.adjMolList = {}
        for atom1 in moleculeAtoms:
            list_ = []
            for atom2 in self.system.connections[atom1]:
                if atom2 in moleculeAtoms:
                    list_.append(atom2)
            self.adjMolList[atom1] = list_

    def prepare_cartesian(self):
        self.cartesian = []
        for atom in self.get_atomsZmatrixType('cartesian'):
            self.cartesian.append([atom.specieNo, atom.pos[0], atom.pos[1],
                                   atom.pos[2]] + atom.zmatMove)
        return self.cartesian

    def prepare_molecule(self):
        T = Tree(adjList=self.adjMolList, root=self.firstAtom)
        T.depth_first_search()
        T.set_visitOrder()
        self.ordAtoms = T.get_atomsFromVertices(T.visitOrder)
        self.alrConstructed = []
        self.molecule = []
        for i, vertex in enumerate(T.visitOrder):
            self.alrConstructed.append(vertex)
            if i == 0:
                #atom = T.get_atomsFromVertices(vertex)
                connection = T.get_atomsFromVertices(vertex)
            elif i == 1:
                atoms = T.get_atomsFromVertices(vertex, T.visitOrder[0])
                connection = self.system.bonds.filter_byAtom(atoms)
            elif i == 2:
                atoms = T.get_atomsFromVertices(vertex, T.visitOrder[0])
                connection = self.system.angles.filter_byAtom(atoms)
                if len(connection) > 1:
                    connection = [connection[0]]
            else:
                # TODO
                atoms = T.get_atomsFromVertices(T.get_pathOfLengthWithConstrain(vertex, n=4,
                                                                   constrain=self.alrConstructed))
                #atoms = T.get_atomsFromVertices(T.get_NthParentPathFromVertex(vertex, n=4))
                connection = self.system.dihedrals.filter_byAtom(atoms)
                if len(connection) > 1:
                    connection = [connection[0]]
            if not len(connection) == 1:
                raise TypeError('At this point we should have only one %s, instead got %i of them. Please check that no connection is repeated.' %
                                (connection[0].__class__.__name__, len(connection)))
            connection = connection[0]
            if not isinstance(connection, Atom):
                connection.order_byFirstAtom(vertex.vertex)
            self.molecule.append(self.get_ZMline(connection))

        return self.molecule

    def prepare_nonZmatrix(self, mass=True):
        self.positionGeometry = []
        for a in self.system:
            #self.positionGeometry.append([a.pos[0], a.pos[1], a.pos[2], a.specieNo])
            l = [a.pos.item(0), a.pos.item(1), a.pos.item(2), a.specieNo]
            #l = list(a.pos)
            #l.append(a.specieNo)
            if not mass:
                #self.positionGeometry.extend(list(a.pos) + [a.specieNo])
                self.positionGeometry.append(l)
            else:
                l.append(a.mass)
                self.positionGeometry.append(l)
    def get_ZMline(self, connection):
        if isinstance(connection, Atom):
            atom = connection
            line = [atom.specieNo, 0, 0, 0, connection.pos[0],
                    connection.pos[1], connection.pos[2]]
        elif isinstance(connection, Bond):
            atom = connection.atoms[0]
            line = [atom.specieNo, 1, 0, 0, connection.distance,
                    connection.get_polar(), connection.get_azimuthal()]
        elif isinstance(connection, Angle):
            atom = connection.atoms[0]
            bond = self.system.bonds.filter_byAtom(atom, connection.atoms[1])[0]
            i = self.ordAtoms.index(connection[1]) + 1
            j = self.ordAtoms.index(connection[2]) + 1
            line = [atom.specieNo, i, j, 0, bond.distance,
                    connection.angle, connection.get_dihedralFromDummyAtom()]
        elif isinstance(connection, Dihedral):
            atom = connection.atoms[0]
            bond = self.system.bonds.filter_byAtom(atom, connection.atoms[1])[0]
            angle = self.system.angles.filter_byAtom(atom, connection.atoms[2])[0]
            i = self.ordAtoms.index(connection[1]) + 1
            j = self.ordAtoms.index(connection[2]) + 1
            k = self.ordAtoms.index(connection[3]) + 1
            line = [atom.specieNo, i, j, k, bond.distance,
                    angle.angle, connection.dihedral]

        line += atom.zmatMove
        line.append(atom.label)


        return line

    def write_toFile(self, filename, t='molecule', mass=False):
        '''
        Dump ZMatrix structure into file.
        '''

        if t is not 'molecule' and t is not 'cartesian' and t is not 'normal':
            raise IOError('Argument "t" can be either "molecule", "cartesian" or "normal".')

        with open(filename, 'w') as f:
            if t == 'molecule':
                for lno, line in enumerate(self.molecule):
                    f.write('%4i%4i%4i%4i%12.4f%12.4f%12.4f%3i%3i%3i%4s%4i\n' % tuple(line+[lno+1]))
            elif t == 'normal':
                for line in self.positionGeometry:
                    if len(line) == 4:
                        # Cartesian line without mass
                        # HERE
                        f.write('%12.4f%12.4f%12.4f%3i\n' % tuple(line))
                    elif len(line) == 5:
                        # Cartesian line with mass
                        f.write('%12.4f%12.4f%12.4f%3i%15f\n' % tuple(line))

    def read_fromFile(self, filename):
        # TODO
        with open(filename, 'r') as f:
            lines = f.readlines()
        self.system = Molecule()
        for i, l in enumerate(lines):
            # dad stands for distance, angle, dihedral
            dad = np.array(l[4:7], dtype=float)
            if i == 1:
                self.system.add_atom(pos=dad)
            elif i == 2:
                pos = get_coordinatesFromSpherical(self.system[0].pos, dad)


class Graph(object):
    def __init__(self, name='', adjList=None):
        self.name = name
        #self.vertices = {} # vertex list
        self.vertices = [] # vertex list
        self.edges = [] # edge list
        if adjList:
            self.origAdjList = adjList
            self.adjacencyList = self.load_graph(adjList)

    def load_graph(self, graph):
        for v in graph:
            self.add_vertex(v)

        adjacencyList = {}
        for u in graph:
            for vertex1 in self.vertices:
                if vertex1.vertex is u:
                    adjacencyList[vertex1] = []
                    for i, v in enumerate(graph[u]):
                        for vertex2 in self.vertices:
                            if vertex2.vertex is v:
                                adjacencyList[vertex1].append(vertex2)
                                self.add_edge(vertex1, vertex2)
        return adjacencyList

    def add_vertex(self, v):
        if isinstance(v, Vertex):
            vertex = v
        else:
            vertex = Vertex(v)

        self.vertices.append(vertex)
        #self.vertices[vertex] = vertex.vertex
        #return vertex

    def add_edge(self, u, v):
        self.edges.append(Edge(u, v))

    #def breadth_first_search(self, start):
        #Q = [start]
        #D = {node:'inf' for node in self.adjacencyList}
        #D[start] = 0
        #T = []
        #while len(Q) > 0:
            #u = Q.pop(0)
            #for v in graph[u]:
                #if D[v] == 'inf':
                    #D[v] = D[u]+1
                    #Q.append(v)
                    #T.append([u, v])
        #return (D, T)

    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not self.adjacencyList.has_key(start):
            return None
        for node in self.adjacencyList[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None
        #path = path + [start]
        #if start == end:
            #return path
        #if not graph.has_key(start):
            #return None
        #for node in graph[start]:
            #if node not in path:
                #newpath = find_path(graph, node, end, path)
                #if newpath: return newpath
        #return None

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not self.adjacencyList.has_key(start):
            return []
        paths = []
        for node in self.adjacencyList[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def get_pathOfLengthWithConstrain(self, start, n=4, constrain=None):
        nLengthedPaths = []
        if constrain:
            for v in constrain:
                paths = self.find_all_paths(start, v)
                for path in paths:
                    if len(path) == n:
                        for vv in path:
                            if not vv in constrain:
                                found = False
                                break
                            found = True
                        if found:
                            nLengthedPaths.append(path)
                            break
        sum_ = 0
        for i, path in enumerate(nLengthedPaths):
            q = sum(map(lambda v: v.level, path))
            if q > sum_:
                sum_ = q
                max_i = i
        return nLengthedPaths[max_i]

    def check_start_type(self, start):
        if isinstance(start, Atom):
            for vertex in self.adjacencyList:
                if vertex.vertex == start:
                    return vertex

        elif not isinstance(start, (Vertex, TreeVertex)):
            raise TypeError('start must be Atom, Vertex or TreeVertex type.')

    def get_atomsFromVertices(self, *vertices):
        # Next comment was useful when DFS was used
        #if not vertices:
            #vertices = self.visitOrder
        #vertices = vertices[0]
        if len(vertices) == 1:
            if isinstance(vertices[0], types.ListType):
                vertices = vertices[0]
            elif isinstance(vertices[0], (Vertex, TreeVertex)):
                vertices = [vertices[0]]
            else:
                raise TypeError('Argument must be a Vertex or TreeVertex instance or a list of them.')
        return [v.vertex for v in vertices]

    def get_vertexFromAtoms(self, *atoms):
        atoms = atoms[0]
        return [v for atom in atoms for v in self.vertices if v.vertex == atom]


class Vertex(object):
    def __init__(self, v=None):
        self.vertex = v

    def __repr__(self):
        return '%s' % (self.vertex,)


class Edge(object):
    def __init__(self, u=None, v=None):
        self.edge = (u, v)

    def __repr__(self):
        return '%s--%s' % (self.edge[0], self.edge[1])


class Tree(Graph):
    def __init__(self, adjList=None, root=None):
        Graph.__init__(self, name=None, adjList=adjList)
        if root:
            self.root = self.check_start_type(root)
            self.root.level = 0
            self.root.parent = None
        for vertex in self.vertices:
            if vertex.vertex is self.root.vertex:
                #self.root = vertex
                vertex.level = 0
                vertex.parent = None
            else:
                vertex.level = 'inf'
                vertex.parent = None
        self.visitOrder = []

    def add_vertex(self, v):
        if isinstance(v, Vertex):
            vertex = TreeVertex(v.vertex)
        else:
            vertex = TreeVertex(v)

        self.vertices.append(vertex)
        #self.vertices[vertex] = vertex.vertex

    def breadth_first_search(self):
        Q = [self.root]
        while len(Q) > 0:
            u = Q.pop(0)
            for v in self.adjacencyList[u]:
                if v.level == 'inf':
                    v.level = u.level + 1
                    v.parent = u
                    self.add_edge(u, v)
                    Q.append(v)

    def depth_first_search(self, u=None):
        if not u:
            self.time = 0
            u = self.root
            self.visitOrder.append(u)

        self.time += 1
        u.d = self.time
        for v in self.adjacencyList[u]:
            if v.level == 'inf':
                self.visitOrder.append(v)
                v.parent = u
                v.level = u.level + 1
                self.depth_first_search(v)
        self.time += 1
        u.f = self.time

    #def iterative_dfs(self, start, path=[]):
        #'''iterative depth first search from start'''
        ##T = Tree(adjList=self.origAdjList)
        #Q = [start]
        #while Q:
            #v = Q.pop(0)
            #if v not in path:
                #path += [v]
                #Q = self.adjacencyList[v] + Q #Order here matters
        #return path

    #def recursive_dfs(graph, start, path=[]):
        #'''recursive depth first search from start'''
        #path=path+[start]
        #for node in graph[start]:
            #if not node in path:
                #path=recursive_dfs(graph, node, path)
        #return path

    def get_NthParentPathFromVertex(self, vertex, n=None):
    #def get_NthParentFromVertex(self, n, vertex):
        result = []
        #for _ in xrange(n):
        while n > 0:
            result.append(vertex)
            vertex = vertex.parent
            n -= 1
        return result
        #for vertex in self.vertices:
            #if vertex.level is n-1:
                #a_path = []
                #in_vertex = vertex
                ##while in_vertex.parent:
                #for i in range(n):
                    #a_path.append(in_vertex.vertex)
                    #in_vertex = in_vertex.parent
                #result.append(a_path)

    def set_visitOrder(self):
        outer = []
        for vertex in list(self.visitOrder):
            if vertex.f - vertex.d == 1:
                outer.append(vertex)
                self.visitOrder.remove(vertex)
        self.visitOrder += outer

    def get_nthFromVertex(self, vertex, n=4):
        last = vertex
        for i in range(n-1):
            last = last.parent
        return last


class TreeVertex(Vertex):
    def __init__(self, v, level=None, parent=None):
        self.vertex = v
        self.level = level
        self.parent = parent


class Connection(object):

    def get_atoms_from_list(self, list_):

        self.atoms = []
        #atoms = []

        if len(list_) is 1:
            list_ = list_[0]

        #if type_ is 'Bond':
            #l = 2
        #elif type_ is 'Angle':
            #l = 3
        #elif type_ is 'Dihedral':
            #l = 4

        for elem in list_:
            if isinstance(elem, Atom):
                self.atoms.append(elem)
                #atoms.append(elem)
            elif isinstance(elem, Vertex):
                self.atoms.append(elem.vertex)
                #atoms.append(elem.vertex)

        #return atoms

    def order_byFirstAtom(self, atom):
        if not isinstance(atom, Atom):
            raise IOError('Argument must be Atom instance.')
        if not atom in self.atoms:
            raise NameError('Atom %s not in %s' % (atom, self))
        #if not self.connections[0] == atom or not self.connections[-1] == atom:
            #raise NameError('Neither first nor last atom is atom %s' % (atom,))
        if self.atoms[0] == atom:
            #list_ = self.connections
            pass
        elif self.atoms[-1] == atom:
            self.atoms = self.atoms[::-1]
        else:
            raise NameError('Neither first nor last atom is atom %s' % (atom,))
        return self

    def __getitem__(self, index):
        return self.atoms[index]

    def __contains__(self, atom):
        return atom in self.atoms
    def __len__(self):
        return len(self.atoms)

    def __eq__(self, other):
        return self.atoms == other.atoms[::-1]

    def __hash__(self):
        return hash(repr(sorted(self.atoms)))


class ConnectionList(object):

    def __init__(self, connections=None):
        if not connections:
            connections = []

        self.connections = connections

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_duplicates(self):
        self.connections = [connection for connection in set(self.connections)]

    def filter_byAtom(self, *args):
        if len(args) == 1 and isinstance(args[0], types.ListType):
            atoms = args[0]
        else:
            atoms = args
        check_arg_atoms(atoms)
        list_ = self.connections[:]
        for atom in atoms:
            list_ = filter(lambda connection: atom in connection, list_)

        return list_
    def __len__(self):
        return len(self.connections)

    def __getitem__(self, index):
        return self.connections[index]


class Plane(object):
    """
    Plane of equation a*x + b*y + c*z = d
    """


    def __init__(self, a=None, b=None, c=None, d=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def get_from_points(self, p1, p2, p3):

        vec1 = p1 - p2
        vec2 = p3 - p2

        self.a, self.b, self.c = np.cross(vec1.reshape((1,3)), vec2.reshape((1,3)))

        self.d = np.inner([self.a, self.b, self.c], p1)


class Cell(object):

    def __init__(self, a0=None, a1=None, a2=None, a3=None, alpha=None,
                 beta=None, gamma=None, fromFile=False):
        self.a0 = a0
        self.a1 = np.array(a1)
        self.a2 = np.array(a2)
        self.a3 = np.array(a3)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        if fromFile:
            self.load_fromFile(fromFile)

    def get_latticePoints(self, n=[0,0,0]):


        n1, n2, n3 = n

        aa1 = np.array([i*self.a1 for i in range(n1+1)])
        aa2 = np.array([i*self.a2 for i in range(n2+1)])
        aa3 = np.array([i*self.a3 for i in range(n3+1)])

        latt = np.array([np.sum(p, axis=0) for p in product(aa3, aa2, aa1)])
        latt *= self.a0

        return latt

    def get_boxCenter(self):
        return self.a0/2*(self.a1+self.a2+self.a3)

    def center_MolInBox(self, m):
        m - m.get_geometryCenter() + self.get_boxCenter()

    def gen_SquareBoxFromMol(self, m, empety=0):
        self.a0 = 1.0
        self.a1 = np.array([m.get_largestLengthInDirection('x')+empety, 0, 0])
        self.a2 = np.array([0, m.get_largestLengthInDirection('y')+empety, 0])
        self.a3 = np.array([0, 0, m.get_largestLengthInDirection('z')+empety])
        self.center_MolInBox(m)

    def normalize_vectors(self):

        self.a1 *= self.a0
        self.a2 *= self.a0
        self.a3 *= self.a0
        self.a0 = 1.0
    def print_CellVectors(self):
        #print '%-15.5f\n' % self.a0
        #print self.a0
        s = str(self.a0) + '\n'
        return s

    def write_cellVectors(self, fn='vectors.data'):
        with open(fn, 'w') as f:
            for v in (self.a1, self.a2, self.a3):
                f.write('%12.5f%12.5f%12.5f\n' % tuple(v))

    def load_fromFile(self, fn):
        if fn is None:
            fn = 'vectors.data'
        self.a1, self.a2, self.a3 = np.loadtxt(fn)


class Axis(object):

    def __init__(self, ax=None, standar=None):

        if ax is None and standar is None:
            self.ax = np.array([[0], [0], [1]])
        else:
            if isinstance(ax, Axis):
                self.ax = ax.ax
            else:
                self.ax = check_3x1(ax)
                self.ax /= np.linalg.norm(self.ax)

