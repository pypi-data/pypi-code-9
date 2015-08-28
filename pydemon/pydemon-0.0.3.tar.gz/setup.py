from distutils.core import setup

with open('README') as file:
	long_description = file.read()

setup(
	name='pydemon',
	version='0.0.3',
	py_modules=['pydemon'],
	author ='becxer',
	author_email='becxer87@gmail.com',
	url = 'https://github.com/becxer/pydemon',
	long_description = long_description,
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
	],
)


	
