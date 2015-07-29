#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

version = "0.1"

readme = open('README.rst').read()

setup(
    name='billparser',
    version=version,
    description="""Parse PDF files and extract fields based on definition files""",
    long_description=readme,
    author='Guillermo M. Narvaja',
    author_email='guillermo.narvaja@radiocut.fm',
    url='https://bitbucket.org/gnarvaja/billparser',
    packages=find_packages(),
    license="BSD",
    zip_safe=False,
    install_requires=['docopt'],
    entry_points={
        'console_scripts': [
            'billparser = billparser:main',
        ]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
