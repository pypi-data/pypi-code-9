__author__ = 'sinisa'

import io
from sbg_cli import __version__ as version
from setuptools import setup, find_packages


requires = [
    x.strip() for x in
    io.open('requirements.txt')
]

setup(
    name="sbg-cli",
    version=version,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['sbg = sbg_cli.main:main']
        },
    install_requires=requires,
    package_data={'': ['*.expr-plugin']},
    long_description=io.open('README.md').read(),
    license='AGPLv3'
)