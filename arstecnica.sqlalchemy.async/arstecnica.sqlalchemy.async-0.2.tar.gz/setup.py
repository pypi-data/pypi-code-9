# -*- coding: utf-8 -*-
# :Progetto:  arstecnica.sqlalchemy.async
# :Creato:    ven 10 lug 2015 10:51:16 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import os
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name='arstecnica.sqlalchemy.async',
    version=VERSION,
    description="Asyncio middleware for SQLAlchemy",
    long_description=README + u'\n\n' + CHANGES,

    author="Alberto Berti",
    author_email="azazel@metapensiero.it",
    maintainer="Lele Gaifax",
    maintainer_email="lele@metapensiero.it",

    url='https://bitbucket.org/leleundfrank/arstecnica.sqlalchemy.async',

    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Database",
        ],
    keywords='asyncio sqlalchemy',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['SQLAlchemy'],
    tests_require=['pytest', 'pytest-asyncio'],
)
