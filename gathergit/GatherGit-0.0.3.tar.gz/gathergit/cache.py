#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

import os

from gathergit.misc import Helper


class Cache(object):
    """Cache representation of a repo"""

    def __init__(self, name, settings, logger, repo=None):
        self.name = name
        self.settings = settings
        self.path = self.settings.get('path', '/tmp/gathergit-cache')
        self.logger = logger
        self.repo = repo

    def init(self):
        """
        Initialize cache
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def update(self, repo):
        """
        Update the cache, e.g. the Git repository in the file system
        """
        self.repo = repo
        branches = self.repo.get('branches')
        changed_refs = []

        for branch_name, branch_settings in Helper.sorted_dict(branches).items():
            repo_path = '{}/{}'.format(self.path, branch_settings.get('repo'))
            repo['remotes'] = {'origin': {'url': branch_settings.get('url')}}

            # the following methods are idempotent, don't worry about their names
            self.repo.git.set_path(repo_path)
            self.repo.git.init()
            self.repo.git.add_remotes(repo['remotes'])

            self.logger.debug('Searching for updates of remote repo %s (ref: %s) in cache %s', self.repo.get('name'), branch_settings.get(
                'ref'), self.name)
            update_info = self.repo.git.update_ref(branch_settings.get('ref'), 'origin', branch_settings.get('repo'))
            if update_info.get('updated'):
                self.logger.info('Found updates of remote repo %s, scheduling repo deployment of ref %s', self.repo.get('name'),
                                 branch_settings.get('ref'))
                changed_refs.append(update_info)
        return changed_refs
