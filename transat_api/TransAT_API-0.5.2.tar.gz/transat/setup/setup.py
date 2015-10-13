from transat.setup.bc import BoundaryConditions
from transat.setup.ic import InitialConditions
from transat.setup.input import Input
from transat.setup.ist import ImmersedSurfaces
from transat.setup.mesh import Mesher
import transat.setup.stt_helper_functions as stt
import os
import sys

from transat.setup.cad import CAD
import glob
import os

"""

"""


class Setup(object):
    def __init__(self, path):
        """Summary line.
        """
        self.input = Input(path)
        self.stt_file = self._get_stt_file(path)
        ini_file = self._get_ini_file(path)

        if self.stt_file is not None:
            self.parse_stt()


    @staticmethod
    def _get_stt_file(path):
        try:
            stt_list =  glob.glob(os.path.join(path, '*.stt'))
            if len(stt_list)>1:
                print "too many stt files"
                print stt_list
                sys.exit()
            return stt_list[0]
        except:
            print "Error: no stt file found"
            sys.exit()

    @staticmethod
    def _get_ini_file(path):
        try:
            return glob.glob(os.path.join(path, 'initialconditions.cxx'))[0]
        except:
            return None

    def parse_stt(self):
        raw = stt.parser(self.stt_file)
        self.ist = ImmersedSurfaces(raw)
        self.mesher = Mesher(raw)
        self.bcs = BoundaryConditions(raw, self.mesher)
        self.raw = raw


    def write(self):
        self.ist.write(self.stt_file)
        self.mesher.write(self.stt_file)
        self.bcs.write(self.stt_file)
        self.input.write()

