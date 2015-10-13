#!/usr/bin/env python
from setuptools import setup

try:
    readme = open('README.md', 'r').read()
except IOError:
    readme = ''

setup(
    name='wordfilter',

    version='0.1.9',

    description="A small module meant for use in text generators that lets you filter strings for bad words.",

    long_description=readme,

    author='Neil Freeman & Jim Witschey, based on work by Darius Kazemi',

    author_email='darius.kazemi@gmail.com',

    url='http://tinysubversions.com',

    license='MIT',

    package_dir={'wordfilter': 'lib/wordfilter'},

    packages=['wordfilter'],

    zip_safe=False,

    package_data={
        'wordfilter': ['../badwords.json']
    },

    test_suite='test',

    classifiers=[
        "Programming Language :: Python",
    ],
)
