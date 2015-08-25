import os
from setuptools import setup

setup(name='itis',
      version='2.0.0',
      description='Check whether a website is up or down',
      keywords='website status website down website up internet check command line too',
      url='http://github.com/akashnimare/itis/',
      author='Akash Nimare',
      author_email='svnitakash@gmail.com',
      license='MIT',
      packages=['itis'],
      entry_points = {
        'console_scripts': ['itis=itis.auto:main'],
        },
      install_requires=[
            'urllib3'
      ],
      zip_safe=False)

