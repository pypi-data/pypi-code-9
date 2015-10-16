# coding=utf-8
# django-simple-blacklist 6/29/15 9:57 AM by mnach #
import os
from setuptools import setup
import blacklist
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simple-blacklist',
    version=blacklist.__version__,
    packages=['blacklist', 'blacklist.migrations', 'blacklist.management', 'blacklist.management.commands'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app which implements blacklists',
    long_description=README,
    url='https://github.com/mnach/django-simple-blacklist',
    author=blacklist.__author__,
    author_email='mnach@ya.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
