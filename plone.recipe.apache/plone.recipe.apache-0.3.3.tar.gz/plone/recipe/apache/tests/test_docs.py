# -*- coding: utf-8 -*-
"""
Doctest runner for 'plone.recipe.apache'.
"""
__docformat__ = 'restructuredtext'

import os
import unittest
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import doctest, renormalizing

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)
current_dir = os.path.dirname(__file__)



def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('plone.recipe.apache', test)
    zc.buildout.testing.install_develop('zc.recipe.cmmi', test)


    # Install any other recipes that should be available in the tests
    #zc.buildout.testing.install('collective.recipe.foobar', test)

def test_suite():

    globs = globals()
    globs['test_dir'] = current_dir
    globs['bin_dir'] = '%s/bin' % current_dir

    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                '../building.txt',
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                globs = globs,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                ),
            doctest.DocFileSuite(
                '../configuring.txt',
                setUp=setUp,
                globs = globs,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                ),
            doctest.DocFileSuite(
                '../doctests/technical_build.txt',
                setUp=setUp,
                globs = globs,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                ),

            doctest.DocFileSuite(
                '../doctests/technical_config.txt',
                setUp=setUp,
                globs = globs,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                ),

            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
