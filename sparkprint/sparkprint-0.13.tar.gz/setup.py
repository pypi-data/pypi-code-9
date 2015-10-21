from setuptools import setup

setup(name='sparkprint',
	version='0.13',
	description='A test of making packages on PyPI',
	url='http://github.com/CoroBot/sparkprint',
	author='meta',
	author_email='test@example.com',
	license='MIT',
	packages=['sparkprint'],
	install_requires=[
		'markdown',
	],
	zip_safe=False)
