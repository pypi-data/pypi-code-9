import os
import transat.setup.stt_helper_functions as stt
import transat.setup.mesh as mesh
from transat.setup.mesh import Rectangle

import collections
import numpy as np
import sys
import copy
"""
This module handles boundary conditions for TransAT
"""


class BCError(Exception):
    """Base class for exceptions in Boundary Conditions

    Args:
        msg (str): Human readable string describing the exception.
        code (int, optional): Error code, defaults to 2.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, msg, code=2):
        self.msg = msg
        self.code = code


class Surface(object):
    """A Surface is an ensemble of rectangles that:
        - are connected together
        - have the same orientation

    Attributes:
        bc (str): Boundary condition name. Should correspond to one of :func:`BoundaryConditions.get_bc_names`
        id (int):
        surface_id (int):
        rectangles (list):

    """
    def __init__(self):
        self.bc = "undefined"
        self.id = 0
        self.surface_id = 0
        self.rectangles = []
        self.issubbc = False
        self.sub_bc_id = None
        self.sub_bc = {}
        self.subbcs = []

    def add_subbc(self, bc_key, dimensions):

        surface = copy.deepcopy(self)

        rect = self.rectangles[0]
        norm = rect.normal
        value = rect.value
        for key in dimensions.keys():
            dimensions[key] = float(dimensions[key])
        rectangle = Rectangle(rect.normal, dimensions, rect.value, rect.orientation )
        surface.rectangles = [rectangle]
        dimensions[norm+"min"] = float(value)
        dimensions[norm+"max"] = float(value)
        surface.sub_bc = dimensions
        surface.set_bc_key(bc_key)
        surface.sub_bc_id = 1
        surface.issubbc = True
        self.subbcs.append(surface)
        return surface

    def set_rectangles(self, rectangles):
        self.rectangles = rectangles

    def get_rectangles(self):
        return self.rectangles

    def get_area(self):
        A = 0
        # loop over all rectangles in surface and sum
        for rect in self.get_rectangleet():
            A += (rect.get_area())

        return A

    def get_location(self):
        # locate (x,y,z)_min of Surface
        loc = {}

        rectangles = self.get_rectangles()
        normal = rectangles[0].normal

        # locate location in 'in plane' directions
        for rect in rectangles:
            for dir in rect.directions:
                if dir not in loc.keys():
                    loc[dir] = float(rect.dimensions[dir+"min"])
                loc[dir] = min(loc[dir], rect.dimensions[dir+"min"])

        # add height of plane in normal direction
        loc[normal] = rectangles[0].value

        return loc

    def get_normal(self):
        return self.get_rectangles()[0].normal

    def get_corners(self):
        dim = {}
        for rect in self.rectangles:
            for dir in ['x', 'y', 'z']:
                val = rect.get_corner(dir, 'min')
                key = dir+"min"
                if key not in dim.keys() or val < dim[key]:
                    dim[dir+"min"] = val

                val = rect.get_corner(dir, 'max')
                if dir+"max" not in dim.keys() or val > dim[dir+"max"]:
                    dim[dir+"max"] = val
        return dim

    def unwrap(self, data):
        self.id = data['id'].split()[0]
        self.bc = data['bc_key']
        self.surface_id = data['boundary']

        if "BBOX" in data.keys():
            for dir in ['x', 'y', 'z']:
                self.sub_bc[dir + 'min'] = data['BBOX'][dir+'min']
                self.sub_bc[dir + 'max'] = data['BBOX'][dir+'max']
                self.sub_bc_id = data['id'].split()[1]
            self.issubbc = True

        return self

    def set_surface_id(self, surface_id):
        self.surface_id = surface_id

    def set_id(self, id):
        self.id = id

    def set_bc_key(self, bc_key):
        self.bc = bc_key

    def get_bc_key(self):
        return self.bc

    def write(self):
        """
        Returns:
            list: data that can be inserted in SURFACE_TREE section of the stt file
        """
        data = collections.OrderedDict()
        data['\t' + 'bc_key'] = self.bc
        data['\t' + 'boundary'] = str(self.surface_id)
        if self.sub_bc_id is None:
            data['\t' + 'id'] = str(self.id) + " ENDid"

        if self.sub_bc_id is not None:
            data['\t' + 'id'] = str(self.id) +" "+str(self.sub_bc_id)+ " ENDid"
            data['\t' + 'dimensions'] = ''
            data['\t' + 'BBOX'] = ''
            data['\t\t' + 'xmin'] = self.sub_bc['xmin']
            data['\t\t' + 'xmax'] = self.sub_bc['xmax']
            data['\t\t' + 'ymin'] = self.sub_bc['ymin']
            data['\t\t' + 'ymax'] = self.sub_bc['ymax']
            data['\t\t' + 'zmin'] = self.sub_bc['zmin']
            data['\t\t' + 'zmax'] = self.sub_bc['zmax']
            data['\t' + 'ENDBBOX'] = ''
        return data


class SurfacesList(object):
    def __init__(self, addsurfaces=[]):
        self.surfaces = addsurfaces

    def get_all(self):
        return self.surfaces

    def is_empty(self):
        return len(self.surfaces) == 0

    def add(self, surface):
        self.surfaces.append(surface)

    def for_dir(self, dir):
        _surfaces = []
        for surface in self.surfaces:
            if surface.rectangles[0].normal == dir:
                _surfaces.append(surface)
        return SurfacesList(_surfaces)

    def minmax(self, name):
        _surfaces = []
        for surface in self.surfaces:
            if surface.rectangles[0].orientation == name:
                _surfaces.append(surface)
        return SurfacesList(_surfaces)

    def for_value(self, value):
        _surfaces = []
        for surface in self.surfaces:
            if surface.rectangles[0].value == value:
                _surfaces.append(surface)
        return SurfacesList(_surfaces)

    def get_values(self):
        values = []
        for sur in self.surfaces:
            values.append(sur.rectangles[0].value)
        return values

    def set_bc_name(self, bc_name):
        if len(self.surfaces) == 0:
            print "Can not set bc_name. I don't have any surfaces"
            sys.exit()
        for s in self.surfaces:
            s.bc = bc_name

    def get_surface_with_point(self, point):
        surfaces = []
        for surface in self.surfaces:
            for rectangle in surface.rectangles:
                if rectangle.contains_point(point):
                    surfaces.append(surface)
        if len(surfaces) == 0:
            print "Did not find a surface with point "+str(point)
            raise GetSurfaceError(point, surfaceList=self)
            sys.exit()
        return SurfacesList(surfaces)

    def get_surface_with_normal(self, axis):
        surfaces = []
        for surface in self.surfaces:
            for rectangle in surface.rectangles:
                if rectangle.normal == axis:
                    surfaces.append(surface)
        if len(surfaces) == 0:
            print "Did not find a surface with normal "+str(axis)
            sys.exit()
        return SurfacesList(surfaces)

class GetSurfaceError(Exception):
    def __init__(self, value, surfaceList):
        self.value = value
        self.surfaceList = surfaceList

    def __str__(self):
        return repr(self.value)


class SurfaceTree(object):
    """A SurfaceTree is collection of surfaces.
    The order in which the tree is sorted matters for the definition of the boundaries.

    Attributes:

        surfaces (list):  Items in surfaces are object of type :class:`Surface`
    """
    def __init__(self, surfaces):
        self.surfaces = SurfacesList(surfaces)
        self.sort()

    def get_all_surfaces(self):
        return self.surfaces

    def get_surface_with_point(self, point):
        return self.surfaces.get_surface_with_point(point)

    def get_surface_with_normal(self, normal):
        return self.surfaces.get_surface_with_normal(normal)

    def get_surfaces_by_bc_name(self, name):
        slist = SurfacesList([])
        for surf in self.surfaces.surfaces:
            if surf.get_bc_key() == name:
                slist.add(surf)

        if slist.is_empty():
            print 'Error: no surface found with name %s, aborting' % name
            sys.exit(0)
        return slist

    def get_bc_names(self, returnundefined = False):
        names = []
        for surf in self.surfaces.surfaces:
            if (surf.get_bc_key() != 'undefined' and returnundefined == False) or (returnundefined == True):
                names.append(surf.get_bc_key())

        return names


    def sort(self):
        new_surfaces = []
        boundary_id = 0
        for dir in ['x', 'y', 'z']:
            sur_dir = self.surfaces.for_dir(dir)

            for ori in ['min', 'max']:
                sur_ori = sur_dir.minmax(ori)
                values = sur_ori.get_values()

                if len(values) > len(set(values)):
                    # TODO print "error in Surface Tree"
                    pass
                values = set(values)
                if ori == 'max':
                    values = sorted(values, reverse=True)
                else:
                    values = sorted(values)

                id = -1
                for val in values:
                    for s in sur_ori.for_value(val).surfaces:
                        if s.issubbc is False:
                            id += 1
                        s.set_surface_id(boundary_id)
                        s.set_id(id)
                        new_surfaces.append(s)
                boundary_id += 1
        self.surfaces = SurfacesList(new_surfaces)
        return new_surfaces


class BoundaryConditions(object):
    """Stores all boundary conditions

    Attributes:
        bc_file (str): Input file of TransAT containing the boundary conditions, generated by the GUI
        bcs (list of BC): All the boundary condition objects

    """

    def __init__(self, stt_data, mesher):
        """Parse a boundary condition file into boundary condition objects

        Args:
            bc_file (str): Input file of TransAT containing the boundary conditions, generated by the GUI

        """
        self.already_created_surface_tree = False
        self.mesher = mesher

        self.tree = self.create_surfaces_tree()
        #self.tree = SurfaceTree([])

        #TODO add some checks
        if "SURFACE_TREE" in stt_data and 'SURFACE' in stt_data['SURFACE_TREE']:
            _surfaces_stt = []
            _subsurfaces_stt = []
            # add all surfaces WITHOUT subbcs to temporary list
            for d in stt_data['SURFACE_TREE']['SURFACE']:
                s = Surface()
                s.unwrap(d)
                if not (s.issubbc):
                    _surfaces_stt.append(d)
                else:
                    _subsurfaces_stt.append(d)

            # append data from temporary list to the surface tree created by the mesher
            for d, s in zip(_surfaces_stt, self.tree.surfaces.surfaces):
                s.unwrap(d)

            # append correct subbcs to corresponding parent surface, create subbc rectangle
            for d in _subsurfaces_stt:
                s = Surface()
                s.unwrap(d)
                surfaces = self.tree.surfaces.surfaces
                sub_surfaces = []
                for dd in surfaces:
                    if s.id == dd.id and s.surface_id == dd.surface_id:
                        sub_surfaces.append(dd.add_subbc(s.get_bc_key(), s.sub_bc))
                self.tree.surfaces.surfaces += sub_surfaces



        if "BCMB" in stt_data:
            self.boundaries = []
            if 'ROW' not in stt_data['BCMB']:
                stt_data['BCMB']['ROW'] = []
            bcrows = stt_data['BCMB']['ROW']
            if isinstance(bcrows, list):
                for b in stt_data['BCMB']['ROW']:
                    self.extract_bc(b)
            else:
                self.extract_bc(stt_data['BCMB']['ROW'])

        #self.create_surfaces_tree()

    def extract_bc(self, b):
        bc = BC(b)
        if b['type'] == "Inflow":
            bc = Inflow(b)
        elif b['type'] == "Opflow":
            bc = Opflow(b)
        elif b['type'] == "Wall":
            bc = Wall(b)
        self.boundaries.append(bc)


    def get_surfaces_from_mesher(self):
        surfaces = []
        for rectangles in self.mesher.get_rectangles():
            sur = Surface()
            sur.set_rectangles(rectangles)
            surfaces.append(sur)
        return surfaces

    def get_surface_tree(self):
        #surfaces = self.get_surfaces_from_mesher()
        return self.tree

    def create_surfaces_tree(self):
        self.tree = SurfaceTree(self.get_surfaces_from_mesher())
        return self.tree

    def write_surfaces(self):
        surfaces = []
        for surface in self.tree.sort():
            surfaces.append(surface.write())
        surfaces = {'SURFACE': surfaces}
        return surfaces

    def write_boundaries(self):
        boundaries = []
        for boundary in self.boundaries:
            boundaries.append(boundary.write())
        boundaries = {'ROW': boundaries}
        return boundaries

    def write(self, stt_file):
        stt.write_section("SURFACE_TREE", self.write_surfaces(), stt_file)
        stt.write_section("BCMB", self.write_boundaries(), stt_file)

    def get_bc_names(self):
        return [bc.name for bc in self.boundaries]

    def get_bc(self, name):
        """Get a boundary condition object from its name

        Args:
            name (str): Name of the boundary, as labelled in TransAT GUI

        Returns:
            BC: Boundary condition object

        """
        for bc in self.boundaries:
            if bc.name == name:
                return bc
        raise BCError("Boundary condition not found: " + name)

    @staticmethod
    def _parse_line(row, keyword):
        name = ""
        for line in row:
            key = line.lstrip().split(" ")[0]
            if keyword == key:
                name = line.split(" ")[-1].rstrip('\n')
        return name

    def _get_type(self, row):
        return self._parse_line(row, 'type')

    def _get_name(self, row):
        return self._parse_line(row, 'name')

    @staticmethod
    def _get_stt_section(keyword, lines):
        sections = []
        reading = False
        for line in lines:
            if "END" + keyword in line:
                section.append(line)
                sections.append(section)
                reading = False
            elif keyword in line:
                reading = True
                section = []
            if reading:
                section.append(line)
        return sections

    def _clean_bcs_in_stt(self):
        bc_file = self.bc_file
        reading = False
        with open(bc_file, 'r') as f:
            data = f.readlines()
            newdata = []
            for line in data:
                if not reading:
                    newdata.append(line)
                if "ENDBCMB" in line:
                    reading = False
                    newdata.append(line)
                elif "BCMB" in line:
                    reading = True
        with open(bc_file, 'w') as f:
            f.writelines(newdata)

    def _write_bcs_in_stt(self):
        # self._clean_bcs_in_stt()
        with open(self.bc_file, 'r') as f:
            data = f.readlines()
            for line, i in zip(data, range(len(data))):
                if "BCMB" in line and "END" not in line:
                    j = i + 1
                    for bc in self.bcs:
                        for new_line in bc.raw:
                            data.insert(j, new_line)
                            j += 1

        with open(self.bc_file, 'w') as f:
            f.writelines(data)


class BC(object):
    """
    Generic boundary condition object
    Different types of boundary conditions are derived from this class:

    .. inheritance-diagram:: transat.setup.bc
        :parts: 2

    """

    def __init__(self, raw):
        self.name = raw['name']
        self.raw = raw

    def write(self):
        return self.raw


class Wall(BC):
    """
    Wall Boundary Condition
    """

    def __init__(self, raw):
        super(Wall, self).__init__(raw)

    def set_temperature(self, temperature):
        self.raw['CORE']['bndtv'] = temperature

    def set_velocities(self, velocities):
        self.raw['CORE']['vbnd_u'] = velocities[0]
        self.raw['CORE']['vbnd_v'] = velocities[1]
        self.raw['CORE']['vbnd_w'] = velocities[2]

    def set_coupling(self, coupling):
        # TODO
        print "setting up coupling boundary condition"
        pass


class DataFileInflow(object):
    def __init__(self, vel_name="u"):
        self.coords = [[1e10,  1e10],
                       [1e10, -1e10],
                       [-1e10,  1e10],
                       [-1e10, -1e10]]
        self.time = []
        self.vel = []
        self.vel_name = vel_name

    def write(self, path):
        a = self.vel
        self.vel = np.array([a,a,a,a]).T
        for data, name in zip([self.coords, self.time, self.vel],
                                  ['coords', 'time', 'vel']):
            filename = os.path.join(path, name+'.dat')
            np.savetxt(filename, data, delimiter=' ')


class Inflow(BC):
    """
    Inflow Boundary Condition
    """

    def __init__(self, raw):
        super(Inflow, self).__init__(raw)

    def set_temperature(self, temperature):
        self.raw['CORE']['inflowtemperature'] = temperature

    def set_volumeflowrate(self, volumeflowrate):
        self.raw['volumeflowrate'] = volumeflowrate

    def set_velocities(self, velocity):
        """set inflow velocities in x, y and z direction

        Args:
            velocity (array): [v_x, v_y, v_z]

        """

        self.raw['CORE']['inflow_velocity_u'] = velocity[0]
        self.raw['CORE']['inflow_velocity_v'] = velocity[1]
        self.raw['CORE']['inflow_velocity_w'] = velocity[2]

    def set_phase_velocities(self, phase, velocity, volume_fraction):
        phase_index = phase.get_index()
        for axe, vel in zip(['u','v', 'w'], velocity):
            self.raw['CORE']['phase' + str(phase_index) + '_' + axe] = vel
        self.raw['CORE']['phase' + str(phase_index) + '_value'] = volume_fraction

    def set_datafile(self, data, path):
        data.write(path)

        self.raw['CORE']['inflowdatafiles_nbpoints'] = len(data.coords)
        self.raw['CORE']['inflowdatafiles_nbtimeinstants'] = len(data.time)
        self.raw['CORE']['inflow_coordinates_datafile'] = "coords.dat"
        self.raw['CORE']['inflow_timeinstants_datafile'] = "time.dat"
        self.raw['CORE']['inflow_'+data.vel_name+'velocity_datafile'] = "vel.dat"
        self.raw['CORE']['inflowdatafiles_'+data.vel_name+'_activated'] = "T"



    def set_coupling(self, coupling):
        # TODO
        print "setting up coupling boundary condition"
        pass


class Opflow(BC):
    """
    Output pressure Boundary Condition
    """

    def __init__(self, raw):
        super(Opflow, self).__init__(raw)

    def set_pressure(self, pressure):
        self.raw['CORE']['outflowpressure'] = pressure

    def set_coupling(self, coupling):
        # TODO
        print "setting up coupling boundary condition"
        pass

