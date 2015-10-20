#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pymip.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``pymip`` (if installed)
or ``python -m pymip`` (no install required).
"""
import sys

from pymip.cli import cli


if __name__ == '__main__':
    # exit using whatever exit code the CLI returned
    sys.exit(cli())
