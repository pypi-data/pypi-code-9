"""
Programmer: JR Padfield
Description: installs PySave
Version: 1
Date:
"""

from distutils.core import setup

setup(name='PySave',
      version='0.1',
      description='All in one data saving from sqlite, mysql, sql, xml, binary',
      author='JR Padfield',
      author_email='admin@crzyware.com',
      url='http://crzyware.com/pysaver',
      packages=['pysave', 'pysave.tests'],
      license="GPLv3",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
      ],
      )
