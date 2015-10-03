#!/usr/bin/env python

from os import path
from setuptools import setup

from mailcat.__version__ import version

README = '\n' + open(path.join(path.dirname(__name__), 'README')).read()

setup(name='mailcat',
    version=version,
    description='Console viewer for MIME mail files',
    long_description=README,
    author='Andrey Golovizin',
    author_email='ag@sologoc.com',
    url='https://python.org/pypi/mailcat',
    license='GPL-3+',
    platforms=['platform-independent'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=['mailcat'],
    install_requires=[
        'termcolor>=1.1.0',
        'html2text',
    ],
    entry_points={
        'console_scripts': ['mailcat = mailcat.__main__:main'],
    }
)
