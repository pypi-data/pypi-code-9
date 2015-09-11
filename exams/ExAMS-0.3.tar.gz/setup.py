""" Setup script. Used by easy_install and pip. """

from distutils.core import setup
from setuptools import find_packages

import os
import sys
import textwrap
import re

VERSIONFILE="ExAMS/exams/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RunTimeError("Unable to find version string in {}.".format(VERSIONFILE))

'''Some functions for showing errors and warnings.'''
def _print_admonition(kind, head, body):
    tw = textwrap.TextWrapper(
        initial_indent='   ', subsequent_indent='   ')

    print ".. %s:: %s" % (kind.upper(), head)
    for line in tw.wrap(body):
        print line

def exit_with_error(head, body=''):
    _print_admonition('error', head, body)
    sys.exit(1)

def print_warning(head, body=''):
    _print_admonition('warning', head, body)

print "Checking python version!"
if not (sys.version_info[0] >= 2 and sys.version_info[1] >= 4):
    exit_with_error("You need Python 2.4 or greater to install ExAMS!")
print "Python version checked."

''' Check for required Python packages. '''
def check_import(pkgname, pkgver):
    try:
        mod = __import__(pkgname)
    except ImportError:
        exit_with_error(
            "Can't find a local %s Python installation." % pkgname,
            "Please read carefully the ``README`` file "
            "and remember that ExAMS needs the %s package "
            "to compile and run." % pkgname )
    else:
        if mod.__version__ < pkgver:
            exit_with_error(
                "You need %(pkgname)s %(pkgver)s or greater to run ExAMS!"
                % {'pkgname': pkgname, 'pkgver': pkgver} )

    print ( "* Found %(pkgname)s %(pkgver)s package installed."
            % {'pkgname': pkgname, 'pkgver': mod.__version__} )
    globals()[pkgname] = mod

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup_args = {
      'name'             :      'ExAMS',
      'version'          :      verstr,
      'author'           :      'Dr. Ardita Shkurti',
      'author_email'     :      'ardita.shkurti@gmail.com',
      'download_url'     :      'https://bitbucket.org/ExAMS/exams/get/exams-0.2.tar.gz',
      'license'          :      'BSD license or similar.',
      'classifiers'      : [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Environment :: Console',
      'License :: OSI Approved :: Python Software Foundation License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.5',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Topic :: Utilities',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: POSIX',
      'Operating System :: Unix'
    ],
      'description'      :      'Package to implement analysis on data from multiple replicas of molecular simulation, producing visual outputs.',
      'long_description' :      'Package to implement analysis on data from multiple replicas of molecular simulation, producing visual outputs.',
      'namespace_packages' :    ['exams'],
      'packages'         : find_packages('ExAMS'),
      'package_dir'      : {'' : 'ExAMS'},
      'scripts'          : ['ExAMS/ExAMS'],
      'install_requires' : ['numpy',
    		          'MDAnalysis'],
      'zip_safe'         : False,
}

setup (**setup_args)
