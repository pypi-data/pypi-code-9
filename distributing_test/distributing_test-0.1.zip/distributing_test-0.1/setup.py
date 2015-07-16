try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': 'Just testing some stuff',
  'author': 'Thomas B.',
  'url': '',
  'download_url': '',
  'author_email': '',
  'version': '0.1',
  'install_requires': ['nose'],
  'packages': ['NAME'],
  'scripts': [],
  'name': 'distributing_test'
  }

setup(**config)
