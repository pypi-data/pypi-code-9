#-------------------------------------------------------------------------------
# unreferenced_finder.py
#
#
# Copyright (C) 2015, Ryosuke Fukatani
# License: Apache 2.0
#-------------------------------------------------------------------------------

import sys
import os
import copy
import collections

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )

import pyverilog.utils.version
from pyverilog.utils.util import *
from pyverilog.dataflow.dataflow import *
from pyverilog_toolbox.verify_tool.dataflow_facade import *
from pyverilog_toolbox.verify_tool.bindlibrary import *
from sympy import *

import pyverilog.controlflow.splitter as splitter


class UnreferencedFinder(dataflow_facade):

    def search_unreferenced(self):
        """[FUNCTIONS]
        search input/reg/wire which not referenced any other output/reg/wire.
        """
        for tv,tk,bvi,bit,term_lsb in self.binds.walk_reg_each_bit():
            target_tree = self.makeTree(tk)
            print(tk)

if __name__ == '__main__':
    u_finder = UnreferencedFinder("../testcode/wired_or.v")
    u_finder.search_unreferenced()
