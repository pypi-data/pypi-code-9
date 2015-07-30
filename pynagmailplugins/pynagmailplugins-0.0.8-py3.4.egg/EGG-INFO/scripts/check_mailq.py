#!python
import argparse

import nagiosplugin

from snowpenguin.nagmail.exim import EximMailqFetcher, EximMailQueue
from snowpenguin.nagmail.nagios import create_mailq_check
from snowpenguin.nagmail.postfix import PostfixMailQueue, PostfixMailqFetcher

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('-w', '--warning', metavar='RANGE', type=int, required=True,
                      help='return warning if mailq counter is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', type=int, required=True,
                      help='return critical if mailq counter is outside RANGE')
    argp.add_argument('-dw', '--deferred-warning', metavar='RANGE', type=int, required=True,
                      help='return warning if deferred mailq counter is outside RANGE')
    argp.add_argument('-dc', '--deferred-critical', metavar='RANGE', type=int, required=True,
                      help='return critical if deferred mailq counter is outside RANGE')
    argp.add_argument('-t', '--type', metavar='TYPE', required=True, choices=['exim', 'postfix'],
                      help='SMTPD type (postfix, exim)')
    argp.add_argument('-s', '--sudo', default=False, action='store_true',
                      help='call mailq executable with sudo')
    args = argp.parse_args()

    if args.type == 'exim':
        f = EximMailqFetcher(use_sudo=args.sudo)
        mailq_if = EximMailQueue(f.get_data)
    else:
        f = PostfixMailqFetcher(use_sudo=args.sudo)
        mailq_if = PostfixMailQueue(f.get_data)

    check = create_mailq_check(mailq_if, args.warning, args.critical, args.deferred_warning, args.deferred_critical)
    check.main()

if __name__ == '__main__':
    main()