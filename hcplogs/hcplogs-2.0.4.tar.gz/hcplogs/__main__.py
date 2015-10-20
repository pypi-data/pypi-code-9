#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Sos of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyrighftware without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copiet notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import logging
from getpass import getuser
from time import sleep

import hcplogs

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # collect the command line options
    opts = hcplogs.parseargs()

    # Read and parse the config file
    try:
        conf = hcplogs.Config(opts.ini)
    except hcplogs.HcplogError as e:
        sys.exit(e)

    logger = logging.getLogger(__name__)

    # create an Handler object for each HCP target
    tgts = {}
    for t in conf.targets.keys():
        logger.debug('creating handler for {}'.format(t))
        try:
            tgts[t] = hcplogs.loghandler.Handler(t, conf)
        except Exception as e:
            logger.error('creation of handler for {} failed\n'
                         '\thint: {}'.format(t, e))
        else:
            logger.debug('created handler for {}'.format(t))

    # pro-actively cancel log preparation for all targets
    for t in tgts.keys():
        try:
            tgts[t].cancel()
        except hcplogs.HcplogError as e:
            logger.error(e)

    # start log preparation for all targets
    for t in tgts.keys():
        try:
            tgts[t].prepare()
        except hcplogs.HcplogError as e:
            logger.error(e)

    # status query for all targets
    lr = tgts.copy()
    while True:
        for t in tgts.keys():
            if t in lr.keys():
                try:
                    tgts[t].status()
                except hcplogs.HcplogError as e:
                    logger.error(e)
                logger.info('status for {}: {}'.format(t, tgts[t].state))

                if tgts[t].state in [hcplogs.loghandler.S_PREPARED,
                                     hcplogs.loghandler.S_ERROR]:
                    del lr[t]
        if not len(lr):
            break
        sleep(conf.c['logging'].getint('status query',
                                       hcplogs.init.Ivars.statuspollrate))

    # download the log
    for t in tgts.keys():
        logger.info('starting download for {}'.format(t))
        try:
            tgts[t].download()
        except hcplogs.HcplogError as e:
            logger.error(e)

    # close all Handler objects
    for t in tgts.keys():
        tgts[t].close()
        logger.debug('closed handler for {}'.format(t))

    try:
        conf.save()
    except hcplogs.HcplogError as e:
        logger.info(
            '(Partially) failed run (user "{}"): {}'.format(getuser(),
                                                            e))
        sys.exit(e)

    logger.info('Finished run (user "{}")\n'.format(getuser()))

if __name__ == '__main__':
    main()