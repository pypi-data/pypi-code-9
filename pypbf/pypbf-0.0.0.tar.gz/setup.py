import os

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from distutils.core import setup, Extension

setup(
    name="pypbf",
    version='0.0.0',
    description='python package for probabilistic bloom filter ',
    long_description='pypbf is a python package for probabilistic bloom filter(PBF), which supports frequency estimation on items',
    classifiers=['Intended Audience :: Developers',
	'License :: Public Domain',
	'Programming Language :: Python',
	'Topic :: Utilities'],
    keywords=('probabilistic bloom filter, frequency estimation'),
    author="Sis Xiong",
    author_email="sxiong@vols.utk.edu",
    url="https://github.com/xsswfm/pypbf/",
    license="Public Domain",
    packages=find_packages(exclude=['ez_setup']),
    platforms=['any'],
    #test_suite="pypbf.tests",
    zip_safe=True,
    install_requires=['bitarray','mmh3']
)
