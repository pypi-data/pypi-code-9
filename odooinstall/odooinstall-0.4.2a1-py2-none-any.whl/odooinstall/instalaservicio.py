#-*- coding: utf-8 -*-

from subprocess32 import call, STDOUT

def scriptInicio(nombre_instancia):
    """
    Instala y configura el script de inicio
    """

    # Se descarga el script
    call(["git",
        "clone",
        "https://MrEvil@bitbucket.org/snippets/bisnesmart/7RAK/odoo-server.git",
        "/opt/"+nombre_instancia+"/scriptinicio"])
    # Se copia a la carpeta de scripts de inicio
    call(["cp",
        "/opt/"+nombre_instancia+"/scriptinicio/odoo-server",
        "/etc/init.d/"+nombre_instancia+"-server"]
        )
    # Se cambian los permisos
    call(["chmod",
        "755",
        "/etc/init.d/"+nombre_instancia+"-server"], 
        stderr=log_file)
    # Se cambia el propietario y grupo a root
    call(["chown",
        "root:",
        "/etc/init.d/"+nombre_instancia+"-server"], stderr=log_file)
    # Se activan los scripts
    call(["update-rc.d",
            nombre_instancia+"-server",
            "defaults"])
    call(["update-rc.d",
        nombre_instancia+"-server",
        "enable"])
    

if __name__ == '__main__':
    scriptInicio(STDOUT)

