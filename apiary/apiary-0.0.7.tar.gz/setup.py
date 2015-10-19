#!/usr/bin/env python

from setuptools import setup


setup(name='apiary',
      version='0.0.7',
      description='Python version of the Ruby Apiary client',
      author='James Birmingham, Apiary',
      author_email='james@dimsum.tv',
      packages=['apiary', 'apiary.command', 'apiary.helpers', 'apiary.file_templates'],
      install_requires=[
          'click',
          'Jinja2==2.8'
      ],
      entry_points={
          "console_scripts": [
              "apiary = apiary.__main__:main"
          ]
      },
      url="https://github.com/Jimflip/apiary-client.git",
      download_url="https://github.com/Jimflip/apiary-client/archive/0.0.7.tar.gz")