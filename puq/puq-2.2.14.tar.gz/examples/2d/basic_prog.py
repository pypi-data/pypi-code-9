#!/usr/bin/env python

import optparse
from puqutil import dump_hdf5

usage = "usage: %prog --x x --y y"
parser = optparse.OptionParser(usage)
parser.add_option("--x", type=float)
parser.add_option("--y", type=float)
(options, args) = parser.parse_args()
x = options.x
y = options.y


z = x**2-3*y+2

dump_hdf5('z', z)
