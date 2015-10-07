'''
Created on 06.10.2015

@author: k
'''
from setuptools import setup
import sys

if sys.version.startswith('2.') :
    jp = 'Jpype1'
else :
    jp = 'Jpype1-py3'    

setup(name='simplace',
      version='0.1.5',
      description='Interact with the simulation framework Simplace',
      long_description = '',
      url='http://www.simplace.net/',
      author='Gunther Krauss',
      author_email='guntherkrauss@ui-bonn.de',
      license='GPL3',
      packages=['simplace'],
      install_requires=[
          jp,
      ],
      zip_safe=False)