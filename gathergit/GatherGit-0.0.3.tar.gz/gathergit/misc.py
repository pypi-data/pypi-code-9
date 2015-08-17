#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

import os
import yaml
import logging
import logging.config
import collections


class Helper(object):
    """
    Contains helper functions
    """

    @staticmethod
    def create_logger(program_name, config=None):
        """
        Initialize logger
        """
        if not config:
            config = {'version': 1}
        logger = logging.getLogger(program_name)
        logging.config.dictConfig(config)
        return logger

    @staticmethod
    def sorted_dict(var):
        """
        Return a sorted dict as OrderedDict
        """
        ret = collections.OrderedDict()
        for key in sorted(list(var.keys())):
            ret[key] = var[key]
        return ret


class ConfigParser(object):
    """
    Parses the configuration file directory
    """

    def __init__(self, confdir, config=None):
        self.confdir = confdir

        if not config:
            config = {'settings': {}, 'deployments': {}}
        self.config = config

    def parse_directory(self):
        """
        Search for YAML files in a directory and parse them
        """
        if not os.path.isdir(self.confdir):
            self.config = None
            return self.config

        for dirname, subdirectories, files in os.walk(self.confdir):
            for file_name in files:
                file_path = '{0}/{1}'.format(dirname, file_name)
                if file_name.endswith('.yaml'):
                    with open(file_path, 'r') as stream:
                        data = yaml.load(stream)
                    if data:
                        for root, value in data.items():
                            if root == 'settings':
                                self.config[root] = value
                            elif root == 'deployments':
                                for repo, settings in value.items():
                                    if repo not in self.config[root].keys():
                                        self.config[root][repo] = settings
                                    else:
                                        self.config[root][repo].update(settings)

    def dump(self):
        """
        Return configuration
        """
        return self.config
