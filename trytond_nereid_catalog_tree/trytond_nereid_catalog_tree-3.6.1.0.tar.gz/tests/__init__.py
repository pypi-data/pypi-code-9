# -*- coding: utf-8 -*-
import unittest
import trytond.tests.test_tryton

from .test_tree import TestTree
from .test_view_depends import TestViewsDepends


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestViewsDepends),
        unittest.TestLoader().loadTestsFromTestCase(TestTree),
    ])

    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
