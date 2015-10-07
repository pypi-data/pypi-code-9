#!/usr/bin/env python

from distutils.core import setup

execfile('pyflamegraph/version.py')

kwargs = {
    "name": "pyflamegraph",
    "version": str(__version__),
    "packages": ["pyflamegraph"],
    "package_data": {"pyflamegraph": ["flamegraph/flamegraph.pl", "flamegraph/docs/cddl1.txt"]},
    "description": "Wrapper around flamegraph.pl.",
    "author": "Herbert Ho",
    "maintainer": "Herbert Ho",
    "author_email": "herbert.ho@gmail.com",
    "maintainer_email": "herbert.ho@gmail.com",
    "license": "CDDL1",
    "url": "https://github.com/herb/pyflamegraph",
    "download_url": "https://github.com/herb/pyflamegraph/archive/master.tar.gz",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**kwargs)
