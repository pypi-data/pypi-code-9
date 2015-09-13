# coding: utf-8
"""Hybrid RBF-polynomial interpolation and approximation.
"""

# This code is a derived work from the file of the same name in
# the SciPy library, based closely on Matlab code by Alex Chirokov
# and
#
#   Copyright (c) 2006-2007, Robert Hetland <hetland@tamu.edu>
#   Copyright (c) 2007, John Travers <jtravs@gmail.com>
#
# with some additional alterations by Travis Oliphant.
#
# The modifications from the SciPy file are
#
#   Copyright (c) 2015, J.J. Green <j.j.green@gmx.co.uk>
#
# This code retains the licence as the original: the SciPy (BSD
# style) license: http://www.scipy.org/scipylib/license.html

import numpy as np
import warnings
import mvpoly.cube
import mvpoly.dict


class RBFBase(object):
    r"""Base class for radial basis functions

    A class for radial basis function approximation/interpolation of
    `n`-dimensional scattered data.

    Parameters
    ----------
    *args : arrays
        `x`, `y`, `z`, ..., `f`, where `x`, `y`, `z`, ... are the vectors
        of the coordinates of the nodes and `f` is the array of values at
        the nodes
    epsilon : float, optional
        Adjustable constant for Gaussian or multiquadrics functions ---
        if not specified then a value will be calculated which is
        approximately the average distance between adjacent nodes.
    smooth : float, optional
        Values greater than zero increase the smoothness of the
        approximation.  The default value of zero gives interpolation, i.e.,
        the function will always go through the nodal points.
    poly_order : non-negative integer or `None`, optional (default 1)
        The order of a (low-order) polynomial to be fitted and added to the
        input data; the default of 1 corresponds to a linear term, 0 to a
        constant, `None` for no polynomial part.
    poly_class : one of the :class:`MVPoly` polynomial classes, optional

    Notes
    -----
    The base class is not used directly, instead one uses a subclass for
    which a particular basis function is defined,

    Examples
    --------
    For a set of `n` points in 3-dimensional space with coordinates
    in the `n`-vectors `x`, `y` and `z`; and with `f` being a
    `n`-vector of the data from which to interpolate, the interpolant
    `rbf` is created with

    >>> from mvpoly.rbf import RBFGauss
    >>> x, y, z, f = np.random.rand(4, 50)
    >>> rbf = RBFGauss(x, y, z, f)
    >>> rbf.name
    Gaussian
    """

    def _norm(self, x1, x2):
        return np.sqrt(((x1 - x2)**2).sum(axis=0))

    def _call_norm(self, x1, x2):
        if len(x1.shape) == 1:
            x1 = x1[np.newaxis, :]
        if len(x2.shape) == 1:
            x2 = x2[np.newaxis, :]
        x1 = x1[..., :, np.newaxis]
        x2 = x2[..., np.newaxis, :]
        return self._norm(x1, x2)

    def _set_epsilon_default(self):
        # default epsilon is the "the average distance between adjacent nodes"
        ximax = np.amax(self.xi, axis=1)
        ximin = np.amin(self.xi, axis=1)
        a = np.prod(ximax - ximin) / self.N
        b = 1.0 / self.dim
        self.epsilon = np.power(a, b)

    def _rbf_matrix(self):
        R = self._call_norm(self.xi, self.xi)
        A = self.radial(R)
        if R.shape != A.shape:
            raise ValueError('radial function returns array of wrong shape')
        if self.smooth != 0.0:
            A += np.eye(self.N) * self.sign * self.smooth
        return A

    def _poly_matrix(self, xa):
        if self.poly_order is None:
            return None
        if not self.poly_basis:
            self.poly_basis = self.poly_class.monomials(self.dim,
                                                        self.poly_order,
                                                        dtype=np.float64)
        K = np.vstack(p(*xa) for p in self.poly_basis)
        return K

    def __init__(self, *args, **kwargs):
        # the data points and the value of the function to be interpolated;
        xa = [np.asarray(a, dtype=np.float64).flatten() for a in args[:-1]]
        self.xi = np.asarray(xa)
        self.fi = np.asarray(args[-1]).flatten()

        if not all([x.size == self.fi.size for x in self.xi]):
            raise ValueError('All arrays must be equal length')

        # the dimension of the interpolation space, and the number of
        # interpolation samples
        self.dim = self.xi.shape[0]
        self.N = self.xi.shape[-1]

        # the shape parameter for the RBF
        self.epsilon = kwargs.pop('epsilon', None)
        if self.epsilon is None:
            self._set_epsilon_default()

        # the smoothing parameter, if zero then the RBF will interpolate,
        # if non-zero then it will approximate.
        self.smooth = kwargs.pop('smooth', 0.0)

        # order of polynomial term ('None' for no polynomial term)
        self.poly_order = kwargs.pop('poly_order', 1)

        # polynomial class
        self.poly_class = kwargs.pop('poly_class', mvpoly.dict.MVPolyDict)

        # polynomial basis (could be user defined without much effort)
        self.poly_basis = None

        # the interpolation (without the polynomial term)
        A = self._rbf_matrix()
        K = self._poly_matrix(xa)

        if K is None:

            self.rbf_coefs = np.linalg.solve(A, self.fi)
            self.poly = None

        else:

            nk = K.shape[0]
            Z = np.zeros((nk, nk), dtype=np.float64)
            A = np.vstack((np.hstack((A, K.T)), np.hstack((K, Z))))
            f = np.hstack((self.fi, np.zeros((nk,), dtype=np.float64)))
            coefs = np.linalg.solve(A, f)

            # RBF coefficients
            self.rbf_coefs = coefs[:self.N]

            # the polynomial
            poly_coefs = coefs[self.N:]
            self.poly = sum(c * p for c, p in zip(poly_coefs, self.poly_basis))

    def rbf(self, *args):
        shp = args[0].shape
        if not all([arg.shape == shp for arg in args]):
            raise ValueError('Array lengths must be equal')
        x = np.asarray([a.flatten() for a in args], dtype=np.float64)
        r = self._call_norm(x, self.xi)
        return np.dot(self.radial(r), self.rbf_coefs).reshape(shp)

    def __call__(self, *args):
        """Evaluate the interpolant instance

        Parameters
        ----------
        *args : numbers or arrays
            The vectors components `x`, `y`, `z`, ... at which to evaluate
            the interpolant.  All must be the same shape.

        Returns
        -------
        array
            A NumPy array which is the same shape as (each of the) input
            arguments.

        Examples
        --------
        With the interpolant `rbf` as defined in the example above, one
        can evaluate the interpolant at arbitrary points `xi`, `yi`, `zi`
        (in this case on a uniform grid) with

        >>> L = np.linspace(0, 1, 20)
        >>> xi, yi, zi = np.meshgrid(L, L, L)
        >>> fi = rbf(xi, yi, zi)
        >>> fi.shape
        (20, 20, 20)
        """
        args = [np.asarray(x, dtype=np.float64) for x in args]
        if len(args) == 0:
            raise ValueError('Need at least one argument')
        if self.poly is None:
            return self.rbf(*args)
        else:
            return self.rbf(*args) + self.poly(*args)


class RBFGaussian(RBFBase):
    r"""An RBF subclass for the *Gaussian* function

    .. math::

        \phi(r) = \exp\left(-(r/\epsilon)^2\right)

    The parameters are as for the base class :class:`RBFBase`.
    """
    @property
    def name(self):
        """
        The name of the function
        """
        return 'Gaussian'

    @property
    def sign(self):
        return 1

    def radial(self, r):
        """
        The radial function itself
        """
        return np.exp(-(r / self.epsilon)**2)


class RBFMultiQuadric(RBFBase):
    r"""An RBF subclass for the *multiquadric* function

    .. math::

        \phi(r) = \sqrt{(r/\epsilon)^2 + 1}.

    The parameters are as for the base class :class:`RBFBase`.
    """

    @property
    def name(self):
        """
        The name of the function
        """
        return 'multiquadric'

    @property
    def sign(self):
        return -1

    def radial(self, r):
        """
        The radial function itself
        """
        return np.sqrt((r / self.epsilon)**2 + 1)


class RBFInverseMultiQuadric(RBFBase):
    r"""An RBF subclass for the *inverse multiquadric*

    .. math::

        \phi(r) = \frac{1}{\sqrt{(r/\epsilon)^2 + 1}}.

    The parameters are as for the base class :class:`RBFBase`.
    """
    @property
    def name(self):
        """
        The name of the function
        """
        return 'inverse multiquadric'

    @property
    def sign(self):
        return 1

    def radial(self, r):
        """
        The radial function itself
        """
        return 1.0 / np.sqrt((r / self.epsilon)**2 + 1)


class RBFThinPlateSpline(RBFBase):
    r"""An RBF subclass for the *thin-plate spline*

    .. math::

        \phi(r) = r^2 \log(r).

    The parameters are as for the base class :class:`RBFBase` excepting
    that the `epsilon` parameter is unused.
    """
    @property
    def name(self):
        """
        The name of the function
        """
        return 'thin-plate spline'

    @property
    def sign(self):
        return 1

    def radial(self, r):
        """
        The radial function itself
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = r**2 * np.log(r)
        result[r == 0] = 0
        return result
