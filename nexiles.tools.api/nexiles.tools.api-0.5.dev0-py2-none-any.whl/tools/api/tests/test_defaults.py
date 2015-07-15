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
import textwrap

# http://readthedocs.org/docs/nose/en/latest/testing_tools.html
#from nose import tools as nt

from nexiles.tools.api import defaults


class PathTestCase(unittest.TestCase):
    def test_get_config_path(self):
        """docstring for test_get_config_path"""
        p = defaults.get_default_config_path()
        assert p.endswith(".nxtools/default.ini")


class ConfigTestCase(unittest.TestCase):

    def get_one(self, path=None):
        return defaults.Configuration(path)

    def test_section(self):
        c = self.get_one()
        assert c.base_section == "nxtools"

    def test_get(self):
        c = self.get_one()
        c.from_string(textwrap.dedent("""
        [nxtools]
        foo = hello
        bar = world"""))

        assert c.get("foo") == "hello"

    def test_get_section(self):
        c = self.get_one()
        c.from_string(textwrap.dedent("""
        [zonk]
        foo = hello
        bar = world"""))

        assert c.get("foo", section="zonk") == "hello"

    def test_get_default(self):
        c = self.get_one()
        c.from_string(textwrap.dedent("""
        [nxtools]
        xfoo = true
        xbar = false"""))

        assert c.get("foo", "asdf") == "asdf"

    def test_bool(self):
        c = self.get_one()
        c.from_string(textwrap.dedent("""
        [nxtools]
        foo = true
        baz = yes
        baf = 1
        qux = no
        quot = 0
        bar = false"""))

        assert c.get_bool("foo") == True
        assert c.get_bool("baz") == True
        assert c.get_bool("baf") == True
        assert c.get_bool("bar") == False
        assert c.get_bool("qux") == False
        assert c.get_bool("quot") == False


class DefaultsTestCase(unittest.TestCase):
    TEST_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "test.ini")

    def get_one(self, path=None):
        return defaults.Defaults(self.TEST_CONFIG_FILE)

    def test_path_set(self):
        c = self.get_one()
        assert c.path == self.TEST_CONFIG_FILE

    def test_defaults(self):
        c = self.get_one()
        assert c.default_url == "http://www.example.com/Windchill"
        assert c.default_type == "epmdocument"
        assert c.verbose == True
        assert c.post_mortem == False
        assert c.logfile == "nxtools.log"

    def test_loglevel(self):
        import logging
        c = self.get_one()
        assert c.loglevel == logging.DEBUG


# vim: set ft=python ts=4 sw=4 expandtab :
