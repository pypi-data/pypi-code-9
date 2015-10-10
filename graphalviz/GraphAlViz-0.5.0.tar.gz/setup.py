"""A setuptools based setup module.
"""
from setuptools import setup, find_packages
from codecs import open
from os import path
from graphalviz import get_version_str

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='GraphAlViz',
    version=get_version_str(),

    description='Graph algorithm visualization library',
    long_description=long_description,

    url='https://bitbucket.org/waldekmalec/graf/',

    author='Waldemar Malec',
    author_email='waldekmalec@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='graph, visualization',

    packages=find_packages(exclude=['tmp', ]),
    package_data={
        'graphalviz': ['*.json', '*.g']
    },

    entry_points={
        'console_scripts': [
            'graphalviz = graphalviz.graphalviz:main',
        ]
    },

    install_requires=[
        'numpy',
        'networkx',
        'matplotlib'
    ],
)
