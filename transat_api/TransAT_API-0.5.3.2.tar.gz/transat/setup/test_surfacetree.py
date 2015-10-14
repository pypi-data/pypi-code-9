import unittest
from transat.simulation import Simulation
from transat.setup.mesh import Rectangle
from transat.setup.mesh import Mesher
from transat.setup.mesh import RectangleFamily
from transat.config import ascomp_setup as config
import os

#  nosetests --nocapture --rednose --verbose transat.setup.test_surfacetree

#global_config = config.install()

"""
Strange problem
When using get_surfaces_by_bc_name multiple times, dan vult de lijst zich en krijg je teveel surfaces die er niet zijn
als we de surfacelijst een [] meegeven is het goed

"""



class TestSurfaceTree(unittest.TestCase):
    def setUp(self):
        self.sim = Simulation("avgsimulation")
        self.sim.set_folder("../../tmp/simsurfacetreetest", ['local'])
        self.sim.load_template("../../tmp/surfacetreetest")




    def test_volume(self):
        self.assertEqual(self.sim.setup.mesher.get_volume(), 0.72)

    def test_surfacetree(self):
        tree = self.sim.setup.bcs.get_surface_tree()

        for surf in tree.get_surfaces_by_bc_name('inflow').get_all():
            self.assertAlmostEqual(surf.get_area(), 0.6*0.6)
            for rect in surf.get_rectangles():
                self.assertAlmostEqual(rect.get_area(), 0.3*0.3)
        for surf in tree.get_surfaces_by_bc_name('outflow1').get_all():
            self.assertAlmostEqual(surf.get_area(), 0.6*0.6)
            for rect in surf.get_rectangles():
                self.assertAlmostEqual(rect.get_area(), 0.3*0.3)

        A = 0
        for surf in tree.get_surfaces_by_bc_name('outflow2').get_all():
            A += surf.get_area()
        self.assertAlmostEqual(A, 2.0*0.6)






if __name__ == '__main__':
    unittest.main()
