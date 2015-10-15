import unittest
import numpy as np
import math
from transat.setup.cad import Pipe
from transat.setup.cad import BoundBox
from transat.setup.cad import Network
from transat.setup.cad import CAD
from transat.config import ascomp_setup as setup

global_config = setup.install()


class TestCAD(unittest.TestCase):
    def setUp(self):
        cad = CAD(freecad_path=global_config.env['path']['freecad'])
        pipe = Pipe(name="pipe.stl", radius=0.01)
        pipe.add_point([0.0, 0.0, 0])
        pipe.add_point([1.0, 0.0, 0], 0.01)
        pipe.add_point([1.0, 1.0, 0])
        self.network = Network(cad, [pipe])
        self.network.create('tmp')

    def test_has_one_pipe(self):
        self.assertEqual(len(self.network.pipes), 1)

    def test_pipe_has_three_bboxes_before_intersection(self):
        pipe = self.network.pipes[0]
        bboxes = pipe.get_bounding_boxes()
        self.assertEqual(len(bboxes), 3)

    def test_bbox_intersection(self):
        pipe = self.network.pipes[0]
        bboxes = pipe.get_bounding_boxes()
        bbox1 = bboxes[0]

    def test_blocks_are_correct_when_elbow_radius_is_small(self):
        pass


class TestBBox(unittest.TestCase):
    def setUp(self):
        self.bbox1 = BoundBox(0, 1, 0, 1, 0, 1)
        self.bbox11 = BoundBox(0, 1, 0, 1, 0, 1)
        self.bbox2 = BoundBox(0.5, 1.5, 0.5, 1.5, 0, 1)

    def test_intersection(self):
        dim = self.bbox1.get_intersection(self.bbox2).unwrap()
        dim_target = {'zmax': 1.0, 'ymax': 1.0, 'zmin': 0.0, 'xmax': 1.0, 'xmin': 0.5, 'ymin': 0.5}
        self.assertEqual(dim, dim_target)

    def test_remove(self):
        tmp_box = self.bbox1.get_intersection(self.bbox2)
        boxes = self.bbox1.remove(tmp_box)
        self.assertEqual(len(boxes), 3)

    def test_equal_true(self):
        value = self.bbox1.equal(self.bbox11)
        self.assertEqual(value, True)

    def test_equal_false(self):
        value = self.bbox1.equal(self.bbox2)
        self.assertEqual(value, False)

class TestPipeNetwork(unittest.TestCase):
    def setUp(self):
        self.radius = 0.1
        self.l = math.sqrt(2)*self.radius

        self.p0 = np.array([0,0,0])
        self.p1 = np.array([1,0,0])
        self.p2 = np.array([1,1,0])

        self.pe_1 = self.p1-np.array([self.radius, 0, 0])
        self.pe_3 = self.p1+np.array([0, self.radius, 0])

        dr =1.0/math.sqrt(2)*(self.l - self.radius)
        self.pe_2 = self.p1+np.array([-dr, dr, 0])

        self.dc1 = np.array([0, 1, 0])
        self.dc3 = np.array([-1, 0, 0])

        self.n = np.array([0, 0, -1])
        self.d1 = np.array([-1, 0, 0])
        self.d2 = np.array([0, 1, 0])

        self.center = np.array([0.9, 0.1, 0])
        self.a = math.pi/2.0

        pipe = Pipe(name="pipe.stl", radius=0.01)
        pipe.add_point(self.p0)
        pipe.add_point(self.p1, self.radius)
        pipe.add_point(self.p2)
        self.pipe = pipe

    def test_get_elbow_points(self):
        pe_1, pe_2, pe_3 = self.pipe._get_elbow_points(radius=self.radius, p0=self.p0, p1=self.p1, p2=self.p2)
        np.testing.assert_almost_equal(pe_1, self.pe_1)
        np.testing.assert_almost_equal(pe_2, self.pe_2)
        np.testing.assert_almost_equal(pe_3, self.pe_3)


    def test_director_vectors(self):
        d1 = self.pipe._get_vector(self.p1, self.p0)
        d2 = self.pipe._get_vector(self.p1, self.p2)
        a = self.pipe._get_angle(d1, d2)

        np.testing.assert_almost_equal(d1, self.d1)
        np.testing.assert_almost_equal(d2, self.d2)
        np.testing.assert_almost_equal(a, self.a)

    def test_get_normal(self):
        n = self.pipe._get_normal_vector(self.d1, self.d2)
        np.testing.assert_almost_equal(n, self.n)

    def test_dc(self):
        dc1, dc3 = self.pipe._get_dc_vectors(self.d1, self.d2, self.pe_1, self.pe_3, self.radius)
        np.testing.assert_almost_equal(dc1, self.dc1)
        np.testing.assert_almost_equal(dc3, self.dc3)

    def test_get_elbow_center(self):
        center = self.pipe._get_elbow_center(self.pe_1, self.dc1, self.radius)
        np.testing.assert_almost_equal(center, self.center)

    def test_get_point_on_circle(self):
        pe_2 = self.pipe._get_point_on_circle(self.center, self.radius, self.dc1, self.dc3)
        np.testing.assert_almost_equal(pe_2, self.pe_2)

    def test_get_l(self):
        l = self.pipe._get_l(self.radius, self.a)
        self.assertAlmostEqual(l, self.l)

    def test_pe(self):
        pe_1 = self.pipe._get_pe(self.p1, self.d1, self.l, self.radius)
        pe_3 = self.pipe._get_pe(self.p1, self.d2, self.l, self.radius)
        np.testing.assert_almost_equal(self.pe_1, pe_1)
        np.testing.assert_almost_equal(self.pe_3, pe_3)


class TestPipeNetwork_clockwise(TestPipeNetwork):
    def setUp(self):
        self.radius = 0.1
        self.l = math.sqrt(2)*self.radius

        self.p0 = np.array([1, 1, 0])
        self.p1 = np.array([1, 0, 0])
        self.p2 = np.array([0, 0, 0])

        self.pe_1 = self.p1+np.array([0, self.radius, 0])
        self.pe_3 = self.p1-np.array([self.radius, 0, 0])

        dr =1.0/math.sqrt(2)*(self.l - self.radius)
        self.pe_2 = self.p1+np.array([-dr, dr, 0])

        self.dc1 = np.array([-1, 0, 0])
        self.dc3 = np.array([ 0, 1, 0])

        self.n = np.array([0, 0, 1])
        self.d1 = np.array([0, 1, 0])
        self.d2 = np.array([-1, 0, 0])

        self.center = np.array([0.9, 0.1, 0])
        self.a = math.pi/2.0

        pipe = Pipe(name="pipe.stl", radius=0.01)
        pipe.add_point(self.p0)
        pipe.add_point(self.p1, self.radius)
        pipe.add_point(self.p2)
        self.pipe = pipe





class TestPipe(TestPipeNetwork):
    def setUp(self):

        self.radius = 0.1
        self.l = math.sqrt(2)*self.radius

        self.p0 = np.array([0,0,0])
        self.p1 = np.array([0,1,0])
        self.p2 = np.array([1,1,0])

        self.pe_1 = self.p1-np.array([0, self.radius, 0])
        self.pe_3 = self.p1+np.array([self.radius, 0, 0])

        dr =1.0/math.sqrt(2)*(self.l - self.radius)
        self.pe_2 = self.p1+np.array([dr, -dr, 0])

        self.dc1 = np.array([ 1, 0, 0])
        self.dc3 = np.array([ 0, -1, 0])

        self.n = np.array([0, 0, 1])
        self.d1 = np.array([0, -1, 0])
        self.d2 = np.array([1, 0, 0])

        self.center = self.p1+np.array([self.radius, -self.radius, 0])
        self.a = math.pi/2.0

        pipe = Pipe(name="pipe.stl", radius=self.radius/2.0)
        pipe.add_point(self.p0)
        pipe.add_point(self.p1, self.radius)
        pipe.add_point(self.p2)
        self.pipe = pipe
        pipe.create(    cad = CAD(freecad_path=global_config.env['path']['freecad']), path="")


