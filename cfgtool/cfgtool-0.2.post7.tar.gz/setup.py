#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup (
    name = "cfgtool",
    version = versioneer.get_version (),
    description = "Cfgtool configuration management",
    long_description = file ("README.rst").read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [],
    keywords = "configuration management",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://pypi.python.org/pypi/cfgtool",
    license = "LGPL v3.0",
    packages = find_packages (exclude = ["tests",]),
    package_data = {
    },
    zip_safe = True,
    install_requires = [line.strip ()
                        for line in file ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
            "cfgtool = cfgtool.main:main",
        ],
    },
)
