from __future__ import unicode_literals
from setuptools import setup, find_packages


setup(name='coinop',
      version = '0.3.1',
      description = 'Crypto-currency conveniences',
      url = 'http://github.com/GemHQ/coinop-py',
      author = 'Matt Smith',
      author_email = 'matt@gem.co',
      license = 'MIT',
      packages = find_packages(exclude=[
          '*.tests', '*.tests.*', 'tests.*','tests']),
      install_requires = [
          'pycrypto',
          'pbkdf2_ctypes',
          'python-bitcoinlib==0.4.0',
          'pycoin==0.52',
          'PyYAML',
          'future',
          'ecdsa'
      ],
      tests_require = [ 'tox' ],
      zip_safe=False)
