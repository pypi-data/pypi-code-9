from setuptools import setup

setup(name='civeng',
	version='0.2.6',
	description='civil engineering tools',
	url='https://pypi.python.org/pypi/civeng',
	author='dutu8ure',
	author_email='dutu8ure@gmail.com',
	license='GPLv3',
	packages=['civeng', 
				'civeng/concrete', 
				'civeng/concrete/modules',
				'civeng/steel',
				'civeng/steel/modules'],
	zip_safe=False)
