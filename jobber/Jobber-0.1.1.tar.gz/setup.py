#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(name='Jobber',
      version='0.1.1',
        description=("Jobber is a program that executes pipelines. It manages job dependencies,"
                     " restarts them if necessary and logs their status in a database. Jobs are"
                     " persisted in a database and survive system crashes."),
      long_description=readme + '\n\n' + history,
      author="Christoph Rodak",
      author_email='christoph@rodak.li',
      url='https://git.scicore.unibas.ch/AnnotationPipelines/Jobber',
      packages=[
          'Jobber',
      ],
      package_dir={'Jobber':
                   'Jobber'},
      include_package_data=True,
      install_requires=requirements,
      license="BSD",
      zip_safe=False,
      keywords='Jobber',
      scripts=['scripts/jobber_server', 'scripts/jobber_web'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
      ],
      test_suite='tests',
      tests_require=test_requirements
)
