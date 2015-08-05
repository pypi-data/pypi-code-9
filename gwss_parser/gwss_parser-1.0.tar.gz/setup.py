from setuptools import setup

setup(
	name='gwss_parser',
	version='1.0',
	description='Garena web stats system',
	url='http://github.com/storborg/funniest',
	author='Nguyen Khac Tung, Tran Minh Tri',
	author_email='tranmt@garena.com',
	license='MIT',
	packages=['gwss_parser'],
	install_requires=[
		'redis', 'pyparsing',
	],
	scripts=['bin/gwss-parser.py'],
	zip_safe=False)
