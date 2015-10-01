# -*- coding: utf-8 -*-
"""
cghq_common.config
~~~~~~~~~~~~~~~~~~
Unified interface to read in config files
"""
from __future__ import absolute_import, unicode_literals
import errno
import logging

from nameko.extensions import DependencyProvider
from path import path
import yaml

from .constants import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class ConfigDependency(DependencyProvider):

    def get_dependency(self, worker_ctx):
        return self.container.config.copy()


def load(file_handle, defaults=None):
    """Populate or update data from a config file.

    Args:
        file_path (file): YAML config file
        defaults (dict, optional): default key-value pairs to merge with

    Returns:
        dict: loaded (and merged) config key-value pairs
    """
    if defaults is None:
        defaults = {}

    try:
        # read YAML key/values
        data = yaml.safe_load(file_handle)
        # overwrite and/or add new key/value pairs
        defaults.update(data)
    except OSError as exception:
        if exception.errno != errno.ENOENT:
            raise exception
        else:
            logger.warning("Can't read file: %s", file_handle.name)

    return defaults


def save(config_obj, file_path=DEFAULT_CONFIG, **options):
    """Save the current key-value pairs using the write handle.

    Args:
        config_obj (Config): Config object to serialize to file
        file_path (str): path to file to write to
        options (kwargs, optional): options to pass to dump (like 'indent')
    """
    the_file = path(file_path)

    # make sure the folders to the files exist
    the_file.dirname().mkdir_p()

    with the_file.open('w') as handle:
        yaml.dump(config_obj, handle, **options)
