from setuptools import setup

setup(
	name='gwss_parser',
	version='1.2',
	description='Garena web stats system',
	url='http://github.com/storborg/funniest',
	author='Garena Online Ltd',
	author_email='tranmt@garena.com',
	license='MIT',
	packages=['gwss_parser'],
	package_data={'gwss_parser': ['common/*']},
	install_requires=[
		'redis', 'pyparsing',
	],
	scripts=['bin/gwss-parser.py'],
	zip_safe=False)
