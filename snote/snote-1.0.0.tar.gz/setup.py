# coding:utf-8

from setuptools import setup, find_packages

long_description = """\
A tool for generating signed, time-limited & tagged tokens of python objects.

See detail at http://github.com/tomokinakamaru/snote.

Copyright (c) 2015, Tomoki Nakamaru.

License: MIT
"""

setup(
    author='Tomoki Nakamaru',
    author_email='tomoki.nakamaru@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='A tool for generating signed, time-limited & tagged tokens'
                ' of python objects',
    license='MIT',
    long_description=long_description,
    name='snote',
    packages=find_packages(),
    platforms='any',
    url='http://github.com/tomokinakamaru/snote',
    version='1.0.0'
)
