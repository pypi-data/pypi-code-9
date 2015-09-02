# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, sys, subprocess, logging

from . import utils, exceptions

################################################################################

class NoSuchExecutableException(Exception):
    pass

class FailedCommandException(Exception):
    def __init__(self, cmd, exit_code, background, stdout, stderr):
        super(FailedCommandException, self).__init__()
        self.cmd = cmd
        self.exit_code = exit_code
        self.background = background
        self.stdout = stdout.decode().strip() if background else None
        self.stderr = stderr.decode().strip() if background else None

################################################################################

class Executable(object):
    def __init__(self, executable):
        self._logger = logging.getLogger(utils.fullname(self))
        self.executable = executable
        self.baked_args = []
        self.success_code = 0

    def __call__(self, *args, **kwargs):
        bg = 'foreground' not in kwargs or not kwargs['foreground']

        cmd = [ self.executable ] + self.baked_args + list(args)

        print(cmd)

        proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE if bg else None
                                                , stderr=subprocess.PIPE if bg else None)
        out, err = proc.communicate()

        if proc.returncode != self.success_code:
            raise FailedCommandException(cmd, proc.returncode, bg, out, err)

        if bg:
            return out.decode().strip(), err.decode().strip()

    def bake(self, *args):
        self.baked_args.extend(list(args))

# class Shell(object):
#     def __getattr__(self, attr):
#         print(globals())
#         for key, value in globals().items():
#             if attr == key:
#                 return value
#
#         if not any([ os.path.exists(os.path.join(p, attr)) for p in os.environ["PATH"].split(os.pathsep) ]):
#             raise NoSuchExecutableException(attr)
#
#         return Executable(attr)
#
# sys.modules[__name__] = Shell()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
