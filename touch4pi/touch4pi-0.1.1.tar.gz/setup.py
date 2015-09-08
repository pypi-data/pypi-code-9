#!/usr/bin/env python

from setuptools import setup, find_packages, Extension

setup(
	name = 'touch4pi',
	version = '0.1.1',
	license='MIT',
	author = 'Jason Barnett',
	author_email = 'jason.barnett@cyntech.co.uk',
	url = 'https://github.com/CyntechUK/touch4pi',
	description = 'Python library for interfacing with the Touch4Pi board',
	long_description=open('README').read(),
	py_modules = [ 'touch4pi' ],
	install_requires = ['rpi.gpio > 0.5'],
)
