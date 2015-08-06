from setuptools import setup, find_packages

from postgres import VERSION


setup(
    name='django-postgresql',
    version='.'.join(map(str, VERSION)),
    description='Postgres-specific django goodness.',
    long_description='Postgres-specific django goodness. Edited setup.py to upload it to pypi.',
    author='Matthew Schinckel',
    author_email='matt@schinckel.net',
    packages=find_packages(),
    install_requires=['Django'],
    tests_require=['Django'],
)
