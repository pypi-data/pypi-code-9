from setuptools import setup

setup(name='pyspriter',
	  version='0.6',
	  description='Command line sprite generator module for Python',
	  url='https://github.com/halilkaya/pyspriter',
	  author='Halil Kaya',
	  author_email='halil@halilkaya.net',
	  license='MPLv2',
	  scripts=['pyspriter.py'],
	  install_requires=['setuptools'],
	  py_modules=['pyspriter'],
	  zip_safe=False)