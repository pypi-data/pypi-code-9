import unittest
from transat.setup.cad import Pipe
from transat.setup.cad import BoundBox
from transat.setup.cad import Network
from transat.setup.cad import CAD
from transat.config import ascomp_setup as setup
from transat.simulation import Simulation

global_config = setup.install()


class TestBC(unittest.TestCase):
    def setUp(self):
        self.sim = Simulation("bcsimulation")
        self.sim.set_folder("simsurfacetreetest", ['local'], base_folder="tmp")
        self.sim.load_template("../data/surfacetree")

        self.tree = self.sim.setup.bcs.get_surface_tree()


    def test_surface_location(self):

        bcs = ['inflow', 'outflow1', 'outflow2']
        locations = [{'x':0.0, 'y':0.0, 'z':0.0},
                     {'x':10.0, 'y':0.0, 'z':0.0},
                     {'y': 0.8, 'x': 10.0, 'z': 0.0}]
        for bc, loc in zip(bcs, locations):
            for surf in self.tree.get_surfaces_by_bc_name(bc).get_all():
                _loc = surf.get_location()
                for key in _loc.keys():
                    self.assertAlmostEqual(_loc[key], loc[key] )


    def test_get_bc_names(self):
        names = self.tree.get_bc_names()
        self.assertEqual(sorted(names), sorted(['inflow', 'outflow1', 'outflow2']))
#
        names = self.tree.get_bc_names(True)
        self.assertEqual(sorted(names), sorted(['inflow', 'outflow1', 'undefined', 'undefined', 'undefined', 'undefined', 'outflow2']))
#
    def test_get_normal(self):
        for surf in self.tree.get_surfaces_by_bc_name('outflow2').get_all():
            self.assertEqual(surf.get_normal(), 'x')
#
        for surf in self.tree.get_surfaces_by_bc_name('outflow1').get_all():
            self.assertEqual(surf.get_normal(), 'x')
#
        for surf in self.tree.get_surfaces_by_bc_name('inflow').get_all():
            self.assertEqual(surf.get_normal(), 'x')