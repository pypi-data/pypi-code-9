
# Copyright 2012 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://launchpad.net/launcherposta

"""Configuration file for Apport."""

from apport.hookutils import attach_related_packages, attach_file_if_exists

from launcherposta import logger


def add_info(report):
    """Add info to the report."""
    # attach the log
    fname = logger.get_filename()
    attach_file_if_exists(report, fname, "LauncherPostaLog")

    # info about dependencies
    packages = ["python-gi", "python-xdg"]
    attach_related_packages(report, packages)
