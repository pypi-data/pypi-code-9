#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from fftresize import fftresize


_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: ISC License (ISCL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Graphics',
]

with open('README.rst', 'r') as rst_file:
    _long_description = rst_file.read()

_setup_args = {
    'author':           fftresize.__author__,
    'author_email':     fftresize.__email__,
    'classifiers':      _classifiers,
    'description':      fftresize.__doc__,
    'license':          fftresize.__license__,
    'long_description': _long_description,
    'name':             'FFTresize',
    'url':              'https://bitbucket.org/eliteraspberries/fftresize',
    'version':          fftresize.__version__,
}

_requirements = [
    'Avena >= 0.6',
    'docopt',
]

_setup_args['install_requires'] = _requirements


if __name__ == '__main__':

    setup(packages=['fftresize'], scripts=['scripts/fftresize'],
          **_setup_args)
