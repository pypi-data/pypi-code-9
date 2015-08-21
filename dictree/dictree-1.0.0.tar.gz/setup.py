# coding:utf-8

from setuptools import setup, find_packages

long_description = """\
Tree structure with dict interface and wildcard feature.

See detail at http://github.com/tomokinakamaru/dictree.

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
    description='Tree structure with dict interface and wildcard feature',
    license='MIT',
    long_description=long_description,
    name='dictree',
    packages=find_packages(),
    platforms='any',
    url='http://github.com/tomokinakamaru/dictree',
    version='1.0.0'
)
