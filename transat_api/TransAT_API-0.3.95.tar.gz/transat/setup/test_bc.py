import unittest
from transat.setup.cad import Pipe
from transat.setup.cad import BoundBox
from transat.setup.cad import Network
from transat.setup.cad import CAD
from transat.config import ascomp_setup as setup

global_config = setup.install()


class TestBC(unittest.TestCase):
    def setUp(self):
        pass
    def test_(self):
        "read and write bc stt are the same"
        pass

