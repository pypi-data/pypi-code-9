"""A setup.py to package KezMenu3 -- a fork of KezMenu by Luca Fabbri."""


import io
import re

from setuptools import setup


def get_version(filename):
    """Uses re to pull out the assigned value to __version__ in filename."""

    with io.open(filename, encoding="utf-8") as version_file:
        version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                                  version_file.read(), re.M)
    if version_match:
        return version_match.group(1)
    return "0.0.0"


setup(
    name="kezmenu3",
    version=get_version("kezmenu3/kezmenu.py"),
    author="Luca Fabbri",
    author_email="lucafbb@gmail.com",
    maintainer="Adam Talsma",
    maintainer_email="adam@talsma.ca",
    packages=["kezmenu3"],
    install_requires=[],  # TODO: pygame + other dep resolution
    url="https://github.com/a-tal/kezmenu3",
    description="KezMenu3 is a KezMenu fork for Python2 and 3.",
    long_description="KezMenu is a GPL PyGame menu library",
    download_url="https://github.com/a-tal/kezmenu3",
    license="GPL",
    classifiers=[  # TODO: classifiers
        "Programming Language :: Python",
    ],
)
