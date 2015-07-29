#-*- coding: utf-8 -*-

# TODO:
#   Crear un script que bloquee el proceso antes de la instalación, de lo contrario no se podrán importar los módulos necesarios. 
#para evitar tener que instalar paquetes desde el script, se incorporan los módulos necesarios
# pero parece que con subprocess32 hay más de un problema. 
# Intentando resolverlo con 

# sudo apt-get install python-dev
# wget https://bootstrap.pypa.io/get-pip.py
# sudo python get-pip.py 
# sudo pip install subprocess32

# Y todo funciona OK.

# Ejecutar como root
# 

# TODO: Separar cada apartado en un módulo distinto para poder hacer tests y evaluar funcionalidades por separado. 

import os


# Para ejecutar comandos del shell, Popen es más completo y será necesario para hacer PIPEs
from subprocess32 import call, PIPE, Popen

# Para poder ejecutar comandos con otro usuario (postgres)
from pwd import getpwnam
# Para poder interactuar con el prompt de la contraseña del rol de postgres
# import pexpect # Dejamos de usarlo, es un módulo no oficial
# Para introducir contraseñas sin que se muestren 
from getpass import getpass
# Para hacer modificaciones en archivos de configuración
import fileinput
# Instalar postgres y tal
import postgres
# Script para configurar los logs
import loggeador
# Script propio para reemplazar líneas en archivos (ojo, los permisos del nuevo fichero habrán cambiado)
import replace
# Script para la configuración del script de inicio
import instalaservicio
# Descarga y reubicación del addon de desconexión de odoo (se requiere instalación)
import stopcalling
# Instalación de las dependencias
import dependencias

import instalagit

def title():
    """
    Muestra la cabecera del programa.
    """
    print ("""
            ###########################################
            # Instalador para odoo 8 en maquina nueva #
            #        Instalador By GoNxI  v2.0        #
            #                   bisnesmart.com        #
            ###########################################

        """)



def instalaSsh(log_file):
    """
    Instala el servidor ssh, que normalmente ya existirá.
    TODO: verificar que o se ha instalado bien o que ya existía con un try o algo. 
    """
    # Instalación del servidor ssh
    ##############################
    print ("""
        Instalando ssh...
        -----------------
        """)
    # Instalar y guardar errores en el archivo que hemos creado. 
    call(['apt-get', 'install', '-y', 'openssh-server'], stderr=log_file)


def updates(log_file):
    """
    Simplemente utiliza el gestor de paquetes para actualizar los que sean necesarios.
    """
    print ("""Actualizando paquetes e instalando dependencias... Esto puede tardar un rato.
             -----------------------------------------------------------------------------""")

    call(['apt-get', 'update', '-y'], stderr=log_file)


def usuario(path, log_file):
    """
    Crea el usuario odoo y le otorga los permisos y grupo pertinentes. 
    """

    print ("""         Creando usuario odoo
              ----------------------------------------""")

    call(['adduser', '--system', '--home=/opt/odoo', '--group', 'odoo'], stderr=log_file)
    # Dando propiedad al usuario odoo de su directorio de logs. Se cambia el grupo a root.
    # El archivo log_files que usaremos habitualmente es el mismo que queremos cambiar, así que
    #   aquí puede haber una paradoja rara si algo falla.
    # TODO: 
    #   cambiar a un check_call para hacer manejo de excepciones. 
    call(['chown', '-R', 'odoo:root', path], stderr=log_file)
    # endoTODO.



def configuracion(log_file, pass_del_rol_postgres):
    """
    Cambios necesarios para nuestra configuración personalizada. 
    """
    
    print("""Personalizando la configuración
        ----------------------------------------""")
    # Se copia el archivo de configuración del servidor original a una ubicación nueva
    call(["cp",
        "/opt/odoo/debian/openerp-server.conf",
        "/etc/odoo-server.conf"], stderr=log_file )
    # Cambio de propietario del archivo de configuración
    call([  "chown",
            "odoo:",
            "/etc/odoo-server.conf" ], 
            stderr=log_file)
    

    # Cambia el acceso por defecto a la base de datos de postgres
    replace.replace("/etc/odoo-server.conf", "db_password = False", "db_password = "+pass_del_rol_postgres)
        # Sustituye a:
        #sudo su - odoo -s /bin/bash -c 'sed "s#db_password = False#db_password = $passpsql_#" /etc/odoo-server.conf > /opt/odoo/temp.txt' 

    # Cambia el directorio de addons que usaremos por uno en el home del usuario odoo
    replace.replace("/etc/odoo-server.conf", "/usr/lib/python2.7/dist-packages/openerp/addons", "/opt/odoo/addons")
        # Sustituye a:
        #   sudo su - odoo -s /bin/bash -c 'sed "s_/usr/lib/python2.7/dist-packages/openerp/addons_/opt/odoo/addons_" /etc/odoo-server.conf > /opt/odoo/temp.txt' 2> /var/log/odoo/instalacion.log
    
    
    # Cambio de permisos del archivo (el propietario ya se modifica en replace())
    call([  "chmod", 
            "640",
            "/etc/odoo-server.conf"  ],
            stderr=log_file)

    #modifico el archivo de configuracion


    #sudo su - odoo -s /bin/bash -c 'sed "s#/usr/lib/python2.7/dist-packages/openerp/addons#/opt/odoo/addons"' /etc/odoo-server.conf
    # 
    replace.appendLine("/etc/odoo-server.conf", "logfile = /var/log/odoo/odoo-server.log")

# TODO: 
#   Falta lo siguiente:
#       - Que se verifique si los paquetes ya están instalados para no volver a intentarlo
#       - Que se verifique si los archivos que se descargan están ya descargados o no para no volver a intentarlo
#       - Servidor nginx y reverse proxy
#       
#       - Mostrar pasos siguientes a seguir:
#           - Instalar módulo stop calling home en locales.
#       - Revisar lo que haya en project.  

def main():
    # Muestra la cabecera.
    title()

    # Contraseña para el rol de postgres
    valida = False

    while not valida:
        pass_del_rol_postgres = getpass("Introduce la contraseña del rol para odoo: ")
        confirmacion = getpass("Repite la contraseña: ")

        if pass_del_rol_postgres == confirmacion: 
            valida = True
        else:
            print ("Las contraseñas no coinciden.\n ")

    # Creación del archivo de logs, nos devuelve la ruta y el objeto file
    path, archivo = logging.logSettings()

    # Instala el servidor ssh
    instalaSsh(archivo)

    # Actualiza paquetes
    updates(archivo)

    # Crea usuario odoo
    usuario(path, archivo)

    # Instalar postgresql
    postgres.instalaPostgres(archivo)

    # Crea el rol de odoo
    #crearRol(name='postgres',password=pass_del_rol_postgres)

    postgres.crearRol2(pass_del_rol_postgres)

    # Instala dependencias python
    dependencias.dependenciasPython(archivo)

    # Instala git y clona el repo:
    instalagit.instalaGit(archivo)

    # Cambia la configuración:
    configuracion(archivo, pass_del_rol_postgres)

    # Instala y configura el script de inicio automático
    instalaservicio.scriptInicio(archivo)


    # Module stop calling home:
    stopcalling.stopCalling(archivo)




    # Cerramos el archivo de logs para finalizar:
    archivo.close()

    # Lanzamos el server:
    call(["/etc/init.d/odoo-server", "start"])

    print("Este es el final del script.")

if __name__ == '__main__':
    main()