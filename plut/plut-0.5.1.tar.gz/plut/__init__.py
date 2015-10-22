from .plut import *
from .cli import cli
import config

import sys


def main():
    """entry point for cli"""
    try:
        cli(*sys.argv[1:])
        sys.exit(0)
    except Exception as why:
        print str(why)
        sys.exit(1)
