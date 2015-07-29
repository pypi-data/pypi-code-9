"""A small set of JSON-related tools."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
	name='sculpt.json_tools',
	version='0.1',
	description='A small set of JSON-related tools.',
	long_description='',
	url='https://github.com/damienjones/sculpt-json-tools',
	author='Damien M. Jones',
	author_email='damien@codesculpture.com',
	license='LGPLv2',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
	], 
	keywords='',
	packages=find_packages(),
	# install_requires=[],
	# package_data={},
	# data_files=[],
	# entry_points={},
	# console_scripts={},
)
