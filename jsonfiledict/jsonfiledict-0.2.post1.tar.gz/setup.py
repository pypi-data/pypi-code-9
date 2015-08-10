#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup (
    name = "jsonfiledict",
    version = versioneer.get_version (),                
    description = "A dict optionally backed by an auto-updating JSON file.",
    long_description = file ("README.rst").read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [],
    keywords = "",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "http://kanga.nu/~claw/",
    license = "LGPL v3",
    packages = find_packages (exclude = ["tests",]),
    package_data = {
    },
    zip_safe = False,
    install_requires = [line.strip ()
                        for line in file ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
