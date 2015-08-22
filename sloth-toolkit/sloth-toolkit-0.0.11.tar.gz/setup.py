from setuptools import setup



setup(
	name='sloth-toolkit',
	version='0.0.11',

	author='crispycret',
	packages=['sloth_toolkit'],

	url='http://github.com/crispycret/sloth-toolkit',

	license='MIT',

	description='A toolkit that can allow me to be lazy in other projects.',
	#long_description=open('README.txt').read(),

	install_requires = [
		'requests',
		'beautifulsoup4',
		'python-slugify',
	],

	zip_safe=False,

)

