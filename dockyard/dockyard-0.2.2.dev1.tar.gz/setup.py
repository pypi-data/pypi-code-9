#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.txt') as file:
    long_description  =  file.read()

setup(name = 'dockyard',
    version = '0.2.2.dev1',
    license = 'MIT',
    description = 'CLI helper for development using Vagrant + Docker',
    long_description = long_description,
    author = 'Joshua Bellamy-Henn',
    author_email = 'josh@psidox.com',
    url = 'https://github.com/smysnk/dockyard',
    install_requires = ['python-vagrant >= 0.5.8', 'docker-py >= 1.1.0'],
    keywords = "docker vagrant build tool dockyard",
    packages = find_packages(),
    entry_points = {
        'console_scripts':
            ['dockyard  =  dockyard.entry:main'],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ], 
)