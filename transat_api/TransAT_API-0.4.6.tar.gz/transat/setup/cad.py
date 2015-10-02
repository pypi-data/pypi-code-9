import sys
import copy
import os
import signal
import numpy as np
import math
import logging

logger = logging.getLogger(__name__)


class PointsAreTheSameError(Exception):
    def __init__(self, p0, p1):
        self.msg = 'Points are the same ' + str(p0) + ' ' + str(p1)

    def __str__(self):
        return self.msg


def load_module(freecad_path):
    sys.path.append(freecad_path)
    import FreeCAD as FreeCAD
    import Part as Part

    return Part, FreeCAD


class Edge(object):
    def __init__(self, p1, p2):
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)

    def is_aligned(self):
        for sign in [-1, 1]:
            for axe in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]:
                axe = Edge([0, 0, 0], axe)
                dir = Edge(self.p2, self.p1)
                if dir.is_collinear_with(axe): return True
        return False

    def is_equal(self, edge):
        if np.all(np.equal(self.p1, edge.p1)) and np.all(np.equal(self.p2, edge.p2)):
            return True
        elif np.all(np.equal(self.p1, edge.p2)) and np.all(np.equal(self.p2, edge.p1)):
            return True
        else:
            return False

    def is_normal_to_surface(self, surface):
        if np.dot(surface.get_normal(), self.get_dir_vector()) == 1.0:
            return True
        elif np.dot(surface.get_normal(), self.get_dir_vector()) == -1.0:
            return True
        else:
            return False

    def has_intersection_with_surface(self, surface):
        if self.is_normal_to_surface(surface):
            d1 = self.distances_to_surface(surface, self.p1)
            d2 = self.distances_to_surface(surface, self.p2)
            if d1 * d2 < 0:
                p = self.get_intersection_point(surface)
                if surface.contains(p):
                    return True
        return False

    def distances_to_surface(self, surface, x0):
        n = surface.get_normal()
        xi = surface.edges[0].p1
        return np.dot(n, x0 - xi)

    def get_dir_vector(self):
        dir = self.p2 - self.p1
        dir = dir / np.linalg.norm(dir)
        return dir

    def is_collinear_with(self, edge):
        dir1 = self.get_dir_vector()
        dir2 = edge.get_dir_vector()
        if np.linalg.norm(dir1 - dir2) < 1e-10:
            return True
        else:
            return False

    def get_intersection_point(self, surface):
        d1 = self.distances_to_surface(surface, self.p1)
        d2 = self.distances_to_surface(surface, self.p2)
        p_star = self.p1 + abs(d1) * self.get_dir_vector()
        if d1 * d2 < 0:
            return p_star


class Surface(object):
    def __init__(self, p1, p2, p3, p4):
        self.edges = []
        points = [p1, p2, p3, p4]
        for point1 in points:
            for point2 in points:
                edge = Edge(point1, point2)
                if point1 != point2 and edge.is_aligned():
                    if not np.any([edge.is_equal(edg) for edg in self.edges]):
                        self.edges.append(edge)

    def get_normal(self):
        for edge1 in self.edges:
            for edge2 in self.edges:
                if edge1 is not edge2:
                    if edge1.is_collinear_with(edge2) == False:
                        n = np.cross(edge1.get_dir_vector(), edge2.get_dir_vector())
                        n = n / np.linalg.norm(n)
                        return n

    def contains(self, point):
        points = []
        for edge in self.edges:
            points.append(edge.p1)
            points.append(edge.p2)
        for i in range(3):
            normal = abs(self.get_normal()[i]) > 0.0
            if not normal:
                max_value = max([p[i] for p in points])
                min_value = min([p[i] for p in points])
                val = float(point[i])
                if val > max_value or val < min_value:
                    return False
        return True

    def get_points(self):
        points = []
        for edge in self.edges:
            points.append(edge.p1)
            points.append(edge.p2)
        return points


class BoundBox(object):
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        n = 8
        # xmin = round(xmin, n)
        #        xmax = round(xmax, n)
        #        ymin = round(ymin, n)
        #        ymax = round(ymax, n)
        #        zmin = round(zmin, n)
        #        zmax = round(zmax, n)

        self.boundaries = {}
        self.boundaries['x'] = {'min': xmin, 'max': xmax}
        self.boundaries['y'] = {'min': ymin, 'max': ymax}
        self.boundaries['z'] = {'min': zmin, 'max': zmax}

        self.surfaces = {}
        self.surfaces['top'] = Surface([xmin, ymin, zmax], [xmin, ymax, zmax],
                                       [xmax, ymin, zmax], [xmax, ymax, zmax])
        self.surfaces['bot'] = Surface([xmin, ymin, zmin], [xmin, ymax, zmin],
                                       [xmax, ymin, zmin], [xmax, ymax, zmin])
        self.surfaces['north'] = Surface([xmin, ymin, zmin], [xmin, ymax, zmin],
                                         [xmin, ymin, zmax], [xmin, ymax, zmax])
        self.surfaces['south'] = Surface([xmax, ymin, zmin], [xmax, ymax, zmin],
                                         [xmax, ymin, zmax], [xmax, ymax, zmax])
        self.surfaces['east'] = Surface([xmax, ymin, zmin], [xmin, ymin, zmin],
                                        [xmax, ymin, zmax], [xmin, ymin, zmax])
        self.surfaces['west'] = Surface([xmax, ymax, zmin], [xmin, ymax, zmin],
                                        [xmax, ymax, zmax], [xmin, ymax, zmax])

    def equal(self, bbox):
        return bbox.unwrap() == self.unwrap()

    def unwrap(self):
        bbox = {}
        for dir in ['x', 'y', 'z']:
            for val in ['min', 'max']:
                bbox[dir + val] = round(self.boundaries[dir][val], 4)
        return bbox

    def remove(self, bbox):
        if bbox == None:
            return []

        points = []
        points += self.get_points()
        points += bbox.get_points()
        points = self.make_points_unique(points)
        xs = sorted(list(set([p[0] for p in points])))
        ys = sorted(list(set([p[1] for p in points])))
        zs = sorted(list(set([p[2] for p in points])))
        bboxes = []
        for i in range(len(xs) - 1):
            for j in range(len(ys) - 1):
                for k in range(len(zs) - 1):
                    bboxes.append(BoundBox(xs[i], xs[i + 1], ys[j], ys[j + 1], zs[k], zs[k + 1]))
        bboxes2 = []
        for _bbox in bboxes:
            if _bbox.unwrap() != bbox.unwrap():
                bboxes2.append(_bbox)
        return bboxes2

    def get_points(self):
        points = []
        for key in self.surfaces.keys():
            points += self.surfaces[key].get_points()
        points = self.make_points_unique(points)
        return points

    def contains_point(self, point):
        ids = {'x': 0, 'y': 1, 'z': 2}
        n = 8
        for key in self.boundaries.keys():
            value = round(point[ids[key]], n)
            bound = self.boundaries[key]
            if value > round(bound['max'], n) or value < round(bound['min'], n):
                return False
        return True

    def contains(self, edge):
        points = []
        # check if wedge is fully inside the bbox
        has_p1 = self.contains_point(edge.p1)
        has_p2 = self.contains_point(edge.p2)
        if has_p1 and has_p2:
            points.append(edge.p1)
            points.append(edge.p2)

        # check if intersection
        for key in self.surfaces.keys():
            surface = self.surfaces[key]
            if edge.has_intersection_with_surface(surface):
                p = edge.get_intersection_point(surface)
                points.append(p)
        return points

    def _get_edges(self):
        edges = []
        for key in self.surfaces.keys():
            for edge in self.surfaces[key].edges:
                if not np.any([edge.is_equal(edg) for edg in edges]):
                    edges.append(edge)
        return edges

    def get_intersection(self, bbox):
        points = []
        for edge in self._get_edges():
            _points = bbox.contains(edge)
            if _points:
                points += _points
        for edge in bbox._get_edges():
            _points = self.contains(edge)
            if _points:
                points += _points
        points = self.make_points_unique(points)
        inter_bbox = self.from_points_to_bbox(points)
        return inter_bbox

    def make_points_unique(self, points):
        _points = []
        for p in points:
            if np.any([np.all(np.abs(p - _p) < 1e-6) for _p in _points]) == False:
                _points.append(p)
        return _points

    def from_points_to_bbox(self, points):
        if len(points) == 0:
            return None
        elif len(points) != 8:
            return None
        else:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            zs = [p[2] for p in points]
            return BoundBox(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


class CAD(object):
    def __init__(self, freecad_path):
        self.freecad_path = freecad_path
        self.load_freecad()

    def load_freecad(self):
        try:
            self.Part, self.FreeCAD = load_module(self.freecad_path)

            def signal_handler(signal, frame):
                raise (KeyboardInterrupt)

            signal.signal(signal.SIGINT, signal_handler)
            return True

        except ImportError, e:
            print "WARNING: import FreeCAD failed. Initializing CAD object with empty attributes"
            print self.freecad_path
            print e
            return False

    def create_cylinder(self, cylinder, path="", name="cylinder.stl"):
        H = cylinder['H']
        r = cylinder['r']
        base = cylinder['base']
        normal = cylinder['normal']
        base_vec = self.FreeCAD.Base.Vector(base[0], base[1], base[2])
        norm_vec = self.FreeCAD.Base.Vector(normal[0], normal[1], normal[2])
        cy = self.Part.makeCylinder(r, H, base_vec, norm_vec)
        cy.exportStl(os.path.join(path, name))
        a = str(cy.BoundBox)
        a, b = a.split('(')
        b, a = b.split(')')
        c = b.split(',')
        return [float(i) for i in c]

    def make_wire(self, segments):
        try:
            wires = []
            for segment in segments:
                ps = []
                for p in segment['points']:
                    ps.append(self.FreeCAD.Base.Vector(p[0], p[1], p[2]))
                if 'arc' in segment.keys():
                    wires.append(self.Part.Arc(ps[0], ps[1], ps[2]).toShape())
                else:
                    wires.append(self.Part.Line(ps[0], ps[1]).toShape())
            return self.Part.Wire(wires)

        except Exception, e:
            print 'Error while making wire with freecad: ' + str(e)
            raise

    def make_circle(self, radius, o, d):
        return self.Part.makeCircle(radius, self.FreeCAD.Base.Vector(o[0], o[1], o[2]),
                                    self.FreeCAD.Base.Vector(d[0], d[1], d[2]))

    def make_pipe(self, wire, circle, filename):
        try:
            circle = self.Part.Wire(circle)
            pipe = wire.makePipeShell([circle], True, False)
            pipe = self.Part.makeSolid(pipe)
            pipe.exportStl(filename)
        except Exception, e:
            print "Can not create Pipe "
            sys.exit()

    def make_rotate_extrude(self, points, vec, pos, name):

        wires = []
        ps = []
        for p in points:
            ps.append(self.FreeCAD.Base.Vector(p[0], p[1], p[2]))
        for i in range(len(ps)-1):
            wires.append(self.Part.Line(ps[i], ps[i+1]).toShape())
        wires.append(self.Part.Line(ps[-1], ps[0]).toShape())
        wire = self.Part.Wire(wires)

        pos = self.FreeCAD.Base.Vector(pos[0], pos[1], pos[2])
        vec = self.FreeCAD.Base.Vector(vec[0], vec[1], vec[2])
        angle = 360
        solid = wire.revolve(pos, vec, angle)
        solid.exportStl(name)

class Network():
    def __init__(self, cad, pipes):
        self.pipes = pipes
        self.cad = cad

    def create(self, path):
        for pipe in self.pipes:
            pipe.create(self.cad, path)

    def _check_bboxes(self):
        for bbox in self.bboxes:
            print bbox

    def get_pipes_name(self):
        return [pipe.get_name() for pipe in self.pipes]

    def remove_intersection(self, bboxes, bbox):
        for _bbox in bboxes:
            if not bbox.equal(_bbox):
                tmp_box = _bbox.get_intersection(bbox)
                if tmp_box is not None:
                    bboxes.remove(_bbox)
                    bboxes += _bbox.remove(tmp_box)
                    return self.remove_intersection(copy.deepcopy(bboxes), bbox)
        return bboxes

    def remove_intersections(self, bboxes):
        for bbox in bboxes:
            _bboxes = self.remove_intersection(bboxes, bbox)
            if bboxes is not _bboxes:
                return self.remove_intersections(copy.deepcopy(_bboxes))
        return bboxes

    def get_blocks(self):
        bboxes = []
        for pipe in self.pipes:
            bboxes += pipe.get_bounding_boxes()
        bboxes = self.remove_intersections(bboxes)
        bboxes = self._unwrap_bboxes(bboxes)
        return bboxes

    def _unwrap_bboxes(self, bboxes):
        _bboxes = []
        for bbox in bboxes:
            _bboxes.append(bbox.unwrap())
        return _bboxes

    def _join(self, _bboxes):
        bboxes = []
        for pipe in self.pipes:
            start = self._get_junction_offset(pipe, 0)
            end = self._get_junction_offset(pipe, -1)
            # bboxes += pipe.get_bounding_boxes(junctions_offset=[start, end])
            bboxes += pipe.get_bounding_boxes()
        return bboxes

    def _get_junction_offset(self, pipe, id):
        junction = pipe.junctions[id]
        if junction == "open":
            return -0.1
        elif junction == "T":
            bbox = pipe.get_bounding_boxes()[id]
            bboxes = []
            for _pipe in self.pipes:
                if pipe != _pipe:
                    bboxes += _pipe.get_bounding_boxes()
            box = self._find_overlapping_box(bboxes, bbox)
            self._find_overlapping_length(box, bbox)
        return 0


    def _1d_overlap(self, box1, box2, dir):
        l1 = box1[dir + "min"] - box2[dir + "min"]
        l2 = box2[dir + "min"] - box1[dir + "max"]
        a = l1 <= 0 and l2 <= 0

        l3 = box2[dir + "min"] - box2[dir + "min"]
        l4 = box1[dir + "min"] - box2[dir + "max"]
        b = l3 <= 0 and l4 <= 0

        return (a or b)

    def _find_overlapping_box(self, bboxes, bbox):
        for box in bboxes:
            if np.all([self._1d_overlap(box, bbox, dir) for dir in ['x', 'y', 'z']]):
                return box

    def _find_overlapping_length(self, box1, box2):
        print box1
        print box2
        pass


class Pipe(CAD):
    def __init__(self, name, radius, junctions=['open', 'open']):
        self.points = []
        self.radius = radius
        self.elbows = []
        self.segments = []
        self.name = name
        self.junctions = junctions

    def add_point(self, point=[], radius=None):
        self.points.append(np.array(point))
        self.elbows.append({'radius': radius})

    def _create_straight_pipe(self):
        pass

    def _create_elbow(self):
        pass

    def _get_vector(self, p0, p1):
        if np.all(p0 - p1 == [0, 0, 0]):
            print "You are trying to compute the direction vector of identical points. Check your setup"
        try:
            d = []
            for a, b in zip(p0, p1):
                d.append(b - a)
            return np.array(d) / np.linalg.norm(d)
        except:
            print "Error in _get_vector"

    def _get_angle(self, d1, d2):
        c = np.dot(d1, d2) / np.linalg.norm(d1) / np.linalg.norm(d2)
        angle = np.arccos(c)  # np.clip(c, -1, 1)) # if you really want the angle
        return angle

    @staticmethod
    def _get_elbow_center(pe_1, pe_3, dc1, dc3, radius):
        center1 = pe_1 - radius * dc1
        center2 = pe_3 + radius * dc3
        dist = np.linalg.norm(center1 - center2)
        if dist > 1e-10:
            raise PointsAreTheSameError(center1, center2)
        else:
            return center1

    @staticmethod
    def _get_point_on_circle(center, radius, p1, l):
        d = center - p1
        norm = np.linalg.norm(d)

        if norm == 0.0:
            raise PointsAreTheSameError(center, p1)

        d = d / norm
        p = p1 + d * (math.sqrt(math.pow(l, 2) + math.pow(radius, 2)) - radius)
        return p

    def _get_elbow_points(self, radius, p0, p1, p2):
        d1 = self._get_vector(p1, p0)
        d2 = self._get_vector(p1, p2)
        a = self._get_angle(d1, d2)
        l = radius / np.tan(a / 2)

        n = np.cross(d1, d2)
        dc1 = np.cross(d1, n)
        dc1 = dc1 / np.linalg.norm(dc1)
        dc3 = np.cross(d2, n)
        dc3 = dc3 / np.linalg.norm(dc3)

        pe_1 = p1 + d1 * l
        pe_3 = p1 + d2 * l

        center = self._get_elbow_center(pe_1, pe_3, dc1, dc3, radius)
        try:
            pe_2 = self._get_point_on_circle(center, radius, p1, l)
        except PointsAreTheSameError:
            return pe_1, pe_1 + d1 * l / 2.0, pe_3,

        return pe_1, pe_2, pe_3


    def _get_three_consequent_points(self, ii):
        p0 = self.points[ii]
        p1 = self.points[ii + 1]
        p2 = self.points[ii + 2]
        return p0, p1, p2

    def _get_elbow_radius(self, ii):
        radius = self.elbows[ii]['radius']
        if radius is None:
            radius = self.radius
        return radius

    def _compute_segment(self, ii):
        radius = self._get_elbow_radius(ii + 1)
        p0, p1, p2 = self._get_three_consequent_points(ii)
        pe_1, pe_2, pe_3 = self._get_elbow_points(radius, p0, p1, p2)
        self.points[ii + 1] = pe_3
        self._add_straight_segment(p0, pe_1)
        self._add_elbow_segment(pe_1, pe_2, pe_3, radius)

    def _add_straight_segment(self, p1, p2):
        self.segments.append({'points': [p1, p2]})

    def _add_elbow_segment(self, p1, p2, p3, radius):
        self.segments.append({'points': [p1, p2, p3], 'arc': True, 'radius': radius})

    def _compute_network_segments(self):
        self.segments = []
        n = len(self.points) - 2
        if n > 0:
            for ii in range(n):
                self._compute_segment(ii)
            self._add_straight_segment(self.points[-2], self.points[-1])
        else:
            self._add_straight_segment(self.points[0], self.points[1])


    def create(self, cad, path):
        self.filename = os.path.join(path, self.name)
        self._compute_network_segments()
        d = self._get_vector(self.points[0], self.points[1])
        circle = cad.make_circle(self.radius, self.points[0], d)
        wire = cad.make_wire(self.segments)
        cad.make_pipe(wire, circle, self.filename)

    def get_name(self):
        return self.name

    def get_bounding_boxes(self):
        bboxes = []
        start_offsets = np.zeros_like(self.segments)
        stop_offsets = np.zeros_like(self.segments)

        if self.junctions[0] == "open":
            start_offsets[0] = -self.radius / 2.0  # junctions_offset[0]
        else:
            start_offsets[0] = 0.0


        if self.junctions[-1] == "open":
            stop_offsets[-1] = -self.radius / 2.0  # junctions_offset[0]
        else:
            stop_offsets[-1] = 0.0

        for idx, segment in enumerate(self.segments):
            offset_values = [start_offsets[idx], stop_offsets[idx]]
            box, _segment = self._get_segment_bounding_boxe(segment, offset_values=offset_values)
            bboxes.append(box)
            self.segments[idx] = _segment
        return bboxes

    def get_inlet_point(self):
        return self.segments[0]['points'][0]

    def get_outlet_point(self):
        return self.segments[-1]['points'][-1]

    def _get_segment_bounding_boxe(self, segment, dr=1.5, offset_values=[0, 0]):
        dirs = self._get_segment_director_vectors(segment)
        points = []
        for side, ii, offset_value in zip(['in', 'out'], [0, -1],
                                          offset_values):
            n = dirs[side]
            d1 = dirs['n']
            d2 = np.cross(n, d1)
            d2 = d2 / np.linalg.norm(d2)

            p = np.array(segment['points'][ii] + n * offset_value)
            segment['points'][ii] = p

            for sign in [1, -1]:
                for k in [d2, d1]:
                    points.append(np.array(p) + sign * np.array(k) * (self.radius * dr))
        names = ['x', 'y', 'z']
        bbox = {}
        for i, name in zip(range(3), names):
            values = [p[i] for p in points]
            bbox[name + "min"] = min(values)
            bbox[name + "max"] = max(values)
        return BoundBox(**bbox), segment

    def _get_segment_director_vectors(self, segment):
        if len(segment['points']) == 2:
            p0 = segment['points'][0]
            p1 = segment['points'][1]
            dv = (p1 - p0) / np.linalg.norm(p1 - p0)
            for trial in [[1, 0, 1], [0, 1, 0], [0, 0, 1]]:
                if np.dot(trial, dv) < 1:
                    n = np.cross(trial, dv)
            return {'in': -dv, 'out': dv, 'n': n}

        elif len(segment['points']) == 3:
            p0 = segment['points'][0]
            p1 = segment['points'][1]
            p2 = segment['points'][2]

            n = np.cross(p1 - p0, p2 - p0)
            n = n / np.linalg.norm(n)

            dc = np.cross(n, p2 - p0)
            dc = dc / np.linalg.norm(dc)
            center = p1 + segment['radius'] * dc

            dv1 = np.cross(p0 - center, n)
            dv1 = dv1 / np.linalg.norm(dv1)

            dv2 = np.cross(p2 - center, n)
            dv2 = dv2 / np.linalg.norm(dv2)

            return {'in': dv1, 'out': -dv2, 'n': n}


if __name__ == "__main__":
    cad = CAD('/usr/lib/freecad/lib')

    H = 10
    x = 0.0
    y = 2
    r = 2

    base = [x, y, 0]
    normal = [1, 0, 0]

    cy = {'base': base, 'normal': normal, 'H': H, 'r': r}
    cad.create_cylinder(**cy)
