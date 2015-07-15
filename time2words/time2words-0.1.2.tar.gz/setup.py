import io
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.rst')

setup(name='time2words',
      version="0.1.2",
      description='A Python library for converting numerical representation '
      'of time to text.',
      long_description=long_description,
      url='https://github.com/YavorPaunov/time2words',
      author='Yavor Paunov',
      author_email='hello@yavorpaunov.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['num2words'],
      platforms='any',
      test_suite="tests")
