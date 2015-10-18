#!/usr/bin/env python3

from distutils.core import setup

setup(  name='echobot',
        version='1.0',
        description='echo messages across chat networks.  Supports Hipchat and IRC and can be easily extended to others.',
        author='David Gilman',
        url='https://github.com/dgilman/echobot',
        packages=['echobot'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Topic :: Communications :: Chat :: Internet Relay Chat',
            'Topic :: Communications :: Chat',
            ],
)
