"""
Setup script for the Python driver for Oracle NoSQL Database
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# TODO
#with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='nosqldb',

    # Version should match the system release, but may vary as patches
    # are created.
    version='3.3.6',

    description='A Python driver for Oracle NoSQL Database',
    # TODO long_description=long_description,

    # The project's main homepage and download page
    url = 'http://www.oracle.com/technetwork/database/database-technologies/nosqldb/downloads',

    # Author details
    author='Luis Rodriguez',
    author_email='luis.g.rodriguez@oracle.com',

    # License is Apache, Version 2.0
    license='Apache V2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Database :: Front-Ends',

        # License -- must match "license" above
        'License :: OSI Approved :: Apache Software License',

        # Supported Python versions
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 3.x -- not yet.  This is because thrift does not
        # officially support Python 3.  There are forks and patches that
        # provide this, and perhaps they should be looked at as alternatives.
        #'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='database, nosql, development',

    # Find packages, don't exclude anything
    packages=find_packages(),

    # Include the proxy, which must be in the nosqldb directory
    include_package_data=True,

    # This package depends on Thrift
    install_requires=['thrift'],
)
