import unittest
import os

from transat.setup.cad import CAD
from transat.config import ascomp_setup as setup


class TestInstallationApp(unittest.TestCase):
    def setUp(self):
        self.global_config = setup.install()

    def test_has_paraview(self):
        try:
            import paraview.simple
            self.assertEqual(True, True)
        except:
            self.assertEqual(False, True, "Could not import paraview")

    def test_has_freecad(self):
        self.cad = CAD(freecad_path=self.global_config.env['path']['freecad'])
        self.assertEqual(True,self.cad.load_freecad())

    def test_has_transat_ui(self):
        has_path = os.path.exists(self.global_config.env['tmb_path']['local'])
        self.assertEqual(has_path, True)

    def test_has_transat_mb(self):
        has_path = os.path.exists(self.global_config.env['path']['ui'])
        self.assertEqual(has_path, True)

