'''
Created on 06.10.2015

@author: k
'''
from setuptools import setup

setup(name='simplace',
      version='0.1.4',
      description='Interact with the simulation framework Simplace',
      url='http://www.simplace.net/',
      author='Gunther Krauss',
      author_email='guntherkrauss@ui-bonn.de',
      license='GPL3',
      packages=['simplace'],
      install_requires=[
          'Jpype1-py3',
      ],
      zip_safe=False)