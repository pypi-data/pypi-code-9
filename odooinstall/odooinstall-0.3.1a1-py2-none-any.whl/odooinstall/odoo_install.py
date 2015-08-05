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

# Para manejar cuentas de usuario y grupos:
import pwd, grp
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

from instaladorapt import instalador

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



def instalaSsh():
    """
    Instala el servidor ssh, que normalmente ya existirá.
     
    """
    # Instalación del servidor ssh
    ##############################
    print ("""
        Instalando ssh...
        -----------------
        """)
    # Instalar y guardar errores en el archivo que hemos creado. 
    instalador('openssh-server')
    # call(['apt-get', 'install', '-y', 'openssh-server'], stderr=log_file)


def updates():
    """
    Simplemente utiliza el gestor de paquetes para actualizar los que sean necesarios.
    """
    print ("""
        Actualizando paquetes e instalando dependencias... Esto puede tardar un rato.
    -----------------------------------------------------------------------------------
    """)

    call(['apt-get', 'update', '-y'])


def usuario(nombre_instancia):
    """
    Crea el usuario odoo y le otorga los permisos y grupo pertinentes. 

    """

    print ("""
            Creando usuario %s 
    ----------------------------------------
    """, % nombre_instancia)

    try:
        pwd.getpwnam(nombre_instancia)

    except KeyError:
        # El usuario no existe, es el caso que esperamos, lo creamos y lo añadimos al grupo odoo
        print('Nombre válido...')
        call([
            'adduser', 
            '--system', 
            '--home=/opt/'+nombre_instancia, 
            '--group', 
            nombre_instancia
            ])
        # Dando propiedad al usuario odoo de su directorio de logs. Se cambia el grupo a root.
        # TODO: 
        #   
        # call(['chown', '-R', 'odoo:root', path])
        # endoTODO.

        # Se añade el usuario al grupo odoo
        call(['useradd', '-G', 'odoo', nombre_instancia])

    

def configuracion(nombre_instancia, pass_del_rol_postgres):
    """
    Cambios necesarios para nuestra configuración personalizada. 
    """
    
    print("""
        Personalizando la configuración
    ----------------------------------------
    """)
    # Se copia el archivo de configuración del servidor original a una ubicación nueva
    # Se guarda con el nombre de la instancia -server.conf
    call(["cp",
        "/opt/odoo/debian/openerp-server.conf",
        "/etc/"+nombre_instancia+"-server.conf"])
    # Cambio de propietario del archivo de configuración
    call([  "chown",
            nombre_instancia+":",
            "/etc/"+nombre_instancia+"-server.conf" ])
    

    # Cambia el acceso por defecto a la base de datos de postgres
    replace.replace(
            "/etc/"+nombre_instancia+"-server.conf", 
            "db_password = False", 
            "db_password = "+pass_del_rol_postgres
            )
        # Sustituye a:
        #sudo su - odoo -s /bin/bash -c 'sed "s#db_password = False#db_password = $passpsql_#" /etc/odoo-server.conf > /opt/odoo/temp.txt' 

    # Cambia el directorio de addons que usaremos por uno en el home del usuario creado
    replace.replace(
            "/etc/"+nombre_instancia+"-server.conf", 
            "/usr/lib/python2.7/dist-packages/openerp/addons", 
            "/opt/"+nombre_instancia+"/addons"
            )
        # Sustituye a:
        #   sudo su - odoo -s /bin/bash -c 'sed "s_/usr/lib/python2.7/dist-packages/openerp/addons_/opt/odoo/addons_" /etc/odoo-server.conf > /opt/odoo/temp.txt' 2> /var/log/odoo/instalacion.log
    
    
    # Cambio de permisos del archivo (el propietario ya se modifica en replace())
    call([  "chmod", 
            "640",
            "/etc/"+nombre_instancia+"-server.conf"
            ])

    #modifico el archivo de configuracion


    #sudo su - odoo -s /bin/bash -c 'sed "s#/usr/lib/python2.7/dist-packages/openerp/addons#/opt/odoo/addons"' /etc/odoo-server.conf
    # 
    replace.appendLine(
        "/etc/"+nombre_instancia+"-server.conf", 
        "logfile = /var/log/odoo/"+nombre_instancia+"server.log")

# TODO: 
#   Falta lo siguiente:
#       
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
    nombre_valido=False

    while not valida:
        pass_del_rol_postgres = getpass("Introduce la contraseña del rol para odoo: ")
        confirmacion = getpass("Repite la contraseña: ")

        if pass_del_rol_postgres == confirmacion: 
            valida = True
        else:
            print ("Las contraseñas no coinciden.\n ")
    while not nombre_valido:
        nombre_instancia = input("Introduce (entre comillas) el nombre de la instancia: ")
        if nombre_instancia == 'odoo' :
            print("El nombre %s no es válido o ya está siendo usado \n Por favor, introduce otro.", % nombre_instancia)

    # Instala el servidor ssh
    instalaSsh()

    # Actualiza paquetes
    updates()

    # Crea usuario odoo
    usuario(nombre_instancia)

    # Instalar postgresql
    postgres.instalaPostgres()

    # Crea el rol de odoo
    #crearRol(name='postgres',password=pass_del_rol_postgres)

    postgres.crearRol2(nombre_instancia, pass_del_rol_postgres)

    # Instala dependencias python
    dependencias.dependenciasPython()

    # Instala git y clona el repo:
    instalagit.instalaGit(nombre_instancia)

    # Cambia la configuración:
    configuracion(nombre_instancia, pass_del_rol_postgres)

    # Instala y configura el script de inicio automático
    instalaservicio.scriptInicio(nombre_instancia)


    # Module stop calling home:
    stopcalling.stopCalling(nombre_instancia)

    # Configuramos nginx
    dominio = input("Introduce el nombre del dominio de la instancia (entre comillas): ")
    configuranginx.nginx(nombre_instancia,dominio)


    # Lanzamos el server:
    call(["/etc/init.d/"+nombre_instancia+"-server", "start"])

    print("Este es el final del script.")

if __name__ == '__main__':
    main()