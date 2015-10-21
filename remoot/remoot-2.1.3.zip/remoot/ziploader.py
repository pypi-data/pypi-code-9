# Copyright (C) 2014 Stefan C. Mueller

"""
Helper methods to create a zip file of packages and to add such a file to the
search path.
"""

import StringIO as stringio
import zipfile
import itertools
import pkgutil
import sys
import inspect
import logging

logger = logging.getLogger(__name__)


def make_package_zip(packages):
    """
    :param packages: List of packages to include in the zip file.
    
    :returns: ZIP-file content as a string.
    """
          
    def _add_package(zf, package):
        path = package.__path__
        prefix = package.__name__ + "."
        for _, modname, ispkg in itertools.chain([(None, package.__name__, True)], pkgutil.walk_packages(path, prefix)):
            if ispkg:
                sourcefile = modname.replace(".", '/') + "/__init__.py"
            else:
                sourcefile = modname.replace(".", '/') + ".py"
    
            try:
                __import__(modname)
            except ImportError as e:
                raise e
            module = sys.modules[modname]
            try:
                src = inspect.getsource(module)
            except IOError as e:
                raise IOError("Could not get source of module %s: %s" %(modname, e))
            logger.debug("Adding to zip: %r" % sourcefile)
            zf.writestr(sourcefile, src)

    s = stringio.StringIO()
    zf = zipfile.ZipFile(s, 'w', compression=zipfile.ZIP_DEFLATED)
    try:
        for package in set(packages):
            _add_package(zf, package)
    finally:
        zf.close()

    return  s.getvalue()


def register_zip(filepath):
    """
    Registers a zip file created with :func:`make_package_zip` such that the packages
    can be loaded.
    """
    sys.path.append(filepath)