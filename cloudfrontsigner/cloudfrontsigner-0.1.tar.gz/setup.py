#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
description = 'Generate AWS CloudFront\'s Signed URLs'

try:
    readme = open(os.path.join(here, 'README.rst')).read()
    changes = open(os.path.join(here, 'CHANGES.txt')).read()
    long_description = '\n\n'.join([readme, changes])
except IOError:
    long_description = description

requires = [
    'rsa',
]

tests_require = [
    'mock',
]

setup(
    name='cloudfrontsigner',
    version='0.1',
    description=description,
    long_description=long_description,
    author='OCHIAI, Gouji',
    author_email='gjo.ext@gmail.com',
    url='https://github.com/gjo/cloudfrontsigner',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    test_suite='cloudfrontsigner.tests',
    extras_require={
        'testing': tests_require,
    },
    entry_points={
        'console_scripts': [
            'cfsign = cloudfrontsigner.cfsign:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
