"""A setuptools based setup module for sharepointcacheprimer.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get current version
with open('VERSION') as version_file:
        version = version_file.read().strip()

setup(
    name='sharepointcacheprimer',
    version=version,

    description='Cache Primer for Sharepoint with ADFSv3',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/rjewell/sharepointcacheprimer',

    # Author details
    author='Bob Jewell',
    author_email='bob@disclosed.org',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='sharepoint adfs cache',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['robobrowser'],
    entry_points={
        'console_scripts': [
            'sharepointcacheprimer=sharepointcacheprimer.cmdline:execute',
        ],
    },
    data_files=[('doc', ['doc/example.ini'])],
)
