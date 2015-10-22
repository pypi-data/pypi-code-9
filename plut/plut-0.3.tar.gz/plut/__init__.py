from .plut import *
from .cli import cli

import sys


def main():
    """entry point for cli"""
    sys.exit(0 if cli(*sys.argv[1:]) else 1)
