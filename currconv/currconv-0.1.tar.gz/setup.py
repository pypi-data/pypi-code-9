try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {

	'description': 'Currency Converter for terminal.',
	'name': 'currconv',
	'url': 'https://github.com/conormdurkan/CurrConv',
	'author_email': 'conormdurkan@gmail.com',
	'version': '0.1',
	  
	'classifiers': [
    'License :: OSI Approved :: MIT License',

	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',],

    'entry_points': {
	  	'console_scripts': [
	    	'currconv = currconv.currconv:main',
	   		],
	   },

	'install_requires': ['setuptools', 'argparse', 'nose', 'yahoo-finance'],
	'packages': ['currconv'],
	'scripts': []
}

setup(**config)