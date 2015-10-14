#!/usr/bin/env python3

'''
simple icinga plugin helper module
'''

__author__ = "Andre Keller"
__copyright__ = "Copyright (c) 2015, VSHN AG, info@vshn.ch"
__license__ = 'BSD'
__version__ = '0.1.0'

import argparse
import sys


class ArgParser(argparse.ArgumentParser):
    '''Custom argument parser.

    This variant will raise a PluginError exception, rather than exit
    and printing the error message on stdout.
    '''

    def error(self, message):
        '''called when error occurs during argument parsing.

        Args:
          - message: String containing error message
        Raises:
          - PluginError
        '''
        raise PluginError(message)

class PluginError(Exception):
    '''Custom exception for plugin related errors.'''
    pass

def plugin_exit(msg, prefix, code, **kwargs):
    '''Exit the plugin nicely.

    This will print a prefixed message to stdout and exit with a proper exit
    code.

    Args:
      - msg: String containing exit message
      - prefix: String containing message prefix
      - code: Integer specifying exit code

    All additional arguments are passed as is to the msg.format() method.
    '''
    try:
        perfdata = []
        for perf in kwargs.pop('perfdata'):
            perfdata.append(
                "'{label}'={value}{uom};{warn};{crit};{min};{max}".format(
                    label=perf.get('label'),
                    value=perf.get('value'),
                    uom=perf.get('uom', ''),
                    warn=perf.get('warn', ''),
                    crit=perf.get('crit', ''),
                    min=perf.get('min', ''),
                    max=perf.get('max', ''),
                )
            )
        perfdata = "|%s" % " ".join(perfdata)

    except KeyError:
        perfdata = ''

    print('%s: %s%s' % (prefix, msg.format(**kwargs), perfdata))
    sys.exit(code)

def exit_ok(msg, **kwargs):
    '''Exit the plugin with prefix 'OK' and exit code 0

    Args:
      - msg: String containing exit message

    All additional arguments are passed as is to the msg.format() method.
    '''
    plugin_exit(msg, prefix='OK', code=0, **kwargs)

def exit_critical(msg, **kwargs):
    '''Exit the plugin with prefix 'CRITICAL' and exit code 2

    Args:
      - msg: String containing exit message

    All additional arguments are passed as is to the msg.format() method.
    '''
    plugin_exit(msg, prefix='CRITICAL', code=2, **kwargs)

def exit_unknown(msg, **kwargs):
    '''Exit the plugin with prefix 'UNKNOWN' and exit code 3

    Args:
      - msg: String containing exit message

    All additional arguments are passed as is to the msg.format() method.
    '''
    plugin_exit(msg, prefix='UNKNOWN', code=3, **kwargs)

def exit_warning(msg, **kwargs):
    '''Exit the plugin with prefix 'WARNING' and exit code 1

    Args:
      - msg: String containing exit message

    All additional arguments are passed as is to the msg.format() method.
    '''
    plugin_exit(msg, prefix='WARNING', code=1, **kwargs)
