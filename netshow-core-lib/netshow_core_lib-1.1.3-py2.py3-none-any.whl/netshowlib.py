# pylint: disable=E1102
"""
This module does OS discovery , and Interface discovery

"""

import os
import glob
import operator
import pkg_resources


def import_module(mod_str):
    """
    inspired by post on stackoverflow
    :param name: import path string like 'netshowlib.linux.provider_discovery'
    :return: module matching the import statement

    """

    _module = __import__(mod_str)
    _mod_parts = mod_str.split('.')
    for _mod_part in _mod_parts[1:]:
        _module = getattr(_module, _mod_part)
    return _module


def provider_check():
    """
    | **Provider discovery check**
    looks into ``netshowlib/provider_discovery`` path for any \
    provider discovery files, and runs \
    the ``name_and_priority()`` function. If this function returns a hash with an \
    operating system name and priority, then this is put in a dict. \
    The OS with the max priority is chosen as the desired OS to use and the OS name \
    is returned

    :return: OS name of best match.
    """

    # get a list of files under the provider_discovery path
    # use pkg_resources to figure it out
    install_location = pkg_resources.require('netshow-core-lib')[0].location
    _dir_entries = glob.glob(install_location + "/../../../share/netshow-lib/providers/*")
    _providernames = {}
    # run os discovery check returns hash entries that look like this
    # { 'linux': 0 }. the integer is a priority . The lower the priority
    # the less likely the os is a match
    for _entry in _dir_entries:
        import_str = \
            "netshowlib.%s.provider_discovery" % \
            os.path.basename(_entry)
        providername = import_module(import_str)
        result = providername.name_and_priority()
        if result:
            _providernames.update(result)

    if _providernames:
        return max(_providernames.items(), key=operator.itemgetter(1))[0].lower()
    # if no OS found, return none
    return None


def feature_cache():
    """
    Performs OS discovery and returns the OS appropriate Cache() module
    """
    providername = provider_check()
    if providername:
        cache_path = "netshowlib.%s.cache" % providername
        cache_module = import_module(cache_path)
        return cache_module.Cache()
    return None


def iface(name, providername=None, cache=None):
    """
    | **Interface Discovery **
    calls into ``netshowlib.[provider].iface.iface()`` to get the correct
    interface type

    :return:  Iface object that best matches interface characteristics
    """
    _providername = providername
    if not _providername:
        _providername = provider_check()

    import_str = 'netshowlib.%s.iface' % _providername
    return import_module(import_str).iface(name, cache=cache)


def system_summary(providername=None):
    """
    returns SystemSummary class from mentioned provider
    """
    _providername = providername
    if not _providername:
        _providername = provider_check()

    import_str = 'netshowlib.%s.system_summary' % _providername
    return import_module(import_str).SystemSummary()


def portname_list(providername=None):
    """
    Return list of ports found by the provider
    """
    _providername = providername
    if not _providername:
        _providername = provider_check()

    import_str = 'netshowlib.%s.iface' % _providername
    return import_module(import_str).portname_list()
