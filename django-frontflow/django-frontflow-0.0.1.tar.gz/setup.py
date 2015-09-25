#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name="django-frontflow",
      version='0.0.1',
      packages=find_packages(),
      include_package_data=True,
      author='Sebastián Acuña',
      author_email='sacuna@gmail.com',
      url='https://github.com/Unholster/django-frontflow',
      download_url='https://github.com/Unholster/django-frontflow/tarball/0.0.1',  # noqa
      description='Grunt based frontend asset management utils',
      license='MIT',
      install_requires=[],
      )
