###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Tests
$Id: tests.py 3934 2014-03-17 07:38:52Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import re
import doctest
import unittest
from zope.testing import renormalizing


checker = renormalizing.RENormalizing([
    (re.compile('\r\n'), '\n'),
    ])


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('checker.txt'),
        doctest.DocFileSuite('../README.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker
            ),
        doctest.DocFileSuite('zcml.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker
            ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
