#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

import os

# Third party libs
from git import Repo as _GitRepo
from git import refs as _GitRefs


class GitRepo(object):
    """
    Implements a Python interface to a Git(Pyton) repository
    """

    def __init__(self, path=None):
        self.path = path
        self.git = None

    def init(self):
        """
        Initializes the Git repository
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
            self.git = _GitRepo.init(self.path)
        else:
            self.git = _GitRepo(self.path)

    # Refs
    def update_ref(self, remote_ref, remote_name, repo_name):
        """
        Download (fetch) objects and update references
        """
        gitremote = self.get_remote(remote_name)
        gitref = None
        reporefs = self.get_refs()
        #gitreporefs = self.get_refs(raw=True)
        #already_fetched = False
        ret = {
            'update_info': None,
            'repo': repo_name,
            'url': gitremote.config_reader.get('url'),
            'old_commit': None,
            'new_commit': None,
            'ref': None,
            'updated': False
        }

        srcref = '{}/{}'.format(remote_name, remote_ref)
        if srcref not in reporefs:
            if remote_ref not in reporefs:
                ret['updated'] = True

            gitremote.fetch()
            reporefs = self.get_refs()
            self.get_refs(raw=True)
            gitref = self.get_ref(remote_ref)

            if srcref not in reporefs:
                # ref is a tag
                srcref = remote_ref
                if srcref in reporefs:
                    # it is a new tag!
                    ret['new_commit'] = gitref.commit
                    ret['ref'] = remote_ref
                    return ret

        if remote_ref not in reporefs:
            self.git.git.checkout(srcref, b=remote_ref)
            gitref = self.get_ref(remote_ref)
            ret['updated'] = True
        else:
            gitref = self.get_ref(remote_ref)

            if not isinstance(gitref, _GitRefs.tag.TagReference):
                if str(gitref.tracking_branch()) == srcref or str(gitref.tracking_branch()).endswith('/{}'.format(srcref)):
                    gitref.checkout(force=True)
                #else:
                #    gitref.set_reference(_GitRefs.symbolic.SymbolicReference(self.git, None))
                #    gitref.delete(self.git, remote_ref)
                #    return self.update_ref(remote_ref, remote_name)
            ret['old_commit'] = gitref.commit

        if not isinstance(gitref, _GitRefs.tag.TagReference):
            ret['update_info'] = gitremote.pull(remote_ref)
        ret['ref'] = remote_ref
        ret['new_commit'] = gitref.commit
        if not ret['updated']:
            ret['updated'] = ret['old_commit'] != ret['new_commit']
        return ret

    def get_refs(self, raw=False):
        """
        Return all references in a Git repository
        """
        gitrefs = []
        for gitref in self.git.refs:
            if raw:
                gitrefs.append(gitref)
            else:
                gitrefs.append(str(gitref))
        return gitrefs

    def get_ref(self, name):
        """
        Get a single GitPython object of a repo reference
        """
        refs = self.get_refs(raw=True)
        for ref in refs:
            if str(name) == str(ref):
                return ref

    def checkout(self, branch):
        """
        Ceckout references like heads (branches) and tags
        """
        gitref = self.get_ref(branch)
        if isinstance(gitref, _GitRefs.tag.TagReference):
            return self.git.git.checkout(gitref.commit)  # TODO this is only a workaround
        elif isinstance(gitref, _GitRefs.head.Head):
            return gitref.checkout(force=True)
        else:
            print(type(gitref))  # TODO
            raise

    # Remotes
    def add_remotes(self, remotes):
        """
        Add remotes to a repository
        """
        for remote_name, remote_settings in remotes.items():
            if remote_name not in self.get_remotes():
                gitremote = self.git.create_remote(remote_name, remote_settings.get('url'))  # TOOD
                self.git.git.config('--add', 'remote.{}.fetch'.format(remote_name), '+refs/tags/*:refs/tags/*')
                gitremote.fetch()

    def get_remote(self, name):
        """
        Get a Git reference object
        """
        i = 0
        for remote in self.git.remotes:
            if str(remote) == name:
                return self.git.remotes[i]
            i = i + 1

    def get_remotes(self):
        """
        Get a list of Git remotes
        """
        remotes = []
        for remote in self.git.remotes:
            remotes.append(str(remote))
        return remotes

    # Filesystem
    def set_path(self, path):
        """
        Set the repository file system path
        """
        self.path = path

    def get_path(self):
        """
        Get the repository file system path
        """
        return self.path
