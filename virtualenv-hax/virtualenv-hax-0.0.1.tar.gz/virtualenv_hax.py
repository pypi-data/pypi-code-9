from __future__ import absolute_import
from __future__ import print_function

import argparse
import distutils.spawn
import subprocess
import sys

import virtualenv


def main(argv=None):
    parser = argparse.ArgumentParser(description=(
        'A wrapper around virtualenv that avoids sys.path sadness. '
        'Any additional arguments are passed directly to `virtualenv`.'
    ))
    parser.add_argument('-p', '--python', default=sys.executable)
    args, rest_argv = parser.parse_known_args(argv)

    # The way virtualenv deals with -ppython is to exec itself with the right
    # interpreter.
    # The problem with this is the following:
    # - python foo/bar/baz.py puts foo/bar on the path
    # - in an environment where virtualenv and future (or others that shadow
    #   stdlib module names) this puts lib/.../site-packages on the path
    # - So for example, consider a python2.7 venv calling
    #   `virtualenv -ppython3.4 venv`
    # - This'll call something like:
    #   `/usr/bin/python3.4 .../lib/python2.7/site-packages/virtualenv.py venv`
    # - This'll put .../lib/python2.7/site-packages on the path *first*
    # - This'll make the py27 site-packages override the stdlib site-packages
    # - If you have python-future installed you'll get something like:
    #   File "/usr/lib/python3.4/re.py", line 324, in <module>
    #     import copyreg
    #   File ".../lib/python2.7/site-packages/copyreg/__init__.py", line 7, in
    # <module>
    #     raise ImportError('This package should not be accessible on
    # Python 3. '
    # ImportError: This package should not be accessible on Python 3. Either
    # you are trying to run from the python-future src folder or your
    # installation of python-future is corrupted.
    exe = distutils.spawn.find_executable(args.python)
    venv_file = virtualenv.__file__.rstrip('co')
    hax_script = (
        'import sys\n'
        'sys.argv[1:] = {rest_argv!r}\n'
        '__file__ = {venv_file!r}\n'
        '__name__ = "__main__"\n'
        'exec(open({venv_file!r}, "rb").read())\n'
    ).format(rest_argv=rest_argv, venv_file=venv_file)
    subprocess.check_call((exe, '-c', hax_script))


if __name__ == '__main__':
    exit(main())
