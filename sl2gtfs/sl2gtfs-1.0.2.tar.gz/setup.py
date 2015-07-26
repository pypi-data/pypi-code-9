from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sl2gtfs',
    version='1.0.2',
    description='Converts SL stop ids to GTFS stop ids',
    long_description=long_description,
    url='https://github.com/johannilsson/sl2gtfs',
    author='Johan Nilsson',
    author_email='johan@markupartist.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='gtfs stockholm',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'sl2gtfs=sl2gtfs:main',
        ],
    },
)