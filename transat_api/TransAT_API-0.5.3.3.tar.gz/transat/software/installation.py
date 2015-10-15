"""
Configure how software programs run on the different computing resources

"""
import subprocess as sp
import os
import logging

logger = logging.getLogger(__name__)


class Installation(object):
    """

    """

    def __init__(self, software, worker, env=None):
        """

        :return:
        """
        self.software = software
        self.worker = worker

        if env is None:
            env = {}
        self.env = env
        self.commands = {action: self.worker.run_cmd for action in software.actions}

    def define_action(self, action, arg=None, cmd=None, wrapper=None):
        if arg is None:
            arg = {}
        self.software.add_action(action)
        self.commands[action] = {'cmd': cmd, 'arg': arg, 'wrapper': wrapper}

    def define_action_as_fun(self, action, arg=None, fun=None, wrapper=None):
        if fun is None:
            fun = self.worker.run_cmd
        if arg is None:
            arg = {}
        self.software.add_action(action)
        self.commands[action] = {'fun': fun, 'arg': arg, 'wrapper': wrapper}

    def _run_fun(self, action, inputs=None):
        if inputs is None:
            inputs = {}
        fun = self.commands[action]['fun']
        args = self.commands[action]['arg']
        z = dict(inputs.items() + args.items())

        return fun(**z)

    def _run_cmd(self, action, inputs=None):
        wrapper = self.commands[action]['wrapper']
        cmd = self.commands[action]['cmd']
        args = self.commands[action]['arg']
        args = dict(inputs.items() + args.items())
        if isinstance(cmd, list):
            for idx, c in enumerate(cmd):
                cmd[idx] = c.format(**args)
        else:
            cmd = cmd.format(**args)
        if wrapper is None:
            return self.worker.run_cmd(cmd, inputs['wd'])
        else:
            return wrapper(cmd, args)

    def run(self, action, inputs=None):
        if 'fun' in self.commands[action].keys():
            return self._run_fun(action, inputs)
        elif 'cmd' in self.commands[action].keys():
            return self._run_cmd(action, inputs)

