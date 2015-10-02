import unittest
from transat.config import ascomp_setup as setup
from transat.simulation import Simulation
import os
import shutil
import math

class TestOutletResultsApp(unittest.TestCase):
    def setUp(self):
        self.global_config = setup.install()
        self.sim = Simulation('')
        self.sim.set_folder('bc_test_geometry', ['local'], 'tmp')
        self.sim.load_template('data/bc_test_geometry')
        self.tree = self.sim.setup.bcs.get_surface_tree()
        self.bc_names = self.tree.get_bc_names()
        r = 0.1/2.
        self.A = math.pi*math.pow(r, 2)

    def get_surfaces(self):
        bc_name = self.bc_names[0]
        return self.tree.get_surfaces_by_bc_name(bc_name).surfaces

    def get_plane(self):
        surface = self.get_surfaces()[0]
        vtm  = self.sim.postprocess.pa.get_last_modified(os.path.join(self.sim.load_path(), "RESULT"))
        data = self.sim.postprocess.pa.pa.OpenDataFile(vtm)
        normal = surface.get_normal()
        corners = surface.get_corners()

        return self.sim.postprocess.pa.get_plane(data, corners, normal)


    def test_setup_has_corrcet_bc_names(self):
        self.assertEqual(self.bc_names, ['inflow1', 'outflow', 'inflow2'])
#
    def test_para_reader_get_plane(self):
        plane = self.get_plane()
        #self.assertEqual(self.sim.postprocess.pa.get_bounds(plane), (0.0, 0.0, 0.0, 1.0, 0.0, 1.0))
#
    def test_has_ist(self):
        pass
#
    def test_input_write_out_all_variables(self):
        pass
#
    def test_avg(self):
        plane = self.get_plane()
        var = "U"
        avg = self.sim.postprocess.pa.massflow_avg(plane, weight=["U"], var=var, cell=False)
        print avg
#
    def test_avg_outflow(self):
        res = self.sim.postprocess.get_bc_results("outflow")[0]
        A = res['1*HembI']
        self.assertAlmostEqual(A, self.A, places=3)

    def test_avg_inflow1(self):
        res = self.sim.postprocess.get_bc_results("inflow1")[0]
        A = res['1*HembI']
        self.assertAlmostEqual(A, self.A, places=3)

    def test_avg_inflow2(self):
        res = self.sim.postprocess.get_bc_results("inflow2")[0]
        A = res['1*HembI']
        self.assertAlmostEqual(A, self.A, places=3)







