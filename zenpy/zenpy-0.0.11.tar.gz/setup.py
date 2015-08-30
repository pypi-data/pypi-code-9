from setuptools import setup
import setuptools

try:
	from pypandoc import convert
	read_md = lambda f: convert(f, 'rst')
except ImportError:
	print("warning: pypandoc module not found, could not convert Markdown to RST")
	read_md = lambda f: open(f, 'r').read()

setup(
	name='zenpy',
	packages=setuptools.find_packages(),
	version='0.0.11',
	description='Python wrapper for the Zendesk API',
	long_description=read_md('README.md'),
	license='GPLv3',
	author='Face Toe',
	author_email='facetoe@facetoe.com.au',
	url='https://github.com/facetoe/zenpy',
	download_url='https://github.com/facetoe/zenpy/releases/tag/0.0.11',
	install_requires=[
		'requests',
		'python-dateutil',
		'cachetools'
	],
	keywords=['zendesk', 'api', 'wrapper'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 2',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
	],
)
