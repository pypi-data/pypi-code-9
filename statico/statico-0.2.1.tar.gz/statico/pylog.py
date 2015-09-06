# -*- coding: utf-8 -*-
"""
    statico.pylog
    -------------
    Provides logging constants and functions
    :license: MIT, see LICENSE for more details.
"""
from colorama import Fore, Back, Style
from .utils import u


TICK = u('\u2713')
CROSS = u('\u2717')
ERROR = Fore.WHITE + Back.RED + 'ERROR' + Fore.RESET + Back.RESET
WARNING = Fore.WHITE + Back.YELLOW + 'WARNING' + Fore.RESET + Back.RESET
SUCCESS = Fore.WHITE + Back.GREEN + Style.BRIGHT + 'SUCCESS' + Fore.RESET + Back.RESET + Style.RESET_ALL


def action(value, success=True):
    return '    ' + TICK + ' ' + value if success else '    ' + CROSS + ' ' + value
