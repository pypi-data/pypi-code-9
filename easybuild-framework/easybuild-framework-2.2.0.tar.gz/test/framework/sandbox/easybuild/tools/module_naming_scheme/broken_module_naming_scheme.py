##
# Copyright 2014 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
Implementation of a broken test module naming scheme.

@author: Kenneth Hoste (Ghent University)
"""

import os

from easybuild.tools.module_naming_scheme import ModuleNamingScheme


UNKNOWN_KEY = 'nosucheasyconfigparameteravailable'


class BrokenModuleNamingScheme(ModuleNamingScheme):
    """Class implementing a simple (but broken) module naming scheme for testing purposes."""

    REQUIRED_KEYS = [UNKNOWN_KEY]

    def det_full_module_name(self, ec):
        return ec[UNKNOWN_KEY]
