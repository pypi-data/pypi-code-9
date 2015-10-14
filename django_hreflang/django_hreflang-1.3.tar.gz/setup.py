# -*- coding: utf-8 -*-

"""
	for installing with pip
"""

from distutils.core import setup
from setuptools import find_packages

setup(
	name='django_hreflang',
	version='v1.3',
	author='Mark V',
	author_email='mdilligaf@gmail.com',
	packages=find_packages(),
	include_package_data=True,
	url='https://bitbucket.org/mverleg/django_hreflang',
	license='Revised BSD License (LICENSE.txt)',
	description='Generate the hreflang html header lines when using i18n urls',
	zip_safe=True,
	install_requires = [
		'django',
	],
)
