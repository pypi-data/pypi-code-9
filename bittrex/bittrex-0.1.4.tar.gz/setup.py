#!/usr/bin/env python

from setuptools import setup

setup(
	name='bittrex',
	url='https://github.com/panchr/python-bittrex',
	license='MIT',
	version='0.1.4',
	packages=['bittrex'],
	description='Unofficial Python bindings for the Bittrex API',
	keywords=['bittrex', 'bitcoin', 'exchange'],
	author='Rushy Panchal',
	author_email='panchal.rushy@gmail.com',
	install_requires=["requests==2.7.0"],
	classifiers=[
	    'Programming Language :: Python',
	    'Programming Language :: Python :: 2.7',
	    'Operating System :: OS Independent',
	    'License :: OSI Approved :: MIT License',
	    'Development Status :: 3 - Alpha',
	    'Topic :: Office/Business :: Financial',
	])
