#!/usr/bin/python
from setuptools import setup, find_packages

# Import the module version
from feedback import __version__

# Run the setup
setup(
    name             = 'feedback',
    version          = __version__,
    description      = 'Feedback and user input manager',
    long_description = open('DESCRIPTION.rst').read(),
    author           = 'David Taylor',
    author_email     = 'djtaylor13@gmail.com',
    url              = 'http://github.com/djtaylor/python-feedback',
    license          = 'GPLv3',
    install_requires = ['colorama>=0.2.5', 'termcolor>=1.1.0'],
    packages         = find_packages(),
    keywords         = 'feedback terminal shell ui output input',
    classifiers      = [
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