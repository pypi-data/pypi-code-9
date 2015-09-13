from mvpoly.rbf import *
from mvpoly.cube import *
from mvpoly.dict import *
import numpy as np
import unittest

RBF_CLASSES  = (RBFGaussian,
                RBFMultiQuadric,
                RBFInverseMultiQuadric,
                RBFThinPlateSpline)

POLY_CLASSES = (MVPolyCube, MVPolyDict)

class TestMVPolyRBF(unittest.TestCase):

    # Check that an RBF interpolates the nodes (1D)

    def check_interp_on_nodes_1d(self, rbf_class, poly_class):
        eps = 1e-10
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        rbf = rbf_class(x, f, poly_class=poly_class)
        fi = rbf(x)
        self.assertTrue(np.allclose(f, fi, atol=eps),
                        "%s: on-node 1D" % rbf.name)

    def test_rbf_interp_on_nodes_1d(self):
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                self.check_interp_on_nodes_1d(rbf_class, poly_class)

    # Check that an RBF interpolates the nodes (2D)

    def check_interp_on_nodes_2d(self, rbf_class, poly_class):
        eps = 1e-10
        x = np.random.rand(50, 1)*4 - 2
        y = np.random.rand(50, 1)*4 - 2
        f = x*np.exp(-x**2 - 1j*y**2)
        rbf = rbf_class(x, y, f, poly_class=poly_class)
        fi = rbf(x, y)
        fi.shape = x.shape
        self.assertTrue(np.allclose(f, fi, atol=eps),
                        "%s: on-node 2D" % rbf.name)

    def test_rbf_interp_on_nodes_2d(self):
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                self.check_interp_on_nodes_2d(rbf_class, poly_class)

    # Check that an RBF instance approximates a smooth function
    # away from the nodes.

    def check_interp_off_nodes_1d(self, rbf_class, poly_class, atol):
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        rbf = rbf_class(x, f, poly_class=poly_class)
        x_fine = np.linspace(0, 10, 100)
        f0 = rbf(x_fine)
        f1 = np.sin(x_fine)
        msg = "abs-diff: %f" % abs(f0 - f1).max()
        self.assertTrue(np.allclose(f0, f1, atol=atol),
                        "%s: off-nodes" % rbf.name)

    def test_rbf_interp_off_nodes_1d(self):
        tol = {
            RBFGaussian : 0.15,
            RBFMultiQuadric : 0.10,
            RBFInverseMultiQuadric : 0.15,
            RBFThinPlateSpline : 0.10,
        }
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                args = (rbf_class, poly_class, tol.get(rbf_class))
                self.check_interp_off_nodes_1d(*args)

    # Check that a vertical shift of interpolation points gives
    # rise to the same shift of the interpolation (or of the
    # approximant, when smooth != 0).

    def check_shift_invariance(self, rbf_class, poly_class, smooth):
        eps = 1e-10
        n = 10
        x = np.linspace(0, n-1, n)
        f = np.random.randn(len(x))
        rbf0 = rbf_class(x, f, smooth=smooth, poly_class=poly_class)
        rbf1 = rbf_class(x, f + 1, smooth=smooth, poly_class=poly_class)
        x_fine = np.linspace(0, n-1, 5*n)
        f0 = rbf0(x_fine) + 1
        f1 = rbf1(x_fine)
        self.assertTrue(np.allclose(f0, f1, atol=eps),
                        '%s shift invariance' % rbf0.name)

    def test_rbf_shift_invariance(self):
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                for smooth in [0, 1e-3, 1e-1]:
                    self.check_shift_invariance(rbf_class, poly_class, smooth)

    # Check that an affine transform of interpolation points
    # gives rise to the same for the interpolation (or of the
    # approximant, when smooth != 0).

    def check_affine_invariance(self, rbf_class, poly_class, smooth):
        eps = 1e-10
        n = 10
        x = np.linspace(0, n-1, n)
        f = np.random.randn(len(x))
        rbf0 = rbf_class(x, f, smooth=smooth, poly_class=poly_class)
        rbf1 = rbf_class(x, f + 3*x + 2, smooth=smooth, poly_class=poly_class)
        x_fine = np.linspace(0, n-1, 5*n)
        f0 = rbf0(x_fine) + 3*x_fine + 2
        f1 = rbf1(x_fine)
        self.assertTrue(np.allclose(f0, f1, atol=eps),
                        '%s: affine invariance' % rbf0.name)

    def test_rbf_affine_invariance(self):
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                for smooth in [0, 1e-3, 1e-1]:
                    self.check_affine_invariance(rbf_class, poly_class, smooth)

    # When using a small positive smoothing parameter on a coarsely
    # discretised step, we expect nodes away from the step to be
    # close (but not that close) to the data samples. (This test will
    # fail if the the `sign` in the smoothing setup is reversed)
    # FIXME - check with plots now smooth is not eig-scaled

    def check_positive_smoothing(self, rbf_class, poly_class):
        eps = 0.005
        n = 10
        x = np.linspace(0, n-1, n)
        f = np.array([-1 if k < n/2 else 1 for k in x], dtype=np.float)
        rbf = rbf_class(x, f, smooth=1e-3, poly_class=poly_class)
        offstep = list(range(0, n//2-1)) + list(range(n//2+1, n))
        x_offstep = x[offstep]
        f0 = rbf(x_offstep)
        f1 = f[offstep]
        msg = "abs-diff: %f" % abs(f0 - f1).max()
        self.assertTrue(np.allclose(f0, f1, atol=eps),
                        "%s: positive smoothing" % rbf.name)

    def test_rbf_positive_smoothing(self):
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                self.check_positive_smoothing(rbf_class, poly_class)

    # Check that an RBF instance can be constructed using
    # a None value of epsilon (and that results in epsilon
    # being chosen non-zero)

    def check_epsilon_auto(self, rbf_class):
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        rbf = rbf_class(x, f, epsilon=None)
        self.assertTrue(rbf.epsilon > 0,
                        '%s: non-positive epsilon' % rbf.name)

    def test_rbf_epsilon_auto(self):
        for rbf_class in RBF_CLASSES:
            self.check_epsilon_auto(rbf_class)

    # Check that an RBF instance with default epsilon is not
    # subject to overshoot

    def check_epsilon_stability(self, rbf_class, poly_class):
        np.random.seed(1234)
        x = np.linspace(0, 10, 50)
        f = x + 4.0 * np.random.randn(len(x))
        rbf = rbf_class(x, f)
        x0 = np.linspace(0, 10, 1000)
        f0 = rbf(x0)
        self.assertTrue(np.abs(f0-x0).max() / np.abs(f-x).max() < 1.1,
                        "%s: default epsilon stability" % rbf.name)

    def test_rbf_epsilon_stability(self):
        for rbf_class in RBF_CLASSES:
            for poly_class in POLY_CLASSES:
                self.check_epsilon_stability(rbf_class, poly_class)

    # check that an RBF instance with poly_order=None has a poly
    # method of None, an that the rbf method is identical to the
    # call method

    def check_poly_order_none(self, rbf_class):
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        rbf = rbf_class(x, f, poly_order=None)
        self.assertTrue(rbf.poly is None, 'poly method not none')
        self.assertTrue(rbf.rbf(np.array(5)) == rbf(5), 'rbf method != call')

    def test_rbf_poly_order_none(self):
        for rbf_class in RBF_CLASSES:
            self.check_poly_order_none(rbf_class)

    # check that an RBF instance with specified poly_order has a
    # poly method which is at most of that degree

    def check_poly_order_natural(self, rbf_class, n):
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        rbf = rbf_class(x, f, poly_order=n)
        self.assertTrue(rbf.poly is not None, 'poly method none')
        self.assertTrue(rbf.poly.degree <= n, 'poly degree wrong')

    def test_rbf_poly_order_natural(self):
        for rbf_class in RBF_CLASSES:
            for n in range(4):
                self.check_poly_order_natural(rbf_class, n)

    # check that attempting to create an RBF instance with a negative
    # specified poly_order raises a ValueError

    def test_rbf_poly_order_negative(self):
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        for rbf_class in RBF_CLASSES:
            with self.assertRaises(ValueError):
                rbf_class(x, f, poly_order=-1)
            for poly_class in POLY_CLASSES:
                with self.assertRaises(ValueError):
                    rbf_class(x, f, poly_order=-1, poly_class=poly_class)

    # check the dtype of the interpolant

    def check_poly_dtype_real(self, rbf_class):
        x = np.linspace(0, 10, 9)
        f = np.sin(x)
        rbf = rbf_class(x, f)
        fi = rbf(5.0)
        self.assertTrue(fi.dtype == np.float64, 'dtype %s' % fi)

    def check_poly_dtype_complex(self, rbf_class):
        x = np.linspace(0, 10, 9)
        f = np.sin(x) * 1j
        rbf = rbf_class(x, f)
        fi = rbf(5.0)
        self.assertTrue(fi.dtype == np.complex128, 'dtype %s' % fi)

    def test_rbf_dtype(self):
        for rbf_class in RBF_CLASSES:
            self.check_poly_dtype_real(rbf_class)
            self.check_poly_dtype_complex(rbf_class)
