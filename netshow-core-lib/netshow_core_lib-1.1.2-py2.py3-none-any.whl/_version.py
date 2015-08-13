# pylint: disable=E1102
""" Assumes package is installed before checking
the version this way
"""
import pkg_resources
import os
import sys

def get_version():
    """
    :return: hash of versions of various netshow components.
    """
    versions = {'netshow-core':
            pkg_resources.require('netshow-core-lib')[0].version}

    _dir_entries = os.listdir(sys.prefix + "/share/netshow-lib/providers/")
    for _entry in _dir_entries:
        provider_pkg = "netshow-%s" % (_entry)
        pkg_name = "netshow-%s-lib" % (_entry)
        versions[provider_pkg] = pkg_resources.require(pkg_name)[0].version
    return versions
