from distutils.core import setup
import os

with open('README.txt') as file:
	long_description = file.read()

print long_description
name = 'pydemon'
src_path = '/'+ os.path.relpath('.','/') +'/'+ name + '.py'
trg_path = '/usr/bin/pydemon'
if os.path.isfile(trg_path):
	os.remove(trg_path)
os.symlink(src_path,trg_path)

setup(
	name=name,
	version='0.0.4',
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


	
