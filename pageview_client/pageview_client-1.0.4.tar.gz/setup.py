#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand  # noqa
import sys


# versioning note
# <major> . <minor> . <travis build number>

version = "1.0.4"


name = "pageview_client"
package = "pageview_client"
description = "clients and models for working with the pageview-* suite"
url = "https://github.com/theonion/pageview-client"
author = "Vince Forgione"
author_email = "vforgione@theonion.com"
license = "MIT"

setup_requires = []

install_requires = [
    "requests",
]

dev_requires = install_requires + [
    "flake8",
    "pytest",
    "django",
    "pytest-django",
    "pytest-cov",
    "mock",
    "coveralls",
]

server_requires = []

if "test" in sys.argv:
    setup_requires.extend(dev_requires)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["tests"]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=[package],
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        "dev": dev_requires,
    },
    cmdclass={
        "test": PyTest
    }
)
