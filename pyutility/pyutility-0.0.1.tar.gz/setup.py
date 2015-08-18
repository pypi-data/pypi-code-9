from setuptools import setup

setup(name='pyutility',
      version='0.0.1',
      description='Some utility functions for data manipulation',
      url='https://github.com/nickytong/pyutility',
      author='nickytong',
      author_email='ptong1@mdanderson.org',
      license='MIT',
      packages=['pyutility'],
	    scripts=['bin/jokeByScript'],
	  entry_points = {
        'console_scripts': ['jokeByEntryPoint=pyutility.command_line:main'],
		},
      zip_safe=False)