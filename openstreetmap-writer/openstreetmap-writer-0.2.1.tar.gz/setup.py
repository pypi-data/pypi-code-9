#! /usr/bin/env python

from setuptools import setup

exec(open("./osmwriter/_version.py").read())

setup(name="openstreetmap-writer",
      version=__version__,
      author="Rory McCann",
      author_email="rory@technomancy.org",
      packages=['osmwriter'],
      install_requires = [
          "six",
      ],
      license = 'AGPLv3+',
      description = "Write OSM data files",
      test_suite='osmwriter.tests',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
      ],
)
