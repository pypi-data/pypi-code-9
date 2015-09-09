#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import subprocess


def current_branch():
    return subprocess.check_output(
        ['git', 'symbolic-ref', '--short', '-q', 'HEAD']
    ).strip()


def review_branch(name=None):
    """ use difftool to review given (current) branch.

    If no branch is passed, it will review the current branch against the
    master.
    """
    try:
        mybranch = current_branch()
        bspec = 'master..{}'.format(mybranch)
        subprocess.call(['git', 'difftool', '--tool=kompare', '-y', bspec])
    except subprocess.CalledProcessError:
        print("\033[31mFailed to run\033[0m \033[32mgit difftool\033[0m")


def push_current():
    """ Push current branch to master.

    This will call ``git push`` as a subprocess. All user creditentials are
    passed directly to git.
    """
    mybranch = current_branch()
    return subprocess.call(['git', 'push', 'origin', mybranch],
                           stdout=subprocess.PIPE)


def get_origin():
    """ Return the remote origin URL. """
    return subprocess.check_output(
        ['git', 'config', '--get', 'remote.origin.url']
    ).strip()


def get_cert():
    return subprocess.check_output(
        ['git', 'config', '--get', 'http.sslCaInfo']
    ).strip() or None

