#!/usr/bin/env python

from distutils.core import setup


setup(
    name='qri-py',
    version='1.0.3',
    description='Qri Python interface',
    author='va-dev',
    author_email='vadimanikin1@gmail.com',
    url='https://github.com/Orderry/qri-py',
    packages=['qri_py'],
    package_dir={'qri_py': 'src/qri_py'},
    install_requires=['pyasn1']
)
