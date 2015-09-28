#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python packaging."""
import os
import sys

from setuptools import setup


#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))
#: Boolean, ``True`` if environment is running Python version 2.
IS_PYTHON2 = sys.version_info[0] == 2


NAME = 'pygcat'
DESCRIPTION = 'Extract statistical information from PostgreSQL.'
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(here, 'VERSION')).read().strip()
AUTHOR = u'Rodolphe Quiédeville'
EMAIL = 'rodolphe@quiedeville.org'
LICENSE = 'BSD'
URL = 'https://pygcat.readthedocs.org/'
CLASSIFIERS = [
    'Programming Language :: Python :: 2.7',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: BSD License',
]
KEYWORDS = [
    'database',
    'postgresql',
    'statistics',
    'pg_stat_statement'
]

REQUIREMENTS = [
    'setuptools',
    'psycopg2']

ENTRY_POINTS = {}
CMDCLASS = {}
SETUP_REQUIREMENTS = [
    'setuptools'
]

TESTS_REQUIREMENTS = [
    'pytest', 'pytest-cov', 'flake8'
]


# Tox integration.
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    """Test command that runs tox."""
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox  # import here, cause outside the eggs aren't loaded.
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


CMDCLASS['test'] = Tox


if __name__ == '__main__':  # Do not run setup() when we import this module.
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=README,
        classifiers=CLASSIFIERS,
        keywords=' '.join(KEYWORDS),
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        packages=['pygcat'],
        license=LICENSE,
        include_package_data=True,
        zip_safe=False,
        install_requires=REQUIREMENTS,
        test_requires=REQUIREMENTS + TESTS_REQUIREMENTS,
        entry_points=ENTRY_POINTS,
        cmdclass=CMDCLASS,
        setup_requires=SETUP_REQUIREMENTS
    )
