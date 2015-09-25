def calc_rmsd(x, y):
    delta = x - y
    N = len(delta)
    np.multiply(delta, delta, delta)
    return np.sqrt((delta.sum() / N))


def interface(rec, lig, interface_d):
    dists = cdist(rec._getCoords(), lig._getCoords(), 'sqeuclidean')
    indices = np.any(dists < (interface_d*interface_d), axis=0).nonzero()[0]
    return indices


def calc_rmsd(ag, ref, interface=None):
    if interface is not None:
        pass
