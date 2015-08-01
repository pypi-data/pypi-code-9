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
# Access environment variables
# ================================
def checkvar(envvar):
    try:
        value = _os.environ[envvar]
    except:
        value = None
    # print(value)
    return value


# Email variable class
class emailprefs(object):
    """Preferences for email notification."""
    def __init__(self, requested=False, environvar=None, value=None):
        self.requested = requested
        self.environvar = environvar
        if value is None:
            self.value = checkvar(environvar)
        else:
            self.value = value
        if self.value is None:
            self.value = _os.environ['PHYSICS_USER']
            print('Using current fphysics login: ' + self.value)

        # raise ValueError('problem')


# Adds action to load email from $NOTIFY_EMAIL if possible
class note_address(_argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print getattr(namespace, self.dest).environvar
        # print values
        if values is None:
            out = emailprefs(True, getattr(namespace, self.dest).environvar)
        else:
            out = emailprefs(True, getattr(namespace, self.dest).environvar, values)
        setattr(namespace, self.dest, out)


if __name__ == '__main__':
    parser = _argparse.ArgumentParser(description=
            'Creates a tunnel primarily for Git.')
    parser.add_argument('-V', action='version', version='%(prog)s v0.1')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose mode.')
    parser.add_argument('-p', '--port', default=7777, type=int,
            help='Local port to listen on.')
    parser.add_argument('-u1', '--user1', default=emailprefs(True, 'USER_NAME'), action=note_address,
            help='User name to use for login.')
    parser.add_argument('-s1', '--server1', default='mcclogin',
            help='First server hop.')
    parser.add_argument('-u2', '--user2', default=emailprefs(True, 'USER_NAME'), action=note_address,
            help='User name to use for login.')
    parser.add_argument('-s2', '--server2', default='iris.slac.stanford.edu',
            help='Second server hop.')
    parser.add_argument('-su', '--stanford', action='store_true',
            help='Tunnel through Stanford')

    arg = parser.parse_args()

    githubtunnel(arg.user1.value, arg.server1, arg.user2.value, arg.server2, arg.port, arg.verbose, stanford=arg.stanford)
