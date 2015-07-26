#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from tornado import gen, ioloop, tcpclient


logger = logging.getLogger(__name__)
loopinstance = ioloop.IOLoop.instance()


class LineStream:
    def __init__(self):
        self.tcp_client_factory = tcpclient.TCPClient()
        self.line_callback = None
        self.connect_callback = None

    @gen.coroutine
    def connect(self, host, port):
        logger.debug('Connecting to server %s:%s', host, port)
        self.connection = yield self.tcp_client_factory.connect(host, port)
        logger.debug('Connected.')
        if self.connect_callback is not None:
            self.connect_callback()
            logger.debug('Called post-connection callback')
        self._schedule_line()

    def handle_line(self, line):
        if self.line_callback is not None:
            self.line_callback(line)

        self._schedule_line()

    def _schedule_line(self):
        self.connection.read_until(b'\n', self.handle_line)

    def write_function(self, line):
        if line[-1] != '\n':
            line += '\n'
        return self.connection.write(line.encode('utf8'))

    def start(self):
        loopinstance.start()


def get_arg_parser():
    import argparse
    arg_parser = argparse.ArgumentParser(description='Pircel IRC Library Test client')
    arg_parser.add_argument('-n', '--nick', default='pircel',
                            help='Nick to use on the server.')
    arg_parser.add_argument('-u', '--username', default='pircel',
                            help='Username to use on the server')
    arg_parser.add_argument('-r', '--real-name', default='pircel IRC',
                            help='Real name to use on the server')
    arg_parser.add_argument('-s', '--server', default='irc.imaginarynet.org.uk',
                            help='IRC Server to connect to')
    arg_parser.add_argument('-c', '--channel', action='append',
                            help='Channel to join on server')
    arg_parser.add_argument('-D', '--debug', action='store_true',
                            help='Enable debug logging')
    arg_parser.add_argument('--die-on-exception', action='store_true',
                            help='Exit program when an unhandled exception occurs, rather than trying to recover')
    arg_parser.add_argument('--debug-out-loud', action='store_true',
                            help='Print selected debug messages out over IRC')
    return arg_parser


def get_parsed_args():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    if not args.channel:
        args.channel = ['#possel-test']

    return args


def main():
    pass

if __name__ == '__main__':
    main()
