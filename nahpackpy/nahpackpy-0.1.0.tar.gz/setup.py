#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import imp
from setuptools import setup


rust_ext = imp.new_module('rust_ext')
with open('rust_ext.py', 'r') as fileh:
    rust_ext_contents = fileh.read()
exec(rust_ext_contents, rust_ext.__dict__)  # pylint: disable=W0122

from rust_ext import (
    Distribution,
    build_rust_cmdclass,
    install_lib_including_rust,
)


VERSION = '0.1.0'


INSTALL_REQUIRES = [
    'cffi>=1.1.0',
]


setup(
    name='nahpackpy',
    version=VERSION,
    author='ijl',
    author_email='ijl@mailbox.org',
    license='Mozilla Public License, Version 2.0',
    description='Python HPACK library using nahpack',
    url='https://github.com/ijl/nahpackpy',
    download_url=(
        'https://github.com/ijl/nahpackpy/archive/%s.tar.gz' % VERSION
    ),
    keywords='hpack http2 header compression encoding rfc 7541',
    packages=['nahpackpy', ],
    package_data={
        'nahpackpy': ['nahpack.h', ],  # for wheel, which ignores MANIFEST
    },
    install_requires=INSTALL_REQUIRES,
    cmdclass={
        'build_rust': build_rust_cmdclass('nahpackpy/nahpack/Cargo.toml'),
        'install_lib': install_lib_including_rust,
    },
    distclass=Distribution,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
