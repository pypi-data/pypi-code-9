#!/usr/bin/env python
"""Usage: run_rdirwatcher.py --config <filename> [--logconfig <logconfig>]

This is a run_rdirwatcher.py description.

Options:
    -h, --help                      Show this screen
    -D                              debug
    --config <filename>             Config file
    --logconfig <logconfig>         Logging config file
"""
import logging
from ConfigParser import SafeConfigParser
import sys
import os
from docopt import docopt
from probe.rdirwatcher import RDirWatcher

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='rdirwatcher.log',
    level=logging.DEBUG,
    format='%(asctime)-8s.%(msecs)03d %(levelname)-8s %(name)s:%(lineno)-3s %(message)s'
)

def get_config(argv):

    args = docopt(__doc__, argv[1:])

    parser = SafeConfigParser()
    parser.read(args.get('--config'))

    # debug
    opt_debug = 0
    opt_debug = int(parser.get('common', 'debug'))
    if args.get('-D') > 0:
        opt_debug = int(args.get('-D'))
    if args.get('--no-debug'):
        opt_debug = 0

    #pkey_file
    opt_pkey_file = '{}/.ssh/id_rsa'.format(os.environ['HOME'])
    if parser.has_option('ssh', 'pkey_file'):
        opt_pkey_file = parser.get('ssh', 'pkey_file')

    #hostnames
    opt_hostname = parser.get('ssh', 'hostnames', None)
    if opt_hostname is not None:
        opt_hostnames = opt_hostname.split(',')
        opt_hostnames = [hostname.strip() for hostname in opt_hostnames]

    #username
    opt_username = os.environ['USER']
    if parser.has_option('ssh', 'username'):
        opt_username = parser.get('ssh', 'username')

    #watch_dir
    opt_watch_dir = None
    if parser.has_option('watch', 'watch_dir'):
        opt_watch_dir = parser.get('watch', 'watch_dir')
    if opt_watch_dir is None:
        opt_watch_dir = '/tmp'
        
    #watch_pattern
    opt_watch_pattern = parser.get('watch', 'watch_pattern')

    #watch_max_age
    opt_watch_max_age = float(parser.get('watch', 'watch_max_age'))

    return {
        'debug' : opt_debug,
        'pkey_file' : opt_pkey_file,
        'hostnames' : opt_hostnames,
        'username' : opt_username,
        'watch_dir' : opt_watch_dir,
        'watch_pattern' : opt_watch_pattern,
        'watch_max_age' : opt_watch_max_age,
    }


def start_watching():
    cfg = get_config(sys.argv)
    logger.debug(repr(cfg).replace('\n', ' '))

    print __name__

    for hostname in cfg['hostnames']:
        cfg_tmp = cfg.copy()
        cfg_tmp['hostname'] = hostname
        logger.debug('cfg_tmp: {}'.format(cfg_tmp))
        rdir_wathcer = RDirWatcher(cfg_tmp)
        comps = rdir_wathcer.check()
        logger.debug('comps: {}'.format(comps))
    return comps

if __name__ == '__main__':
    if start_watching():
        pass
