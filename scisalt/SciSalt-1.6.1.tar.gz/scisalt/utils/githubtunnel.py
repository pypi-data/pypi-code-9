#!/usr/bin/env python3

import os as _os
import argparse as _argparse
import shlex
from subprocess import call

__all__ = ['githubtunnel']


def githubtunnel(user1, server1, user2, server2, port, verbose, stanford=False):
    """
    Opens a nested tunnel, first to *user1*@*server1*, then to *user2*@*server2*, for accessing on *port*.

    If *verbose* is true, prints various ssh commands.

    If *stanford* is true, shifts ports up by 1.

    Attempts to get *user1*, *user2* from environment variable ``USER_NAME`` if called from the command line.
    """
    if stanford:
        port_shift = 1
    else:
        port_shift = 0

    # command1 = 'ssh -nNf -L {}:quickpicmac3.slac.stanford.edu:22 {}@{}'.format(port, user, server)
    command1 = 'ssh -nNf -L {}:{}:22 {}@{}'.format(port-1-port_shift, server2, user1, server1)
    command2 = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -nNf -L {}:cardinal.stanford.edu:22 -p {} {}@localhost'.format(port-port_shift, port-port_shift-1, user2)
    command3 = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -nNf -L {}:github.com:22 -p {} {}@localhost'.format(port, port-1, user2)
    if verbose:
        print(command1)
        if stanford:
            print(command2)
        print(command3)
    try:
        call(shlex.split(command1))
        if stanford:
            call(shlex.split(command2))
        call(shlex.split(command3))
    except:
        print('Failure!')
        pass


# ================================
# Get info one way or another
# ================================
def environvar(prompt, val):
    if val is None:
        val = input(prompt + ' ')

    return val


def _script():
    # ================================
    # Access command line arguments
    # ================================
    parser = _argparse.ArgumentParser(description=
            'Creates a tunnel primarily for Git.')
    parser.add_argument('-V', action='version', version='%(prog)s v0.1')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose mode.')
    parser.add_argument('-p', '--port', default=7777, type=int,
            help='Local port to listen on.')
    parser.add_argument('-s1', '--server1', default='mcclogin',
            help='First server hop.')
    parser.add_argument('-s2', '--server2', default='iris.slac.stanford.edu',
            help='Second server hop.')
    parser.add_argument('-su', '--stanford', action='store_true',
            help='Tunnel through Stanford')
    parser.add_argument('-u1', '--user1', default=_os.environ.get('PHYSICS_USER'),
            help='User name to use for login.')
    parser.add_argument('-u2', '--user2', default=_os.environ.get('PHYSICS_USER'),
            help='User name to use for login.')

    arg = parser.parse_args()

    # ================================
    # Ask user for logins if needed
    # ================================
    prompt1 = 'User name for server {}?'.format(arg.server1)
    prompt2 = 'User name for server {}?'.format(arg.server2)
    user1 = environvar(prompt1, arg.user1)
    user2 = environvar(prompt2, arg.user2)

    # ================================
    # Run with command line arguments
    # ================================
    githubtunnel(user1, arg.server1, user2, arg.server2, arg.port, arg.verbose, stanford=arg.stanford)

if __name__ == '__main__':
    _script()
