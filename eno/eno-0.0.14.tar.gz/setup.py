"""The eno-python package."""

from setuptools import setup


with open('readme.md') as f:
  README = f.read()


VERSION = '0.0.14'


setup(
  name='eno',
  version=VERSION,
  description='eno test client',
  long_description=README,
  url='http://github.com/endaga/eno-python',
  download_url='https://github.com/endaga/eno-python/tarball/%s' % VERSION,
  author='Matt Ball',
  author_email='matt@endaga.com',
  license='MIT',
  packages=['eno'],
  install_requires=[
    "Adafruit-BBIO==0.0.30",
    "Flask==0.10.1",
    "Jinja2==2.8",
    "MarkupSafe==0.23",
    "PyYAML==3.11",
    "Werkzeug==0.10.4",
    "argparse==1.2.1",
    "itsdangerous==0.24",
    "pyserial==2.7",
    "python-gsmmodem==0.9",
    "requests==2.7.0",
    "wsgiref==0.1.2",
  ],
  zip_safe=False,
  scripts=[
    'scripts/run_eno_server',
  ]
)
