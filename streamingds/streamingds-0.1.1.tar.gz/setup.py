# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2012 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from __future__ import (absolute_import, division, print_function,
                        with_statement)

from imp import load_source
import os
import sys
import warnings

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    setuptools = None
    from distutils.core import setup
    from distutils.extension import Extension


PY2 = sys.version_info[0] == 2
PYPY = hasattr(sys, 'pypy_version_info')

cmdclass = {}
ext_modules = []

try:
    import cython
    from Cython.Distutils import build_ext as cmd_class
    cmdclass = {'build_ext': cmd_class}
    ext_modules = [
        Extension('streamingds.countminsketch',
                  sources=['streamingds/countminsketch.py'],
                  extra_compile_args=['-O3', '-Wall',
                                      '-Wno-strict-prototypes'],
                  libraries=['m']
                  )
    ]
    print('Using Cython to build the optimized version')
except ImportError:
    cython = None

if not cython and not PYPY:
    print('Trying to build the generated Cython files')
    # don't build the C extensions when running on pypy
    from distutils.command.build_ext import build_ext as c_b_ext
    from distutils.errors import CCompilerError
    from distutils.errors import DistutilsPlatformError, DistutilsExecError
    if sys.platform == 'win32' and sys.version_info > (2, 6):
        # 2.6's distutils.msvc9compiler can raise an IOError when failing to
        # find the compiler
        build_errors = (CCompilerError, DistutilsExecError,
                        DistutilsPlatformError, IOError)
    else:
        build_errors = (CCompilerError, DistutilsExecError,
                        DistutilsPlatformError)

    ext_modules = [
        Extension('streamingds.countminsketch',
                  sources=['streamingds/countminsketch.c'],
                  extra_compile_args=['-O3', '-Wall',
                                      '-Wno-strict-prototypes'],
                  libraries=['m']
                  )
    ]

    class cmd_class(c_b_ext):
        """Allow C extension building to fail.

        The Cython code speeds up the datastructures but are not necessary in
        order to use them.
        """

        warning_message = """
    ********************************************************************
    WARNING: %s could not
    be compiled. No C extensions are needed to use any datastructure but they
    improve their speed significantly.

    %s

    Here are some hints for popular operating systems:

    If you are seeing this message on Linux you probably need to
    install GCC and/or the Python development package for your
    version of Python.

    Debian and Ubuntu users should issue the following command:

        $ sudo apt-get install build-essential python-dev

    RedHat, CentOS, and Fedora users should issue the following command:

        $ sudo yum install gcc python-devel
    ********************************************************************
    """

        def run(self):
            try:
                c_b_ext.run(self)
            except DistutilsPlatformError:
                e = sys.exc_info()[1]
                sys.stdout.write('%s\n' % str(e))
                a = 'Extension modules'
                b = ' There was an issue with your platform configuration'
                c = ' - see above.'
                warnings.warn(self.warning_message % (a, b, c))

        def build_extension(self, ext):
            name = ext.name
            if sys.version_info[:3] >= (2, 4, 0):
                try:
                    c_b_ext.build_extension(self, ext)
                except build_errors:
                    e = sys.exc_info()[1]
                    sys.stdout.write('%s\n' % str(e))
                    a = 'The %s extension module' % name
                    b = ('The output above this warning shows how the ' +
                         'compilation failed')
                    warnings.warn(self.warning_message % (a, b))
            else:
                a = 'The %s extension module' % name
                b = ('Please use Python >= 2.4 to take advantage of the ' +
                     'extension')
                warnings.warn(self.warning_message % (a, b))

    cmdclass = {'build_ext': cmd_class}

init = load_source('init', os.path.join('streamingds', '__init__.py'))

tests_require = [
    'pytest',
    'pytest-cov',
]

if sys.version_info < (2, 7):
    tests_require.append('unittest2')

extras_require = {}
extras_require['test'] = tests_require
extras_require['redis'] = ['redis', 'hiredis']

setup(
    name='streamingds',
    version='.'.join([str(v) for v in init.__version__]),

    author='Daniel Truemper',
    author_email='truemped@gmail.com',

    description='',
    packages=['streamingds', 'streamingds.redis'],

    install_requires=[
        'bitstring',
        'pyhashxx',
        'cytoolz'
    ],

    tests_require=tests_require,
    extras_require=extras_require,

    cmdclass=cmdclass,
    ext_modules=ext_modules
)
