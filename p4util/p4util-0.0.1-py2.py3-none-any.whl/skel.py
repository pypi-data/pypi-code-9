'''
Skelton for a P4Python script

$Author: lester_cheung $
$Id: //guest/lester_cheung/p4util/p4util/skel.py#5 $
'''

__version__ = '0.{0}'.format('$Change: 10738 $'.split()[-2])

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
    # ap.add_argument('-y', '--do-it', action='store_true', default=False)
    # ap.add_argument('--encoding', '-E',
    #                 help='Encoding to use to decode raw byte strings from the (non-Unicode) server')

    ## Here's how to implement sub-commands
    # sp = ap.add_subparsers(help='Sub-commands')
    # cmd0 = sp.add_parser('cmd0', help='help for cmd0')

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

    ## YOUR PROG HERE
    from pprint import pformat
    log.info(pformat(p4.run_info()))

    p4.disconnect()

if __name__ == '__main__':
    main()
