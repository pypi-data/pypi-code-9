from setuptools import setup

setup(name='lov2pi',
      	version='0.1.9',
      	description='Python sdk for lov2pi webservice',
      	url='https://github.com/nyo16/lov2pi',
      	author='Nikos Maroulis',
      	author_email='nik.maroulis@gmail.com',
      	license='MIT',
      	packages=['lov2pi'],
      	zip_safe=False,
	install_requires=[
          'requests',
		  'netifaces',
		  'psutil',
		  'daemons'
      	],
	scripts=['bin/lov2pi'])
