#!/usr/bin/env python

from setuptools import setup


setup(
    name='salvage',
    version='0.1.3',
    description='Allows a group of people to hold sensitive information using a simple secret-splitting scheme.',
    long_description=open('README.rst').read(),
    author='Peter Sagerson',
    author_email='psagersDjwublJf@ignorare.net',
    packages=[],
    scripts=['bin/salvage'],
    url='https://bitbucket.org/psagers/salvage',
    license='BSD',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
    ],
)
