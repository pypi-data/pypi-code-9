#-*- coding: utf-8 -*-

from subprocess32 import call

def stopCalling(log_file):
	"""
	Clonado del repositorio, 
	"""

	call(["git",
			"clone",
			"https://bitbucket.org/BizzAppDev/oerp_no_phoning_home.git",
			"/opt/odoo/stopcalling"
			], stderr=log_file)

	call(["rm",
			"-rf",
			"/opt/odoo/stopcalling/.git/",
			"/opt/odoo/stopcalling/.gitignore"], stderr=log_file)
	call([	"mv",
			"/opt/odoo/stopcalling/",
			"/opt/odoo/addons"], stderr=log_file)


if __name__ == '__main__':
	
	with open("test.txt", 'w') as myfile:
		stopCalling(myfile)