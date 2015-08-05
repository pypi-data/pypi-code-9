#-*- coding: utf-8 -*-

from subprocess32 import call, STDOUT
from instaladorapt import instalador
def nginx(dominio, log_file=STDOUT):
    """
    Instala nginx y configura para nuestra disposición de odoo.
    El dominio es mediante el cuál se accederá al servicio odoo. 
    """
    # Instala nginx
    instalador(['nginx'])
    # Borra la configuración por defecto:
    call(["rm",
            "/etc/nginx/sites-enabled/default"],
            stderr=log_file)


    # Se descarga el archivo de configuración
    call(["git",
        "clone",
        "https://MrEvil@bitbucket.org/snippets/bisnesmart/yRA4/configuranginx.git",
        "/opt/odoo/nginx"], 
        stderr=log_file)

    # Se hacen las modificaciones necesarias para nuestro caso

    # Se mueve el archivo a /etc/nginx/conf.d/odoo.conf
    
if __name__ == '__main__':
    nginx()