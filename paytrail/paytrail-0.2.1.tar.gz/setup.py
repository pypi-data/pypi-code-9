"""Paytrail API libraries

https://docs.paytrail.com
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='paytrail',

    version='0.2.1',

    description='Paytrail API libraries',
    long_description=long_description,

    packages=find_packages(exclude=['contrib', 'docs', 'tests*'], include=['paytrail']),
    test_suite='tests', 

    url='https://github.com/paytrail/paytrail',

    author='Vesa Kaihlavirta',
    author_email='vesa.kaihlavirta@paytrail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='paytrail api connectapi',
)
