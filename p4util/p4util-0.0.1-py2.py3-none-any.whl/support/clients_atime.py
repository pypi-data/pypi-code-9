#!/usr/bin/env python2.7

'''
Shows the last access time of clients.

$Author: lester_cheung $
$Id: //guest/lester_cheung/p4util/p4util/support/clients_atime.py#3 $
'''

from __future__ import print_function
__version__ = '0.{0}'.format('$Change: 9166 $'.split()[-2])

import argparse
import logging
import os
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)
import P4


def parse_args():
    '''parse command-line options'''
    ap = argparse.ArgumentParser(description=__doc__)
    p4 = P4.P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))

    return ap.parse_args()

def main():
    log = logging.getLogger(__name__)
    cfg = parse_args()
    log.debug(cfg)
    p4 = P4.P4()
    p4.prog = os.path.basename(__file__)

    if cfg.user:
        p4.user = cfg.user
    if cfg.port:
        p4.port = cfg.port
    if cfg.client:
        p4.client = cfg.client
    if cfg.charset:
        p4.charset = cfg.charset

    p4.connect()

    clients = []
    for c in p4.iterate_clients():
        clients.append(
            dict(atime=c.get('Access', ''),
                 client=c.get('Client', ''),
                 owner=c.get('Owner', '')))
    p4.disconnect()
    clients.sort(key=lambda x: x.get('atime'), reverse=True)
    print('{:<20} {:<40} {}'.format('ACCESSED', 'CLIENT', 'OWNER'))
    for c in clients:
        print('{atime} {client:<40} {owner}'.format(atime=c.get('atime'),
                                                    client=c.get('client'),
                                                    owner=c.get('owner')))
if __name__ == '__main__':
    main()
