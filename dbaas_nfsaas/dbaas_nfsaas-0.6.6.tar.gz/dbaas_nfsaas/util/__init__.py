# -*- coding: utf-8 -*-
import logging
import paramiko
import socket
from dbaas_cloudstack.models import HostAttr as CsHostAttr

LOG = logging.getLogger(__name__)


def exec_remote_command(server, username, password, command, output={}):

    try:
        LOG.info(
            "Executing command [%s] on remote server %s" % (command, server))
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        log_stdout = stdout.readlines()
        log_stderr = stderr.readlines()
        exit_status = stdout.channel.recv_exit_status()
        LOG.info("Comand return code: %s, stdout: %s, stderr %s" %
                 (exit_status, log_stdout, log_stderr))
        output['stdout'] = log_stdout
        output['stderr'] = log_stderr
        return exit_status
    except (paramiko.ssh_exception.BadHostKeyException,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.SSHException,
            socket.error) as e:
        LOG.warning("We caught an exception: %s ." % (e))
        output['exception'] = str(e)
        return None


def clean_unused_data(export_id, export_path, host, databaseinfra, provider):
    provider.grant_access(environment=databaseinfra.environment,
                          host=host,
                          export_id=export_id)

    mount_path = "/mnt_{}_{}".format(databaseinfra.name, export_id)
    command = "mkdir -p {}".format(mount_path)
    command += "\nmount -t nfs -o bg,intr {} {}".format(
        export_path, mount_path)
    command += "\nrm -rf {}/*".format(mount_path)
    command += "\numount {}".format(mount_path)
    command += "\nrm -rf {}".format(mount_path)
    LOG.info(command)

    cs_host_attr = CsHostAttr.objects.get(host=host)

    output = {}
    exec_remote_command(server=host.address,
                        username=cs_host_attr.vm_user,
                        password=cs_host_attr.vm_password,
                        command=command,
                        output=output)

    LOG.info(output)
