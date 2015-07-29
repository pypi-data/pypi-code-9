import unittest
from transat.setup.input import Input
import shutil


class TestSetup(unittest.TestCase):
    def setUp(self):
        src = 'transat/templates/three_pipes_olga/transat_mb.inp'
        dst = 'tmp/transat_mb.inp'
        shutil.copyfile(src, dst)
        self.input = Input('tmp')

    def test_get_phase_names(self):
        names = ['Phase 1', 'Phase 2']
        _names = self.input.sections['&PHASES'].get_phase_names()
        self.assertEqual(_names, names)

    def test_get_phase_with_name(self):
        phase = self.input.sections['&PHASES'].get_phase('Phase 1')
        self.assertEqual(phase.get_name(), 'Phase 1')

    def test_set_phase_name(self):
        phase = self.input.sections['&PHASES'].get_phase('Phase 1')
        phase.set_name("asasdd")
        self.input.write()

    def test_set_visc(self):
        phase = self.input.sections['&PHASES'].get_phase('Phase 1')
        phase.set_viscosity(123)
        self.input.write()


if __name__ == '__main__':
    unittest.main()
