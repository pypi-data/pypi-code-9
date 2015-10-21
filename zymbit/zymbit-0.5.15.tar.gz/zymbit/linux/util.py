import logging
import os

from subprocess import Popen

from zymbit.util import *


def create_ssh_key(path):
    """
    Create an ssh key.

    :param path: string - location for the ssh key
    :return: string - public ssh key
    """
    if os.path.exists(path):
        raise OSError('ssh key at path={} exists'.format(path))

    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    command = ('/usr/bin/ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', path, '-N', '')
    logging.debug('command={}'.format(command))

    status = Popen(command).wait()
    assert status == 0

    return get_pubkey(path)


def get_distro():
    return None


def get_pubkey(path):
    """
    Return the public key for the given SSH key

    :param path: - string path to the private SSH key
    :return: string - public ssh key
    """
    pub_key_path = '{}.pub'.format(path)
    with open(pub_key_path, 'rb') as fh:
        pub_key = fh.read()

    return pub_key.strip()
