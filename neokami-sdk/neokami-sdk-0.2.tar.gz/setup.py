from setuptools import setup, find_packages
from codecs import open
from os import path
from glob import glob
from os.path import basename
import os
from os.path import splitext

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

py_modules = [
	'neokami.src.Neokami.Exceptions.NeokamiBaseException',
	'neokami.src.Neokami.Exceptions.NeokamiSDKException',
	'neokami.src.Neokami.Exceptions.NeokamiAuthorizationException',
	'neokami.src.Neokami.Exceptions.NeokamiBlockedException',
	'neokami.src.Neokami.Exceptions.NeokamiServerException',
	'neokami.src.Neokami.Exceptions.NeokamiParametersException',
	'neokami.src.Neokami.Exceptions.NeokamiResponseException',
	'neokami.src.Neokami.NeokamiRequest',
	'neokami.src.Neokami.NeokamiResponse',
	'neokami.src.Neokami.HttpClients.NeokamiCurl',
	'neokami.src.Neokami.Base',
	'neokami.src.Neokami.ImageAnalyser',
    'neokami.src.Neokami.SentimentAnalyser',
    'neokami.src.Neokami.VisualCortex'

]

setup(
  name = 'neokami-sdk',
  packages = find_packages("./"),
  package_dir={"neokami": "neokami"},
  version = '0.2',
  py_modules = py_modules,
  description = 'Python sdk for Neokami API',
  long_description=long_description,

  author = 'Neokami',
  author_email = 'team@neokami.com',

  license ='Apache Software License',

  url = 'https://github.com/NeokamiCode/Python-SDK',
  keywords = ['sdk', 'machine learning', 'neokami'],

  classifiers = [
	# How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: Apache Software License',

    # Specify the Python versions you support here.
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',


  ],

  install_requires=['requests', 'dicttoxml', 'six'],

   package_data={
	   'tests/data':
		   [
				'tests/data/team1.jpg',
				'tests/data/cat1.jpg'
		   ]


   },

   include_package_data=True,
)