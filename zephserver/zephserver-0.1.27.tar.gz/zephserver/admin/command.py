# -*- coding: utf-8 -*-
'''
Copyright 2015 
    Centre de données socio-politiques (CDSP)
    Fondation nationale des sciences politiques (FNSP)
    Centre national de la recherche scientifique (CNRS)
License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''


import sys
import socket

def main(argv, target=None):
    if target is None:
        from zephserversettings import CONFIGURATION_NETWORK_INTERFACE
        target = CONFIGURATION_NETWORK_INTERFACE

    command_asked = argv[0]
    try:
        command_to_serv = argv[1:]
        command_to_serv_string = command_asked
        for string in command_to_serv:
            command_to_serv_string += ' ' + string
    except:
        command_to_serv_string = command_asked

    if is_unix_addr(target):
        s = socket.socket(socket.AF_UNIX)
        s.connect(target)
    else:
        addr, port = target.split(':')
        s = socket.socket(socket.AF_INET)
        s.connect((addr, int(port)))
    if command_to_serv != None:
        s.sendall(command_to_serv_string)
    else :
        s.sendall(command_to_serv_string)
    ready = True
    while(ready):
        data = s.recv(1024)
        
        if  data != None and data != '':#signal de fin de communication
            lines = str(data).split('\n')
            for line in lines:
                if '#!#end_communication#!#' == line:
                    ready = False
                    break
                else:
                    print(line)
    s.close()


def stop():
    main(['stop'])

def command(args):
    to_remove = None
    target = None
    for arg in args:
        if arg.startswith('--interface='):
            target=arg[len('--interface='):]
            to_remove = arg
    if not to_remove is None:
        args.remove(to_remove)

    if not target is None:
        main(args, target=target)
    else:
        main(args)


def is_unix_addr(addr):
    # TODO better adress type detection
    if ':' in addr: 
        return False
    else:
        return True



if __name__ == '__main__':
    main(sys.argv[1:])
