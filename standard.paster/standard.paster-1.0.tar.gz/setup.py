#!/bin/env python

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='standard.paster',
      version_command=('git describe --tags --dirty', 'pep440-git'),
      description="Quickly create a standard Python module layout",
      long_description=README,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Plugins',
          'Framework :: Paste',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Code Generators',
      ],
      keywords='paster bootstrap',
      author='Jon Miller',
      author_email='jonEbird@gmail.com',
      url='https://github.com/jonEbird/standard-paster',
      license='Apache',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'Paste',
          'PasteScript',
          'Cheetah',
          # -*- Extra requirements: -*-
      ],
      setup_requires=["setuptools_git", "setuptools_version_command"],
      dependency_links=[],
      # tests_require=['nose'],
      entry_points="""
        # These will declare what templates paster create command can find
        # -*- Entry points: -*-
        [paste.paster_create_template]
        standard = python_template.newmodule:PyTemplate
        """
      )
