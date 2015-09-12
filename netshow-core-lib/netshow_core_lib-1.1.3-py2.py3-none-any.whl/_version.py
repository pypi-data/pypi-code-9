# pylint: disable=E1102
""" Assumes package is installed before checking
the version this way
"""
import pkg_resources
import glob
import os


def get_version():
    """
    :return: hash of versions of various netshow components.
    """
    versions = {'netshow-core':
                pkg_resources.require('netshow-core-lib')[0].version}

    install_location = pkg_resources.require('netshow-core-lib')[0].location
    _dir_entries = glob.glob(install_location +
                             "/../../../share/netshow-lib/providers/*")
    for _entry in _dir_entries:
        provider_pkg = "netshow-%s" % (os.path.basename(_entry))
        pkg_name = "netshow-%s-lib" % (os.path.basename(_entry))
        versions[provider_pkg] = pkg_resources.require(pkg_name)[0].version

    return versions
