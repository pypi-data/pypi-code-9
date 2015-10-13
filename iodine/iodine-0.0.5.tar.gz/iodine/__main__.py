#!/usr/bin/env python
"""Iodine - A salt api client using IPython shell

Usage:
    iodine [options] [<user@hostname:port>]

Options:

    -n --noupdatecheck    Dont check for updates

"""
from __future__ import print_function
import os
from getpass import getpass, getuser
import logging
from docopt import docopt
import iodine.magic
import iodine.update

# http://stackoverflow.com/questions/954834/how-do-i-use-raw-input-in-python-3-1
# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass


def get_salt_magic(ipshell, username=None, master=None, password=None,
                   port=8001, no_cache=False):
    default_user = getuser()
    default_master = 'localhost'
    master = master or input("Master (%s):" % default_master)
    username = username or input("Username (%s):" % default_user)
    return iodine.magic.SaltMagics(
        ipshell,
        username=username or default_user,
        password=(password or getpass('Password: ')),
        master=master or default_master,
        port=int(port) if port else 8001,
        no_cache=no_cache,
    )


def main():
    args = docopt(__doc__)
    if not args.get('--noupdatecheck'):
        iodine.update.update()
    uri = args['<user@hostname:port>']
    user, host, port = None, None, None
    if uri:
        if '@' in uri:
            user, host = uri.split('@')
        else:
            host = uri
        if ':' in host:
            host, port = host.split(':')
    # http://ipython.org/ipython-doc/dev/interactive/reference.html#defining-your-own-magics
    logging.basicConfig(filename='iodine.log', level=logging.DEBUG)
    from IPython.terminal.embed import InteractiveShellEmbed
    ipshell = InteractiveShellEmbed()
    magics = get_salt_magic(ipshell, username=user, master=host, port=port)
    ipshell.register_magics(magics)
    ipshell.set_hook('complete_command', magics._salt_completer, str_key='%salt')
    ipshell()
    magics.client.logout()

if __name__ == '__main__':
    main()
