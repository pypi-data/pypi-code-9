import pdb
# encoding: utf-8

import emzed

def average(*a):
    a = [ai for ai in a if ai is not None]
    if len(a) == 0:
        return None
    return float(sum(a)) / len(a)

t = emzed.utils.toTable("value1", (1, 2, 3), type_=float)
t.addColumn("value2", (1, 2, None),  type_=float)
t.addColumn("mean", t.apply(average, (t.value1, t.value2), keep_nones=True))
print t


