"""A setuptools based setup module.

Based on https://github.com/pypa/sampleproject.

"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as g:
        long_description = f.read() + '\n\n' + g.read()

setup(
    name='django-view-export',
    version='0.5.4',
    description='Export CSV reports of database views.',
    long_description=long_description,
    url='https://gitlab.com/Sturm/django-view-export',
    author='Ben Sturmfels',
    author_email='ben@sturm.com.au',
    license='Apache License, Version 2.0',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'pandas>=0.13.1',
    ],
)
