#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from setuptools import setup, find_packages


def parse_requirements(filename):
    """Parse requirement file and transform it to setuptools requirements
    """
    from pip.req import parse_requirements as _parse_requirements
    if os.path.exists(filename):
        return list(str(install_requirement.req) for install_requirement in _parse_requirements(filename, session=False))
    else:
        return []


setup(
    name='qa_tests',
    version=__import__('qa_tests').__version_string,
    packages=find_packages(),
    author="Mappy QA Team",
    author_email="dt.qa@mappy.com",
    description="QA tests tools",
    install_requires=parse_requirements("requirements.pip"),
    url="http://confluence/pages/viewpage.action?pageId=20616082",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': ['multibot=qa_tests.multibot:main']
    }
)
