from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='pln',
      version='0.0.1',
      description=u"A library to apply successive operations on your data.",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Taurus Olson",
      author_email='taurusolson@gmail.com',
      url='https://github.com/TaurusOlson/pln',
      license='MIT',
      # packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False
      )
