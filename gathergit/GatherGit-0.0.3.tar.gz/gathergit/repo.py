#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

import os

# Third party libs
from sh import rsync

from gathergit.gitrepo import GitRepo


class Repo(dict):
    """Represents a repository/ module
    """

    def __init__(self, logger):
        """
        Constructor initializing instance variables
        """
        dict.__init__(self)
        self['name'] = ''
        self['defaults'] = {}
        self['branches'] = {}
        self['updates'] = {}
        self['target'] = '/tmp/gitgather-deployment'
        self.git = GitRepo()
        self.logger = logger

    def add_branches(self, branches, deployment_settings):
        """
        Add branches to our Repo object
        """
        for branch, _branch_settings in branches.items():
            branch_name = str(branch)
            branch_settings = _branch_settings

            # REF
            if isinstance(_branch_settings, str) or isinstance(_branch_settings, float) or isinstance(_branch_settings, int):
                branch_settings = {'ref': str(_branch_settings)}
            if not isinstance(branch_settings.get('ref'), str):
                branch_settings['ref'] = str(branch_settings['ref'])

            if branch_name not in self['branches'].keys():
                self['branches'][branch_name] = branch_settings
            else:
                self['branches'][branch_name].update(branch_settings)

            # REPO
            if 'repo' not in self['branches'][branch_name].keys():
                self['branches'][branch_name]['repo'] = self.get('defaults').get('repo', self['name'])

            # URL
            if 'url' not in self['branches'][branch_name].keys():
                url = self.get('defaults').get('url', deployment_settings.get('defaults', {}).get('url'))
                if url is None:
                    base_url = self['branches'][branch_name].get('base_url', self.get('defaults').get(
                        'base_url', deployment_settings.get('defaults', {}).get('base_url')))
                    url = '{}/{}'.format(base_url, self['branches'][branch_name]['repo'])

                self['branches'][branch_name]['url'] = url

    def sync(self, local_branch, remote_branch, root=''):
        """
        Sync/ update/ deploy a repository
        """
        src_path = '{}/{}'.format(self.git.get_path(), root)
        dst_path = '{}/{}/{}/'.format(self.get('target'), local_branch, self.get('name'))

        if not os.path.isdir(dst_path):
            os.makedirs(dst_path)
        if not src_path.endswith('/'):
            src_path += '/'
        if not dst_path.endswith('/'):
            dst_path += '/'

        self.logger.debug('Preparing repo sync %s by checking out ref %s', self['name'], remote_branch)
        self.git.checkout(remote_branch)

        self.logger.info('Synchronizing repo using source path %s and destination path %s', src_path, dst_path)

        rsync_args = ['--verbose', '--archive', '--checksum', '--delete', '--exclude=.git/', src_path, dst_path]

        self.logger.debug('Running rsync with the arguments %s', rsync_args)
        rsync(rsync_args)
