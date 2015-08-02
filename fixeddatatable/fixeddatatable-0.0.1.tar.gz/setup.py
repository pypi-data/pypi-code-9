from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fixeddatatable',
    version='0.0.1',
    description='Utilities for interfacing with FixedDataTable.js',
    long_description=long_description,
    url='https://github.com/jeffroche/fixed-data-table-py',
    author='Jeff Roche',
    author_email='jeff.roche@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='js',
    packages=['fixeddatatable'],
    install_requires=[],
)
