#!/usr/bin/env python

'''Wrapper for P4, the command line client, using the same interface
as P4.P4 in P4Python.

Usage:
from p4cli import P4
P4.p4bin = '/absolute/path/to/your/p4/executable' # if not in your path
p4 = P4()

To use P4CLI when you have P4Python installed, use p4cli.P4CLI
instead.

Currently only works for Python2.7+ but can be extended to
support older versions.

If this behaves differently to P4Python, it's a bug.

$Id: //guest/lester_cheung/p4util/p4util/p4cli.py#9 $
$Author: lester_cheung $
$DateTime: 2015/07/05 20:28:47 $

'''

import logging
import marshal
import os
import re
import shlex
import sys
import tempfile

from pprint import pprint, pformat
from subprocess import Popen, PIPE, check_output


# DEBUGLVL = logging.DEBUG
# logging.basicConfig(
#     level=DEBUGLVL,
#     format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
#     datefmt='%Y-%m-%d %H:%M',
# )
#pylint: disable=invalid-name
log = logging.getLogger(os.path.basename(__file__))

__version__ = '$Change: 14832 $'


# Yucky bits to handle Python2 and Python3 differences...
# sys.version_info.major won't work until 2.7 :(
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# if PY2:
#     from StringIO import StringIO
# elif PY3:
#     from io import StringIO


class P4CLI(object):
    '''Poor mans's implimentation of P4Python using P4
    CLI... just enough to support p4review2.py.

    '''
    charset = None      # P4CHARSET
    encoding = 'utf8'    # default encoding
    input = None      # command input
    array_key_regex = re.compile(r'^(\D*)(\d*)$')  # depotFile0, depotFile1...
    tempfiles = []

    def __init__(self):
        self.user = self.env('P4USER')
        self.port = self.env('P4PORT')
        self.client = self.env('P4CLIENT')
        if self.env('P4CHARSET') == 'none':
            # you *can* have "P4CHARSET=none" in your config...
            self.charset = None

    def __repr__(self):
        return '<P4CLI({u}@{c} on {p})>'.format(u=self.user, c=self.client,
                                                p=self.port)

    def __del__(self):
        '''cleanup '''
        for f in self.tempfiles:
            os.unlink(f)

    def __getattr__(self, name):
        if name.startswith('run'):
            p4cmd = None
            if name.startswith('run_'):
                p4cmd = name[4:]

            def p4runproxy(*args):  # stubs for run_*() functions
                cmd = self.p4pipe
                if p4cmd:  # command is in the argument for calls to run()
                    cmd += [p4cmd]
                if isinstance(args, tuple) or isinstance(args, list):
                    for arg in args:
                        if isinstance(arg, list):
                            cmd.extend(arg)
                        else:
                            cmd.append(arg)
                else:
                    cmd += [args]
                cmd = [str(c) for c in cmd]

                if self.input:
                    tmpfd, tmpfname = tempfile.mkstemp()
                    self.tempfiles.append(tmpfname)
                    tmpfd = open(tmpfname, 'rb+')
                    marshal.dump(self.input, tmpfd, 0)
                    tmpfd.seek(0)
                    p = Popen(cmd, stdin=tmpfd, stdout=PIPE)
                else:
                    p = Popen(cmd, stdout=PIPE)

                rv = []
                while 1:
                    try:
                        rv.append(marshal.load(p.stdout))
                    except EOFError:
                        break
                    except Exception:
                        log.error('Unknown error while demarshaling data'
                                  'from server.')
                        log.error(' '.join(cmd))
                        break
                p.stdout.close()
                log.debug(pformat(rv))  # raw data b4 decoding
                self.input = None  # clear any inputs after each p4 command

                rv2 = []        # actual array that we will return
                # magic to turn 'fieldNNN' into an array with key 'field'
                for r in rv:    # rv is a list if dictionaries
                    r2 = {}
                    for key in r:
                        decoded_key = key
                        if PY3 and isinstance(decoded_key, bytes):
                            decoded_key = decoded_key.decode(self.encoding)
                        val = r[key]
                        if PY3 and isinstance(val, bytes):
                            val = val.decode(self.charset or self.encoding or
                                             'utf8')
                        regexmatch = self.array_key_regex.match(decoded_key)
                        if not regexmatch:  # re.match may return None
                            continue
                        k, num = regexmatch.groups()

                        if num:  # key in 'filedNNN' form.
                            v = r2.get(k, [])
                            if isinstance(v, str):
                                v = [v]
                            v.append(val)
                            r2[k] = v
                        else:
                            r2[k] = val
                    rv2.append(r2)
                log.debug(pformat(rv2)) # data after decoding
                return rv2
            return p4runproxy
        elif name in 'connect disconnect'.split():
            return self.noop
        elif name in 'p4pipe'.split():
            cmd = [self.p4bin] + \
                  shlex.split('-G -p {port} -u {user} -c {client}'.format(
                      port=self.port, user=self.user,
                      client=self.client))
            if self.charset:
                cmd += ['-C', self.charset]
            return cmd
        else:
            raise AttributeError("'P4CLI' object has no attribute '{}'".format(
                name))

    def identify(self):
        return 'P4CLI, using {0}'.format(self.p4bin)

    def connected(self):
        '''With CLI, we are always (dis)connected.'''
        return True

    def run_login(self, *args):
        cmd = self.p4pipe + ['login']
        if '-s' in args:
            cmd += ['-s']
            proc = Popen(cmd, stdout=PIPE)
            out = proc.communicate()[0]
            if marshal.loads(out).get('code') == 'error':
                raise Exception('P4CLI exception - not logged in.')
        else:
            proc = Popen(cmd, stdin=PIPE, stdout=PIPE)
            out = proc.communicate(input=self.password)[0]
            out = '\n'.join(out.splitlines()[1:])  # Skip the password prompt..
        return [marshal.loads(out)]

    def env(self, key):
        rv = check_output([self.p4bin, 'set', key]).decode('utf8')
        rv = rv.split(' (config)')[0]
        rv = rv.split(' (set)')[0]
        # don't use the keyword "maxsplit" as it will break in Python2
        rv = rv.split('=', 1)
        if len(rv) != 2:
            rv = None
        else:
            rv = rv[1]

        if not rv:
            if key == 'P4USER':
                from getpass import getuser
                rv = getuser()
            elif key == 'P4CLIENT':
                from socket import gethostname
                rv = gethostname()
            elif key == 'P4PORT':
                rv = 'perforce:1666'
        return rv

    def noop(*args, **kws):
        pass    # stub - it's a class method which returns None.

    def run_plaintext(self, *args):
        '''Run P4 commands normally and return the outputs in plaintext'''
        cmd = '''{bin} -p "{p4port}" -u {p4user} -c {p4client}'''.format(
            bin=self.p4bin,
            p4port=self.port,
            p4user=self.user,
            p4client=self.client)
        cmd = shlex.split(cmd) + list(args)
        rv = check_output(cmd)
        if PY3 and isinstance(rv, bytes):
            rv = rv.decode(self.charset or self.encoding or 'utf8')
        return rv


class P4Debug(object):
    '''class for debugging P4CLI'''
    def __init__(self):
        self.p4 = P4()

    def __getattr__(self, name):
        if name.startswith('run_'):
            def proxy(*args):
                log.debug(name)
                log.debug('+++++++++++')
                log.debug(args)
                rv = self.p4.__getattr__(name)(*args)
                return rv
            return proxy
        elif name in 'prog port user charset connect disconnect login'.split():
            try:
                return self.p4.__getattribute__(name)
            except AttributeError:
                return self.p4.__getattr__(name)
        log.warning(name+'not found!')
        raise AttributeError    # not found


def sh_which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """
    (copied from shutil.py in Python 3.3.2, so this works for Python2)

    Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode) and
                not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up
    # directly rather than referring to PATH directories. This
    # includes checking relative to the current directory,
    # e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if os.curdir not in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if normdir not in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None

# So ALL instances of P4 knows where to find the P4 binary.
P4CLI.p4bin = '/usr/local/bin/p4'
# pushing common locations of P4 to system path
for d in ['/p4/common/bin']:
    sys.path.append(d)
for f in 'p4 p4.exe'.split():
    if sh_which(f, path=os.pathsep.join(sys.path)):
        P4CLI.p4bin = sh_which(f)
        break

try:
    from P4 import P4
except ImportError:
    P4 = P4CLI


if __name__ == '__main__':
    p4 = P4CLI()
    pprint(p4.run(sys.argv[1:]))
