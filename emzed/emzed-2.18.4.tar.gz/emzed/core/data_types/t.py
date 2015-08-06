# encoding: utf-8
from __future__ import print_function

import emzed

t = emzed.utils.isotopeDistributionTable("C23", R=1e5, minp=0.000001)
t.setColFormat("abundance", "%.6f")
print(t)
