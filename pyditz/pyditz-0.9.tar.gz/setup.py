# Setup script for PyDitz.

import os

# Bootstrap setuptools.
from conf.ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

# Set up entry points.
entry_points = """
[console_scripts]
%s = ditz.console:main
""" % os.environ.get("DITZCMD", "pyditz")

# Do the setup.
from conf.tools import read_pkginfo
info = read_pkginfo("ditz")

setup(name             = info.__title__,
      version          = info.__version__, 
      author           = info.__author__,
      author_email     = info.__email__,
      description      = info.__desc__,
      long_description = "\n" + open("README").read(),
      license          = info.__license__,
      url              = info.__url__,
      classifiers      = info.__classifiers__.strip().split("\n"),

      packages = ["ditz"],
      include_package_data = True,
      entry_points = entry_points,

      setup_requires = [
          'hgtools',
          'flake8',
      ],

      install_requires = [
          'pyyaml >= 3.10',
          'jinja2 >= 2.7',
          'voluptuous >= 0.8',
          'six >= 1.8.0',
      ],

      tests_require = [
          'nose >= 1.3.0',
          'mock >= 1.0.1',
          'coverage >= 3.6',
      ],

      test_suite = 'nose.collector')

# flake8: noqa
