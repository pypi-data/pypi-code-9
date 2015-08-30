from setuptools import setup

setup(
	name='zenpy',
	packages=['zenpy'],
	version='0.0.5',
	description='Python wrapper for the Zendesk API',
	author='Face Toe',
	author_email='facetoe@facetoe.com.au',
	url='https://github.com/facetoe/zenpy',
	download_url='https://github.com/facetoe/zenpy/releases/tag/0.0.5',
	install_requires=[
		'requests'
	],
	keywords=['zendesk', 'api', 'wrapper'],
	classifiers=[],
)
