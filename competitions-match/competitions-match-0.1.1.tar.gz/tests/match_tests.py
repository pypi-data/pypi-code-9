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

from competitions.match import MatchConfig, config
from competitions.match.default.SimpleMatch import SimpleMatch


class TestMatchRegistration(TestCase):

    """Tests for match class finding."""

    def test_basic(self):
        """Test default and explicit match classes."""
        self.assertEqual(config.base_match, SimpleMatch)
        config.base_match = 'competitions.test'
        self.assertEqual(config.base_match, TestMatch)
        config.base_match = 'competitions.unused'
        self.assertIsNone(config.base_match)
    
    def test_singleton(self):
        """Test to ensure the configuration object's singleton status."""
        self.assertRaises(RuntimeError, MatchConfig)


class TestSimpleMatch(TestCase):

    """Basic sanity checks for SimpleMatch."""

    def test_simulation(self):
        """Test SimpleMatch construction and simulation."""
        config.base_match = 'competitions.simple'
        team1 = 'Team 1'
        team2 = 'Team 2'
        for __ in range(1000):
            match = config.base_match(team1, team2)
            self.assertIsInstance(match, SimpleMatch, 'Wrong class.')
            self.assertEqual(match.team1, team1)
            self.assertEqual(match.team2, team2)
            match.play()
            if match.score1 > match.score2:
                self.assertEqual(match.winner, team1)
            elif match.score2 > match.score1:
                self.assertEqual(match.winner, team2)
            else:
                self.assertIsNone(match.winner)
            shortstr = '{}-{}'.format(match.score1, match.score2)
            self.assertEqual(match.shortstr(), shortstr)
            longstr = '{} {} - {} {}'.format(team1, match.score1, match.score2,
                                             team2)
            self.assertEqual(str(match), longstr)
