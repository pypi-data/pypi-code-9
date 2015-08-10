__author__ = 'Sinisa'


import os
import glob
from sbg_cli.config import Config
from sbg_cli.command import Command, Utility


__version__ = '0.1.4'


pth = os.path.dirname(__file__)
utilities = filter(lambda x: os.path.isdir(x) and not x.split('/')[-1].startswith('__'), glob.glob(os.path.dirname(__file__) + '/*'))
__all__ = ['.'.join(f.split('/')[-2:]) for f in utilities]


def disable_warnings():
    import requests
    requests.packages.urllib3.disable_warnings()
