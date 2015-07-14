#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Pythn3 ghubtrending
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read().replace('.. :changelog:', '')

setup(
    name='ghubtrending',
    version='0.0.4',
    description="""
        This bot monitors github trending repositories and twitts about them
    """,
    long_description=README + '\n\n' + HISTORY,
    author="David Francos",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/ghubtrending',
    packages=[
        'ghubtrending',
    ],
    package_dir={'ghubtrending':
                 'ghubtrending'},
    include_package_data=True,
    install_requires=[
        'birdy',
        'github3.py'
    ],
    license="BSD",
    zip_safe=False,
    keywords='ghubtrending',
    entry_points={
        'console_scripts': [
            'ghubtrending = ghubtrending.ghubtrending:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests'
)
