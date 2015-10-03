#!/usr/bin/env python
#
# Copyright (c) 2015 Johnny Wezel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main program
"""
import sys
import os
from subprocess import call
from time import strftime

from jw.util import file
from pkg_resources import get_distribution

def processors():
    if os.path.exists('/proc/cpuinfo'):
        return len([line for line in open('/proc/cpuinfo').readlines() if line.startswith('processor\t:')])

VERSION = get_distribution('jw.util').version
EMERGE = (
    "emerge --jobs 4 --load-average {} --nospinner --update --newuse --deep --keep-going --autounmask y "
     "--autounmask-write y".format(processors())
)
BACKUP_DIR = '/var/lib/emerge_update'
BACKUP_GENERATIONS = 8

def Main():
    import sys
    from argparse import ArgumentParser

    class Program(object):
        """
        Program
        """

        def __init__(self):
            argp = ArgumentParser(description='Do extended package maintenance')
            argp.add_argument('--dry-run', '-n', action='store_true', help="don't execute commands, just print them")
            argp.add_argument('--verbose', '-v', action='store_true', help="print commands as they are executed")
            argp.add_argument('--version', '-V', version=VERSION, action='version')
            argp.add_argument('--output', '-o', action='store', help='specify output file')
            argp.add_argument('--append', '-a', action='store_true', help='append to output file instead of overwriting')
            self.args = argp.parse_args()
            self.variables = {
                'EMERGE': EMERGE
            }
            if self.args.output in ('-', None):
                self.output = sys.stdout
            else:
                self.output = open(self.args.output, 'wa'[self.args.append], 1)

        def do(self, *args):
            """
            Run something in shell

            :param args: list of arguments which are concatenated with space
            """
            if self.args.dry_run:
                self.log(*args)
                return 0
            else:
                if self.args.verbose:
                    self.log(*args)
                return call(self.subst(*args), stdin=None, stdout=self.output, stderr=self.output, shell=True)

        def log(self, *args):
            """
            Write something to the output file
            """
            self.output.write('\n=== {}\n'.format(self.subst(*args)))

        def subst(self, *args):
            """
            Join and substitute arguments

            :param args: list of arguments concatenated with space
            """
            return ' '.join(a.format(**self.variables) for a in args)

        def backup(self, path):
            """
            Back up a file or directory

            :param str rpath: pathname to file

            The path follows symbolic links.

            Backups are done by renaming and hard linking if possible or tar if the path is a mount point.
            """
            rpath = os.path.realpath(path)
            if os.path.ismount(rpath):
                # In this case, we can't just move the directory. A full backup is due
                tarpath = os.path.join(BACKUP_DIR, rpath.lstrip('/').replace('/', '-') + '.tar.gz')
                if self.args.verbose or self.args.dry_run:
                    self.log('Backup', rpath, 'with tar to', tarpath, "because it's a mount point")
                if not self.args.dry_run:
                    try:
                        os.makedirs(BACKUP_DIR)
                    except OSError as e:
                        if e.errno == 17:
                            if self.args.verbose or self.args.dry_run:
                                self.log('Created backup directory', BACKUP_DIR)
                        else:
                            raise
                self.do('tar --totals --backup=t -czf', tarpath, rpath + os.path.sep)
            else:
                if self.args.verbose or self.args.dry_run:
                    self.log('Backup', rpath, 'to', rpath + '.1')
                if not self.args.dry_run:
                    backup = file.Backup(rpath, mode=BACKUP_GENERATIONS)
                    backup()
                # Use bash to do the dirty work
                self.do('cp -la {0}.1 {0}'.format(rpath))

        def run(self):
            """
            Run program
            """
            sys.stderr = self.output
            self.log('emerge_update {} on {} '.format(VERSION, strftime('%F at %T')).ljust(128, '='))
            self.do('qcheck --badonly --all')
            self.do('eix-sync -v')
            self.backup('/etc')
            if self.do('{EMERGE} @world'):
                self.log('Emerge returned non-zero. Update config files and retry.')
                self.do('etc-update --automode=-5 /etc/portage')
                self.do('{EMERGE} @world)')
            self.do('emerge --depclean')
            self.do('revdep-rebuild --ignore')
            self.do(
                'emerge --jobs 4 --load-average {} --nospinner --keep-going --autounmask y '
                 '--autounmask-write y @preserved-rebuild'.format(processors())
            )
            self.do('python-updater')
            self.do('perl-cleaner --all')
            self.do('cfg-update --update --automatic-only')
            self.do('cfg-update --index')
            self.do('prelink --all')
            self.backup('/var/db/pkg')
            self.do('qcheck --all --update')
            self.do('emaint -c all')
            return 0

    program = Program()
    return program.run()

if __name__ == '__main__':
    sys.exit(Main())
