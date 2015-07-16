# -*- coding: utf-8 -*-

from collective.localheaderandfooter.testing import FUNCTIONAL_TESTING
from plone.testing import layered, z2

import doctest
from interlude import interact
import os
import pprint
import unittest

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
optionflags |= doctest.REPORT_ONLY_FIRST_FAILURE

dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith('test_') and f.endswith('.txt')]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(t, globs={'interact': interact,
                                               'pprint': pprint.pprint,
                                               'z2': z2,
                                               }, optionflags=optionflags),
                layer=FUNCTIONAL_TESTING)
        for t in tests
    ])
    return suite
