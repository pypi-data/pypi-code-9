###############################################################################
#
# Copyright (c) 2013 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
###############################################################################
"""Start script and config
$$
"""
__docformat__ = "reStructuredText"

import sys
import socket
import traceback
import optparse

import p01.kibana.server
import p01.kibana.logger


def get_options(args=None):
    if args is None:
        args = sys.argv
    original_args = args
    parser = optparse.OptionParser(usage=("usage: <script> [options]"))
    parser.add_option('--interface', dest='interface',
        help="interface [host]:port (defaults to 0.0.0.0:2200)",
        default='0.0.0.0:2200',
        )
    parser.add_option('--elasticsearch', dest='elasticsearch',
        help="a elasticsearch backend  [host]:port (defaults to 0.0.0.0:9200)",
        default='0.0.0.0:9200',
        )
    parser.add_option('--interval', dest='interval',
        default=p01.kibana.server.INTERVAL,
        help="flush interval, in seconds (default %s)" % (
            p01.kibana.server.INTERVAL),
        )
    parser.add_option('--timeout', dest='timeout',
        default=p01.kibana.server.TIMEOUT,
        help="elasticsearch connection timeout, in seconds (default %s)" % (
            p01.kibana.server.TIMEOUT),
        )
    parser.add_option('--max-queue-size', dest='maxQueueSize', type='int',
        help="max (log event) queue size (default=1000)",
        default=p01.kibana.server.MAX_QUEUE_SIZE,
        )
    parser.add_option('--max-batch-size', dest='maxBatchSize', type='int',
        help="max (log event) batch size (default=250)",
        default=p01.kibana.server.MAX_QUEUE_SIZE,
        )
    parser.add_option('--loglevel', dest='loglevel', type='int',
        help="python logging level (default=40) (40=ERROR)",
        default=40,
        )
    parser.add_option('--trace', dest='trace', type='int',
        help="add logging handler for elasticsearch.trace",
        default=0,
        )
    options, positional = parser.parse_args(args)
    options.original_args = original_args
    options.loglevel = p01.kibana.logger.getLoggingLevel(options.loglevel)
    return options


def main(args=None):
    options = get_options(args)

    # setup logging
    p01.kibana.logger.setUpLogger(options)
    try:
        # stops with signal.SIGINT on KeyboardInterrupt
        # XXX: seems taht circus does not catch stdout during startup
        #      Also during stop a server with circus will the log get ignored
        #      just use stderr, that's what the circus daemon will listen on
        #      startup a watcher
        sys.stderr.write("Starting server\n")
        server = p01.kibana.server.KibanaServer(options.interface,
            hosts=options.elasticsearch, interval=options.interval,
            timeout=options.timeout, maxQueueSize=options.maxQueueSize,
            maxBatchSize=options.maxBatchSize, loglevel=options.loglevel)
        sys.stderr.write("Server started at: %s\n" % options.interface)
        sys.stderr.write("Elasticsarch used: %s\n" % options.elasticsearch)
        server.start()
    except Exception, e:
        sys.stderr.write("interface: %s\n" % options.interface)
        sys.stderr.write("backend: %s\n" % options.elasticsearch)
        sys.stderr.write("interval: %s\n" % options.interval)
        sys.stderr.write("maxQueueSize: %s\n" % options.maxQueueSize)
        sys.stderr.write("loglevel: %s\n" % options.loglevel)
        sys.stderr.write("args: %s\n" % options.original_args)
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
