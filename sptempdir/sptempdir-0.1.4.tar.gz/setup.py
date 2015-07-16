# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# Upload pypi:
# python setup.py sdist --formats=gztar upload

# @formatter:off (pycharm - no formatting)
try:
	import pypandoc
	long_description_text = pypandoc.convert('README.md', 'rst')
except Exception as e:
	long_description_text = ''


setup(
	name='sptempdir',

	# https://packaging.python.org/en/latest/distributing.html#version
	version='0.1.4',

	keywords=['tempdir', 'sptempdir', 'temporary directory'],
	description='This module generates temporary directories',
	long_description=long_description_text,

	# The project homepage
	url='https://github.com/sefikail/sptempdir/',

	# Author details
	author='sefikail',
	author_email='aleskrejcicz@gmail.com',

	packages=find_packages(exclude=['docs', 'tests', 'examples']),
	include_package_data=True,

	platforms='any',
	# https://packaging.python.org/en/latest/distributing.html#classifiers
	classifiers=[
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	],

	# License
	license="See: https://creativecommons.org/licenses/by/3.0/",
)
# @formatter:on (pycharm - no formatting)
