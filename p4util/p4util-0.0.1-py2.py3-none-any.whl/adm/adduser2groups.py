'''
Add user to one or more groups.

Groups are created automatically if not exist.

May be able to create new users someday.

$Id: //guest/lester_cheung/p4util/p4util/adm/adduser2groups.py#1 $
$Author: lester_cheung $

'''

__version__ = '0.{0}'.format('$Change: 15148 $'.split()[-2])

import sys
import P4
import logging
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)

import argparse

def parse_args():
    ap = argparse.ArgumentParser(description=__doc__)
    p4 = P4.P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))
    ap.add_argument('newuser')
    ap.add_argument('groups', nargs='+')

    return ap.parse_args()

def main():
    log = logging.getLogger(__name__)
    cfg = parse_args()
    log.debug(cfg)
    p4 = P4.P4()
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

    for group in cfg.groups:
        grp = p4.run_group(['-o', group])[0]
        members =  grp.get('Users', [])
        if cfg.newuser not in members:
            members.append(cfg.newuser)
            grp['Users'] = members
            p4.input = grp
            log.debug(p4.run_group('-i'))

    p4.disconnect()

if __name__ == '__main__':
    main()
