import os
from setuptools import setup
def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()
setup(
    # Application name:
    name="oprex",

    # Version number (initial):
    version="0.9.1",

    # Application author details:
    author="Ron Panduwana",
    author_email="panduwana@gmail.com",

    # Packages
    packages=["oprex"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://pypi.python.org/pypi/oprex/",

    #
    # license="LICENSE.txt",
    description="another python parser",
	keywords = ['testing', 'logging', 'example'], # arbitrary keywords
	classifiers = [],
    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "argparse>=1.2.1",
		"ply>=3.4",
		"regex>=2014.12.24",
    ],
)