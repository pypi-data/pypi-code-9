#!/usr/bin/env python
"""
Move a provided file to the trash on Mac OS X

Note: Only tested on OS X 10.9 (Mavericks)
"""
from __future__ import print_function
import argparse
import logging
import os
import re
import shutil
import sys
import time

version_info = (1, 0, 0)
__version__ = '.'.join([str(x) for x in version_info])


class OSXUser(object):
    """Class representing a System level OS X User"""

    def __init__(self, username=None):
        """Create an OSXUser instance

        :param username: The name of the system user to track
        """
        if username is None:
            username = os.path.expanduser('~').split(os.sep)[-1]
        self.username = username
        self.home = '/Users/{}'.format(self.username)
        self.uid = os.getuid()

    def __str__(self):
        """Generic string representation for this user, shows both username and
        uid
        """
        return '<User {}> {}'.format(self.uid, self.username)
    __repr__ = __str__


class Trash(object):
    """Base Trash type. Implements common functionality among trash types"""

    def __init__(self, src):
        """Create a new :class:`Trash` instance

        :param src: The source file to move to the trash
        """
        self.src = src
        self.user = OSXUser()
        self.trash_dir = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.regex = re.compile('Destination path.*already exists')

    def delete(self, dest=None):
        """Actually move the file to the trash bin"""
        if self.trash_dir is None:
            raise NotImplementedError()
        if dest is None:
            dest = os.path.join(self.trash_dir, self.src.split(os.sep)[-1])
        logging.info('Dest = %s', dest)
        try:
            self.logger.info('Moving %s to Trash at %s', self.src, self.trash_dir)
            shutil.move(self.src, dest)
        except shutil.Error as e:
            # If we failed to move the file, because the destination already
            # existed, add a timestamp to the filepath and recurse until we
            # find a winner.
            if self.regex.match(e.message):
                # Grab an epoch timestamp, convert it to a string, and lose
                # the decimal point to build a reliable timestamp
                dest += str(time.time()).replace('.', '')
                self.delete(dest)


class LocalTrash(Trash):
    """:class:`LocalTrash` is a handle on deleting from the local disk, to the
    current user's trash directory.
    """

    def __init__(self, *args, **kwargs):
        """Create a new :class:`Trash` Instance and build the directory path
        where local files are moved to the trash
        """
        super(LocalTrash, self).__init__(*args, **kwargs)
        self.trash_dir = os.path.join(self.user.home, '.Trash')
        if not os.path.exists(self.trash_dir):
            pass  # Raise exception and log
            self.logger.warning('No local .Trash found at %s', self.trash_dir)
            raise NoLocalTrash()
        self.logger.info('Local .Trash found at %s', self.trash_dir)

    def delete(self):
        """Actually move the file to the trash bin"""
        self.logger.info('Moving %s to Trash at %s', self.src, self.trash_dir)
        super(LocalTrash, self).delete()


class MountedTrash(Trash):
    """:class:`MountedTrash` provides the functionality of deleting from a
    mounted disk. It attempts to move the file to the mounted disk's `.Trashes`
    directory. If no such directory exists, then it fails over to the local
    user's trash.
    """
    def __init__(self, *args, **kwargs):
        super(LocalTrash, self).__init__(*args, **kwargs)
        dirs = file_path.split('/')
        self.trash_dir = os.path.join(dirs[1], dirs[2], '.Trashes')
        self.logger.info('Mounted .Trashes found at %s', self.trash_dir)

    def _user_trash(self):
        """If the .Trashes directory for the mounted device doesn't exist,
        create it. Either way, build the path to that .Trashes directory and
        return it.

        :returns: The path to the current :class:`OSXUser`'s trash directory on
            the mounted device.
        """
        users_volume_trash = os.path.join(self.trash_dir, str(self.user.uid))
        if not os.path.exists(users_volume_trash):
            os.mkdir(users_volume_trash)
        return users_volume_trash

    def delete(self):
        """Attempt to move the file into the .Trashes directory on the mounted
        device. If we can't find the appropriate .Trashes directory, then
        failover and move it to the user's local Trash directory.
        """
        if os.path.exists(self.trash_dir):
            dest = self._user_trash()
            self.logger.info('Moving %s to Trash at %s',
                             self.src, self.trash_dir)
            shutil.move(self.src, self.trash_dir)
        else:
            self.logger.info('Failed to delete on mounted disk. Trying '
                             'locally.')
            LocalTrash(self.src).delete()


def trash(src):
    """Utility function used to determine whether the source file is stored
    locally or on a mounted disk. It creates the appropriate :class:`Trash`
    subclass and call's delete on it.
    """
    # Determine where the source file is located. Is it stored locally, or on a
    # mounted device.
    logger = logging.getLogger('trash')
    if not os.path.isabs(src):
        src = os.path.abspath(src)
    if not os.path.exists(src):
        print('No such file or directory:', src)
        sys.exit(1)

    disk = src.split('/')[1]
    if disk == 'Users':
        logger.info('Moving %s to the trash locally.', src)
        trash = LocalTrash(src)
    elif disk == 'Volumes':
        logger.info('Moving %s to the trash on mounted disk.', src)
        trash = MountedTrash(src)
    else:
        raise UnsupportedDiskFormat()
    trash.delete()


class TrashException(Exception):
    message = None

    def __str__(self):
        return self.message


class NoLocalTrash(TrashException):
    message = 'The current user has no local .Trash directory'


class UnsupportedDiskFormat(TrashException):
    message = 'Unable to parse Trash directory from provided file path'


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False,
                        help='Toggle verbose output')
    parser.add_argument('--version', action='store_true',
                        default=False, help='Print version info and exit')
    parser.add_argument('src', nargs='*',
                        help=('A list of files and directories to move to the '
                              'Trash. Relative and absolute paths are both '
                              'fine.'))
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.version:
        print('osx_trash Version:', __version__)
        sys.exit(0)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    for src in args.src:
        trash(src)


if __name__ == '__main__':
    main()
