from setuptools import setup
from subprocess import call
from distutils.command.install import install as _install

def _post_install(dir):
	global call
	try:
		import espeak
	except:
		print "missing espeak. installing it for you"
		call(['sudo','apt-get','install','python-espeak','flac','-y'])

class install(_install):
	def run(self):
		_install.run(self)
		self.execute(_post_install,(self.install_lib),msg='running post install')	

setup(name="godcomplex",
	cmdclass={'install':install},
	version="0.0.5",
	description="this will say something if you say god",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="GNU",
	packages=["godcomplex"],
	scripts=['bin/godcomplex'],
	keywords=["god","irony","speech recognition"],
	install_requires=['SpeechRecognition'],
	zip_safe=False)
