from setuptools import find_packages, setup
from codecs import open
from os import path

import pocker


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pocker',
    version=pocker.__version__,
    description='Python wrapper for docker console client',
    long_description=long_description,
    author='Sergey Anuchin',
    author_email='sergunich@gmail.com',
    license='MIT',
    packages = find_packages('pocker'),

    keywords='docker client',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        #'Programming Language :: Python :: 2.6', #TODO
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only ', #FIXME
        #'Programming Language :: Python :: 3.4', #TODO
        #'Programming Language :: Python :: 3.5', #TODO
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
