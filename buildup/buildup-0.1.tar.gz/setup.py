#!/usr/bin/env python2
import os
from setuptools import setup
from setuptools import find_packages

setup(
    name="buildup",
    version="0.1",
    description="Static Blog Generator",
    author="Chris Choi",
    author_email="chutsu@gmail.com",
    packages=find_packages(),
    data_files=[
        (
            "templates",
            [os.path.join("templates", f) for f in os.listdir("templates")]
        )
    ],
    install_requires=[
        "markdown",
        "jinja2",
        "beautifulsoup4"
    ]
)
