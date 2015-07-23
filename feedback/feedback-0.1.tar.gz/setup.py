#!/usr/bin/python
import feedback
from setuptools import setup, find_packages

# Module version / long description
version = feedback.__version__
long_desc = open('DESCRIPTION.rst').read()

# Run the setup
setup(
    name='feedback',
    version=version,
    description='Feedback and user input manager',
    long_description=long_desc,
    author='David Taylor',
    author_email='djtaylor13@gmail.com',
    url='http://github.com/djtaylor/python-feedback',
    license='GPLv3',
    packages=find_packages(),
    keywords='feedback terminal shell ui output input',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals',
    ]
)