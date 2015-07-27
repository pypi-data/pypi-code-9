#!/usr/bin/env python
'''A hack to avoid typing "p4" over and over. A Perforce REPL shell!
Inspired by:
http://robots.thoughtbot.com/announcing-gitsh

TODO:
* colors!
* alias for `p4 help`
* pipes!

'''

from __future__ import print_function # for PY3 print()

import os
import re
import shlex
import subprocess
import sys
import logging as log
try:
    from cmd2 import Cmd
except ImportError as e:
    log.warn('Module cmd2 is not available - importing the bundled `cmd` module instead (with less functionality).')
    from cmd import Cmd

from pprint import pprint
from .helper import check_output

def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    Stolen from Python 3.3
    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None


class P4Shell(Cmd):
    """Welcome to the Perforce shell - a Perforce client as a REPL shell.
This is a work in progress - contact @p4lester for questions/comments.
    """

    intro = __doc__

    def __init__(self, p4bin=which('p4')):
        """initialization

        Arguments:
        - `p4bin`: the P4 executable
        """
        self._p4bin = p4bin
        p4env = check_output( [p4bin, 'set'], universal_newlines=True ).splitlines()
        p4env = dict([e.split('=', 1) for e in p4env])
        for k in p4env:
            x = re.sub(r'\(.*\)', r'', p4env[k]).strip()
            p4env[k] = x
        self._p4env = p4env

        self.prompt = '{0}@{1} ({2})$ '.format(p4env.get('P4USER', os.getlogin()),
                                               p4env.get('P4PORT', 'P4PORT'),
                                               p4env.get('P4CLIENT', 'P4CLIENT'))
        Cmd.__init__(self)

    # def do_info(self, arg):
    #     """p4 info"""
    #     print('do_info', arg)

    def __getattr__(self, name):
        print(name, end=' ')
        if not name.startswith('do_'):
            raise KeyError
        p4cmd = name[3:]
        def f(arg=''):
            cmd = [self._p4bin, p4cmd]+shlex.split(arg)
            print(cmd)
            subprocess.call(cmd)
        return f

    def __dir__(self):
        cmds = '''
        add          Open a new file to add it to the depot
	annotate     Print file lines along with their revisions
	attribute    Set per-revision attributes on revisions
	branch       Create or edit a branch specification
	branches     Display list of branches
	change       Create or edit a changelist description
	changes      Display list of pending and submitted changelists
	changelist   Create or edit a changelist description
	changelists  Display list of pending and submitted changelists
	client       Create or edit a client specification and its view
	clients      Display list of known clients
	copy         Schedule copy of latest rev from one file to another
	counter      Display, set, or delete a counter
	counters     Display list of known counters
	cstat        Dump change/sync status for current client
	delete       Open an existing file to delete it from the depot
	depot        Create or edit a depot specification
	depots       Display list of depots
	describe     Display a changelist description
	diff         Display diff of client file with depot file
	diff2        Display diff of two depot files
	dirs         List subdirectories of a given depot directory
	edit         Open an existing file for edit
	filelog      List revision history of files
	files        List files in the depot
	fix          Mark jobs as being fixed by named changelists
	fixes        List what changelists fix what job
	flush        Fake a 'p4 sync' by not moving files
	fstat        Dump file info
	grep         Print lines from text files matching a pattern
	group        Change members of a user group
	groups       List groups (of users)
	have         List revisions last synced
	help         Print the requested help message
	info         Print out client/server information
	integrate    Schedule integration from one file to another
	integrated   Show integrations that have been submitted
	interchanges Report changes that have not yet been integrated
	istat        Show integrations needed for a stream
	job          Create or edit a job (defect) specification
	jobs         Display list of jobs
	key          Display, set, or delete a key/value pair
	keys         Display list of known keys and their values
	label        Create or edit a label specification and its view
	labels       Display list of labels
	labelsync    Synchronize label with the current client contents
	list         Create an in-memory (label) list of depot files
	lock         Lock an opened file against changelist submission
	logger       Report what jobs and changelists have changed
	login        Login to Perforce by obtaining a session ticket
	logout       Logout of Perforce by removing or invalidating a ticket
	merge        Schedule merge (integration) from one file to another
	move         Moves files from one location to another
	opened       Display list of files opened for pending changelist
	passwd       Set the user's password on the server (and Windows client)
	populate     Populate a branch or stream with files
	print        Retrieve a depot file to the standard output
	protect      Modify protections in the server namespace
	protects     Display protections in place for a given user/path
	reconcile    Reconcile client to offline workspace changes
	rename       Moves files from one location to another
	reopen       Change the type or changelist number of an opened file
	resolve      Merge open files with other revisions or files
	resolved     Show files that have been merged but not submitted
	revert       Discard changes from an opened file
	review       List and track changelists (for the review daemon)
	reviews      Show what users are subscribed to review files
	set          Set variables in the registry (Windows only)
	shelve       Store files from a pending changelist into the depot
	status       Preview reconcile of client to offline workspace changes
	sizes        Display size information for files in the depot
	stream       Create or edit a stream specification
	streams      Display list of streams
	submit       Submit open files to the depot
	sync         Synchronize the client with its view of the depot
	tag          Tag files with a label
	tickets      Display list of session tickets for this user
	unlock       Release a locked file but leave it open
	unshelve     Restore shelved files from a pending changelist
	update       Update the client with its view of the depot
	user         Create or edit a user specification
	users        Display list of known users
	where        Show how file names map through the client view
	workspace    Create or edit a client specification and its view
	workspaces   Display list of known clients
'''
        attrs = Cmd.get_names(self) + \
                ['do_'+cmd.split(maxsplit=1)[0] for cmd in cmds.strip().splitlines()]
        return attrs

    def do_exit(self, *args):
        """exit the shell - useful when cmd2 is not avilable."""
        sys.exit(0)

    def do_EOF(self, *args):
        self.do_exit()

if __name__ == '__main__':
    P4Shell().cmdloop()
