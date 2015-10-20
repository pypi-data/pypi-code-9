#!/usr/bin/env python
# -*- coding: utf-8 -*-



from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'fabric',
    'jinja2'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='fabian',
    version='0.1.0',
    description="Fabian is a set of common functions useful for installing webapps on Debian machines using fabric",
    long_description=readme + '\n\n' + history,
    author="Luke Drummond",
    author_email='luke@ajenta.net',
    url='https://tracker.ajenta.net/projects/fabian',
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='fabian',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
