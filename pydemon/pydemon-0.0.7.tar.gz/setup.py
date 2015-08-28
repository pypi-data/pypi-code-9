from distutils.core import setup
import os, sys, stat

with open('README.txt') as file:
	long_description = file.read()

name = 'pydemon'
src_path = '/usr/local/lib/python2.7/site-packages/'+ name + '.py'
trg_path = '/usr/bin/pydemon'

if os.path.islink(trg_path):
	os.remove(trg_path)
if os.path.isfile(src_path):
	os.chmod(src_path,'0755')

os.symlink(src_path,trg_path)

setup(
	name=name,
	version='0.0.7',
	py_modules=['pydemon'],
	author ='becxer',
	author_email='becxer87@gmail.com',
	url = 'https://github.com/becxer/pydemon',
	description ='Monitor for any changes in your Project',
	long_description = long_description,
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
	],
)


	
