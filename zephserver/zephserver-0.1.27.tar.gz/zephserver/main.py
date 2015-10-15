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



from zephserver.infra.bootstrap import Bootstrap
from zephserver.admin.command import stop, command


def main():
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0].lower() == 'start':
            bootstrap = Bootstrap(args[1:])
            sys.exit(bootstrap.start_server())
        if args[0].lower() == 'stop':
            stop()
        else:
            command(args)