#!/usr/bin/python

from distutils.core import setup

setup(
    name = "gistimporter",
    packages = ["gistimporter"],
    version = "1.0.1",
    description = "An importer for Python 3.x to allow import modules from gists.",
    author = "Salvador de la Puente González",
    author_email = "salva@unoyunodiez.com",
    url = "https://github.com/delapuente/gistimporter",
    download_url = "https://github.com/delapuente/gistimporter/tarball/1.0.0",
    keywords = ["gist", "import", "importer", "github"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
