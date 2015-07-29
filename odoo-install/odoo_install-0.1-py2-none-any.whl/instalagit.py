#-*- coding: utf-8 -*-


from subprocess32 import call, STDOUT

def instalaGit(log_file):
	"""
	Función de instalación de git y de clonación del repo. 
	"""

	print("""			Instalando GIT...
			----------------------------------------""")
  	call(["apt-get",
  		 "install",
  		 "git",
  		 "-y"], 
  		 stderr=log_file)

	#clono el repo
	print("""			Clonando repo...
			----------------------------------------""")
	# Añadido punto al final para que no se produzca lo de /odoo/odoo
	call([	"git",
			"clone",
			"https://www.github.com/odoo/odoo",
			"--depth",
			"1",
			"--branch",
			"8.0",
			"--single-branch",
			"/opt/odoo"])

	call(['chown', '-R', 'odoo:odoo', "/opt/odoo"], stderr=log_file)