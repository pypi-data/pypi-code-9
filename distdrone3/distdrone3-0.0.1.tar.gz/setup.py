from setuptools import setup
from subprocess import call
import os, socket, sys
from distutils.command.install import install as _install

def _post_install(dir):
	global call
	call(['pip','install','-e','.'])
	try:
		os.chdir('/home/pi/.ipython')
	except:
		os.mkdir('/home/pi/.ipython')
		call(['chown','pi','/home/pi/.ipython'])
		call(['chmod','777','/home/pi/.ipython'])
		os.chdir('/home/pi/.ipython')
	try:
		import pygame
	except:
		print("building without pygame")
	call(['rm','-rf','profile_picluster3'])
	call(['sudo','-u','pi','git','clone','https://github.com/isaacrob/picluster3','profile_picluster3'])
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	myip=s.getsockname()[0]
	os.chdir('profile_picluster')
	call(['sudo','-u','pi','python','writeremotehosts.py','--controller_ip='+myip])

class install(_install):
	def run(self):
		_install.run(self)
		self.execute(_post_install, (self.install_lib,),msg='running post install')

def readme():
	with open("README.txt") as f:
		return f.read()

setup(name="distdrone3",
	cmdclass={'install':install},
	version="0.0.1",
	description="package to drive parallel drone swarm",
	url="https://github.com/isaacrob/distdrone3",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="GNU",
	packages=["distdrone3","distdrone3.motion","distdrone3.imgproc"],
	scripts=["bin/trigger3","bin/testpredictor3","bin/centersearch3","bin/installdronedeps3"],
	keywords=['drone','OpenCV','IPython','parallel'],
	install_requires=['ipython','psutil>=3','paramiko>=1.15','click>=4','pyzmq','dill','picamera'],
	zip_safe=False)
