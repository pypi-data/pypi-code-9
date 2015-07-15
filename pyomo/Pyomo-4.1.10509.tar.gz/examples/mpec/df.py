#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________
#
# df.py
# Problem adapted from
#
# Modeling and solution environments for MPEC: GAMS and MATLAB
# Steven P Dirkse and Michael C. Ferris
# in Reformulation: Nonsmooth, Piecewise Smooth, Semismooth and Smoothing Methods
# Applied Optimization Volume 22, 1999, pp. 127-147.
# Editors Masao Fukushima and Liqun Qi
#

# df.py
from pyomo.environ import *
from pyomo.mpec import *

M = ConcreteModel()
M.x = Var(bounds=(-1,2))
M.y = Var()

M.o  = Objective(expr=(M.x - 1 - M.y)**2)
M.c1 = Constraint(expr=M.x**2 <= 2)
M.c2 = Constraint(expr=(M.x - 1)**2 + (M.y - 1)**2 <= 3)
M.c3 = Complementarity(expr=complements(M.y - M.x**2 + 1 >= 0, M.y >= 0))

model = M
