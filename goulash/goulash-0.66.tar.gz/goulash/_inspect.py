""" goulash._inspect
"""
import os
import inspect
from addict import Dict
from setuptools import find_packages


def _main_package(src_root):
    """ typically find_packages() returns something like
        ['foo','foo.bar','foo.baz'].  in that case, "foo"
        is the main pasckage.
    """
    packages = find_packages(where=src_root, exclude=('tests',))
    packages = set([p.split('.')[0] for p in packages])
    if len(packages) == 0 or 1 < len(packages):
        err = 'cannot guess pkg_root and it was not provided.  '
        err += 'setuptools.find_packages() returns "{0}", '
        err += 'working dir is "{1}"'
        err = err.format(packages, os.getcwd())
        raise RuntimeError(err)
    else:
        pkg_root = list(packages)[0]
        return pkg_root


def getcaller(level=2):
    """ """
    x = inspect.stack()[level]
    frame = x[0]
    file_name = x[1]
    flocals = frame.f_locals
    fglobals = frame.f_globals
    func_name = x[3]
    himself = flocals.get('self', None)
    try:
        kls = himself and himself.__class__
    except AttributeError:
        # python uses self only by convention, so it's
        # possible there is a "himself" local but it's
        # not actually an object.
        kls = None
    kls_func = getattr(kls, func_name, None)
    if type(kls_func) == property:
        func = kls_func
    else:
        try:
            func = himself and getattr(himself, func_name)
        except AttributeError:
            func = func_name + '[nested]'
    out = dict(file=file_name,
               self=himself,
               locals=flocals,
               globals=fglobals,
               func=func,
               func_name=func_name)
    out.update({'class': kls})
    return Dict(out)
get_caller = getcaller
