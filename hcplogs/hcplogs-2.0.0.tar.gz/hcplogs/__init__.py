# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse
import logging
from logging.handlers import RotatingFileHandler
import configparser
from os import access, F_OK, makedirs
from os.path import normpath, split
from getpass import getuser

from hcplogs.init import Gvars, Ivars
from hcplogs.template import template
import hcplogs.loghandler


class HcplogError(Exception):
    """
    Raised on generic errors in **hcplog**.
    """

    def __init__(self, reason):
        """
        :param reason:  an error description
        """
        self.args = (reason,)


def parseargs():
    """
    args - build the argument parser, parse the command line and
           run the respective functions.
    """
    maindescription = '''
                        %(prog)s downloads access logs for the REST-based
                        interfaces (native/HS3/HSwift) from HCP systems.
                        It keeps a timestamp of the last successfully
                        downloaded logs and excludes everything older than
                        it when running %(prog)s again.
                      '''

    mainparser = argparse.ArgumentParser(description=maindescription)
    mainparser.add_argument('--version', action='version',
                            version="%(prog)s: {0}\n".format(Gvars.Version))
    mainparser.add_argument('-i', dest='ini',
                            default=normpath('./hcplogs_config.ini'),
                            help='path/name of the ini-file containing the '
                                 'configuration (defaults to the current '
                                 'directory)')

    result = mainparser.parse_args()
    return result


def log(stdout, logtofile, debug, logfile, rotatemb, backups):
    """
    Setup logging

    :param stdout:      logging to stdout (bool)
    :param logtofile:   logging to file (bool)
    :param debug:       log in debug mode (bool)
    :param logfile:     name of file to log to
    returns:            the logger object
    """

    if not stdout and not logtofile:
        raise HcplogError('Err: at least one logger is needed')
    if logtofile and not logfile:
        raise HcplogError('Err: logfile needed')

    if debug:
        # fh = logging.Formatter('%(asctime)s [%(levelname)-6s] %(name)s.'
        #                        '%(module)s.%(funcName)s(%(lineno)d): '
        #                        '%(message)s',
        fh = logging.Formatter('%(asctime)s [%(levelname)-6s] %(name)s'
                               '.%(funcName)s(%(lineno)d): '
                               '%(message)s',
                               '%m/%d %H:%M:%S')
    else:
        fh = logging.Formatter('%(asctime)s [%(levelname)-6s] '
                               '%(message)s',
                               '%m/%d %H:%M:%S')

    logger = logging.getLogger()

    if stdout:
        sh = logging.StreamHandler()
        sh.setFormatter(fh)
        logger.addHandler(sh)
    if logtofile:
        try:
            makedirs(split(logfile)[0], exist_ok=True)
            lh = RotatingFileHandler(logfile,
                                     maxBytes=rotatemb * 1024 * 1024,
                                     backupCount=backups)
        except Exception as e:
            raise HcplogError('Err: logfile: {}'.format(e))
        else:
            lh.setFormatter(fh)
            logger.addHandler(lh)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    try:
        logger.debug('logging initialized')
    except KeyError as e:
        raise HcplogError(e)

    return logger


def createtemplate(file):
    """
    Create a template ini file

    :param file:    the filename to be created as template
    :raises:        *HcplogsError*
    """
    print('A configuration file is not available.')
    answer = input('Do you want me to create a template for you (y/n)? ')

    if answer in ['y', 'Y', 'yes', 'Yes', 'YES']:
        try:
            with open(file, 'w') as outhdl:
                outhdl.write(template)
        except Exception as e:
            raise HcplogError(e)
    else:
        raise HcplogError('user denied creation')


class Config(object):
    """
    Read and update the configuration .ini file

    :var targets:       a dict of targets to collect from
    :var accesslogs:    a dict of logs to collect
    """

    def __init__(self, inifile):
        """
        :param inifile:     the inifile from args
        :raises:            *HcplogError*
        """
        self.inifile = inifile
        self.targets = {}
        self.accesslogs = {}

        if not access(inifile, F_OK):
            try:
                createtemplate(inifile)
            except HcplogError as e:
                raise HcplogError('Creation of template config file "{}" '
                                  'failed\n\thint: {}'
                                  .format(inifile, e))
            else:
                raise HcplogError('Creation of template config file "{}" '
                                  'was successfull\n\tYou need to edit it '
                                  'to fit your needs!'.format(inifile))

        try:
            confhdl = open(self.inifile, 'r')
        except Exception as e:
            raise HcplogError('Opening the config file "{}" failed:\n'
                              '\thint: {}'.format(inifile, e))

        # Read the configuration file
        try:
            self.c = configparser.ConfigParser(interpolation=None)
            self.c.read_file(confhdl)
            confhdl.close()

            # Configure logging
            log(self.c.getboolean('logging', 'log to stdout'),
                self.c.getboolean('logging', 'log to file'),
                self.c.getboolean('logging', 'debug'),
                self.c['logging']['logfile'],
                self.c.getint('logging', 'rotatemb', fallback='10'),
                self.c.getint('logging', 'backups', fallback='9'))
            logger = logging.getLogger(__name__ + '.Config')
            logger.info('Started run (user "{}")'.format(getuser()))

            logger.debug('Configuration file content:')
            for s in self.c.sections():
                logger.debug('[{}]'.format(s))
                for k in self.c.options(s):
                    logger.debug('\t{} = {}'.format(k, self.c[s][k]))

            # Make sure we have the targets to collect from
            for s in self.c.sections():
                if s.startswith('target '):
                    self.targets[s] = {'fqdn': self.c[s]['fqdn'],
                                       'user': self.c[s]['user'],
                                       'password': self.c[s]['password'],
                                       'folder': self.c[s]['folder'],
                                       'last collected':
                                           self.c[s]['last collected']}

            # Make sure we know which logs are wanted
            self.accesslogs = {'access': self.c.getboolean('access logs',
                                                           'access'),
                               'mapi': self.c.getboolean('access logs',
                                                         'mapi'),
                               'admin': self.c.getboolean('access logs',
                                                          'admin')}
        except (KeyError, ValueError, configparser.NoSectionError,
                configparser.NoOptionError) as e:
            raise HcplogError('Parsing the config file "{}" failed:\n'
                              '\thint: {}'.format(inifile, e))

    def save(self):
        """
        Write the configuration ini file back to disk

        :raises:    *HcplogError*
        """
        for t in self.targets:
            if self.targets[t]['last collected'] != \
                    self.c[t]['last collected']:
                self.c[t]['last collected'] = \
                    self.targets[t]['last collected']

        try:
            with open(self.inifile, 'w') as confhdl:
                self.c.write(confhdl)
        except Exception as e:
            raise HcplogError('re-write of config file "{}" failed\n'
                              '\thint: {}'.format(self.inifile, e))
