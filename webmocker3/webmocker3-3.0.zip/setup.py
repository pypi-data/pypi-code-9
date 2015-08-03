from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'webmocker3',
  packages=find_packages(), # this must be the same as the name above
  version = '3.0',
  description = 'A test lib for stubbing http response',
  author = 'Shelton Paul',
  install_requires=['pretend_extended3','bottle'],
  author_email = 'sheltonpaul89@gmail.com',
  url = 'https://github.com/sheltonpaul89/web-mocker3', # use the URL to the github repo
  download_url = 'https://github.com/sheltonpaul89/web-mocker3/tarball/3.0',
  keywords = ['web', 'stubbing', 'http','mock','Web Stubs'], # arbitrary keywords
  classifiers = [],
)
