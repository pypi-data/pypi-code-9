import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return codecs.open(path).read()

setup(
    name = 'easycommandline',
    packages = ['easycommandline'],
    version = '1.8.1',
    description = 'python command-line interfaces made easy',
    long_description = read("README.rst"),
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = 'python command line option argument argv',
    author = 'Tracy Lai',
    author_email = 'me@tracycool.com',
    url = 'https://github.com/tracycool/easycommandline',
    license = 'MIT',
    include_package_data = True,
    zip_safe = True
)
 