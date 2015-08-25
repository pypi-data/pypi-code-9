import os
from setuptools import setup, find_packages

try:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except IOError:
    README = ''

setup(
    name = 'psqldumper',
    version = '0.1.5',
    author = 'Nicolas Brisac',
    author_email = 'nbrisac@oasiswork.fr',
    description = 'Postgresql dump management helper.',
    license = 'MIT',
    url = 'https://git.owk.cc/nbrisac/psqldumper',
    packages = find_packages(),
    namespace_packages = ['psqldumper'],
    install_requires = [],
    extras_require = {},
    entry_points = {'console_scripts': [
        'psqldumper = psqldumper.main:main',
    ]},
    package_data = {'psqldumper': ['etc/*.conf.sample']},
    classifiers = [])
