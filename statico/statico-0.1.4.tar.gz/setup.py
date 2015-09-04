#!/usr/bin/env python

import os
from setuptools import setup

VERSION = __import__('statico').__version__

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)
for dirpath, dirnames, filenames in os.walk('statico'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[12:]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

print(packages)

setup(name='statico',
      version=VERSION,
      description='Static site generator',
      long_description=open('README.rst').read(),
      author='Ossama Edbali',
      author_email='ossedb@gmail.com',
      url='https://github.com/oss6/statico/',
      license='MIT',
      platforms='any',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.4',
          'Topic :: Utilities'
      ],
      packages=packages, # ['statico']
      include_package_data=True,
      entry_points={
          "console_scripts": ['statico = statico.statico:run']
      },
      install_requires=[
        'pathlib',
        'feedparser',
        'github3.py',
        'Jinja2',
        'livereload',
        'Markdown',
        'MarkupSafe',
        'oauthlib',
        'pytz',
        'PyYAML',
        'requests',
        'requests-oauthlib',
        'uritemplate.py',
        'Pygments',
        'colorama',
        'python-slugify'
      ],
)
