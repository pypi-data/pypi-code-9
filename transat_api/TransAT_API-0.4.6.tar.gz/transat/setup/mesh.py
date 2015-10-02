import transat.setup.stt_helper_functions as stt
import os
import copy
import collections
import numpy as np
import sys
from transat.setup.cad import BoundBox

class Block(object):
    def __init__(self, stt_data=None, dimensions=None):
        if dimensions:
            try:
                self.set_dimensions(**dimensions)
            except TypeError:
                self.set_dimensions( **dimensions.unwrap())

        if stt_data:
            self.unwrap(stt_data)

    def make_2D(self, axis, value, origin=0.0):
        min_val = self.dimensions[axis+'min']
        max_val = self.dimensions[axis+'max']
        mean_val = min_val + (max_val-min_val)/2.0
        if mean_val == origin:
            self.dimensions[axis+'min'] = mean_val-value
            self.dimensions[axis+'max'] = mean_val+value
            return True
        else:
            return False

    def get_volume(self):
        volume = 1
        for dir in ['x', 'y', 'z']:
            dx = self._get_length(dir)
            volume = volume * dx
        return volume

    def get_lengths(self):
        lengths = {}
        for dir in ['x', 'y', 'z']:
            lengths[dir] = self._get_length(dir)
        return lengths

    def _get_length(self, dir):
        return float(self.dimensions[dir + 'max']) - float(self.dimensions[dir + 'min'])

    def split(self):
        lengths = self.get_lengths()
        dir = max(lengths, key=lengths.get)
        dis1 = lengths[dir] / 2.0
        value = self.dimensions[dir + 'max'] - dis1
        dim1 = copy.deepcopy(self.dimensions)
        dim1[dir + 'max'] = value
        dim2 = copy.deepcopy(self.dimensions)
        dim2[dir + 'min'] = value
        return [Block(dimensions=dim1), Block(dimensions=dim2)]

    def unwrap(self, stt_data):
        self.id = stt_data['grid']
        dimensions = collections.OrderedDict()
        for val in ['min', 'max']:
            for dir in ['x', 'y', 'z']:
                dimensions[dir + val] = stt_data[dir + val]
        self.set_dimensions(**dimensions)

    def write(self):
        block = collections.OrderedDict()
        block['grid'] = self.id
        block['father'] = "0"
        block['multifather'] = "0"
        block['level'] = "1"
        block['factor'] = -1
        block['factorx'] = 1
        block['factory'] = 1
        block['factorz'] = 1

        for val in ['min', 'max']:
            for dir in ['x', 'y', 'z']:
                key = dir + val
                block[key] = self.dimensions[key]

        block['length'] = 4.8
        block['zone'] = 0
        return block

    def set_dimensions(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.dimensions = {}
        self.dimensions['ymin'] = float(ymin)
        self.dimensions['xmin'] = float(xmin)
        self.dimensions['zmin'] = float(zmin)
        self.dimensions['ymax'] = float(ymax)
        self.dimensions['xmax'] = float(xmax)
        self.dimensions['zmax'] = float(zmax)

    def set_id(self, id):
        self.id = id

    def get_rectangles(self):
        rectangles = []
        directions = ['x', 'y', 'z']
        extr = ['min', 'max']
        for dir in directions:
            for ext in extr:
                tmp = {}
                tmp['dimensions'] = {}
                for dir2 in directions:
                    if dir != dir2:
                        for ext2 in extr:
                            tmp['dimensions'][dir2 + ext2] = float(self.dimensions[dir2 + ext2])
                    else:
                        tmp["value"] = self.dimensions[dir + ext]
                rectangles.append(Rectangle(dir, tmp['dimensions'], tmp['value'], ext))
        return rectangles


class RectangleFamily(object):
    def __init__(self, father):
        self.rectangles = [father]

    def find(self, rectangles):
        found_new_child = False
        for a_rectangle in list(self.rectangles):
            for b_rectangle in list(rectangles):
                if a_rectangle.is_connected(b_rectangle) and not a_rectangle.equal(b_rectangle):
                    rectangles.remove(b_rectangle)
                    self.rectangles.append(b_rectangle)
                    found_new_child = True
                if a_rectangle.equal(b_rectangle):
                    rectangles.remove(b_rectangle)
        if found_new_child:
            return self.find(rectangles)
        else:
            return rectangles

    def get_family_picture(self):
        return self.rectangles


class Rectangle(object):
    def __init__(self, normal, dimensions, value, orientiation):
        self.normal = normal
        self.dimensions = dimensions
        self.value = value
        self.directions = list(set([dir[0] for dir in self.dimensions.keys()]))
        self.orientation = orientiation

    def get_corner(self, dir, key="min"):
        key = dir+key
        if self.normal == dir:
            return float(self.value)
        return float(self.dimensions[key])

    def has_same_dimensions(self, dimensions):
        for key in dimensions.keys():
            if abs(self.dimensions[key] - dimensions[key]) > 1e-8:
                return False
        return True

    def equal(self, surface):
        if self.normal != surface.normal:
            return False
        # elif self.has_same_dimensions(surface.dimensions):
        elif self.dimensions != surface.dimensions:
            return False
        elif self.value != surface.value:
            return False
        else:
            return True

    def contains_point(self, point):
        n = 8
        point = {'x': round(point[0],n), 'y': round(point[1],n), 'z': round(point[2],n)}
        if point[self.normal] != round(self.value, n):
            return False
        for dir in self.directions:
            if point[dir] > round(self.dimensions[dir + 'max'], n) or \
               point[dir] < round(self.dimensions[dir + 'min'], n):
                return False
        return True

    def contains(self, surface):
        for dir in self.directions:
            if surface.dimensions[dir + 'min'] >= self.dimensions[dir + 'max'] or \
                            surface.dimensions[dir + 'max'] <= self.dimensions[dir + 'min']:
                return False
        return True

    def intersection(self, surface):
        if self.normal != surface.normal:
            return None
        elif self.value != surface.value:
            return None
        else:
            tmp = {}
            for dir in self.directions:
                intersection = self.get_1d_intersection(surface, dir)
                if intersection is None:
                    return None
                tmp[dir] = intersection
            surfaces = self.get_nine_surfaces(tmp)
            surfaces = self.remove(surfaces, surface)
            return surfaces

    def remove(self, surfaces, surface):
        _surfaces = []
        for _sur in surfaces:
            if self.contains(_sur) and not surface.contains(_sur):
                _sur.orientation = self.orientation
                _surfaces.append(_sur)
            elif surface.contains(_sur) and not self.contains(_sur):
                _sur.orientation = surface.orientation
                _surfaces.append(_sur)
        return _surfaces

    def get_nine_surfaces(self, values):
        surfaces = []
        for i in range(3):
            for j in range(3):
                dimensions = {}
                dimensions[self.directions[0] + 'min'] = values[self.directions[0]][i]
                dimensions[self.directions[0] + 'max'] = values[self.directions[0]][i + 1]
                dimensions[self.directions[1] + 'min'] = values[self.directions[1]][j]
                dimensions[self.directions[1] + 'max'] = values[self.directions[1]][j + 1]
                surfaces.append(Rectangle(self.normal, dimensions, self.value, self.orientation))
        return surfaces

    def get_1d_intersection(self, surface, dir):
        if self.dimensions[dir + 'min'] >= surface.dimensions[dir + 'max'] or self.dimensions[dir + 'max'] <= \
                surface.dimensions[dir + 'min']:
            return None
        else:
            a = [self.dimensions[dir + 'min'], self.dimensions[dir + 'max'], surface.dimensions[dir + 'min'],
                 surface.dimensions[dir + 'max']]
            a.sort()
            return a

    def get_area(self):
        A = 1
        for dir in ["x", "y", "z"]:
            try:
                A *= abs(self.dimensions[dir + 'min'] - self.dimensions[dir + 'max'])
            except:
                pass
        return A

    def _touching(self, dir, surface):
        return abs(self.dimensions[dir + 'min'] - surface.dimensions[dir + 'max']) < 1e-8 or \
               abs(self.dimensions[dir + 'max'] - surface.dimensions[dir + 'min']) < 1e-8

    def _aligned(self, dir, surface):
        return (self.dimensions[dir + 'max'] <= surface.dimensions[dir + 'max'] and \
                self.dimensions[dir + 'min'] >= surface.dimensions[dir + 'min']) or \
               (self.dimensions[dir + 'max'] >= surface.dimensions[dir + 'max'] and \
                self.dimensions[dir + 'min'] <= surface.dimensions[dir + 'min'])


    def is_connected(self, surface):
        if self.normal != surface.normal:
            return False
        elif self.value != surface.value:
            return False
        for i in range(len(self.directions)):
            dir = self.directions[i]
            dir2 = self.directions[i - 1]
            if self._touching(dir, surface) and self._aligned(dir2, surface):
                # print "+ + "+str(self.dimensions)+"  "+str(surface.dimensions)
                return True
                #else:
                #    print "- -  "+str(self.dimensions)+"  "+str(surface.dimensions)
        return False


class Mesher(object):
    def __init__(self, stt_data):
        self.sections = ["BOUNDARY", "GRIDPROPERTIES", "BBMR"]
        if self._check_stt_data(stt_data, self.sections):
            self.grid_properties = stt_data['GRIDPROPERTIES']
            self.blocks = [Block(stt_data=a) for a in stt_data['BBMR']['grids']]
            self.bbmr = self._check_bbmr(stt_data['BBMR'])
            self.boundary = stt_data['BOUNDARY']
            self.user_ref = stt_data['USERDEFREF']

    def _check_bbmr(self, bbmr):
        bbmr['grids'] = []
        return bbmr

    def _check_stt_data(self, stt_data, sections):
        for section in sections:
            if section not in stt_data.keys():
                print "ERROR in Mesher: " + section + " not in stt_data"
                return False
        return True

    def write(self, stt_file):
        self._set_boundaries()
        stt.write_section("USERDEFREF", self.user_ref, stt_file)
        stt.write_section("BOUNDARY", self.boundary, stt_file)
        stt.write_section("GRIDPROPERTIES", self.grid_properties, stt_file)
        grids = {'grids': [b.write() for b in self.blocks]}
        self.bbmr['grids'] = grids
        stt.write_section("BBMR", self.bbmr, stt_file)

    def add_user_ref(self, dir="x", point1= [0,0,0], point2=None):
        self.grid_properties["ref_mod"] = str(2)
        point1 = " ".join( [str(p) for p in point1])
        data = collections.OrderedDict()
        data['enable'] = 1
        if point2 is not None:
            point2 = " ".join( [str(p) for p in point2])
            data['type'] = 1
            data['point1'] = str(point1)
            data['point2'] = str(point2)
        else:
            data['type'] = 0
            data['point1'] = str(point1)
        key = dir.upper()+"REF"
        if key in self.user_ref:
            self.user_ref[key].append(data)
        else:
            self.user_ref[key] = [data]

    def add_block(self, block):
        self._update_block_id(block)
        self.blocks.append(block)

    def get_all_blocks_rectangles(self):
        rectangles = []
        for b in self.blocks:
            rectangles += b.get_rectangles()
        return rectangles

    @staticmethod
    def split_surfaces(surfaces):
        for a_surface in surfaces:
            for b_surface in surfaces:
                if a_surface != b_surface:
                    new_surfaces = b_surface.intersection(a_surface)
                    if new_surfaces is not None:
                        surfaces.remove(b_surface)
                        surfaces.remove(a_surface)
                        surfaces += new_surfaces
                        return Mesher.split_surfaces(surfaces)

        return surfaces

    def get_rectangles(self):
        rectangles = self.get_all_blocks_rectangles()
        rectangles = self.split_surfaces(rectangles)
        rectangles_dict = self.sort_surfaces_in_dict(rectangles)
        for dir in rectangles_dict.keys():
            for val in rectangles_dict[dir].keys():
                # get all rectangles in one dir at one value
                surfaces = rectangles_dict[dir][val]
                surfaces = self._merge_surfaces(surfaces)
                rectangles_dict[dir][val] = surfaces
        rectangles = []
        for dir in rectangles_dict.keys():
            for val in rectangles_dict[dir].keys():
                for a in rectangles_dict[dir][val]:
                    rectangles.append(a)
        return rectangles

    def sort_surfaces_in_dict(self, surfaces):
        bc_surfaces = {}
        for surface in surfaces:
            if surface.normal not in bc_surfaces.keys():
                bc_surfaces[surface.normal] = {}
            if surface.value not in bc_surfaces[surface.normal].keys():
                bc_surfaces[surface.normal][surface.value] = []
            bc_surfaces[surface.normal][surface.value].append(surface)
        return bc_surfaces

    def _merge_surfaces(self, surfaces):
        families = []
        while len(surfaces) > 0:
            family = RectangleFamily(surfaces[0])
            surfaces = family.find(surfaces)
            families.append(family.get_family_picture())
        return families

    def set_number_of_cells(self, nx=None, ny=None, nz=None):
        for dir, n in zip(['X', 'Y', 'Z'], [nx, ny, nz]):
            if n is not None:
                self.grid_properties[dir + '_DIRECTION']['cornerpoint_number'] = n

    def set_dx(self, dx):
        for dir in ['X', 'Y', 'Z']:
            self.set_grid_spacing(dir, dx)

    def get_dx(self):
        dx = []
        for dir in ['x', 'y', 'z']:
            dx[dir] = self.get_grid_spacing(dir)
        return dx

    def set_grid_spacing(self, axis, dx):
        box = self._get_bounding_box()
        l = box[axis.lower()]['max'] - box[axis.lower()]['min']
        n = l / dx
        self.grid_properties[axis.upper() + '_DIRECTION']['cornerpoint_number'] = int(n)

    def get_grid_spacing(self, axis):
        box = self._get_bounding_box()
        l = box[axis.lower()]['max'] - box[axis.lower()]['min']
        n = int(self.grid_properties[axis.upper() + '_DIRECTION']['cornerpoint_number'])
        dx = l / n
        return dx

    def create_domain(self, lx, ly, lz):
        bb = BoundBox(**{ 'xmin': 0, 'zmin': 0, 'ymin': 0,
                          'xmax': lx, 'ymax': ly, 'zmax': lz})
        self.set_blocks([bb])

    def get_number_of_blocks(self):
        return len(self.blocks)

    def _update_block_id(self, block):
        id = self.get_number_of_blocks()
        block.set_id(id + 1)
        return block, id

    def set_blocks(self, bboxes):
        self.blocks = []
        for bbox in bboxes:
            block = Block(dimensions=bbox)
            self.add_block(block)

    def split_blocks_in_two(self, blocks, volume):
        _blocks = []
        _continue = False
        for block in blocks:
            if block.get_volume() > volume:
                for b in block.split():
                    _blocks.append(b)
                    _continue = True
            else:
                _blocks.append(block)
        if _continue:
            return self.split_blocks_in_two(_blocks, volume)
        else:
            return _blocks


    def split_blocks(self, volume=None):
        volumes = []
        for block in self.blocks:
            volumes.append(block.get_volume())
        minimum = min(volumes)

        blocks = []

        if volume is None:
            for block in self.blocks:
                for b in block.split():
                    blocks.append(b)
        else:
            blocks = self.split_blocks_in_two(self.blocks, volume)
        self.blocks = []
        for block in blocks:
            self.add_block(block)

    def set_ratios(self, rx, ry, rz):
        for dir, n in zip(['X', 'Y', 'Z'], [rx, ry, rz]):
            self.grid_properties[dir + '_DIRECTION']['ratio'] = float(n)


    def _get_bounding_box(self):
        if len(self.blocks)==0:
            print "No block(s) added to setup. Try to add blocks with 'sim.setup.mesher.set_blocks()'"
            sys.exit()

        bbox = {}
        for dir in ['x', 'y', 'z']:
            min_values = [block.dimensions[dir + 'min'] for block in self.blocks]
            max_values = [block.dimensions[dir + 'max'] for block in self.blocks]
            bbox[dir] = {}
            bbox[dir]['min'] = float(min(min_values))
            bbox[dir]['max'] = float(max(max_values))
        return bbox

    def _set_boundaries(self):
        bbox = self._get_bounding_box()
        for dir in ['x', 'y', 'z']:
            # TODO repare grid spacing problems
            offset = 0#self.get_grid_spacing(dir) * 0.25
            self.boundary['minimal_' + dir] = bbox[dir]['min'] - offset
            self.boundary['maximal_' + dir] = bbox[dir]['max'] + offset

    def get_center(self, dir):
        bbox = self._get_bounding_box()
        tmp = bbox[dir]['max']-bbox[dir]['min']
        tmp = tmp/2.0
        return bbox[dir]['min']+tmp

    def get_min(self, dir):
        bbox = self._get_bounding_box()
        return bbox[dir]['min']

    def get_max(self, dir):
        bbox = self._get_bounding_box()
        return bbox[dir]['max']

    def get_volume(self):
        volume = 1
        for dir in ['x', 'y', 'z']:
            volume *= abs(self.get_max(dir)-self.get_min(dir))
        return volume

    def set_2D(self, axis1, axis2, offset=1e-7, origin=0.0):
        axes = ['x', 'y', 'z']
        axis = [a for a in axes if a is not axis1 and a is not axis2][0]
        blocks = []
        for b in self.blocks:
            if b.make_2D(axis, offset, origin=origin):
                blocks.append(b)
            else:
                print "Could not make block 2D"
                sys.exit()
        self.blocks=blocks
        axis.upper()
        self.set_grid_spacing(axis, offset)
