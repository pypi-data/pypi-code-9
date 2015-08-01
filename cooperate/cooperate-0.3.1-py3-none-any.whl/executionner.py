#!/usr/bin/env python

import subprocess
import sys


DEFAULT_COMMAND = 'date'


def execute(cmd):
    shell = not isinstance(cmd, (list, tuple))
    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=shell)
        stdout, stderr = proc.communicate()
    except Exception as error:
        msg = str(error)
        return {
            'error': msg
        }

    if sys.version_info < (3, 0):
        return {
            'stdout': stdout.rstrip('\r\n') or None,
            'stderr': stderr.rstrip('\r\n') or None,
            'code': proc.returncode
        }
    else:
        return {
            'stdout': stdout.decode('utf-8').rstrip('\r\n') or None,
            'stderr': stderr.decode('utf-8').rstrip('\r\n') or None,
            'code': proc.returncode
        }

if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='*', default=DEFAULT_COMMAND)
    args = parser.parse_args()
    response = execute(args.command)
    print(json.dumps(response, indent=2))
