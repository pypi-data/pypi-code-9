import codecs
import os
import re

from setuptools import setup, find_packages


####################################################################

NAME = "veryfay"
VERSION = "0.1.0"
DESCRIPTION = "Activity based authorization."
URL = "https://github.com/florinn/veryfay-python"
AUTHOR = "Florin Nitoi"
EMAIL = "florin.nitoi@gmail.com"
LICENSE = "MIT"
PACKAGES = ['veryfay']
META_PATH = os.path.join("veryfay", "__init__.py")
KEYWORDS = ["authorization", "engine", "activity", "role", "permission"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
]
INSTALL_REQUIRES = []
TEST_REQUIRES = ["behave>=1.2.4", "pyhamcrest>=1.8.5"]

###################################################################

setup(
    name=NAME,
	version=VERSION,
    description=DESCRIPTION,
	long_description=DESCRIPTION,
    packages=PACKAGES,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
	license=LICENSE,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    keywords=KEYWORDS,
    )
