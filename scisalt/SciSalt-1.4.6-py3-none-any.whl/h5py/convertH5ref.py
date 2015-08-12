import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np


def convertH5ref(dataset, f):
    vals = _np.array([])
    for ref in dataset[:, 0]:
        vals = _np.append(vals, f[ref])

    return vals
