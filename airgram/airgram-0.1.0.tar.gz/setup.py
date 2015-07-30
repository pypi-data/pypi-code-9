#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup


def get_version():
    import os
    import re
    version_file = os.path.join("airgram", "__init__.py")
    initfile_lines = open(version_file, 'rt').readlines()
    version_reg = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(version_reg, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError(
        u"Unable to find version string in {}".format(version_file)
    )


version = get_version()
requirements = open("requirements.txt").read().split("\n")


setup(
    name="airgram",
    version=version,
    description="Wrapper for the airgram service",
    long_description="",
    author="d01",
    author_email="jungflor@gmail.com",
    url="https://github.com/the01/python-airgram",
    packages=[
        "airgram"
    ],
    install_requires=requirements,
    license="MIT License",
    keywords="airgram",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ]
)
