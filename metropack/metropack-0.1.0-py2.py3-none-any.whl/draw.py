from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt


def _unwrap_one_layer(r, L, n):
    """For a set of points in a 2 dimensional periodic system, extend the set of
    points to tile the points at a given period.

    Parameters
    ----------
    r: float array, shape (:, 2).
        Set of points.
    L: float array, shape (2,)
        System lengths.
    n: integer.
        Period to unwrap.

    Returns
    -------
    rcu: float array, shape (:, 2).
        The set of points. tiled at the periods at a distance `n` from the
        origin.
    """
    try:
        L[0]
    except (TypeError, IndexError):
        L = np.ones([r.shape[1]]) * L
    if n == 0:
        return list(r)
    rcu = []
    for x, y in r:
        for ix in range(-n, n + 1):
            for iy in range(-n, n + 1):
                if abs(ix) == n or abs(iy) == n:
                    rcu.append(np.array([x + ix * L[0], y + iy * L[1]]))
    return rcu


def _unwrap_to_layer(r, L, n=1):
    """For a set of points in a 2 dimensional periodic system, extend the set of
    points to tile the points up to to a given period.

    Parameters
    ----------
    r: float array, shape (:, 2).
        Set of points.
    L: float array, shape (2,)
        System lengths.
    n: integer.
        Period to unwrap up to.

    Returns
    -------
    rcu: float array, shape (:, 2).
        The set of points. tiled up to the periods at a distance `n` from the
        origin.
    """
    rcu = []
    for i_n in range(n + 1):
        rcu.extend(_unwrap_one_layer(r, L, i_n))
    return rcu


def draw_medium(r, R, L, n=1, ax=None):
    """Draw circles representing circles in a two-dimensional periodic system.
    Circles may be tiled up to a number of periods.

    Parameters
    ----------
    r: float array, shape (:, 2).
        Set of points.
    R: float
        Circle radius.
    L: float array, shape (2,)
        System lengths.
    n: integer.
        Period to unwrap up to.
    ax: matplotlib axes instance or None
        Axes to draw circles onto. If `None`, use default axes.

    Returns
    -------
    None
    """
    if ax is None:
        ax = plt.gca()
    for ru in _unwrap_to_layer(r, L, n):
        c = plt.Circle(ru, radius=R, alpha=0.2)
        ax.add_artist(c)
