# Copyright 2015 Alex Orange
# 
# This file is part of LDB LAPACK.
# 
# LDB LAPACK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LDB LAPACK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with LDB LAPACK.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(name='LDB_LAPACK',
      version='0.1',
      description='A CFFI wrapper and helper functions/objects for LAPACK',
      author='Alex Orange',
      author_email='alex@eldebe.org',
      packages=['ldb', 'ldb.lapack'],
      namespace_packages=['ldb'],
      url='http://www.eldebe.org/ldb/lapack/',
      license='AGPLv3',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Scientific/Engineering :: Mathematics',
      ],
      setup_requires=["cffi>=1.0.0", "setuptools_hg"],
      cffi_modules=["cffi/build_lapack.py:ffi"],
      install_requires=["cffi>=1.0.0"],
      tests_require=["cffi>=1.0.0"],
      test_suite='test',
     )
