from fabric.api import (run, local, env, cd, task, sudo, execute, get, settings,
    put, with_settings)
from fabric.contrib import project
from weaver.utils import _
from os import path

@task
def rsync(remote_dir, **kwargs):
    #local_dir=None, exclude=(), delete=False,
    #extra_opts='', ssh_opts='', capture=False):
    remote_dir_tmp = "/tmp"
    project.rsync_project(remote_dir_tmp, **kwargs)
    local_dir = kwargs.get('local_dir')
    head, tail = path.split(local_dir)
    if head:
        src = path.join(remote_dir_tmp, head)
    else:
        src = path.join(remote_dir_tmp, tail)

    dst = remote_dir
    cmd = _("mv {src} {dst}")
    sudo(cmd)

@task
def ssh(ip=None):
    """
    Ssh into service
    """
    #FIXME: handle list of keys
    #FIXME: handle multiple hosts
    key = env.key_filename
    user = env.user
    host = env.host
    if ip:
        host = ip
    local(_("""ssh -i {key} {user}@{host}""",
        flags=["oneline"]))

@task
def scp(_local, remote, to_remote='True',extra=""):
    remote = env.user + '@' + env.host + ":" + remote
    if to_remote == 'True':
        src, dst  = _local, remote
    else:
        src, dst = remote, _local
    key = env.key_filenam
    local(_("""scp -i {key} {extra} {src} {dst}"""))
