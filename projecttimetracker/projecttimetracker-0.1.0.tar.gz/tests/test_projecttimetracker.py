#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project-time-tracker
----------------------------------

Tests for `projecttimetracker` module.
"""

import unittest
from click.testing import CliRunner

from projecttimetracker import projecttimetracker


class TestProjecttimetracker(unittest.TestCase):

    def setUp(self):
        pass

    def test_hw(self):
        runner = CliRunner()
        result = runner.invoke(projecttimetracker.cli)
        assert result.exit_code == 0
        assert result.output == 'hiya\n'

    def tearDown(self):
        pass
