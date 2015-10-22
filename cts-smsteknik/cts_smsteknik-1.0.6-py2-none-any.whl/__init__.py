#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals, print_function
from .smsteknik import SMSTeknikClient
from .exc import *

def _get_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Send SMS')
    parser.add_argument('-t', '--to', action='append', help='recipients')
    parser.add_argument('-m', '--message', help='Text to send', type=lambda s: unicode(s, 'utf-8'))
    parser.add_argument('-c', '--config', default=['/etc/smsteknik.conf'], help='Configuration file', action='append')
    return parser


def main():
    '''
    Entry point for commandline interface

    .. autoprogram:: smsteknik:_get_parser()
        :prog: smsteknik
    '''
    import ConfigParser

    parser = _get_parser()
    args = parser.parse_args()

    configfile = ['/etc/smsteknik.conf']

    config = ConfigParser.ConfigParser()
    config.read(configfile)

    sms_opts = dict(config.items('SMS Teknik'))
    smsclient = SMSTeknikClient(**sms_opts)

    if args.to is None:
        print("Error: No recipients")
        return 1

    if args.message is None:
        print("Error: No Message")
        return 1

    print(smsclient.send(args.to, args.message))


if __name__ == '__main__':
    main()
