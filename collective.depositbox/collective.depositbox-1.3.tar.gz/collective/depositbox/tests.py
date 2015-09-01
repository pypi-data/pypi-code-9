from zope.component import testing
from zope.testing import doctestunit
import doctest
import unittest


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        doctestunit.DocFileSuite(
            'README.txt', package='collective.depositbox',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.ELLIPSIS),

        doctestunit.DocFileSuite(
            'usage.rst', package='collective.depositbox',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.ELLIPSIS),

        ])
