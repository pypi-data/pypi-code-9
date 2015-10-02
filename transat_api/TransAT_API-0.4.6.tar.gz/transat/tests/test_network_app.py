import unittest

from transat.simulation import Simulation
import transat.appbuilder as appbuilder
from transat.setup.cad import Pipe
from transat.setup.cad import Network
from transat.setup.cad import CAD
from transat.config import ascomp_setup as setup

global_config = setup.install()


class TestNewtorkApp(unittest.TestCase):
    def create_network(self):
        pipe = Pipe(name="pipe.stl", radius=0.025)
        pipe.add_point([-0.5, 0.0, 0])
        pipe.add_point([0.5, 0.0, 0], 0.1)
        pipe.add_point([0.5, -0.5, 0], 0.1)
        pipe.add_point([1.0, -0.5, 0])
        # pipe.add_point([ 1.0, -0.5, 1])

        self.pipe = pipe

        pipe2 = Pipe(name="pipe2.stl", radius=0.025)
        pipe2.add_point([0, 0.5, 0])
        pipe2.add_point([0, 0.0, 0])
        self.pipe2 = pipe2

        network = Network(self.cad, [pipe, pipe2])
        network.create(self.sim.load_path('local'))
        self.network = network

    def setUp(self):
        self.cad = CAD(freecad_path=global_config.env['path']['freecad'])
        self.sim = Simulation('test_api')
        self.sim.set_folder('test_hydrate', ['local'], base_folder="tmp")
        self.sim.load_template('templates/network')
        self.create_network()
        self.sim.setup.mesher.set_blocks(self.network.get_blocks())
        self.sim.setup.ist.add(self.network.get_pipes_name())

        self.sim.setup.mesher.set_number_of_cells(500, 500, 50)

        self.sim.setup.bcs.get_bc('inflow_gas').set_velocities([1, 0, 0])

        self.sim.setup.mesher.split_blocks()

        tree = self.sim.setup.bcs.create_surfaces_tree()
        tree.get_all_surfaces().set_bc_name('wall')
        tree.get_surface_with_point(self.pipe.get_inlet_point()).set_bc_name('inflow_gas')
        tree.get_surface_with_point(self.pipe.get_outlet_point()).set_bc_name('outflow')
        tree.get_surface_with_point(self.pipe2.get_inlet_point()).set_bc_name('outflow')
        self.tree = tree
        self.sim.setup.write()

    def test_has_4_xmin_surfaces(self):
        surfaces = self.tree.get_all_surfaces().for_dir('x').minmax('min').surfaces
        self.assertEqual(len(surfaces), 4)

    def test_has_4_xmax_surfaces(self):
        surfaces = self.tree.get_all_surfaces().for_dir('x').minmax('max').surfaces
        self.assertEqual(len(surfaces), 4)

    def print_surfaces(self, surfaces):
        for s in surfaces:
            print s.rectangles[0].normal + " " + str(s.rectangles[0].value) + " "
            for r in s.rectangles:
                print "\t" + str(r.dimensions)

    def test_has_3_ymin_surfaces(self):
        surfaces = self.tree.get_all_surfaces().for_dir('y').minmax('min').surfaces
        self.assertEqual(len(surfaces), 3)

    def test_has_5_ymax_surfaces(self):
        surfaces = self.tree.get_all_surfaces().for_dir('y').minmax('max').surfaces
        self.assertEqual(len(surfaces), 5)

    def test_has_1_zmin_surfaces(self):
        self.assertEqual(len(self.tree.get_all_surfaces().for_dir('z').minmax('min').surfaces), 1)

    def test_has_1_zmax_surfaces(self):
        self.assertEqual(len(self.tree.get_all_surfaces().for_dir('z').minmax('max').surfaces), 1)







