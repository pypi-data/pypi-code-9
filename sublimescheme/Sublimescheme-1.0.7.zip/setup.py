# SublimeScheme setup
# Last updated (TSK, 2015-08-18)

from sys import version
if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
#from setuptools import setup
from distutils.core import setup

setup(
	name='Sublimescheme',
	version='1.0.7',
	description='Easily create a Sublime text Color Scheme with as little as six lines of code',
	long_description = open('README').read(),
	author='Taiwo Kareem',
	author_email='taiwo.kareem36@gmail.com',
	url='https://github.com/tushortz/sublimescheme',
	packages=['sublimescheme','sublimescheme/example'],
	package_data={
		'sublimescheme/example':['*.py', 'sublimescheme/example/*.py'],
		},
	platforms='any',
	keywords='Sublime text Color Scheme generator',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Education', 
		'Intended Audience :: Information Technology',
		'Intended Audience :: Other Audience',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
)

