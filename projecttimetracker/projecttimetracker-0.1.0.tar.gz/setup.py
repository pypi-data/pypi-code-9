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

version = '0.1.0'

requirements = [
    # TODO: put package requirements here
    'Click'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='projecttimetracker',
    version=version,
    description="CLI for easily tracking how much time you spend on each project",
    long_description=readme + '\n\n' + history,
    author="Andy Ruestow",
    author_email='andrew.ruestow@gmail.com',
    url='https://github.com/reustonium/projecttimetracker',
    packages=[
        'projecttimetracker',
    ],
    package_dir={'projecttimetracker':
                 'projecttimetracker'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv2",
    zip_safe=False,
    keywords='projecttimetracker',
    entry_points='''
        [console_scripts]
        trk=projecttimetracker.projecttimetracker:cli
    ''',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
    tests_require=test_requirements
)
