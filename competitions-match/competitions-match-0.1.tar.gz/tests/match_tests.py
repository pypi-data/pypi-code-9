# -*- coding: utf-8  -*-
"""Tests for match class registration and use."""

# Copyright (C) 2015 Alexander Jones
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from . import TestCase, TestMatch

from competitions.match import config
from competitions.match.default.SimpleMatch import SimpleMatch


class TestMatchRegistration(TestCase):

    """Tests for match class finding."""

    def test_basic(self):
        """Test default and explicit match classes."""
        self.assertEqual(config.base_match, SimpleMatch)
        config.base_match = 'competitions.test'
        self.assertEqual(config.base_match, TestMatch)
