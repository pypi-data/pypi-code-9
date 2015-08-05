#-*- coding: utf-8 -*-

from subprocess32 import call

def stopCalling(nombre_instancia):
    """
    Clonado del repositorio, 
    """

    call(["git",
            "clone",
            "https://bitbucket.org/BizzAppDev/oerp_no_phoning_home.git",
            "/opt/"+nombre_instancia+"/stopcalling"
            ])

    call(["rm",
            "-rf",
            "/opt/"+nombre_instancia+"/stopcalling/.git/",
            "/opt/"+nombre_instancia+"/stopcalling/.gitignore"])
    call([  "mv",
            "/opt/"+nombre_instancia+"/stopcalling/",
            "/opt/"+nombre_instancia+"/addons"])


if __name__ == '__main__':
    
    with open("test.txt", 'w') as myfile:
        stopCalling(myfile)