#!/usr/bin/env python

from setuptools import setup

setup(name='koodous-py',
      packages=['koodous'],
      version='0.2',
      description='Module to interact with Koodous API',
      author='Antonio Sanchez',
      author_email='asanchez@koodous.com',
      license='Apache Version 2',
      url='https://koodous.com/',
      download_url='https://github.com/Koodous/python-sdk/archive/master.zip',
      keywords=['koodous', 'api', 'sdk', 'python', 'android', 'apk', 'malware'],
      install_requires=[
        "requests"
      ],
     )
