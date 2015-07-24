# -*-coding:utf-8-*-

__all__ = ["Shell"]

import os
import subprocess


class Shell(object):
    """
    Execute a shell script on local or remote.
    """

    def __init__(self, remote_user_host, execute_dir):
        self.remote_user_host = remote_user_host
        self.execute_dir = execute_dir

    def local(self, cmd, wrap=None, return_output=False):
        # TODO replace with subprocess
        if wrap:
            cmd = wrap(cmd)
        print "[command]", cmd
        if return_output:
            return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        else:
            return os.system(cmd)

    def remote(self, cmd):
        return self.local(cmd, wrap=self.wrap_remote_python_env)

    def wrap_remote_python_env(self, cmd):
        # TODO support zsh profile
        return """ssh %s "source ~/.bash_profile
                  cd %s
                  if [ -f ENV/bin/activate ];
                      then source ENV/bin/activate
                  fi;
                  %s"
                """ % (self.remote_user_host,
                       self.execute_dir,
                       cmd,)
