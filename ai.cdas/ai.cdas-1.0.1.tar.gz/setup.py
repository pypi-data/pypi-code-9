# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'ai.cdas',
    version = '1.0.1',
    description = 'Python interface to CDAS data via REST API',
    long_description = long_description,
    url = 'https://bitbucket.org/isavnin/ai.cdas',
    author = 'Alexey Isavnin',
    author_email = 'alexey.isavnin@gmail.com',
    license = 'MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = 'coordinated data analysis web cdaweb cdas spdf research space physics data facility nasa science',
    packages = find_packages(exclude=['tests*']),
    install_requires = ['numpy', 'requests', 'wget', 'astropy'],
    extras_require = {
        'CDF': ['spacepy']
    }
)