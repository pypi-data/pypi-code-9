#! /usr/bin/env python
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Script to start the Websourcebrowser server component.

If you're developing or don't have Websourcebrowser installed, do
_not_ use this script but instead start the server with

    python browser.py [options]

at the shell prompt while you're in the main directory of the
Websourcebrowser distribution. This directory is either the root of an
unpacked tarball or the root of a working directory cloned with
Mercurial.
"""

import sys

from websourcebrowser import browser


if __name__ == '__main__':
    browser.main()

