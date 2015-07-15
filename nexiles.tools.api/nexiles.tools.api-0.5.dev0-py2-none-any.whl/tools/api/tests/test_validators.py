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


import unittest
import argparse

# http://readthedocs.org/docs/nose/en/latest/testing_tools.html
from nose import tools as nt

from nexiles.tools.api.validators import is_oid
from nexiles.tools.api.validators import is_url
from nexiles.tools.api.validators import is_bool
from nexiles.tools.api.validators import is_resource
from nexiles.tools.api.validators import is_file_path


class TestOIDValidator(unittest.TestCase):

    def test_oid_valid(self):
        self.assertTrue(is_oid("OR:foo:1234"))
        self.assertTrue(is_oid("VR:foo:1234"))

    def test_oid_valid_pasted(self):
        self.assertTrue(is_oid("OR%3Awt.epm.EPMDocument%3A100431"))

    @nt.raises(argparse.ArgumentTypeError)
    def test_oid_invalid_empty(self):
        is_oid("")

    @nt.raises(argparse.ArgumentTypeError)
    def test_oid_invalid_invalid_prefix(self):
        is_oid("XX:abs:123")

    @nt.raises(argparse.ArgumentTypeError)
    def test_oid_invalid_somestring(self):
        is_oid("invalid")

    @nt.raises(argparse.ArgumentTypeError)
    def test_oid_invalid_no_sequence(self):
        is_oid("VR:foo:abc")


class TestFilePathValidator(unittest.TestCase):

    def test_file_path_valid(self):
        self.assertTrue(is_file_path("/etc/hosts"))
        self.assertTrue(is_file_path("~/.vimrc"))

    @nt.raises(argparse.ArgumentTypeError)
    def test_file_not_there(self):
        is_file_path("/nonexisting")

    @nt.raises(argparse.ArgumentTypeError)
    def test_file_special(self):
        is_file_path("/dev/zero")


class TestValidResValidator(unittest.TestCase):

    def test_valid_resource(self):
        v = is_resource("document", "part")
        self.assertTrue(v("document"))
        self.assertTrue(v("documents"))
        self.assertTrue(v("part"))
        self.assertTrue(v("parts"))

    def test_valid_resource_1(self):
        v = is_resource("all")
        self.assertTrue(v("document"))
        self.assertTrue(v("documents"))
        self.assertTrue(v("part"))
        self.assertTrue(v("parts"))

    @nt.raises(argparse.ArgumentTypeError)
    def test_invalid_resource(self):
        v = is_resource("document", "part")
        v("role")

    @nt.raises(argparse.ArgumentTypeError)
    def test_invalid_resource_1(self):
        v = is_resource("all")
        v("foobar")


class TestBoolValidator(unittest.TestCase):

    def test_truthy(self):
        for k in "yes Yes True true On 1".split():
            assert is_bool(k) == True, "%s is expecxted to be truthy" % k

    def test_falsy(self):
        for k in "False 0 Off off false".split():
            assert is_bool(k) == False, "%s is expecxted to be falsy" % k

    def test_falsy_nomatch(self):
        assert is_bool("") == False

# vim: set ft=python ts=4 sw=4 expandtab :
