# -*- coding: utf-8 -*-
"""
Command Session

TODO:
    - contextmanager to allow caller to set stream preference
    - override of environment and cwd
    - ParamDict should unpack itself (CommandSession should nto have to)
"""
__all__ = ["CommandError", "CommandSession", "CommandSessionMixin", "ParamDict"]

import os
import sys
import six
import subprocess

from boltons.dictutils import OrderedMultiDict


ParamDict = OrderedMultiDict


class CommandError(subprocess.CalledProcessError):
    def __init__(self, session):
        super(CommandError, self).__init__(
            session.last_returncode,
            session.last_command,
            output=session.last_output
        )
    def __str__(self):
        return "Command {} returned {} with {}".format(
            self.cmd,
            self.returncode,
            self.output
        )

class CommandSession(object):
    """Wrapper around multiple invocations of subprocess.Popen, tracking
    and saving execution results and output.
    Provides methods having similar interface as `subprocess.call()`,
    `subprocess.check_call()`, and subprocess.check_output()`.

    Params:
        stream (bool): should output be streamed to stdout, in additin to being
        captured?
        env (dict): environment to use, in place of current process environment
        cwd (str): current working directory to replace `os.cwd()`
        force_shell (bool): whether or not to force `shell=True` param 
            to `Popen()`; if the shell (/bin/sh) is required (for instance,
            if you intend to use a shell builtin), you can force this;
            normally, `shell` param is only used for commands given as
            strings (subprocess prefers commands given as lists, which is
            the default for this module).
    """
    def __init__(self, stream=False, env=None, cwd=None, force_shell=False):
        self.log = []
        self._stream = sys.stdout if stream else None
        self._env = env
        self._cwd = cwd
        self._shell = force_shell

    @property
    def last_returncode(self):
        """Get the return code of the last command exevuted."""
        try:
            return self.log[-1][1]
        except IndexError:
            raise RuntimeError('Nothing executed')

    @property
    def last_command(self):
        """Get the output of the last command exevuted."""
        if not len(self.log):
            raise RuntimeError('Nothing executed')

        return self.log[-1][0]

    @property
    def last_output(self):
        """Get the output of the last command exevuted."""
        if not len(self.log):
            raise RuntimeError('Nothing executed')

        return self.log[-1][2]

    @property
    def last_error(self):
        """Get the output of the last command exevuted."""
        if not len(self.log):
            raise RuntimeError('Nothing executed')

        try:
            errs = [l for l in self.log if l[1] != 0]

            return errs[-1][2]
        except IndexError:
            # odd case where there were no errors
            #TODO
            return 'no last error'

    @property
    def output(self):
        """Get the output of the entire session."""

        return '\n'.join(['\n'.join(l[2]) for l in self.log])

    def _stream_write(self, line):
        if self._stream:
            self._stream.write(line)
            self._stream.write(os.linesep)

    def _exec(self, cmd):
        shell = self._shell
        if isinstance(cmd, six.string_types):
            shell=True

        popen_kwargs = {
            'shell': shell,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT
        }
        if self._env:
            popen_kwargs['env'] = self._env

        if self._cwd:
            popen_kwargs['cwd'] = self._cwd

        p = subprocess.Popen(
            cmd, **popen_kwargs
        )
        output = []
        for line in iter(p.stdout.readline, six.binary_type('', 'utf-8')):
            line = line.decode('utf-8').strip()
            self._stream_write(line)
            output.append(line)

        p.wait()

        log = [
            ' '.join(cmd) if not shell else cmd, 
            p.returncode,
            output
        ]
        self.log.append(log)

        return p.returncode, '\n'.join(output)

    def check_output(self, cmd):
        """Wrapper for subprocess.check_output."""
        ret, output = self._exec(cmd)
        if not ret == 0:
            raise CommandError(self)

        return output

    def check_call(self, cmd):
        """Fake the interface of subprocess.call()."""
        ret, _ = self._exec(cmd)
        if not ret == 0:
            raise CommandError(self)

        return ret

    def call(self, cmd):
        """Fake the interface of subprocess.call()."""
        ret, _ = self._exec(cmd)
        return ret

    @staticmethod
    def unpack_args(*args, **kwargs):
        gnu = kwargs.pop('gnu', False)
        assert isinstance(gnu, bool)
        def _transform(argname):
            """Transform a python identifier into a 
            shell-appropriate argument name
            """
            if len(argname) == 1:
                return '-{}'.format(argname)

            return '--{}'.format(argname.replace('_', '-'))

        ret = []
        for k, v in kwargs.items():
            if isinstance(v, list):
                for item in v:
                    if gnu:
                        ret.append('{}={}'.format(
                            _transform(k),
                            str(item)
                        ))
                    else:
                        ret.extend([
                            _transform(k),
                            str(item)
                        ])
            else:
                if gnu:
                    ret.append('{}={}'.format(_transform(k), str(v)))
                else:
                    ret.extend([
                        _transform(k),
                        str(v)
                    ])

        if len(args): 
            for item in args:    
                ret.append(_transform(item))

        return ret

    @staticmethod
    def unpack_pargs(positional_args, param_kwargs, gnu=False):
        """Unpack multidict and positional args into a
        list appropriate for subprocess.
        :param param_kwargs: 
            ``ParamDict`` storing '--param' style data.
        :param positional_args: flags
        :param gnu: 
            if True, long-name args are unpacked as:
                --parameter=argument
            otherwise, they are unpacked as:
                --parameter argument
        :returns: list appropriate for sending to subprocess
        """

        def _transform(argname):
            """Transform a python identifier into a 
            shell-appropriate argument name
            """
            if len(argname) == 1:
                return '-{}'.format(argname)

            return '--{}'.format(argname.replace('_', '-'))

        args = []
        for item in param_kwargs.keys():
            for value in param_kwargs.getlist(item):
                if gnu:
                    args.append('{}={}'.format(
                        _transform(item),
                        value
                    ))
                else:
                    args.extend([
                        _transform(item),
                        value
                    ])
        if positional_args: 
            for item in positional_args:    
                args.append(_transform(item))

        return args

class CommandSessionMixin(object):
    def __init__(self, session=None):
        self.session = session or CommandSession()


