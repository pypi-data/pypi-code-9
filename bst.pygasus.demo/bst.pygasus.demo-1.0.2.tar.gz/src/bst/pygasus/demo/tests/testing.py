import doctest
import unittest
from bst.pygasus.demo.tests.browser import BrowserTest

optionflags = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS + doctest.IGNORE_EXCEPTION_DETAIL


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([BrowserTest('response_check')
    ])
    return suite