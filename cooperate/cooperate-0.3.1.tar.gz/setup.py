#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as file:
    content = file.read()

setup(
    name='cooperate',
    version='0.3.1',
    description='Distribute commands to many nodes',
    long_description=content,
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    url='https://github.com/johnnoone/cooperate',
    packages=find_packages(),
    keywords=[
        'infrastructure',
        'asyncio',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Clustering',
    ],
    install_requires=[
        'aioutils',
        'PyYAML',
    ],
    extras_require={
        ':python_version=="3.3"': ['asyncio'],
    },
    entry_points={
        'console_scripts': [
            'cooperate = cooperate.__main__:main'
        ]
    }
)
