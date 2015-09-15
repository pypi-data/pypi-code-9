#!/usr/bin/env python

from distutils.core import setup

setup(name='pyisi',
      version='0.0.6',
      description='Unofficial Isilon interface for Python',
      author="Jason Kingsbury",
      author_email="jason@relva.co.uk",
      url="https://bitbucket.org/jrelva/pyisi",
      download_url="https://bitbucket.org/jrelva/pyisi/get/0.0.6.tar.gz",
      keywords=['onefs', 'isilon', 'api'],
      packages=["pyisi"],
      install_requires=["requests"]
      )

