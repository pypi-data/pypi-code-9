# encoding: utf-8
from __future__ import print_function

from setuptools import setup


version = (0, 0, 1)

setup(
    name='demo-package',
    version="%d.%d.%d" % version,
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    license="BSD",

    #entry_points={
        #'console_scripts': ["say_hi=demo_package.greeter:greet"]
    #},
)
