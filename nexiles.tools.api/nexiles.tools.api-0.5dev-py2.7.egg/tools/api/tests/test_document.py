# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import os
import unittest

# http://readthedocs.org/docs/nose/en/latest/testing_tools.html
#from nose import tools as nt

from nexiles.tools.api import document


class ManifestTestCase(unittest.TestCase):
    TEST_MANIFEST_FILE = os.path.join(os.path.dirname(__file__), "document_manifest.json")

    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(self.TEST_MANIFEST_FILE))

    def tearDown(self):
        os.chdir(self.cwd)

    def get_one(self):
        return document.Manifest.from_file(self.TEST_MANIFEST_FILE % {"filename": self.TEST_MANIFEST_FILE})

    def test_mf_from_file(self):
        document.Manifest.from_file(self.TEST_MANIFEST_FILE)

    def test_content_info(self):
        mf = self.get_one()

        assert len(mf.content) == 2
        assert len(mf.content["PRIMARY"]) == 1
        assert len(mf.content["SECONDARY"]) == 2

        ci = mf.content
        assert ci["PRIMARY"][0]["filename"] == "test.ini"
        assert ci["SECONDARY"][0]["filename"] == "test.ini"
        assert ci["SECONDARY"][1]["filename"] == "test.ini"
        assert ci["SECONDARY"][1]["mimetype"] == "application/json"

    def test_required(self):
        mf = self.get_one()

        assert mf.number == "4711"
        assert mf.name == "document_name"
        assert mf.container == "TestProduct"

    def test_optionals(self):
        mf = self.get_one()

        assert mf.folder == "/Defaults/foo"
        assert mf.description == "A Test Document"

    def test_attributes(self):
        mf = self.get_one()
        assert isinstance(mf.attributes, dict)
        assert len(mf.attributes) == 2

    def test_validation_error(self):

        with self.assertRaises(AssertionError):
            mf = self.get_one()
            mf.name = None
            mf.validate()

        with self.assertRaises(AssertionError):
            mf = self.get_one()
            mf.number = None
            mf.validate()

        with self.assertRaises(AssertionError):
            mf = self.get_one()
            mf.container = None
            mf.validate()

# vim: set ft=python ts=4 sw=4 expandtab :
