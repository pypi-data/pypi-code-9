from setuptools import setup
from subprocess import call
from distutils.command.install import install as _install
from distutils.command.install import INSTALL_SCHEMES
import sys

for scheme in INSTALL_SCHEMES.values():
	scheme['data']=scheme['purelib']

def _post_install(dir):
	global call
	try:
		import espeak
	except:
		print "missing espeak. installing it for you"
		call(['sudo','apt-get','install','python-espeak','flac','-y'])
	print "finished post install"
	call(['chmod','777',"/usr/local/lib/python2.7/dist-packages/godcomplex/batman.mp3"])
	call(['chmod','777',"/usr/local/lib/python2.7/dist-packages/godcomplex/daffy_language.mp3"])

class install(_install):
	def run(self):
		_install.run(self)
		_post_install(self.install_lib)	

setup(name="godcomplex",
	cmdclass={'install':install},
	data_files=[('godcomplex',['batman.mp3','daffy_language.mp3'])],
	version="0.1.00",
	description="this will say something if you say god. or other stuff",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="GNU",
	packages=["godcomplex"],
	scripts=['bin/godcomplex','bin/batmancomplex','bin/swearcomplex'],
	keywords=["god","irony","speech recognition"],
	install_requires=['SpeechRecognition'],
	zip_safe=False)
