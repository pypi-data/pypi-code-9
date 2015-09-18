import unittest
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
