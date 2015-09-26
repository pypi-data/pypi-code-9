import os
from setuptools import setup

from osx_trash import __version__


setup(name='osx_trash',
      version=__version__,
      description=('An extendible utility for moving files to the trash, '
                   'from the commandline, on OS X.'),
      author='Jonathan Nappi',
      author_email='moogar@comcast.net',
      maintainer='Jonathan Nappi',
      maintainer_email='moogar@comcast.net',
      license='http://www.gnu.org/copyleft/gpl.html',
      platforms=['OS X'],
      url='https://github.com/moogar0880/osx_trash',
      py_modules=['osx_trash'],
      zip_safe=False,
      entry_points={
          'console_scripts': ['trash = osx_trash:main']
      },
      )
