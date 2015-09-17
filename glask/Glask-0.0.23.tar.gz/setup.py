from sys import argv, builtin_module_names

from setuptools import setup

version = '0.0.23'

install_requires = ['Flask>=0.10.1', 'python-dateutil>=2.2',
                    'Flask-DebugToolbar>=0.9.0', 'Flask-WTF>=0.10.2',
                    'inflection', 'selenium', 'Flask-SQLAlchemy', 'alembic']

if '__pypy__' in builtin_module_names:
    install_requires.append('psycopg2cffi')
else:
    install_requires.append('psycopg2')

if 'develop' in argv[1:]:
    install_requires += ['pytest>=2.5.2']

setup(name='Glask', version=version, packages=['glask'], license='BSD',
      description='An extension for flask applications with best practices.',
      url='https://github.com/vamf12/Glask',
      install_requires=install_requires)
