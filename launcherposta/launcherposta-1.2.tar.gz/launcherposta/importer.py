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

"""Nice importer utility."""

import  logging
import sys

IMPORT_MSG = """
ERROR trying to import {module!r}: {error}

Probably you need to install a dependency, the
package {package!r} version {pack_ver} or greater.
"""

logger = logging.getLogger('Importer')


def _get_version(module_path):
    """Get the version of a module."""
    mod = sys.modules[module_path]
    for attr in ('version', '__version__', 'ver', '_version'):
        v = getattr(mod, attr, None)
        if v is not None:
            return v
    return "<unknown>"


def check(module_path, package, pack_ver):
    try:
        __import__(module_path)
    except Exception, err:
        print IMPORT_MSG.format(module=module_path, package=package,
                                pack_ver=pack_ver, error=err)
        import pdb;pdb.set_trace()
        logger.error("Import error for module %r: %s", module_path, err)
    else:
        version = _get_version(module_path)
        msg = "Module %r imported ok, version %r" % (module_path, version)
        print msg
        logger.info(msg)
