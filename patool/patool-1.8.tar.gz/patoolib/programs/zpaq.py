# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 Bastian Kleineidam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Archive commands for the zpaq program."""
import os

def extract_zpaq(archive, compression, cmd, verbosity, outdir):
    """Extract a ZPAQ archive."""
    cmdlist = [cmd, 'x', os.path.abspath(archive)]
    return (cmdlist, {'cwd': outdir})


def list_zpaq(archive, compression, cmd, verbosity):
    """List a ZPAQ archive."""
    return [cmd, 'l', archive]


def create_zpaq(archive, compression, cmd, verbosity, filenames):
    """Create a ZPAQ archive."""
    cmdlist = [cmd, 'c', archive]
    cmdlist.extend(filenames)
    return cmdlist


def test_zpaq(archive, compression, cmd, verbosity):
    """Test a ZPAQ archive."""
    return [cmd, 'l', archive]
