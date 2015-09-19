# coding: utf-8
from setuptools import find_packages, setup

setup(name='miniorm',
      version='1.5.1',
      keywords='mini mysql db orm :: miniorm',
      description='mini mysql db orm :: miniorm',
      long_description=open("README.rst", 'rb').read(),
      packages=find_packages(exclude=["*.tests", "*.tests.*"]),
      author="inwn",
      author_email="ininwn@gmail.com",
      include_package_data=True,
      license="MIT",
      zip_safe=False,
      # install_requires=[
      #       'mysql-connector-python>=2.0.4'
      # ]
      )
