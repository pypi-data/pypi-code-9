#!/usr/bin/env python

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

if os.path.exists('README.txt'):
    README = open('README.txt').read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='wagtail-global-settings',
    version='0.1.0',
    packages=['wagtail_global_settings', 'wagtail_global_settings.templatetags'],
    package_data={'wagtail_global_settings': ['templates/wagtail_global_settings/*.html']},
    install_requires=['wagtail', 'django-solo'],
    include_package_data=True,
    license='BSD License',
    description='Global settings editor for Wagtail using django-solo',
    long_description=README,
    url='https://bitbucket.org/jordanmarkov/wagtail-global-settings',
    download_url='https://bitbucket.org/jordanmarkov/wagtail-global-settings/get/0.1.0.tar.gz',
    author='Jordan Markov',
    author_email='jmarkov@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
