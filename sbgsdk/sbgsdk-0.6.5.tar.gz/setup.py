from setuptools import setup, find_packages
import sys
import os.path

sys.path.append(os.path.dirname(__file__))

from sbdk import VERSION


with open('requirements-dev.txt') as f:
    required = f.read().splitlines()

setup(
    name="sbgsdk",
    version=VERSION,
    include_package_data=True,
    install_requires=required,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['sbg = sbdk.main:main'],
    }
)
