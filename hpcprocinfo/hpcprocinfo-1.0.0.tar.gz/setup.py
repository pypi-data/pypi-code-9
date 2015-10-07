#!/usr/bin/env python
from setuptools import setup


def get_version(filename):
    with open(filename) as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


setup(
    name='hpcprocinfo',
    version=get_version("hpcprocinfo.py"),
    description='script for checking the stats of HPC (cluster) processes',
    author='Michael Goerz',
    author_email='goerz@stanford.edu',
    url='https://github.com/goerz/hpcprocinfo',
    py_modules=['hpcprocinfo'],
    license='GPL',
    install_requires=[
        'Click',
        'psutil',
    ],
    entry_points='''
        [console_scripts]
        hpcprocinfo=hpcprocinfo:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
