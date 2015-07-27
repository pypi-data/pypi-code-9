'''A script to populate a branch with all the move records.

For use with pre-2014.1 servers before the "-f" option in "p4
copy" was added.

Usage:

  python -m p4util.user.populate_with_move //depot/main/... //depot/dev/...


$Author: lester_cheung $
$Id: //guest/lester_cheung/p4util/p4util/user/populate_with_move.py#2 $

'''

__version__ = '0.{0}'.format('$Change: 11056 $'.split()[-2])

import argparse

import logging
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)

try:
    from ..p4cli import P4
except:
    # failback to P4Python (so we can run the script without installing the module)
    from P4 import P4

def parse_args():
    ap = argparse.ArgumentParser(description='MYPROG')
    p4 = P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))
    ap.add_argument('-y', '--do-it', action='store_true', default=False)

    ap.add_argument('src')
    ap.add_argument('dst')

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

    move_deleted_files = [ ( x.get('depotFile'), x.get('rev') )
                           for x in p4.run_files(cfg.src)
                           if x.get('action') == 'move/delete' ]

    ## NOTE NOTE NOTE
    # here we assume there will be no "move/delete" records at
    # rev 1 - which is not the case if you have used "p4 copy -f"
    # which copies delete records to target.
    src_base = cfg.src.rstrip('/...')
    dst_base = cfg.dst.rstrip('/...')
    for src, src_rev in move_deleted_files:
        src_rev = int(src_rev) - 1
        dst = '{}/{}'.format(dst_base, src.lstrip(src_base))
        log.debug('p4 copy {}#{} {}'.format(src, src_rev, dst))
        if cfg.do_it:
            p4.run_copy( ['{}#{}'.format(src, src_rev), dst] )

    log.info('Submitting last non-deleted revisions of files with "move/delete" at #head')
    if cfg.do_it:
        p4.run_submit(['-d', 'Submitting last non-deleted revisions of files with "move/delete" at #head'])

    log.info('Now we are doing a regular copy...')
    log.info('p4 copy {} {}'.format(cfg.src, cfg.dst))
    if cfg.do_it:
        p4.run_copy( [cfg.src, cfg.dst] )
        p4.run_submit( ['-d', 'p4 copy {} {}'.format(cfg.src, cfg.dst)] )

    p4.disconnect()
    if not cfg.do_it:
        log.info('Preview only - rerun with "-y" to actually create the branch')

if __name__ == '__main__':
    main()
