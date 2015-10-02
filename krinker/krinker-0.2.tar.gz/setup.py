'''
Created on Sep 29, 2015

@author: alkrinker
'''
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name='krinker',
      version='0.2',
      description='Testing python\'s distribute',
      url='http://al-krinker.blogspot.com/',
      author='Al Krinker',
      author_email='al.krinker@gmail.com',
      license='MIT',
      packages=['krinker'],
#       install_requires=[
#           'random',
#       ],
      zip_safe=False)