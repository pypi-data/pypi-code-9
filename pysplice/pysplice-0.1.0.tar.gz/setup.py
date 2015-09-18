#! /usr/bin/env python

from setuptools import setup

setup(
    name='pysplice',
    version='0.1.0',
    description='CFFI wrapper around the splice syscall',
    author='Dario Bertini',
    author_email='berdario+pypi@gmail.com',
    url='https://github.com/berdario/pysplice',
    license='MIT License',
    packages=['pysplice'],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["pysplice/cffi_build.py:ffi"],
    install_requires=["cffi>=1.0.0"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux']
)
