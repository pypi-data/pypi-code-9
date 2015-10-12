# -*- coding: utf-8 -*-
from path import path

from .compat import iteritems

CONFIG_ROOT = path('~/.clinical').expanduser()
MAIN_CONFIG = path('config.yaml')
DEFAULT_CONFIG = CONFIG_ROOT.joinpath(MAIN_CONFIG)

ANALYSIS_MAP = {'EXO': 'exomes', 'WGS': 'genomes'}
TAG_MAP = {value: key for key, value in iteritems(ANALYSIS_MAP)}
