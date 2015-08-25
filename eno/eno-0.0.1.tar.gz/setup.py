"""The eno-python package."""

from setuptools import setup


with open('readme.md') as f:
  README = f.read()


VERSION = '0.0.1'


setup(
  name='eno',
  version=VERSION,
  description='eno test client',
  long_description=README,
  url='http://github.com/endaga/eno-python',
  download_url=('https://github.com/endaga/eno-python/tarball/%s' %
                VERSION),
  author='Matt Ball',
  author_email='matt@endaga.com',
  license='MIT',
  packages=['eno'],
  install_requires=[],
  zip_safe=False
)
