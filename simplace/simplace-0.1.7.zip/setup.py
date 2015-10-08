'''
Created on 06.10.2015

@author: k
'''
from setuptools import setup
import sys
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


if sys.version.startswith('2.') :
    jp = 'Jpype1'
else :
    jp = 'Jpype1-py3'    

__version__ = ''
exec(open('simplace/_version.py').read())

setup(name='simplace',
      version=__version__,
      description='Interact with the simulation framework Simplace',
      long_description = read('simplace/README.rst'),
      url='http://www.simplace.net/',
      author='Gunther Krauss',
      author_email='guntherkrauss@ui-bonn.de',
      license='GPL3',
      packages=['simplace'],
      install_requires=[
          jp,
      ],
      zip_safe=False)