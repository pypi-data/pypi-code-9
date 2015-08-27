'''
Created on Jul 28, 2015

@author: venkman69@yahoo.com
'''
from setuptools import setup

setup(name='wikitoexcel',
      version='0.1.1',
      description='Convert Wiki to Excel while maintaining formatting',
      url='http://github.com/venkman69/WikiToExcel',
      author='Narayan Natarajan',
      author_email='venkman69@yahoo.com',
      license='MIT',
      packages=['wikitoexcel','example'],
      install_requires=[
          'openpyxl',
          'py-wikimarkup',
          'beautifulsoup4'
      ],
      zip_safe=False)
