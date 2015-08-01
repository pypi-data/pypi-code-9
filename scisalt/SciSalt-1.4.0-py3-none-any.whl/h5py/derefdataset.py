import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import matplotlib.pyplot as _plt
    import scipy as _sp


def derefdataset(dataset, f):
    # Get the dataset shape, initialize output
    out = _np.empty(dataset.shape[0])

    # Iterate over references, save to out.
    for i, val in enumerate(dataset):
        out[i] = f[val[0]][0, 0]

    return out


def derefstr(dataset):
    intarr = _np.array(dataset)
    strarr = intarr.view('S2')
    strarr = strarr.flatten()
    strarr = ''.join(strarr)

    return strarr


def derefimgs(dataset, datasetbg, f):
    # Get the dataset shape, initialize output
    out = _np.empty([dataset.shape[0], 734, 1292])

    # Iterate over references, save to out.
    for i, val in enumerate(dataset):
        intarr = f[val[0]]
        intarr = _np.array(intarr)
        strarr = intarr.view('S2')
        strarr = strarr.flatten()
        strarr = ''.join(strarr)
        img = _plt.imread(strarr)

        val = datasetbg[i]
        intarr = f[val[0]]
        intarr = _np.array(intarr)
        strarr = intarr.view('S2')
        strarr = strarr.flatten()
        strarr = ''.join(strarr)

        img_bg = _sp.io.loadmat(strarr)
        img_bg = img_bg['img']

        out[i, :, :] = img - img_bg

    return out
