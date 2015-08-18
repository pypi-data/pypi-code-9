from setuptools import setup

setup(name='pyspriter',
	  version='0.5',
	  description='Command line sprite generator module for Python',
	  url='https://github.com/halilkaya/pyspriter',
	  author='Halil Kaya',
	  author_email='halil@halilkaya.net',
	  license='MPLv2',
	  packages=['pyspriter'],
	  scripts=['pyspriter/pyspriter.py'],
	  install_requires=['setuptools'],
	  py_modules=['pyspriter/pyspriter'],
	  zip_safe=False)