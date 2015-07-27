'''
Show members in a Perforce group

$Author: lester_cheung $
$Id: //guest/lester_cheung/p4util/p4util/adm/lsgroup.py#1 $
'''

__version__ = '0.{0}'.format('$Change: 15148 $'.split()[-2])

import sys
import P4
import logging
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)

import argparse
from pprint import pprint

def parse_args():
    ap = argparse.ArgumentParser(description='MYPROG')
    p4 = P4.P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))
    ap.add_argument('-s', '--show-subgroups', action='store_true', default=False)
    ap.add_argument('groups', nargs='*')

    return ap.parse_args()

def get_group_members(p4, cfg, grp, visited=[]):

    if grp in visited:
        return {}

    users = {}
    g = p4.run_group(['-o', grp])[0] # "p4 group" will always return something
    visited.append(grp)
    for usr in g.get('Users'):
        if not users.get(usr):
            users[usr] = []
        users[usr].append(grp)

    if not cfg.show_subgroups:
        return users

    for subgrp in g.get('Subgroups', []):
        users2 = get_group_members(p4, cfg, subgrp, visited)
        for u2 in users2:
            if not users.get(u2):
                users[u2] = []
            users[u2].extend(users2[u2])

    return users

def main():
    log = logging.getLogger(__name__)
    cfg = parse_args()
    # log.debug(cfg)
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

    for grp in cfg.groups:
        members = get_group_members(p4, cfg, grp)
        print("{0:<20} {1}".format("USER", "GROUPS"))
        for member in members:
            print("{0:<20} {1}".format(member, ', '.join(members[member])))

    p4.disconnect()

if __name__ == '__main__':
    main()
