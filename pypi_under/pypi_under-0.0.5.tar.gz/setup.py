from setuptools import setup, find_packages
from app import __version__

README = open('README.txt').read()

setup(name='pypi_under',
      version=__version__,
      description=' Under x Hyphen problem test',
      url='http://www.usuaro.com',
      long_description=README,
      author='usuario',
      author_email='usuario@gmail.com',
      classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
      license="GNU GPLv2",
      packages=find_packages()
      )
