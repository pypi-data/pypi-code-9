#from distutils.core import setup
from setuptools import setup, find_packages
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mozurestsdk'))
from config import __version__

long_description="""
    1. https://github.com/mozu/mozu-pyton-sdk/ - README
    2. https://developer.mozu.com/api - API Reference
  """

setup(
  name="mozurestsdk",
  version= __version__,
  author='Mozu',
  author_email='integrations@mozu.com',
  packages=find_packages(),
  scripts=[],
  url="https://github.com/mozu/mozu-python-sdk",
  license='Apache License',
  description='Mozu Rest SDK.',
  long_description=long_description,
  install_requires=['requests', 'six'],
  extras_require={'test': ['coverage']},
  classifiers=[
	'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['mozu', 'rest', 'sdk']
)
