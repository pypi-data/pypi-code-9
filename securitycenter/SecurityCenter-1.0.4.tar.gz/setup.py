#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='SecurityCenter',
    version='1.0.4',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    url='https://bitbucket.org/davidism/securitycenter',
    license='BSD',
    author='David Lord',
    author_email='davidism@gmail.com',
    description='Python wrapper for Tenable SecurityCenter API.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Systems Administration'
    ],
    install_requires=['requests', 'six']
)
