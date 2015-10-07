#!/usr/bin/env python
# coding: utf-8
from setuptools import find_packages, setup

from replay_parser import VERSION

setup(
    name="rocket-league-replay-parser",
    version=".".join(str(n) for n in VERSION),
    url="https://github.com/danielsamuels/rocket-league-replay-parser",
    author="Daniel Samuels",
    author_email="daniel.samuels1@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    description='Parser for Rocket League replay files.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
)
