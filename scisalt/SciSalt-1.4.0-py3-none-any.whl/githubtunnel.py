#!/usr/bin/env python3

import argparse
import shlex
import pytools.classes as mtcl
from subprocess import call


def githubtunnel(user1, server1, user2, server2, port, verbose, stanford=False):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
            'Creates a tunnel primarily for Git.')
    parser.add_argument('-V', action='version', version='%(prog)s v0.1')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose mode.')
    parser.add_argument('-p', '--port', default=7777, type=int,
            help='Local port to listen on.')
    parser.add_argument('-u1', '--user1', default=mtcl.emailprefs(True, 'USER_NAME'), action=mtcl.note_address,
            help='User name to use for login.')
    parser.add_argument('-s1', '--server1', default='mcclogin',
            help='First server hop.')
    parser.add_argument('-u2', '--user2', default=mtcl.emailprefs(True, 'USER_NAME'), action=mtcl.note_address,
            help='User name to use for login.')
    parser.add_argument('-s2', '--server2', default='iris.slac.stanford.edu',
            help='Second server hop.')
    parser.add_argument('-su', '--stanford', action='store_true',
            help='Tunnel through Stanford')

    arg = parser.parse_args()

    githubtunnel(arg.user1.value, arg.server1, arg.user2.value, arg.server2, arg.port, arg.verbose, stanford=arg.stanford)
