import os
from setuptools import setup

setup(name='isonline',
      version='1.0.0',
      description='Check if the internet connection is up',
      keywords='website status website down website up internet check command line too',
      url='http://github.com/akashnimare/isonline/',
      author='Akash Nimare',
      author_email='svnitakash@gmail.com',
      license='MIT',
      packages=['isonline'],
      entry_points = {
        'console_scripts': ['isonline=isonline.auto:main'],
        },
      install_requires=[
            'urllib3'
      ],
      zip_safe=False)

