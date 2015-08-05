#-*- coding: utf-8 -*-

# Instala git y clona el repo principal.

from subprocess32 import call, STDOUT
from instaladorapt import instalador
import os

def instalaGit(nombre_instancia):
    """
    Función de instalación de git y de clonación del repo. 
    """

    print("""           Instalando GIT...
            ----------------------------------------""")

    instalador('git')
    

    # Una vez instalado, comprobamos si odoo ha sido instalado ya.
    print("""           Clonando repo...
            ----------------------------------------""")

    # Añadido punto al final para que no se produzca lo de /odoo/odoo
    if not os.path.exists('/opt/odoo/addons'):
        os.makedirs('/opt/odoo')

    call([  "git",
            "clone",
            "https://www.github.com/odoo/odoo",
            "--depth",
            "1",
            "--branch",
            "8.0",
            "--single-branch",
            "/opt/odoo"])

    call(['chown', '-R', nombre_instancia+':odoo', "/opt/odoo"])