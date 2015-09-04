from distutils.core import setup

version = '0.0.0'

urltemplate = 'https://github.com/rectangletangle/dunderscore/tarball/{version}'

setup(name='dunderscore-py',
      packages=['dunderscore'],
      version=version,
      description='Dunderscore, useful functions for Python 2 or 3',
      author='Drew French',
      author_email='rectangletangle@gmail.com',
      url='https://github.com/rectangletangle/dunderscore',
      download_url=urltemplate.format(version=version))