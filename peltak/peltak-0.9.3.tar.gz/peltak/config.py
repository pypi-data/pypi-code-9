# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join, normpath


#----------------------------------------------------------------------------//
def projpath(path):
    return normpath(join(dirname(abspath(__file__)), '..', path))


MR_TEMPLATE_PATH = '.peltak/mr-template.rst'
MR_CACHE_PATH = ".peltak/mr-cache.json"
CONFIG_PATH = '.peltak/config.json'
LOG_FILENAME = '.peltak/gitlab-cli.log'
ACTIONS_PATH = 'peltak/actions'
ACTIONS_DIRS = (
    projpath('peltak/actions'),
    '.peltak/actions',
)

