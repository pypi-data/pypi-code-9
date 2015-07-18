#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
	name='django-pypiwik',
	version='0.1.4',
	description='Django helper application around pypiwik',
	long_description=open('README.md').read(),
	author='Johann Schmitz',
	author_email='johann@j-schmitz.net',
	url='https://ercpe.de/projects/django-pypiwik',
	download_url='https://code.not-your-server.de/django-pypiwik.git/tags/',
	packages=find_packages('src'),
	package_dir={'': 'src'},
	include_package_data=True,
	zip_safe=False,
	license='GPL-3',
)
