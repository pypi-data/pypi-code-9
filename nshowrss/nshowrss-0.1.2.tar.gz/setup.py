#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'requests',
    'feedparser',
    'SimpleTorrentStreaming==0.1.3',
    'futures',
    'npyscreen',
    'pychapter==0.1.9',
    'tvdb_api',
    'imdbpie'
]

test_requirements = [
]

setup(
    name='nshowrss',
    version='0.1.2',
    description="Ncurses interface for downloading showrss.info series, and keeping track of the watched / not watched episodes",
    long_description=readme + '\n\n' + history,
    author="David Francos Cuartero",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/nshowrss',
    packages=[
        'nshowrss',
    ],
    package_dir={'nshowrss':
                 'nshowrss'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='nshowrss',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': ['nshowrss=nshowrss.nshowrss:main']
    },
    test_suite='tests',
    tests_require=test_requirements
)
