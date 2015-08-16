# Copyright (C) 2011-2014 Jens Kasten. All Rights Reserved.
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 

"""
Package for RSBAC.

Copyright (C) Jens Kasten. All Rights Reserved.
"""

__author__  = "Jens Kasten <jens@kasten-edv.de>"
__status__  = "beta"
__date__    = "10 July 2014"

__all__ = ["which", "get_pid_from_name", "get_linux_dist_distrubution"
    "class_for_name"]


import os
import sys
from subprocess import Popen, PIPE
import platform
import importlib

import logging
logging.basicConfig(format='%(levelname)s:%(name)s:line %(lineno)s: %(message)s')
log = logging.getLogger(__name__)


RSBAC_PROC_INFO_DIR = "/proc/rsbac-info"

ADMIN_PATHS = ["/bin", "/usr/bin", "/sbin", "/usr/sbin", "/usr/local/bin",
    "/usr/local/sbin", "/usr/lib", "/usr/libexec"]

def which(file_name):
    """Python implementation of which. Filter out /usr/local/jails."""
    if os.path.isdir(file_name):
        return file_name
    for path in ADMIN_PATHS:
        service = os.path.join(path, file_name)
        if os.path.isfile(service):
            return service
    for path in os.environ["PATH"].split(":"):
        # exclude the /usr/local/jails path to avoid endless loop
        # this could be happend when the /usr/local/jails on first place
        # in the PATH environment
        if path == "/usr/local/jails":
            continue
        service = os.path.join(path, file_name)
        if os.path.isfile(service):
            return service
    log.info("Could not found %s." % file_name)
    return False

def get_version():
    """Return version number."""
    import rsbactools.__version__
    return __version__.__version__

def get_pid_from_name(prog_name):
    """Try to get the pid number from a give program name.
    If more then one pids are delivered its return the first one.
    On success return int otherwise None."""
    process = Popen([which("pgrep"), prog_name], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        log.info(error.decode())
        return False
    else:
        output = output.decode().split("\n")
        try:
            return int(output[0])
        except IndexError as error:
            log.info("Not found pid info for %s:" % prog_name)
            return False

def get_linux_distribution(full=False):
    """Return the name of linux distribution.
    If full not set return the name as lower string.
    Otherwise a tuple(name, version)."""
    try:
        result = platform.linux_distribution()
        if not full:
            return result[0].split(" ")[0].lower()
        else:
            return (result[0], result[1])
    except IndexError as error:
        log.info(error)


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c

