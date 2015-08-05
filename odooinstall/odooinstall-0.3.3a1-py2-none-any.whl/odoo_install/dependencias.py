#-*- coding: utf-8 -*-
# Instala las dependencias para odoo
# Test OK.

# Esta dependencia está en el setup
from subprocess32 import call, STDOUT

from instaladorapt import instalador


from platform import uname

def dependenciasPython(log_file):
    """
    Instala depencencias necesarias para odoo
    """
    
    #*****************************wkhtmltopdf*****************************************
    # wkhtmltopdf tiene una version muy vieja en los repos

    print("""Instalando la librería wkhtmltopdf para generar pdfs
            ----------------------------------------------------""")

    # Dependencias necesarias para que se pueda instalar el paquete wkhtmltopdf
    # Se añade el -y
    dependencias_wk = [
                "xfonts-utils", 
                "xfonts-base",
                "xfonts-75dpi"
                ]
    instalador(dependencias_wk)

    (system, node, release, version, machine, processor) = uname()

    # La versión 0.12.1 va bien pero la 12.2 no, nos sale la línea superior dichosa
    if '64' in machine:
        ######### Arquitectura de 64 bits Instala paquetes para ésta. #########
        call(["wget",
            "http://download.gna.org/wkhtmltopdf/0.12/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb"
            ], 
            stderr=log_file) 
        call(["dpkg",
                "-i",
                "download"], 
                stderr=log_file) 
    else:
        ######### Arquitectura de 32 bits #########
        call(["wget",
              "http://download.gna.org/wkhtmltopdf/0.12/0.12.1/wkhtmltox-0.12.1_linux-trusty-i386.deb"
              ],
              stderr=log_file)
        # Para este enlace (el de 32 bits) la descarga se guarda como wkhtmltox-0.12.2.1_linux-trusty-i386.deb
        call(["dpkg",
             "-i",
             "wkhtmltox-0.12.2.1_linux-trusty-i386.deb"],
             stderr=log_file)

    # Mover archivos a la ubicación correcta del sistema
    # Esto dio algún error, verificar que ya no sucede, podía ser por permisos.
    call(["cp", "/usr/local/bin/wkhtmltopdf", "/usr/bin"], stderr=log_file)
    call(["cp", "/usr/local/bin/wkhtmltoimage", "/usr/bin"], stderr=log_file)

if __name__ == '__main__':
    dependenciasPython(STDOUT)