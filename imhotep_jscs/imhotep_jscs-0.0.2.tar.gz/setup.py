import sys
from setuptools import setup, find_packages

setup(
    name='imhotep_jscs',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/justinabrahms/imhotep_jscs',
    license='MIT',
    install_requires=['imhotep>=0.4.0'],
    tests_require=['mock', 'pytest'],
    author='Justin Abrahms',
    author_email='justin@abrah.ms',
    description='An imhotep plugin for jscs validation',
    entry_points={
        'imhotep_linters': [
            '.js = imhotep_jscs.plugin:JSCS'
        ],
    },
)
