# -*- coding: utf-8 -*-
from setuptools import setup
import re


def get_version():
    with open('hepdata_converter_ws/version.py', 'r') as version_f:
        content = version_f.read()

    r = re.search('^__version__ *= *\'(?P<version>.+)\'', content, flags=re.MULTILINE)
    if not r:
        return '0.0.0'
    return r.group('version')

setup(
    name='hepdata-converter-ws',
    version=get_version(),
    install_requires=[
        'hepdata-converter',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'hepdata-converter-ws = hepdata_converter_ws:main',
        ]
    },
    packages=['hepdata_converter_ws'],
    url='https://github.com/HEPData/hepdata-converter-ws/',
    license='GPL',
    author='Michał Szostak',
    author_email='michal.florian.szostak@cern.ch',
    description='Flask webservices enabling usage of hepdata-converter as a separate server over the network',
    download_url='https://github.com/HEPData/hepdata-converter-ws/tarball/%s' % get_version(),
)