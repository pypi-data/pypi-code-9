import os

from setuptools import setup

def read (*paths):
	with open (os.path.join (*paths), 'r') as aFile:
		return aFile.read()

setup (
	name = 'Opy',
	version = '1.1.12',
	description = 'OPY - Obfuscator for Python, string obfuscation added, keyword added',
	long_description = (
		read ('README.rst') + '\n\n' +
		read ('qQuickLicence.txt')
	),
	keywords = ['opy', 'obfuscator', 'obfuscation', 'obfuscate', 'kivy', 'pyo', 'python'],
	url = 'https://github.com/JdeH/Opy/',
	license = 'qQuickLicence',
	author = 'Jacques de Hooge',
	author_email = 'jacques.de.hooge@qquick.org',
	packages = ['opy'],	
	include_package_data = True,
	install_requires = [],
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: Other/Proprietary License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
	],
)
