# encoding: utf-8
# Created by Jeremy Bowman at Thu Feb  6 17:41:45 2014
# Copyright (c) 2014 Safari Books Online, LLC. All rights reserved.

from __future__ import unicode_literals

import os
from shutil import rmtree
from subprocess import PIPE, Popen, STDOUT
from unittest import TestCase

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..', '..', 'docs'))
OUTPUT_DIR = os.path.join(DOCS_DIR, '_test')


class TestOutput(TestCase):
    """
    Tests of generating the documentation for sbo-sphinx itself.
    """

    def setUp(self):
        """Remove any output from a previous test run with errors"""
        self._clean()

    def tearDown(self):
        """Remove any generated output"""
        self._clean()

    def test_html(self):
        """The HTML output should build correctly"""
        process = Popen(['sphinx-build', '-b', 'html', '.', '_test'],
                        cwd=DOCS_DIR,
                        stderr=STDOUT,
                        stdout=PIPE,
                        universal_newlines=True)
        output, _ = process.communicate()
        self._verify_intermediate_files(output)
        expected = [
            os.path.join('_static', 'favicon.ico'),
            os.path.join('_static', 'safari_logo.png'),
            'genindex.html',
            'index.html',
            'objects.inv',
            'readme.html',
            'readthedocs.html',
            'search.html',
            'searchindex.js',
        ]
        for path in expected:
            assert os.path.exists(os.path.join(OUTPUT_DIR, path)), output

    def _clean(self):
        """Remove any generated output and intermediate files"""
        rmtree(OUTPUT_DIR, ignore_errors=True)
        rmtree(os.path.join(DOCS_DIR, 'javascript'), ignore_errors=True)
        rmtree(os.path.join(DOCS_DIR, 'python'), ignore_errors=True)

    def _verify_intermediate_files(self, output):
        """Make sure that the expected javascript/*.rst and python/*.rst files
        are generated"""
        # Intermediate files
        expected = [
            os.path.join('javascript', 'files.rst'),
            os.path.join('javascript', 'index.rst'),
            os.path.join('python', 'modules.rst'),
            os.path.join('python', 'sbo_sphinx.rst'),
        ]
        for path in expected:
            assert os.path.exists(os.path.join(DOCS_DIR, path)), output
