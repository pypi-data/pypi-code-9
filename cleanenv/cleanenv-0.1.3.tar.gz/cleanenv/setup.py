import os
import re
import sys
from setuptools import setup, find_packages


def _version():
    here = os.path.dirname(__file__)
    src_dir = os.path.join(here, 'cleanenv_inside')
    version_py = open(os.path.join(src_dir, '__init__.py')).read()
    match = re.search(r"__version__\s*=\s*'([^']+)'", version_py)
    return match.group(1)


if sys.version_info[0] == 2:
    packages = ['subprocess32>=3.2.6']
    if sys.version_info[1] <= 6:
        packages += ['argparse>=1.4.0']
else:
    packages = []


setup(name='cleanenv-inside',
      version=_version(),
      description='Clean environment using docker',
      author='Michael Peick',
      author_email='python-cleanenv@n-pq.de',
      url='',
      packages=find_packages(exclude=['commands']),
      package_data={'cleanenv': ['distribution']},
      install_requires=[
          'configobj==5.0.6',
          'docker-py'
      ] + packages,
      entry_points={
          'console_scripts': [
              'cleanenv = cleanenv_inside.cli:main',
              'inenv    = cleanenv_inside.commands.exec_:main'
          ],
          'cleanenv': [
              'destroy = cleanenv_inside.commands.destroy',
              'exec    = cleanenv_inside.commands.exec_',
              'link    = cleanenv_inside.commands.link',
              'reset   = cleanenv_inside.commands.reset'
          ],
      }
    )

