# -*- coding: utf-8 -*-

__version__ = '0.1.4'
__author__ = 'Ossama Edbali (ossedb@gmail.com)'


from colorama import Fore, Back, Style


TICK = u'\u2713'
ERROR = Fore.WHITE + Back.RED + 'ERROR' + Fore.RESET + Back.RESET
WARNING = Fore.WHITE + Back.YELLOW + 'WARNING' + Fore.RESET + Back.RESET
SUCCESS = Fore.WHITE + Back.GREEN + Style.BRIGHT + 'SUCCESS' + Fore.RESET + Back.RESET + Style.RESET_ALL


def action(value):
    return '    ' + TICK + ' ' + value
