import unittest
from transat.setup.mesh import Rectangle
from transat.setup.mesh import Mesher
from transat.setup.mesh import RectangleFamily
from transat.config import ascomp_setup as config

global_config = config.install()


class TestRectangle(unittest.TestCase):
    def setUp(self):
        self.surface1 = Rectangle('x', dimensions={'ymin': 0, 'ymax': 1, 'zmin': 0, 'zmax': 1}, value=0,
                                  orientiation='min')
        self.surface2 = Rectangle('x', dimensions={'ymin': 0, 'ymax': 1, 'zmin': 0, 'zmax': 1}, value=2,
                                  orientiation='max')
        self.surface3 = Rectangle('x', dimensions={'ymin': 0.1, 'ymax': 0.9, 'zmin': 0.1, 'zmax': 0.9}, value=0,
                                  orientiation='min')

    def test_check_double_different_value(self):
        self.assertEqual(self.surface1.equal(self.surface2), False)

    def test_check_double(self):
        self.assertEqual(self.surface1.equal(self.surface1), True)


    def test_if_rectangles_are_connected(self):
        pass


class TestSurface(unittest.TestCase):
    def setUp(self):
        rect1 = Rectangle('x', dimensions={'ymin': 0, 'ymax': 1, 'zmin': 0, 'zmax': 1}, value=0, orientiation='min')
        rect2 = Rectangle('x', dimensions={'ymin': 0.1, 'ymax': 0.9, 'zmin': 0.1, 'zmax': 0.9}, value=0,
                          orientiation='min')
        pass
        # self.surface1 = Surface([rect1])
        #self.surface2 = Surface([rect2])


    def test_find_intersection_surface(self):
        pass
        # intersection = self.surface1.get_intersection(self.surface2)
        #self.assertEqual(intersection.equal(self.surface2), True )

    def test_remove_the_intersection_surface(self):
        pass
        # intersection = self.surface2.get_intersection(self.surface2)
        #surface = self.surface1.remove(intersection)
        #rectangles = surface.get_rectangles()


class TestRectangleFamily(unittest.TestCase):
    def setUp(self):
        self.rect1 = Rectangle('x', dimensions={'ymin': 1, 'ymax': 3, 'zmin': -1, 'zmax': 1}, value=0,
                               orientiation='min')
        self.rect2 = Rectangle('x', dimensions={'ymin': 0, 'ymax': 4, 'zmin': 0, 'zmax': 4}, value=0,
                               orientiation='max')
        self.rect3 = Rectangle('x', dimensions={'ymin': 1, 'ymax': 3, 'zmin': 1, 'zmax': 3}, value=0,
                               orientiation='min')

        self.rect4 = Rectangle('x', dimensions={'ymin': 4, 'ymax': 8, 'zmin': 0, 'zmax': 4}, value=0,
                               orientiation='max')
        self.rect5 = Rectangle('x', dimensions={'ymin': 3, 'ymax': 5, 'zmin': 1, 'zmax': 3}, value=0,
                               orientiation='min')

    def test_split_has_six(self):
        self.rectangles = [self.rect1, self.rect2]
        self.rectangles = Mesher.split_surfaces(self.rectangles)
        self.assertEqual(len(self.rectangles), 6)

    def test_split_has_height3(self):
        self.rectangles2 = [self.rect3, self.rect2]
        self.rectangle2 = Mesher.split_surfaces(self.rectangles2)
        self.assertEqual(len(self.rectangles2), 8)


    def test_split_has_height(self):
        rectangles = [self.rect2, self.rect3]
        rectangles = Mesher.split_surfaces(rectangles)
        self.assertEqual(len(rectangles), 8)

    def test_family_find(self):
        rectangles = [self.rect2, self.rect3]
        rectangles = Mesher.split_surfaces(rectangles)
        family = RectangleFamily(rectangles[0])
        family.find(rectangles)
        self.assertEqual(len(family.get_family_picture()), 8)

    def test_split_has_height2(self):
        self.assertEqual(len(self.rect2.intersection(self.rect3)), 8)

    def test_split_has_height2_inverse(self):
        self.assertEqual(len(self.rect3.intersection(self.rect2)), 8)

    def test_split_4(self):
        a = self.rect3.intersection(self.rect2)
        for b in a[1:]:
            c = a[0].intersection(b)
            self.assertIsNone(c)


    def test_family_with_3_rectangles(self):
        rectangles = [self.rect2, self.rect4, self.rect5]
        rectangles = Mesher.split_surfaces(rectangles)
        family = RectangleFamily(rectangles[0])
        family.find(rectangles)
        self.assertEqual(len(family.get_family_picture()), 10)


if __name__ == '__main__':
    unittest.main()
