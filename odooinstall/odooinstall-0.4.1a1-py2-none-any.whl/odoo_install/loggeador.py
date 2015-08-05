#-*- coding: utf-8 -*-

import os

def logSettings(path=None, filename="instalacion.txt"):
	"""
	Creación del directorio y archivos para el log. 
	"""
	# Ruta
	if path == None:
		path = "/var/log/odoo"

	# Creación del directorio
	if not os.path.exists(path):
		os.makedirs(path)

	# Creación del archivo
	archivo = open(os.path.join(path, filename),'w')

	return path, archivo

