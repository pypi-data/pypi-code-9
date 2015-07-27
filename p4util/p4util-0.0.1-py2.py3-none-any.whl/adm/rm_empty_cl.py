'''Simply loop over all changelists and try to delete changes
with no file associated to it.

$Author: lester_cheung $
$DateTime: 2015/07/24 17:22:15 $
$Id: //guest/lester_cheung/p4util/p4util/adm/rm_empty_cl.py#1 $

TODO:
* check for job association
* use p4cli

'''

from __future__ import print_function

__version__ = '0.{0}'.format('$Change: 15148 $'.split()[-2])

import argparse
import logging
import re
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)

from pprint import pprint
from ..p4cli import P4

def parse_args():
    ap = argparse.ArgumentParser(description='MYPROG')
    p4 = P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))
    ap.add_argument('-y', '--do-it', action='store_true', default=False)
    ap.add_argument('-f', '--force', action='store_true', default=False)

    ap.add_argument('-s', '--status', metavar='submitted/pending', default='submitted', help='default is "submitted"')
    ap.add_argument('-A', '--author', help='only consider changelists by author.'
                    'Prefix username with "^" to inverse the filter.'
                    'E.g. "^foo" to remove empty changelist not owned by "foo".')
    ap.add_argument('-R', '--client-regex', help='only consider changelists associated with clients that match the pattern')


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

    hit_list = []

    for chg in p4.run_changes(['-s'+cfg.status]):
        chgno = chg['change']

        # filter changelists with change author
        if cfg.author:
            if cfg.author.startswith('^'):
                if chg.get('user') == cfg.author[1:]:
                    continue
            elif chg.get('user') != cfg.author:
                continue

        # skip changelists which doesn't match the specified regex
        if cfg.client_regex:
            if not re.search(cfg.client_regex, chg['client']):
                continue

        # only consider empty changelists
        d = p4.run_describe(['-s', chgno])
        if not d:
            continue
        if 'depotFile' not in d[0] or not d[0]['depotFile']:
            hit_list.append(chgno)

    if cfg.do_it:
        for chgno in hit_list:
            if cfg.force:
                log.debug(p4.run_change(['-df', chgno]))
            else:
                log.debug(p4.run_change(['-d', chgno]))
        log.info('Removed the following changelists: {}'.format(hit_list))
    else:
        log.info('Would remove the following changelists with the -y option: {}'.format(hit_list))

    p4.disconnect()


if __name__ == '__main__':
    main()
