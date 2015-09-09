# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import sys, os

from . import core, sh, exceptions

################################################################################

class Git(core.FileHandler):
    """Git

    :param root:
    """
    def __init__(self, root):
        super(Git, self).__init__(root)
        self._git = sh.Executable('git')
        self._git.bake('--git-dir=%s/.git' % root,
                       '--work-tree=%s' % root)

        try:
            self('status')
        except exceptions.GitCommandException as e:
            if e.exit_code == 128:
                self('init')
                self('config', 'branch.autosetuprebase', 'always')
                self('config', 'remote.origin.push', 'HEAD')
            else:
                raise e

    def __call__(self, *args, **kwargs):
        """__call__

        :param *args:
        """
        self._logger.debug(args)

        cwd = os.getcwd()
        os.chdir(self._root_dir) # necessary for git-stash

        try:
            return self._git(*args, **kwargs)
        except sh.FailedCommandException as e:
            raise exceptions.GitCommandException(e.cmd, e.stdout, e.stderr, e.exit_code)
        finally:
            os.chdir(cwd)

    def owns(self, path):
        """owns_path

        :param path:
        """
        if super(Git, self).owns(path):
            try:
                self('ls-files', path, '--error-unmatch')
                return True
            except:
                pass
        return False

    def add(self, path):
        """TODO: Docstring for link.

        :param path: a path to an existing file.
        :param new_path: a path to an existing file.
        :returns: the path of the resulting (owned) file.
        """
        return self('add', path)

    def move(self, path, new_path):
        """_move

        :param path:
        :param new_path:
        :param force:
        """
        return self('mv', path, new_path)

    def _remove(self, path, recursive):
        """_remove

        :param path:
        :param recursive:
        """
        if recursive:
            return self('rm', path)
        else:
            return self('rm', '--recursive', path)

    def branch(self):
        """branch"""
        return self('symbolic-ref', '--short', 'HEAD')[0]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
