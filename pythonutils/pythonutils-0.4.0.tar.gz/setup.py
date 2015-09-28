#!/usr/bin/env python
# setup.py
# Distutils setup for the pythonutils package.
# Uses some of the buildutils commands.

# Copyright Michael Foord 2005-07
# EMail: fuzzyman AT voidspace DOT org DOT uk

# Released subject to the BSD License
# Please see http://www.voidspace.org.uk/python/license.shtml

# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# For information about bugfixes, updates and support, please join the
# ConfigObj mailing list:
# http://lists.sourceforge.net/lists/listinfo/configobj-develop
# Comments, suggestions and bug reports welcome.

import sys
from distutils.core import setup
try:
    import buildutils
except ImportError:
    pass

from pythonutils import __version__ as VERSION
NAME = 'pythonutils'
DESCRIPTION = 'The Voidspace Pythonutils Collection'
URL = 'http://www.voidspace.org.uk/python/modules.shtml'
PACKAGE = True
LICENSE = 'BSD License'
PLATFORMS = ['Platform Independent']

if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

if PACKAGE:
    packages = [NAME]
    py_modules = None
else:
    py_modules = [NAME]
    packages = None

setup(name= NAME,
      version = VERSION,
      description = DESCRIPTION,
      license = LICENSE,
      platforms = PLATFORMS,
      author = 'Michael Foord',
      author_email = 'fuzzyman@voidspace.org.uk',
      url = URL,
      py_modules = py_modules,
      packages = [''],
      package_dir = {'':'pythonutils'},
      extra_path = 'pythonutils',
     )


"""
TODO
====

This is a **TODO** list for the ``setup.py`` file.

Get the pudge stuff working.

Add a download url.

Get the announce stuff working.

Also the setuptools egg stuff.

"""
