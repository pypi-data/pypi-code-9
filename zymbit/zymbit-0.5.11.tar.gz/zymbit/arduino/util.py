from subprocess import PIPE, Popen

from zymbit.util import *


def create_ssh_key(identity_file):
    dirname = os.path.dirname(identity_file)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    command = ('/usr/bin/dropbearkey', '-t', 'rsa', '-s', '2048', '-f', identity_file)
    return run_command(command)


def get_distro():
    if os.path.exists('/etc/linino'):
        return 'linino'


def get_pubkey(identity_file):
    command = ('/usr/bin/dropbearkey', '-y', '-f', identity_file)
    proc = Popen(command, stdout=PIPE)
    output = proc.communicate()[0]

    for line in output.splitlines():
        if line.startswith('ssh-rsa'):
            return line
