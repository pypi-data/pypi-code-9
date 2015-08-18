#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-06 00:39:17
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-07 01:26:37
from __future__ import print_function

import os

from docopt import docopt
from logger import Logger
from use import __doc__ as usage
from use import __version__
import logging
from worker import scraper


log = Logger.log


def main():
    opts = docopt(usage, version=__version__)
   
    if opts['-i']:
        log.info('Starting the graphical interface...')
        try:
            import gui
            gui.run()
            return
        except Exception, e:
            log.critical(e)
            return
    
    opts = set_opts(opts)
    opts = set_log(opts)
    if not opts['<url>'] or not opts['<url>'].startswith('http'):
        log.critical("URL must contain http:// or https://")
        return

    try:
        scraper(opts['<url>'], opts['--depth'],
                opts['--to'], opts['--sameroot'], opts['-o'])
    except Exception, e:
        log.error(e)


def set_opts(opts):
    opts['<url>'] = opts['<url>'].strip()
    if not opts['<url>'].startswith('http://'):
        opts['<url>'] = 'http://' + opts['<url>']
    log.info('Root url: %s' % opts['<url>'])
    opts['--depth'] = int(opts['--depth'])
    log.info('Level required: %s' % opts.get('--depth', 0))
    if opts['--depth'] > 3:
        log.warning('It could take few minutes or hours')
    opts['--to'] = opts.get('--to', './')
    opts['--to'] = os.path.abspath(opts['--to'])
    log.info('--to: %s' % opts['--to'])
    return opts


def set_log(opts):
    log_path = os.path.abspath(opts['--log'])

    if not os.path.isfile(log_path):
        log_path = os.path.join(log_path, 'log.txt')

    log.info('log will be save in: %s' % log_path)
    opts['log_path'] = log_path
    f = open(log_path, 'wb')
    f.close()
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(levelname)-1s| %(message)s :: %(filename)s:%(lineno)s")
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return opts


if __name__ == '__main__':
    main()
