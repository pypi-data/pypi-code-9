# -*- coding: utf-8 -*-
#
# File is part of the djsourceview Project
#
# Author: Roger Pereira Boff <rogerboff@gmail.com>
#

from distutils.core import setup

from setuptools import find_packages

from djsourceview import __version__, __author__, __email__

setup(name='djsourceview',
      version=__version__,
      description='Module for Django to view the javascript source code and html',
      long_description='Module for Django to view the javascript source code and html',
      author=__author__,
      author_email=__email__,
      maintainer=__author__,
      maintainer_email=__email__,
      url='https://github.com/rogerboff/djsourceview',
      py_modules=['djsourceview'],
      keywords=['django', 'djsourceview'],
      platforms=['OS Independent'],
      license='MIT License',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2.7',
      ],
      packages=find_packages(),
      package_data={'': ['*.js', '*.css', '*.html']},
      include_package_data=True,
      install_requires=['django'],
      zip_safe=True
      )
