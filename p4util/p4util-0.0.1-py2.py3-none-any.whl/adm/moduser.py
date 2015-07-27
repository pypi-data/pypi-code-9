#!/usr/bin/env python

'''Update user specifications easily and quickily!

Currently only changes the AuthMethod to facilitate wholesale
migration to LDAP auth.

$Author: lester_cheung $
$Id: //guest/lester_cheung/p4util/p4util/adm/moduser.py#1 $

'''

__version__ = '0.{0}'.format('$Change: 15148 $'.split()[-2])

import argparse

import logging
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)

try:
    from ..p4cli import P4
except:
    # failback to P4Python (so we can run the script without installing the module)
    from P4 import P4

from pprint import pformat, pprint

def parse_args():
    ap = argparse.ArgumentParser(description='MYPROG')
    p4 = P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))

    ap.add_argument('-A', '--auth-method')

    ap.add_argument('users', nargs='*')

    return ap.parse_args()

def main():
    log = logging.getLogger(__name__)
    cfg = parse_args()
    log.debug(cfg)
    p4 = P4()
    p4.prog = __file__

    if cfg.user:
        p4.user = cfg.user
    if cfg.port:
        p4.port = cfg.port
    if cfg.client:
        p4.client = cfg.client
    if cfg.charset:
        p4.charset = cfg.charset

    p4.connect()

    for user in cfg.users:
        spec = p4.run_user(['-o', user])[0]
        pprint(spec)
        if cfg.auth_method:
            spec['AuthMethod'] = cfg.auth_method
        p4.input = spec
        p4.run_user('-if')

    p4.disconnect()

if __name__ == '__main__':
    main()
