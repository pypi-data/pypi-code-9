#-*- coding: utf-8 -*-

from subprocess32 import call, STDOUT
from instaladorapt import instalador
from replace import replace
import os

def nginx(nombre_instancia,dominio):
    """
    Instala nginx y configura para nuestra disposición de odoo.
    El dominio es mediante el cuál se accederá al servicio odoo. 
    """

    # Instala nginx
    instalador(['nginx'])
    # Borra la configuración por defecto:
    try:
        os.remove("/etc/nginx/sites-enabled/default")
    except OSError:
        pass
    # call(["rm","/etc/nginx/sites-enabled/default"])


    # Se descarga el archivo de configuración
    call(["git",
        "clone",
        "https://MrEvil@bitbucket.org/snippets/bisnesmart/yRA4/configuranginx.git",
        "/opt/"+nombre_instancia+"/nginx"])

    # Se hacen las modificaciones necesarias para nuestro caso
    replace("/opt/"+nombre_instancia+"/nginx","yourhostname.com",dominio)


    # Se mueve el archivo a /etc/nginx/conf.d/odoo.conf
    os.rename("/opt/"+nombre_instancia+"/nginx/odoo.conf","/etc/nginx/conf.d/"+nombre_instancia+".conf")
    # Se reinicia el servicio de nginx
    call(["service","nginx","restart"])


    
if __name__ == '__main__':
    nginx()