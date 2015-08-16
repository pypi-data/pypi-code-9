"""
Pack n-dimensional spheres into finite spaces.
"""
from __future__ import print_function, division
import numpy as np
from scipy.spatial.distance import pdist
from spatious.geom import sphere_volume
from spatious.distance import pdist_sq_periodic
from metropack.metros import metro_rcp_factory

every = 5000


def n_to_pf(L, n, R):
    """Returns the packing fraction for a number of non-intersecting spheres.

    Parameters
    ----------
    L: float array, shape (d,)
        System lengths.
    n: integer
        Number of spheres.
    R: float
        Sphere radius.

    Returns
    -------
    pf: float
        Fraction of space occupied by the spheres.
    """
    dim = L.shape[0]
    return (n * sphere_volume(R=R, n=dim)) / np.product(L)


def pf_to_n(L, pf, R):
    """Returns the number of non-intersecting spheres required to achieve
    as close to a given packing fraction as possible, along with the actual
    achieved packing fraction. for a number of non-intersecting spheres.

    Parameters
    ----------
    L: float array, shape (d,)
        System lengths.
    pf: float
        Fraction of space to be occupied by the spheres.
    R: float
        Sphere radius.

    Returns
    -------
    n: integer
        Number of spheres required to achieve a packing fraction `pf_actual`
    pf_actual:
        Fraction of space occupied by `n` spheres.
        This is the closest possible fraction achievable to `pf`.
    """
    dim = L.shape[0]
    n = int(round(pf * np.product(L) / sphere_volume(R, dim)))
    pf_actual = n_to_pf(L, n, R)
    return n, pf_actual


def _pack_simple_periodic(R, L, n, rng):
    dim = L.shape[0]
    r = np.empty([n, dim])
    while True:
        for i_dim in range(dim):
            r[:, i_dim] = rng.uniform(-L[i_dim] / 2.0, L[i_dim] / 2.0,
                                      size=(n,))
        if not np.any(pdist_sq_periodic(r, L) < (2.0 * R) ** 2):
            return r, R


def _pack_simple(R, L, n, rng):
    dim = L.shape[0]
    r = np.empty([n, dim])
    while True:
        for i_dim in range(dim):
            r[:, i_dim] = rng.uniform(-L[i_dim] / 2.0 + R, L[i_dim] / 2.0 - R,
                                      size=(n,))
        if not np.any(pdist(r, metric='sqeuclidean') < (2.0 * R) ** 2):
            return r, R


def pack_simple(R, L, pf=None, n=None, rng=None, periodic=False):
    """Pack a number of non-intersecting spheres into a system.

    Can specify packing by number of spheres or packing fraction.

    This implementation uses a naive uniform distribution of spheres,
    and the Tabula Rasa rule (start from scratch if an intersection occurs).

    This is likely to be very slow for high packing fractions

    Parameters
    ----------
    R: float
        Sphere radius.
    L: float array, shape (d,)
        System lengths.
    pf: float or None
        Packing fraction
    n: integer or None
        Number of spheres.
    rng: RandomState or None
        Random number generator. If None, use inbuilt numpy state.
    periodic: bool
        Whether or not the system is periodic.

    Returns
    -------
    r: float array, shape (n, d)
        Coordinates of the centres of the spheres for a valid configuration.
    R_actual: float
        Actual sphere radius used in the packing.
        In this implementation this will always be equal to `R`;
        it is returned only to provide a uniform interface with the
        Metropolis-Hastings implementation.
    """
    if rng is None:
        rng = np.random
    if pf is not None:
        if pf == 0.0:
            return np.array([]), R
        # If packing fraction is specified, find required number of spheres
        # and the actual packing fraction this will produce
        n, pf_actual = pf_to_n(L, pf, R)
    elif n is not None:
        if n == 0:
            return np.array([]), R
    if periodic:
        return _pack_simple_periodic(R, L, n, rng)
    else:
        return _pack_simple(R, L, n, rng)


def pack(R, L, pf=None, n=None, rng=None, periodic=False,
         beta_max=1e4, dL_max=0.02, dr_max=0.02):
    """Pack a number of non-intersecting spheres into a periodic system.

    Can specify packing by number of spheres or packing fraction.

    This implementation uses the Metropolis-Hastings algorithm for an
    NPT system.

    Parameters
    ----------
    R: float
        Sphere radius.
    L: float array, shape (d,)
        System lengths.
    pf: float or None
        Packing fraction
    n: integer or None
        Number of spheres.
    rng: RandomState or None
        Random number generator. If None, use inbuilt numpy state.
    periodic: bool
        Whether or not the system is periodic.


    Metropolis-Hastings parameters
    ------------------------------
    Playing with these parameters may improve packing speed.

    beta_max: float, greater than zero.
        Inverse temperature which controls how little noiseis in the system.
    dL_max: float, 0 < dL_max < 1
        Maximum fraction by which to perturb the system size.
    dr_max: float, 0 < dr_max < 1
        Maximum system fraction by which to perturb sphere positions.

    Returns
    -------
    r: float array, shape (n, d)
        Coordinates of the centres of the spheres for a valid configuration.
    R_actual: float
        Actual sphere radius used in the packing.
    """
    if pf is not None:
        if pf == 0.0:
            return np.array([]), R
        # If packing fraction is specified, find required number of spheres
        # and the actual packing fraction this will produce
        n, pf_actual = pf_to_n(L, pf, R)
    elif n is not None:
        if n == 0:
            return np.array([]), R
        # If n is specified, find packing fraction
        pf_actual = n_to_pf(L, n, R)

    # Calculate an initial packing fraction and system size
    # Start at at most 0.5%; lower if the desired packing fraction is very low
    pf_initial = min(0.005, pf_actual / 2.0)
    # Find system size that will create this packing fraction
    dim = L.shape[0]
    increase_initial_ratio = (pf_actual / pf_initial) ** (1.0 / dim)
    L_0 = L * increase_initial_ratio

    # Pack naively into this system
    r_0, R = pack_simple(R, L_0, n=n, rng=rng, periodic=periodic)

    mg = metro_rcp_factory(periodic, r_0, L_0, R, dr_max, dL_max, rng=rng)

    print('Initial packing done, Initial packing: {:g}'.format(mg.pf))

    t = 0
    while mg.pf < pf_actual:
        t += 1
        beta = beta_max * mg.pf
        mg.iterate(beta)

        if not t % every:
            print('Packing: {:g}%'.format(100.0 * mg.pf))

    print('Final packing: {:g}%'.format(100.0 * mg.pf))

    return mg.r, mg.R
