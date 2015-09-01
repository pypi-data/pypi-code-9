#!/usr/bin/env python
from jquerypluginbp.boilerplate import BOILERPLATE
import os
from setuptools import setup, find_packages
import sys

extra_kwargs = {}
extra_kwargs['install_requires'] = ['pystache==0.5.4']
if sys.version_info < (2, 7):
    extra_kwargs['install_requires'].append('argparse')

package_data = [os.path.join('boilerplate', boilerplate) for boilerplate in BOILERPLATE]
package_data.extend(['lice/*.txt'])

setup(name="jquerypluginbp",
    packages=['jquerypluginbp', 'jquerypluginbp.lice'],
    package_dir={'jquerypluginbp': 'jquerypluginbp'},
    package_data={'jquerypluginbp': package_data},
    version="0.1.1",
    description="Script to generate boilerplate for your jQuery plugin",
    license="MIT",
    author="Andrea Stagi",
    author_email="stagi.andrea@gmail.com",
    url="",
    keywords= "jquery plugin script boilerplate",
    entry_points = {
        'console_scripts': [
            'jquerypluginbp = jquerypluginbp.main:main',
        ],
    },
    zip_safe = False,
    **extra_kwargs)
