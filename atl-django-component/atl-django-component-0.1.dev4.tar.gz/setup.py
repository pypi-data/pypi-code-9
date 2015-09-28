# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path
from atl_django_component import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='atl-django-component',
    version=__version__,
    description='An initiative to encapsulate components in django',
    long_description=long_description,
    url='https://pypi.python.org/pypi/atl-django-component',
    author='Hailem Dreis Carrasco Fuentes',
    author_email='hailem@atlantedigital.com',
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='django component',
    packages=find_packages(),
    include_package_data=True,
)