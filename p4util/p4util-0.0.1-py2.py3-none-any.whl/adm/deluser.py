from __future__ import print_function

import argparse
import logging
import sys
import itertools
import getpass
import socket
import textwrap

from pprint import pprint
from datetime import datetime, timedelta

try:
    from ..p4cli import P4
except:
    # failback to P4Python (so we can run the script without
    # installing the p4util module)
    from P4 import P4

if sys.version_info[0] <= 2:     # PY2
    input = raw_input

logfmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=logfmt)
LOG = logging.getLogger(__name__)


class App(object):
    def __init__(self, args=None):
        args = self.parse_args(args)

        p4 = self.p4 = P4()
        if args.port:
            p4.port = args.port
        if args.user:
            p4.user = args.user
        if args.client:
            p4.client = args.client
        if args.charset:
            p4.charset = args.charset
        p4.connect()

        alluserspecs = p4.run_users()
        allusers = set([x.get('User') for x in alluserspecs])

        inactive_users = excluded_users = set()

        if args.expiry:
            inactive_users = set(filter(self.is_inactive_user, allusers))
            LOG.info('{}/{} users are inactive in the last {} days.'.format(
                len(inactive_users), len(allusers), self.args.expiry))

        if args.group_excluded:
            excluded_users = set(itertools.chain.from_iterable([
                p4.run_group(['-o', g])[0].get('Users') for g in args.group_excluded ]))
            LOG.info('{} users are excluded '.format(len(excluded_users)))

        self.users_to_be_removed = inactive_users.union(args.users) - excluded_users

    def is_inactive_user(self, p4user):
        userspec = self.p4.run_user(['-o', p4user])
        if not userspec:
            return False
        userspec = userspec[0]
        accessed = datetime.strptime(userspec.get('Access', '1970/1/1 0:0:0'),
                                     '%Y/%m/%d %H:%M:%S')
        if datetime.now() - accessed > timedelta(days=self.args.expiry):
            return True
        return False

    def go(self):

        p4 = self.p4
        if not self.users_to_be_removed:
            LOG.info('No users to be deleted - exiting.')
            return 0            # exit states

        if not self.args.do_it and not self.args.dry_run:
            print('{} users to be deleted:'.format(len(self.users_to_be_removed)))
            print(textwrap.fill(', '.join(self.users_to_be_removed),
                                initial_indent='\t', subsequent_indent='\t'))
            while 1:
                ans = input('Delete the above {} users? [y/N]'.format(
                    len(self.users_to_be_removed)))
                if ans.upper() in 'YN' or ans == '':
                    break
            if ans.upper() == 'Y':
                self.deluser(self.users_to_be_removed, do_it=True)
            else:
                self.deluser(self.users_to_be_removed, do_it=False)
        elif self.args.do_it:                   # option -y
            self.deluser(self.users_to_be_removed, do_it=True)
        else:                   # dry run
            self.deluser(self.users_to_be_removed, do_it=False)

    def deluser(self, users, do_it=False):
        log = logging.getLogger('deluser()')
        if do_it:
            log.info('delting {} users...'.format(len(users)))
        else:
            log.info('previewing the deletion of {} users...'.format(len(users)))

        p4 = self.p4
        # revert opened files
        for user in self.users_to_be_removed:
            opened_files = p4.run_opened(['-a', '-u', user])
            if not opened_files:
                continue
            if do_it:
                for ofile in opened_files:
                    p4.run_revert(['-C', ofile.get('client'), ofile.get('depotFile')])
                log.info('Reverted {x} files {user} opened.'.format(user=user, x=len(opened_files)))
                for ofile in opened_files:
                    log.debug('... {}'.format(ofile))
            else:               # FIXME
                _ = '{user} has {x} files opened - deleting the users will revert them on the server.'
                log.info(_.format(user=user, x=len(opened_files)))
                for ofile in opened_files:
                    log.debug('... {}'.format(ofile))
        # remove users from all groups
        gpurge = {}
        for usr in self.users_to_be_removed:
            for g in p4.run_groups(['-u', usr]):
                gname = g.get('group')
                if gname:
                    e = gpurge.get(gname, set())
                    e.add(usr)
                    gpurge[gname] = e

        for g in gpurge:
            if do_it:
                # bulk remove all unregistered users from the groups
                gspec = p4.run_group(['-o', g])[0]
                for u in gpurge[g]:
                    gspec.get('Users', []).remove(u)
                p4.input = gspec
                p4.run_group('-i')
                log.debug('Removed {} from group **{}**.'.format(', '.join(gpurge[g]), g))
            else:
                log.info('Would remove {} users from group {}.'.format(len(gpurge[g]), g))

        # purge the user at last
        for usr in self.users_to_be_removed:
            if do_it:
                log.debug(p4.run_user(['-df', usr]))


    def parse_args(self, args):
        ap = argparse.ArgumentParser(description='MYPROG')
        p4 = P4()
        _port = p4.port or p4.env('P4PORT') or '1666'
        _user = p4.user or p4.env('P4USER') or getpass.getuser()
        _client = p4.env('P4CLIENT') or socket.gethostname()
        _charset = p4.env('P4CHARSET') or 'none'
        ap.add_argument('-p', '--port', metavar=_port, default=_port)
        ap.add_argument('-u', '--user', metavar=_user, default=_user)
        ap.add_argument('-c', '--client', metavar=_client, default=_client)
        ap.add_argument('-C', '--charset', metavar=_charset, default=_charset)
        ap.add_argument('-y', '--do-it', action='store_true', default=False)
        ap.add_argument('-n', '--dry-run', action='store_true', default=False)
        ap.add_argument('-G', '--group-excluded', action='append')
        ap.add_argument('-E', '--expiry', type=float,
                        help='User accessed the server in the last specified DAYS are '
                        'considered active and thus will not be removed.')

        ap.add_argument('users', nargs='*')

        self.args = ap.parse_args(args)
        LOG.debug(self.args)
        return self.args


if __name__ == '__main__':
    sys.exit(App().go())
