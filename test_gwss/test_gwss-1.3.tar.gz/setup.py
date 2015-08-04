from setuptools import setup

setup(
	name='test_gwss',
	version='1.3',
	description='Garena web stats system',
	url='http://github.com/storborg/funniest',
	author='Tran Minh Tri',
	author_email='tranmt@garena.com',
	license='MIT',
	packages=['test_gwss'],
	install_requires=[
		'markdown',
	],
	scripts=['bin/test-gwss'],
	zip_safe=False)