# Pygeminfo setup
# Last updated (TSK, 2015-08-08)

from sys import version
if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
#from setuptools import setup
from distutils.core import setup

setup(
	name='pygeminfo',
	version='0.0.1',
	description='A Python package that displays several information about a RubyGem.',
	long_description = open('README').read(),
	author='Taiwo Kareem',
	author_email='taiwo.kareem36@gmail.com',
	url='http://github.com/tushortz/pygeminfo',
	packages=['pygeminfo','pygeminfo/example'],
	package_data={
		'pygeminfo/examples':['*.py', 'pygeminfo/example/*.py'],
		},
	platforms='any',
	keywords='ruby, gems, RubyGem, rubygem stats, rubygem information',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Other Audience',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Utilities',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Programming Language :: Ruby',
		'Operating System :: OS Independent',
	],

)

