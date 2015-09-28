#!/usr/bin/env python
import os

from distutils.core import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
        SCRIPT_DIR = os.getcwd()


# put together list of requirements to install
install_requires = []
with open(os.path.join(SCRIPT_DIR, 'requirements.txt')) as fh:
    for line in fh.readlines():
        if line.startswith('-'):
            continue

        install_requires.append(line.strip())

data_files = [(dirpath, [os.path.join(dirpath, x) for x in filenames]) for dirpath, dirnames, filenames in os.walk('files') if filenames]

setup(name='zymbit',
      version='0.5.14',
      description='Zymbit cloud library',
      author='Roberto Aguilar',
      author_email='roberto@zymbit.com',
      packages=[
          'zymbit', 'zymbit.arduino', 'zymbit.commands',
          'zymbit.common', 'zymbit.compat', 'zymbit.darwin',
          'zymbit.linux', 'zymbit.messenger', 'zymbit.raspberrypi'
      ],
      scripts=['scripts/zymbit'],
      data_files=data_files,
      long_description=open('README').read(),
      url='http://datavytals.com/',
      license='LICENSE',
      install_requires=install_requires,
)
