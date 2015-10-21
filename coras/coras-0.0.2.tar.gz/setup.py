#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)
install_dev_reqs = parse_requirements("requirements_dev.txt", session=False)
# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
requirements = [str(ir.req) for ir in install_reqs]



test_requirements = requirements + [str(ir.req) for ir in install_dev_reqs]

setup(
    name='coras',
    version='0.0.2',
    description="Python Coras is a python SDK for the coras.io API.",
    long_description=readme + '\n\n' + history,
    author="Philip Roche",
    author_email='phil.roche@coras.io',
    url='https://github.com/philroche/python_coras',
    packages=[
        'CorasLib',
    ],
    package_dir={'CorasLib':
                 'CorasLib'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='coras',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
