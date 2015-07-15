# -*- coding: utf-8 -*-
#
# File: log.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import logging

logger = logging.getLogger("nexiles.tools.api")

__all__ = ["setup_logging"]


def setup_logging(logfile=None, level=logging.DEBUG):
    if logfile is None:
        logging.basicConfig(level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")
    else:
        logging.basicConfig(filename=logfile, level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")


# vim: set ft=python ts=4 sw=4 expandtab :
