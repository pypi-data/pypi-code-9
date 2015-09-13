import numpy as np
import scipy as sp
import mvpoly.util.common
import unittest

class TestMPUtilCommonBinom(unittest.TestCase) :

    def test_binom_reference(self) :
        for n, i in [ (3,2), (5,0), (7, 6) ] :
            a = mvpoly.util.common.binom(n, i)
            b = int(round(sp.special.binom(n, i)))
            self.assertTrue(a == b, "binomial against reference")

class TestMPUtilCommonKronn(unittest.TestCase):

    def test_kronn_simple(self) :
        a = np.array([1, -1])
        b = np.array([1, 1])
        expected = np.array([1, 1, 1, 1, -1, -1, -1, -1])
        obtained = mvpoly.util.common.kronn(a, b, b)
        self.assertTrue((expected == obtained).all(),
                        "bad kronn:\n%s" % repr(obtained))

    def test_kronn_1_arg(self) :
        a = np.array([2, 3])
        self.assertRaises(TypeError, mvpoly.util.common.kronn, a)

    def test_kronn_2_arg(self) :
        a = np.array([2, 3])
        b = np.array([4, 1])
        expected = np.kron(a, b)
        obtained = mvpoly.util.common.kronn(a, b)
        self.assertTrue((expected == obtained).all(),
                        "bad kronn:\n%s" % repr(obtained))

    def test_kronn_dtype(self) :
        for dt in (int, float) :
            a = np.array([[2, 3], [4, 5]], dtype=dt)
            expected = dt
            obtained = mvpoly.util.common.kronn(a, a, a).dtype
            self.assertTrue(expected == obtained,
                            "bad kronn dtype:\n%s" % repr(obtained))


class TestMPUtilCommonMonimialIndices(unittest.TestCase):

    def test_monomial_indices_count(self) :
        data = {
            (1, 0) : 1,
            (1, 1) : 2,
            (1, 2) : 3,
            (3, 0) : 1,
            (3, 1) : 4,
            (3, 2) : 10,
            (3, 3) : 20,
            (3, 4) : 35,
            (4, 0) : 1,
            (4, 1) : 5,
            (4, 2) : 15,
            (4, 3) : 35,
            (4, 4) : 70,
        }
        for arg, expected in data.items():
            obtained = len(list(mvpoly.util.common.monomial_indices(*arg)))
            msg = "bad (%i, %i) monomial count:\n%i" % (arg[0], arg[1], obtained)
            self.assertTrue(expected == obtained, msg)

    def test_monomial_indices_explicit(self) :
        data = {
            (1, 0) : [(0,)],
            (1, 1) : [(0,), (1,)],
            (1, 2) : [(0,), (1,), (2,)],
            (2, 0) : [(0, 0)],
            (2, 1) : [(0, 0), (1, 0), (0, 1)],
            (2, 2) : [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)],
        }
        for arg, expected in data.items():
            obtained = list(mvpoly.util.common.monomial_indices(*arg))
            msg = "%s != %s" % (repr(expected), repr(obtained))
            self.assertTrue(expected == obtained, msg)

    def test_monomial_bad_num_vars(self) :
        for n in (-2, -1, 0):
            with self.assertRaises(ValueError):
                list(mvpoly.util.common.monomial_indices(n, 2))

    def test_monomial_bad_max_order(self) :
        for k in (-3, -2, -1):
            with self.assertRaises(ValueError):
                list(mvpoly.util.common.monomial_indices(2, k))


if __name__ == '__main__':
    unittest.main()
