
from setuptools import setup, find_packages
import sys, os

version = '1.1.3'

setup(
    name = 'daprot',
    version = version,
    description = "daprot is a data prototyper and mapper library.",
    packages = find_packages( exclude = [ 'ez_setup'] ),
    include_package_data = True,
    zip_safe = False,
    entry_points = {},
    author = 'Bence Faludi',
    author_email = 'bence@ozmo.hu',
    license = 'GPL',
    install_requires = [
        'dm',
        'funcomp',
    ],
    test_suite = "daprot.tests"
)
