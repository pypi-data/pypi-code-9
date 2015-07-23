"""
Programmer: JR Padfield
Description: installs PySave
Version: 1
Date:
"""

from distutils.core import setup

setup(name='PySave',
      version='1.0',
      description='All in one data saving from sqlite, mysql, sql, serialization, ini',
      author='JR Padfield',
      author_email='admin@crzyware.com',
      url='https://github.com/TheDocter/PySave',
      packages=['pysave', 'pysave.tests'],
      install_requires=[
        'sqlalchemy>=1.0.7'
      ],
      license="GPLv3",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
      ],
      )
