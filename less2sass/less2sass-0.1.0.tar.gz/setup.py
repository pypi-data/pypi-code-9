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
    'click<5.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='less2sass',
    version='0.1.0',
    description="Python package that will convert valid less code into sass code.",
    long_description=readme + '\n\n' + history,
    author="Sydney Henry",
    author_email='shenry@handycodejob.com',
    url='https://github.com/sydhenry/less2sass',
    packages=[
        'less2sass',
    ],
    package_dir={'less2sass':
                 'less2sass'},
    entry_points={
        'console_scripts': [
            'less2sass = less2sass.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='less2sass',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
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
