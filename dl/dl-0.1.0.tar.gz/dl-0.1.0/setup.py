from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(	name='dl',
	version='0.1.0',
	description='dl - rm with forgivness',
	author='Dan Brooks',
	author_email='dan@cs.uml.edu',
	url='http://www.github.com/mrdanbrooks/dl.git',
	scripts=['dl'],
	long_description="""\
    Provides a safe alternative to using the rm command to remove files.
    By training yourself to type a different combination of letters to remove a file, such as dl, you become more aware of your actions when using rm.
    dl moves your files to the desktop trash can. 
	""",
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python",
		"Environment :: Console",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Operating System :: POSIX",
		"Topic :: Utilities"
	],
	keywords='dl, rm, archiving',
	license='BSD',
	install_requires=requirements,
	)
