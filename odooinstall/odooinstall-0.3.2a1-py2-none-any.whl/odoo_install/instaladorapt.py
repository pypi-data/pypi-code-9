#-*- coding: utf-8 -*-

#!/usr/bin/env python
# aptinstall.py

import apt
import sys

def instalador(paquetes_a_instalar):
    """
    Instala paquetes usando apt-get.
    Se necesitarán los permisos pertinentes, claro. 
    @paquetes
        Lista de cadenas con los nombres de los paquetes
        a instalar.
    """
    if type(paquetes_a_instalar) is str:
        paquetes = []
        paquetes.append(paquetes_a_instalar)
    elif type(paquetes_a_instalar) is list:
        paquetes = paquetes_a_instalar
    else:
        print "El argumento debe ser una cadena o lista de cadenas."


    cache = apt.cache.Cache()
    cache.update()
    for nombre_del_paquete in paquetes:
        print """
            Instalando {nombre_del_paquete}
        ----------------------------------------""".format(nombre_del_paquete=nombre_del_paquete)
        pkg = cache[nombre_del_paquete]
        if pkg.is_installed:
            print "{nombre_del_paquete} ya está instalado".format(nombre_del_paquete=nombre_del_paquete)
        else:
            pkg.mark_install()

            try:
                cache.commit()
            except Exception, arg:
                print >> sys.stderr, "Vaya, no se ha podido instalar el paquete. [{err}]".format(err=str(arg))