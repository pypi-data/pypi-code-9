#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf_8

"""Add doc string

Subparser Entry Points

validate-rtc # shows summary as well
validate-tc  # shows summary as well
resolve      # launch interactive resolver

"""
import sys
from pbcommand.cli import get_default_argparser

__author__ = 'Michael Kocher'
__version__ = '0.1.0'


def get_parser():
    p = get_default_argparser(__version__, "pbcommand line tools")
    return p


def main():

    return 0


if __name__ == '__main__':
    sys.exit(main())
