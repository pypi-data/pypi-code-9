import os
import re
import sys
from setuptools import setup


def _version():
    here = os.path.dirname(__file__)
    src_dir = os.path.join(here, 'cleanenv', 'cleanenv_inside')
    version_py = open(os.path.join(src_dir, '__init__.py')).read()
    match = re.search(r"__version__\s*=\s*'([^']+)'", version_py)
    return match.group(1)


if sys.version_info[0] == 2:
    packages = ['subprocess32>=3.2.6']
else:
    packages = []


setup(name='cleanenv',
      version=_version(),
      description='Clean environment using docker',
      author='Michael Peick',
      author_email='python-cleanenv@n-pq.de',
      url='',
      packages=[
          'cleanenv',
          'cleanenv.commands',
          'cleanenv.cleanenv_inside',
          'cleanenv.cleanenv_inside.commands'],
      package_data={'cleanenv': ['distribution/*']},
      install_requires=[
          'argparse>=1.2.1',
          'configobj>=4.7.2',
          'virtualenv>=1.9.1',
      ] + packages,
      setup_requires=[
          'pip>=0.7.2',
          'setuptools>=0.6.14'
      ],
      entry_points={
          'console_scripts': [
              'cleanenv = cleanenv.cleanenv_inside.cli:main'
          ],
          'cleanenv': [
              'create = cleanenv.commands.create',
          ],
      }
    )
