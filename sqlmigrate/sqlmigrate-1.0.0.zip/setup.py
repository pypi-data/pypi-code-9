from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

try:
    f = open(os.path.join(os.path.dirname(__file__), 'docs', 'index.txt'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(name='sqlmigrate',
      version=version,
      description="Database schema migration tool that works in SQL",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
      ],
      keywords='sql database schema migration evolution migrate sqlalchemy',
      author='Max Ischenko',
      author_email='ischenko@gmail.com',
      url='https://bitbucket.org/msm2e4d534d/sqlmigrate',
      license='Apache License, Version 2.0',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      test_suite = "nose.collector",
      zip_safe=True,
      install_requires=[
          "SQLAlchemy",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
