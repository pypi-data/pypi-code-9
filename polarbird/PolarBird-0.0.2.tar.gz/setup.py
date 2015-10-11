# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='PolarBird',
    version='0.0.2',
    author='Lukáš Pohlreich',
    author_email='pohlreichlukas@gmail.com',
    packages=find_packages(),
    install_requires=['twitter', 'pgi'],
    description='Terminal based Twitter client for simple use.',
    license='MIT license',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'polarbird = polarbird:start_app'
        ]
    }
)
