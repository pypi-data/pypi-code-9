#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open
import os

from pip.req import parse_requirements
kwargs = {}
try:
    # pip's parse_requirements added a required 'session=' argument after version 6.0+.
    #
    # Given that the pip installed on our Jenkins is older, we can't just use the newer
    # config. So I'm catching the import error and defaulting to None if it's older pip.
    from pip.download import PipSession
    kwargs['session'] = PipSession()
except ImportError:
    pass

from setuptools import setup, find_packages

install_requirements = [str(requirement.req) for requirement in
                        parse_requirements('./requirements.txt', **kwargs)]
test_requirements = [str(requirement.req) for requirement in
                     parse_requirements('./test_requirements.txt', **kwargs)]

# Get the long description from the relevant file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spex',
    version='0.1.1',
    description='PEX for PySpark',
    long_description=long_description,
    keywords='spex',
    author='',
    author_email='bowyer@urx.com',
    license='Proprietary',
    # The project's main homepage
    url='https://github.com/URXTech/spex',
    packages=find_packages(exclude=['*tests*']),
    package_data={
        'spex': ['*.txt']
    },
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requirements,
    tests_require=test_requirements,

    entry_points={
        'console_scripts': [
            'spex = spex.bin.spex:main',
        ]
    }
)
