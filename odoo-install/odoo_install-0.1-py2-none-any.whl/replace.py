#-*- coding: utf-8 -*-


# Reemplaza líneas en un archivo de texto.
# Test OK.

from tempfile import mkstemp
from shutil import move
from os import remove, close, stat
from grp import getgrgid
from pwd import getpwuid
from subprocess32 import call, STDOUT

def getOwnership(file_path):
    """
    Returns a file's user id and group id.
    file_path is a string containing the full path of the file.
    """
    uid = stat(file_path).st_uid
    gid = stat(file_path).st_gid
    return uid, gid

def changeOwnership(file_path, uid, gid):
    """
    Changes owner and group of a file
    """
    call(['chown', '-R', str(uid)+':'+str(gid), file_path], stderr=STDOUT)

def replace(file_path, pattern, subst):
    """
    Replaces every instance of pattern with subst in the file file_path.
    """
    # Save the owner and group of the file before we probably overwrite them.
    uid, gid = getOwnership(file_path)
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

    changeOwnership(file_path, uid, gid)


def appendLine(file_path, line):
    """
    Adds a line at the end of the file.
    If used from command line, the new line character \\n is ignored (needs parsing) 
    """

    with open(file_path, 'a') as myfile:
        myfile.write('\n')
        myfile.write(line)

    # No hace falta cerrar el archivo porque usando el with ya se cierra. 




if __name__ == "__main__":
    # Si el módulo se ejecuta como un script, tomamos los argumentos de la línea de comandos.
    import sys
    replace(sys.argv[1],sys.argv[2],sys.argv[3])
    appendLine(sys.argv[1], sys.argv[4])
    