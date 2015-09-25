# -*- coding: utf-8 -*-
# :Project:   arstecnica.raccoon.autobahn -- A set of common utilities over Autobahn
# :Created:   ven 25 set 2015, 11.20.05, CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

import os
from codecs import open

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

requires=[
    'autobahn',
    'nssjson',
    'setuptools',
    'six',
    'txaio',
]

setup(
    name="arstecnica.raccoon.autobahn",
    version=VERSION,
    url="https://gitlab.com/arstecnica/arstecnica.raccoon.autobahn",

    description="A set of common utilities over Autobahn",
    long_description=README + u'\n\n' + CHANGES,

    author="Lele Gaifax",
    author_email="lele@metapensiero.it",

    license="GPLv3+",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        ],
    keywords='',

    packages=['arstecnica.raccoon.autobahn'],
    package_dir={'': 'src'},
    namespace_packages=['arstecnica', 'arstecnica.raccoon'],

    install_requires=requires,
    extras_require={'dev': ['metapensiero.tool.bump_version']},
)
