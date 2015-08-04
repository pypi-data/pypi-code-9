#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

from simple_pypi_statistics import __version__ as VERSION


# A comment is a line starting with # or --
is_comment = re.compile('^\s*(#|--).*').match


def load_requirements(fname):
    with open(fname) as fo:
        return [line.strip() for line in fo
                if not is_comment(line) and line.strip()]

requirements = load_requirements('requirements.txt')

test_requirements = []

setup(
    name='simple_pypi_statistics',
    version=VERSION,
    description="API and commandline for fetching simple statistics from PyPi's API",
    long_description=readme + '\n\n' + history,
    author="Benjamin Bach",
    author_email='benjamin@overtag.dk',
    url='https://github.com/benjaoming/simple-pypi-statistics',
    packages=[
        'simple_pypi_statistics',
    ],
    package_dir={'simple_pypi_statistics':
                 'simple_pypi_statistics'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv2",
    zip_safe=False,
    keywords='simple_pypi_statistics',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'simple-pypi-statistics = simple_pypi_statistics.__main__:main'
        ]
    },
)
