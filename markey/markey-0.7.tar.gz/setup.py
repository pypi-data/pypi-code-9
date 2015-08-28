#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


version = '0.7'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


test_requires = [
    'coverage',
    'pytest',
    'pytest-cov>=1.4',
    'pytest-flakes',
    'pytest-pep8',
    'python-coveralls',
]


install_requires = []


dev_requires = [
    'flake8>=2.0',
    'invoke',
    'twine'
]


setup(
    name='markey',
    description='Markup parser',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    version=version,
    license='BSD',
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='http://github.com/EnTeQuAk/markey/',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    tests_require=test_requires,
    install_requires=install_requires,
    extras_require={
        'docs': ['sphinx'],
        'tox': ['tox'],
        'tests': test_requires,
        'dev': dev_requires,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
