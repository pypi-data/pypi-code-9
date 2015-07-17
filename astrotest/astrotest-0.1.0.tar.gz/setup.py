# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='astrotest',
    version='0.1.0',
    author=u'Julian Harley',
    author_email='astrotest.20.learningfuture@spamgourmet.com',
    packages=['astrotest'],
    url='https://github.com/julzhk/autogenerate_functional_tests',
    license='GNU licence, see LICENCE.txt',
    description='Auto generate unit-tests for a function from'
                ' executions of the function.'
                '',
    long_description=open('astrotest/README.txt').read(),
)