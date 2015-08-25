#!/usr/bin/env python

from __future__ import absolute_import

from argparse import ArgumentParser
from os.path import isfile
import sys
import ConfigParser

import logging
import logging.handlers

from .manager import PsqlDumperManager

def parse_args():
    parser = ArgumentParser(description='PsqlDumper - PostgreSQL Dumps Manager')

    parser.add_argument('-c', '--config', dest='config', type=str, nargs='?', default='/usr/local/etc/psqldumper.conf',
                        help="Main configuration file location. Default: '/usr/local/etc/psqldumper.conf'.")
    parser.add_argument('-u', '--pg-user', dest='pg_user', type=str, nargs='?', default='postgres',
                        help="PostgreSQL user to run commands as. Default: 'postgres'.")
    parser.add_argument('-d', '--dump-directory', dest='dump_root', type=str, nargs='?', default='/var/backups/pg_dumps',
                        help="Directory where the dumps will be stored. Default: '/var/backups/pg_dumps'.")
    parser.add_argument('-l', '--logfile', dest='logfile', type=str, nargs='?', default=None,
                        help="Log file location. Default: stdout")
    parser.add_argument('-e', '--email', dest='email', type=str, nargs='?', default=None,
                        help="Email address to send notifications to. No adress means no notifications.")
    parser.add_argument('--notify-success', dest='notify_success', action='store_true',
                        help="Send email notifications for successful dumps too.")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help="Show progress messages on stdout.")

    return parser, parser.parse_args()


def main():
    argparser, args = parse_args()

    if not isfile(args.config):
        print('Configuration file {} does not exist or is not readable'.format(args.config))
        sys.exit(1)

    if args.logfile:
        logging.getLogger('psqldumper').setLevel(logging.DEBUG)
        handler = logging.handlers.TimedRotatingFileHandler(args.logfile,when='D',backupCount=7)
        FORMAT = "%(asctime)-15s %(message)s"
        fmt = logging.Formatter(FORMAT,datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(fmt)
        logging.getLogger('psqldumper').addHandler(handler)
    else:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    logging.getLogger('psqldumper').info('Loading configuration')
    config = ConfigParser.RawConfigParser()
    config.read(args.config)

    logging.getLogger('psqldumper').info('Starting PsqlDumper manager')
    dumper = PsqlDumperManager(config._sections, args.pg_user, args.dump_root, email=args.email, success=args.notify_success)

    logging.getLogger('psqldumper').info('Checking if we are a PG master')
    if not dumper.check_if_master():
        logging.getLogger('psqldumper').info('Looks like we are a slave, exiting')
        sys.exit(0)

    logging.getLogger('psqldumper').info('Selecting databases for dumping')
    dumper.select_databases()

    logging.getLogger('psqldumper').info('Running dump jobs')
    dumper.run_jobs()

    logging.getLogger('psqldumper').info('Sending notifications')
    dumper.send_notifications()
