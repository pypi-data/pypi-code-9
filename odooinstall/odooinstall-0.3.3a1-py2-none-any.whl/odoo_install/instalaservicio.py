#-*- coding: utf-8 -*-

from subprocess32 import call, STDOUT

def scriptInicio(log_file=STDOUT):
	"""
	Instala y configura el script de script
	"""
	# Se descarga el script
	call(["git",
		"clone",
		"https://MrEvil@bitbucket.org/snippets/bisnesmart/7RAK/odoo-server.git",
		"/opt/odoo/scriptinicio"], 
		stderr=log_file)
	# Se copia a la carpeta de scripts de inicio
	call(["cp",
		"/opt/odoo/scriptinicio/odoo-server",
		"/etc/init.d/odoo-server"], 
		stderr=log_file)
	# Se cambian los permisos
	call(["chmod",
		"755",
		"/etc/init.d/odoo-server"], 
		stderr=log_file)
	# Se cambia el propietario y grupo a root
	call(["chown",
		"root:",
		"/etc/init.d/odoo-server"], stderr=log_file)
	# Se activan los scripts
	call(["update-rc.d",
			"odoo-server",
			"defaults"], 
			stderr=log_file)
	call(["update-rc.d",
		"odoo-server",
		"enable"], 
		stderr=log_file)
	




if __name__ == '__main__':
	scriptInicio(STDOUT)

